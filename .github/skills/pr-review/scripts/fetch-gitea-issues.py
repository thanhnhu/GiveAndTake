#!/usr/bin/env python3
"""
Gitea Issues & Comments Collector

Fetches specific Gitea issue/PR comments and produces a flat JSON report with
feedback annotations. Only the referenced comments are kept in the output.

Input file format (one entry per URL; feedback on same line or next line):
  https://gitea.example.com/{owner}/{repo}/pulls/{n}#issuecomment-{id} => feedback text
  https://gitea.example.com/{owner}/{repo}/pulls/{n}#issuecomment-{id} -> feedback text
  - URL => feedback
  URL
  => feedback on next line

  # Lines starting with # are ignored

Output JSON schema (flat list):
  [
    {
      "repo":      "owner/repo",
      "path":      "path/to/file.ts",   // empty for PR-level or review-body comments
      "body":      "AI comment body",
      "diff_hunk": "@@ ... @@",          // empty for non-inline comments
      "feedback":  "developer response"  // or list of strings if multiple
    },
    ...
  ]

Usage:
  python fetch-gitea-issues.py --file urls-with-feedback.txt
  python fetch-gitea-issues.py --file urls.txt --output report.json
  GITEA_TOKEN=xxx python fetch-gitea-issues.py --file urls.txt

Environment:
  GITEA_TOKEN   Personal access token (required for private repos)
"""

import sys
import os
import re
import json
import ssl
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _opener():
    ctx = ssl.create_default_context()
    return urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))


def gitea_get(url: str, token: str | None) -> dict | list:
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers, method="GET")
    with _opener().open(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def gitea_get_paginated(base_url: str, token: str | None, per_page: int = 50) -> list:
    results, page = [], 1
    while True:
        sep = "&" if "?" in base_url else "?"
        data = gitea_get(f"{base_url}{sep}limit={per_page}&page={page}", token)
        if not data:
            break
        results.extend(data)
        if len(data) < per_page:
            break
        page += 1
    return results


# ---------------------------------------------------------------------------
# URL / input file parsing
# ---------------------------------------------------------------------------

# Matches: https://host/owner/repo/pulls-or-issues/123[/anything][#anchor]
URL_RE = re.compile(
    r"(https?://[^/\s]+)/([^/\s]+)/([^/\s]+)/(issues|pulls)/(\d+)",
    re.IGNORECASE,
)
COMMENT_ID_RE = re.compile(r"#issuecomment-(\d+)")
FEEDBACK_RE = re.compile(r"^[-=*>]+\s*")  # strip leading markers like => - > * etc.


def parse_url(raw: str) -> dict | None:
    """Extract PR/issue components from a raw URL string."""
    m = URL_RE.search(raw)
    if not m:
        return None
    base, owner, repo, kind, number = m.groups()
    cm = COMMENT_ID_RE.search(raw)
    return {
        "base_url": base,
        "api_url": f"{base}/api/v1",
        "owner": owner,
        "repo": repo,
        "repo_label": f"{owner}/{repo}",
        "kind": kind,
        "number": int(number),
        "comment_id": int(cm.group(1)) if cm else None,
        "original_url": raw.strip(),
    }


def parse_input_file(path: str) -> list[dict]:
    """
    Parse a file of URL + feedback pairs into a list of entry dicts.

    Returns list of: {parsed_url, feedback}
    """
    with open(path, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    entries = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1

        # Skip blanks and comments
        if not line or line.startswith("#"):
            continue

        # Try to find a URL on this line
        p = parse_url(line)
        if p is None:
            continue

        # Look for inline feedback: "URL => feedback" or "URL -> feedback"
        inline_fb = re.split(r"\s*(?:=>|->)\s*", line, maxsplit=1)
        feedback_text = inline_fb[1].strip() if len(inline_fb) > 1 else ""

        # If no inline feedback, peek at subsequent lines for a feedback line
        if not feedback_text:
            while i < len(lines):
                next_line = lines[i].strip()
                if not next_line:
                    i += 1
                    continue
                # If the next line starts with a feedback marker but has no URL, treat as feedback
                if not URL_RE.search(next_line) and re.match(r"^[-=>*]", next_line):
                    feedback_text = FEEDBACK_RE.sub("", next_line).strip()
                    i += 1
                    # Allow multi-line feedback continuation (lines that continue without a URL)
                    while i < len(lines):
                        cont = lines[i].strip()
                        if not cont or URL_RE.search(cont) or re.match(r"^[-=>*#]", cont):
                            break
                        feedback_text += " " + cont
                        i += 1
                break  # Don't consume non-feedback lines

        entries.append({"parsed": p, "feedback": feedback_text or None})

    return entries


def parse_inline_urls(urls: list[str]) -> list[dict]:
    """Parse a plain list of URL strings (no feedback)."""
    result = []
    for raw in urls:
        p = parse_url(raw)
        if p:
            result.append({"parsed": p, "feedback": None})
        else:
            print(f"[WARN] Cannot parse URL, skipping: {raw}", file=sys.stderr)
    return result


# ---------------------------------------------------------------------------
# Gitea data fetching — per unique PR
# ---------------------------------------------------------------------------

def fetch_pr_data(parsed: dict, token: str | None) -> dict:
    """
    Fetch all comment sources for a single PR and return a lookup dict keyed
    by comment ID.

    Sources:
      - inline review comments  (from /pulls/{n}/reviews/{id}/comments)
      - review body comments    (from /pulls/{n}/reviews — the review's own body)
      - issue timeline comments (from /issues/{n}/comments)
    """
    api = parsed["api_url"]
    owner = parsed["owner"]
    repo = parsed["repo"]
    number = parsed["number"]
    repo_label = parsed["repo_label"]

    by_id: dict[int, dict] = {}

    # ── Inline review comments ───────────────────────────────────────────────
    try:
        reviews = gitea_get_paginated(
            f"{api}/repos/{owner}/{repo}/pulls/{number}/reviews", token
        )
        for review in reviews:
            rid = review.get("id")
            if not rid:
                continue

            # Review body itself (maps to an issuecomment anchor in html_url)
            rv_url = review.get("html_url", "")
            cm = COMMENT_ID_RE.search(rv_url)
            if cm:
                cid = int(cm.group(1))
                by_id[cid] = {
                    "repo": repo_label,
                    "path": "",
                    "body": (review.get("body") or "").strip(),
                    "diff_hunk": "",
                }

            # Inline comments within the review
            try:
                inline = gitea_get_paginated(
                    f"{api}/repos/{owner}/{repo}/pulls/{number}/reviews/{rid}/comments",
                    token,
                )
                for c in inline:
                    cid = c.get("id")
                    if cid:
                        by_id[cid] = {
                            "repo": repo_label,
                            "path": c.get("path", ""),
                            "body": (c.get("body") or "").strip(),
                            "diff_hunk": (c.get("diff_hunk") or "").strip(),
                        }
            except urllib.error.HTTPError:
                pass
    except urllib.error.HTTPError:
        pass

    # ── Issue timeline comments ──────────────────────────────────────────────
    try:
        timeline = gitea_get_paginated(
            f"{api}/repos/{owner}/{repo}/issues/{number}/comments", token
        )
        for c in timeline:
            cid = c.get("id")
            if cid:
                by_id[cid] = {
                    "repo": repo_label,
                    "path": "",
                    "body": (c.get("body") or "").strip(),
                    "diff_hunk": "",
                }
    except urllib.error.HTTPError:
        pass

    return by_id


def fetch_pr_meta(parsed: dict, token: str | None) -> dict:
    """Fetch minimal PR/issue metadata."""
    api = parsed["api_url"]
    owner = parsed["owner"]
    repo = parsed["repo"]
    number = parsed["number"]
    try:
        return gitea_get(f"{api}/repos/{owner}/{repo}/issues/{number}", token)
    except Exception:
        return {}


# ---------------------------------------------------------------------------
# Build flat output records
# ---------------------------------------------------------------------------

def build_output(entries: list[dict], token: str | None) -> list[dict]:
    """
    For each input entry, fetch the referenced comment and produce a flat record.
    PRs are fetched once and cached.
    """
    # Group entries by unique PR key to avoid duplicate API calls
    pr_cache: dict[str, dict] = {}  # key -> {by_id, meta}

    def pr_key(p: dict) -> str:
        return f"{p['api_url']}|{p['owner']}|{p['repo']}|{p['number']}"

    def ensure_fetched(p: dict):
        k = pr_key(p)
        if k not in pr_cache:
            print(f"  → {p['repo_label']} #{p['number']}", file=sys.stderr)
            pr_cache[k] = {
                "by_id": fetch_pr_data(p, token),
                "meta": fetch_pr_meta(p, token),
            }
        return pr_cache[k]

    result = []
    for entry in entries:
        p = entry["parsed"]
        feedback = entry["feedback"]
        cid = p["comment_id"]

        cached = ensure_fetched(p)
        by_id = cached["by_id"]
        meta = cached["meta"]

        if cid is not None:
            # Specific comment referenced
            if cid not in by_id:
                print(f"    [WARN] Comment {cid} not found in {p['repo_label']} #{p['number']}", file=sys.stderr)
                continue
            record = dict(by_id[cid])  # {repo, path, body, diff_hunk}
        else:
            # PR-level feedback — no specific comment
            record = {
                "repo": p["repo_label"],
                "path": "",
                "body": (meta.get("body") or "").strip(),
                "diff_hunk": "",
            }

        if feedback:
            # If same comment appears multiple times with different feedback, accumulate
            existing = next(
                (r for r in result if r.get("_comment_id") == cid and r["repo"] == record["repo"]),
                None,
            )
            if existing and cid is not None:
                fb = existing.get("feedback")
                if fb is None:
                    existing["feedback"] = feedback
                elif isinstance(fb, list):
                    fb.append(feedback)
                else:
                    existing["feedback"] = [fb, feedback]
                continue  # don't add a duplicate record

            record["feedback"] = feedback

        record["_comment_id"] = cid  # temp key for dedup, removed before writing
        result.append(record)

    # Strip internal tracking key
    for r in result:
        r.pop("_comment_id", None)

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Collect Gitea PR comments with feedback into a flat JSON report.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "urls",
        nargs="*",
        help="One or more Gitea issue/PR URLs (no feedback).",
    )
    parser.add_argument(
        "--file", "-f",
        metavar="FILE",
        help="Input file with URL => feedback pairs (one per entry).",
    )
    parser.add_argument(
        "--output", "-o",
        metavar="FILE",
        default="gitea-issues-report.json",
        help="Output JSON file path (default: gitea-issues-report.json).",
    )
    parser.add_argument(
        "--token",
        metavar="TOKEN",
        default=None,
        help="Gitea personal access token (overrides GITEA_TOKEN env var).",
    )

    args = parser.parse_args()

    # Collect entries
    entries: list[dict] = []
    if args.file:
        try:
            entries.extend(parse_input_file(args.file))
        except FileNotFoundError:
            print(f"[ERROR] File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    if args.urls:
        entries.extend(parse_inline_urls(args.urls))

    if not entries:
        parser.print_help()
        sys.exit(1)

    token = args.token or os.environ.get("GITEA_TOKEN")
    if not token:
        print("[WARN] No GITEA_TOKEN found — requests will be unauthenticated.", file=sys.stderr)

    print(f"Processing {len(entries)} input URL(s)...", file=sys.stderr)
    records = build_output(entries, token)

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(records, fh, indent=2, ensure_ascii=False)

    total_fb = sum(1 for r in records if "feedback" in r)
    print(f"\nDone. {len(records)} record(s), {total_fb} with feedback → {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
