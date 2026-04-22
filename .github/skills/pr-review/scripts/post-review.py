#!/usr/bin/env python3
"""
PR Review Comment Dispatcher

Unified dispatcher script that handles everything after generating review.json:
- Reads review.json from project root
- Reads platform from project.config.json (searches multiple locations)
- Resolves repo config from platformConfig (and optional repos map)
- Transforms standard review output to platform-specific API format
- Posts inline comments directly to the appropriate Git platform
- Sends Google Chat notification if enableNotification is true in config

Supported Platforms:
- GitHub (via GitHub API)
- GitLab (via GitLab API)
- Gitea (via Gitea API)
- Bitbucket (via Bitbucket API)

Configuration Options:
- enableCommentPosting (boolean, default: true): Enable/disable posting inline comments
- enableNotification (boolean, default: false): Enable/disable Google Chat notifications

Operation Modes (controlled by config + token availability):

1. Full Mode: Posts inline comments + sends notification
   - Config: enableCommentPosting=true, enableNotification=true
   - Requires: Platform token configured
   
2. Comment-Only Mode: Posts inline comments, no notification
   - Config: enableCommentPosting=true, enableNotification=false
   - Requires: Platform token configured
   
3. Notification-Only Mode: Skips inline comments, only sends notification
   - Config: enableCommentPosting=false, enableNotification=true
   - OR: enableCommentPosting=true (but no token), enableNotification=true
   - No platform token needed
   - Useful for testing or when you only want notifications

All platform-specific logic is integrated into this single dispatcher script.

Usage:
    python {PR_REVIEW_SKILL_PATH}/scripts/post-review.py              # Post review comments
    python3 {PR_REVIEW_SKILL_PATH}/scripts/post-review.py             # Alternative Python 3 command
    python {PR_REVIEW_SKILL_PATH}/scripts/post-review.py --dry-run    # Transform only, do not post

    Where {PR_REVIEW_SKILL_PATH} is the absolute path to pr-review skill folder:
    - Cursor IDE: .cursor/skills/pr-review
    - GitHub Copilot: .github/skills/pr-review
    - Other agents: .agent/skills/pr-review (or configured path)

    The script reads review.json from the project root directory.
"""

import sys
import os
import json
import ssl
import urllib.request
import urllib.error
import urllib.parse
import base64
import re
from datetime import datetime

# Default file paths
DEFAULT_REVIEW_FILE = 'review.json'
CONFIG_SEARCH_PATHS = [
    '.documents-design/project.config.json',
    '.cursor/project.config.json',
    '.github/project.config.json',
    '.agent/project.config.json',
    '.claude/project.config.json'
]

def load_json_file(file_path: str) -> dict:
    """Load and parse a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_no_proxy_opener():
    """Create a URL opener that bypasses proxy settings with SSL verification disabled."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return urllib.request.build_opener(
        urllib.request.ProxyHandler({}),
        urllib.request.HTTPSHandler(context=ctx)
    )

def get_config() -> tuple[dict, str]:
    """Load the project configuration. Returns (config, path)."""
    for config_path in CONFIG_SEARCH_PATHS:
        if os.path.isfile(config_path):
            return load_json_file(config_path), config_path
    raise FileNotFoundError(f"Configuration file not found. Searched: {CONFIG_SEARCH_PATHS}")


def resolve_repo_config(config: dict, repo_name: str) -> dict:
    """Resolve repo-specific config from platformConfig and optional repos map.
    
    Supports two config styles:
    1. Flat: platformConfig contains all fields (apiUrl, owner, repo) directly.
       The key inside platformConfig does not need to match the platform value.
    2. Split: platformConfig has apiUrl, repos map has owner/repo per repo name.
    
    Returns a merged dict with all connection fields (apiUrl, owner, repo, etc.).
    """
    platform = config.get('platform', 'github')
    platform_cfg = config.get('platformConfig', {})
    # Try matching by platform name first, then fall back to the first entry
    platform_config = platform_cfg.get(platform) or next(iter(platform_cfg.values()), {})
    repo_config = config.get('repos', {}).get(repo_name, {}).get(platform, {})
    return {**platform_config, **repo_config}

def get_platform(config: dict) -> str:
    """Extract platform from configuration."""
    return config.get('platform', 'github')

def is_notification_enabled(config: dict) -> bool:
    """Check if notifications are enabled."""
    return config.get('enableNotification', False)

def is_comment_posting_enabled(config: dict) -> bool:
    """Check if comment posting is enabled. Defaults to True for backward compatibility."""
    return config.get('enableCommentPosting', False)

def has_platform_token(platform: str) -> bool:
    """Check if the required token for the platform is available."""
    token_map = {
        'github': 'GITHUB_TOKEN',
        'gitlab': 'GITLAB_TOKEN',
        'gitea': 'GITEA_TOKEN',
        'bitbucket': 'BITBUCKET_TOKEN'
    }
    env_var = token_map.get(platform)
    return bool(env_var and os.environ.get(env_var))


# =============================================================================
# GitHub Platform Implementation
# =============================================================================

def transform_to_github_format(standard_review: dict) -> dict:
    """Transform standard review output to GitHub Reviews API format."""
    status_map = {
        "APPROVE": "APPROVE",
        "REQUEST_CHANGES": "REQUEST_CHANGES",
        "COMMENT": "COMMENT"
    }
    event = status_map.get(standard_review.get('status', 'COMMENT'), 'COMMENT')
    
    # Build summary body with statistics
    stats = standard_review.get('statistics', {})
    summary_parts = [standard_review.get('summary', 'Automated PR Review')]
    
    if stats:
        summary_parts.append(f"\n\n📊 **Review Statistics**")
        summary_parts.append(f"- Files reviewed: {stats.get('filesReviewed', 0)}")
        summary_parts.append(f"- Critical issues: {stats.get('criticalCount', 0)}")
        summary_parts.append(f"- Warnings: {stats.get('warningCount', 0)}")
        summary_parts.append(f"- Suggestions: {stats.get('suggestionCount', 0)}")
    
    # Transform comments
    github_comments = []
    for comment in standard_review.get('comments', []):
        github_comment = {
            "path": comment.get('path'),
            "line": comment.get('line'),
            "side": "RIGHT",
            "body": transform_comment_body(comment)
        }
        github_comments.append(github_comment)
    
    return {
        "event": event,
        "body": "\n".join(summary_parts),
        "comments": github_comments
    }


def post_github_review(standard_review: dict, config: dict, dry_run: bool = False) -> dict:
    """Post review to GitHub API."""
    if dry_run:
        github_payload = transform_to_github_format(standard_review)
        return {"success": True, "dryRun": True, "platform": "github", "payload": github_payload}
    
    repo_name = config.get('_repoName', 'webAuto')
    resolved = resolve_repo_config(config, repo_name)
    api_url = resolved.get('apiUrl', 'https://api.github.com')
    owner = resolved.get('owner')
    repo = resolved.get('repo')
    
    if not owner or not repo:
        return {
            "success": False,
            "platform": "github",
            "error": f"Owner and repo must be specified in platformConfig or repos.{repo_name}.github"
        }
    
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        return {
            "success": False,
            "platform": "github",
            "error": "GitHub token not found. Set GITHUB_TOKEN environment variable.",
            "skipped": True
        }
    
    pr_number = standard_review.get('prNumber')
    github_payload = transform_to_github_format(standard_review)
    url = f"{api_url}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(github_payload).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        opener = create_no_proxy_opener()

        with opener.open(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return {
                "success": True,
                "platform": "github",
                "reviewId": result.get('id'),
                "htmlUrl": result.get('html_url'),
                "state": result.get('state'),
                "commentsPosted": len(github_payload.get('comments', []))
            }
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        return {
            "success": False,
            "platform": "github",
            "error": f"HTTP {e.code}: {e.reason}",
            "details": error_body
        }
    except urllib.error.URLError as e:
        return {
            "success": False,
            "platform": "github",
            "error": f"Connection error: {e.reason}"
        }


# =============================================================================
# GitLab Platform Implementation
# =============================================================================

def escape_html_tags(text: str) -> str:
    """Wrap bare HTML tags in backticks so they render as literal text in markdown."""
    import re
    return re.sub(r'<(/?\w[\w\d]*(?:\s[^>]*)?)>', r'`<\1>`', text)


def transform_comment_body(comment: dict) -> str:
    """Transform a single comment to markdown format."""
    severity_emoji = {
        'critical': '🔴',
        'warning': '🟡',
        'suggestion': '💡'
    }.get(comment.get('severity', 'warning'), '💬')

    category = comment.get('category', 'Review')
    title = comment.get('title', 'Issue')
    body = escape_html_tags(comment.get('body', ''))
    recommendation = escape_html_tags(comment.get('recommendation', ''))
    code_snippet = comment.get('codeSnippet', '')

    parts = [f"{severity_emoji} **[{category}] {title}**", body]

    if recommendation:
        parts.append(f"**Recommendation:** {recommendation}")

    if code_snippet:
        parts.append(f"```\n{code_snippet}\n```")

    return "\n\n".join(parts)


def build_summary_note(standard_review: dict) -> str:
    """Build the summary note for GitLab."""
    status = standard_review.get('status', 'COMMENT')
    stats = standard_review.get('statistics', {})
    
    status_emoji = {
        'APPROVE': '✅',
        'REQUEST_CHANGES': '⚠️',
        'COMMENT': '💬'
    }.get(status, '💬')
    
    summary_parts = [f"{status_emoji} **Automated MR Review**"]
    summary_parts.append("")
    summary_parts.append(standard_review.get('summary', ''))
    
    if stats:
        summary_parts.append("")
        summary_parts.append("📊 **Statistics**")
        summary_parts.append(f"| Metric | Count |")
        summary_parts.append(f"|--------|-------|")
        summary_parts.append(f"| Files reviewed | {stats.get('filesReviewed', 0)} |")
        summary_parts.append(f"| Critical issues | {stats.get('criticalCount', 0)} |")
        summary_parts.append(f"| Warnings | {stats.get('warningCount', 0)} |")
        summary_parts.append(f"| Suggestions | {stats.get('suggestionCount', 0)} |")
    
    return "\n".join(summary_parts)


def get_mr_versions(project_id: str, mr_iid: int, api_url: str, token: str) -> dict:
    """Get diff versions to obtain SHA values required for inline comments."""
    encoded_project_id = urllib.parse.quote(str(project_id), safe='')
    url = f"{api_url}/projects/{encoded_project_id}/merge_requests/{mr_iid}/versions"
    
    headers = {'PRIVATE-TOKEN': token}
    req = urllib.request.Request(url, headers=headers, method='GET')
    
    try:
        opener = create_no_proxy_opener()

        with opener.open(req) as response:
            versions = json.loads(response.read().decode('utf-8'))
            if versions and len(versions) > 0:
                latest = versions[0]
                return {
                    "success": True,
                    "head_sha": latest.get('head_commit_sha'),
                    "base_sha": latest.get('base_commit_sha'),
                    "start_sha": latest.get('start_commit_sha')
                }
            return {"success": False, "error": "No versions found"}
    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP {e.code}: {e.reason}"}


def post_gitlab_note(project_id: str, mr_iid: int, body: str, api_url: str, token: str) -> dict:
    """Post a general note to MR."""
    encoded_project_id = urllib.parse.quote(str(project_id), safe='')
    url = f"{api_url}/projects/{encoded_project_id}/merge_requests/{mr_iid}/notes"
    
    headers = {
        'Content-Type': 'application/json',
        'PRIVATE-TOKEN': token
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps({"body": body}).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        opener = create_no_proxy_opener()

        with opener.open(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return {"success": True, "noteId": result.get('id')}
    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP {e.code}: {e.reason}"}


def post_gitlab_discussion(project_id: str, mr_iid: int, comment: dict, 
                           sha_info: dict, api_url: str, token: str) -> dict:
    """Post an inline discussion thread."""
    encoded_project_id = urllib.parse.quote(str(project_id), safe='')
    url = f"{api_url}/projects/{encoded_project_id}/merge_requests/{mr_iid}/discussions"
    
    payload = {
        "body": transform_comment_body(comment),
        "position": {
            "position_type": "text",
            "new_path": comment.get('path'),
            "new_line": comment.get('line'),
            "base_sha": sha_info.get('base_sha'),
            "head_sha": sha_info.get('head_sha'),
            "start_sha": sha_info.get('start_sha')
        }
    }
    
    headers = {
        'Content-Type': 'application/json',
        'PRIVATE-TOKEN': token
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        opener = create_no_proxy_opener()

        with opener.open(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return {"success": True, "discussionId": result.get('id')}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        return {"success": False, "error": f"HTTP {e.code}", "details": error_body}


def approve_gitlab_mr(project_id: str, mr_iid: int, api_url: str, token: str) -> dict:
    """Approve the MR."""
    encoded_project_id = urllib.parse.quote(str(project_id), safe='')
    url = f"{api_url}/projects/{encoded_project_id}/merge_requests/{mr_iid}/approve"
    
    headers = {'PRIVATE-TOKEN': token}
    req = urllib.request.Request(url, headers=headers, method='POST')
    
    try:
        opener = create_no_proxy_opener()

        with opener.open(req) as response:
            return {"success": True, "approved": True}
    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP {e.code}: {e.reason}"}


def post_gitlab_review(standard_review: dict, config: dict, dry_run: bool = False) -> dict:
    """Post review to GitLab API."""
    if dry_run:
        return {
            "success": True,
            "dryRun": True,
            "platform": "gitlab",
            "summary": build_summary_note(standard_review),
            "comments": [transform_comment_body(c) for c in standard_review.get('comments', [])]
        }
    
    repo_name = config.get('_repoName', 'webAuto')
    resolved = resolve_repo_config(config, repo_name)
    api_url = resolved.get('apiUrl', 'https://gitlab.com/api/v4')
    project_id = resolved.get('projectId')
    
    if not project_id:
        return {
            "success": False,
            "platform": "gitlab",
            "error": f"projectId must be specified in platformConfig or repos.{repo_name}.gitlab"
        }
    
    token = os.environ.get('GITLAB_TOKEN')
    if not token:
        return {
            "success": False,
            "platform": "gitlab",
            "error": "GitLab token not found. Set GITLAB_TOKEN environment variable.",
            "skipped": True
        }
    
    mr_iid = standard_review.get('prNumber')
    status = standard_review.get('status', 'COMMENT')
    
    # Get SHA values
    sha_info = get_mr_versions(project_id, mr_iid, api_url, token)
    if not sha_info.get('success'):
        return {
            "success": False,
            "platform": "gitlab",
            "error": f"Failed to get MR versions: {sha_info.get('error')}"
        }
    
    # Post summary note
    summary_body = build_summary_note(standard_review)
    summary_result = post_gitlab_note(project_id, mr_iid, summary_body, api_url, token)
    
    # Post inline comments
    successful = 0
    failed = []
    
    for comment in standard_review.get('comments', []):
        result = post_gitlab_discussion(project_id, mr_iid, comment, sha_info, api_url, token)
        if result.get('success'):
            successful += 1
        else:
            failed.append({
                "path": comment.get('path'),
                "line": comment.get('line'),
                "error": result.get('error')
            })
    
    # Handle approval
    approval_result = None
    if status == 'APPROVE':
        approval_result = approve_gitlab_mr(project_id, mr_iid, api_url, token)
    
    return {
        "success": len(failed) == 0,
        "platform": "gitlab",
        "mrIid": mr_iid,
        "summaryPosted": summary_result.get('success', False),
        "commentsPosted": successful,
        "failedComments": failed if failed else None,
        "approved": approval_result.get('approved') if approval_result else None
    }


# =============================================================================
# Gitea Platform Implementation
# =============================================================================

def transform_to_gitea_format(standard_review: dict) -> dict:
    """Transform standard review output to Gitea Reviews API format."""
    
    # Build summary body with statistics
    stats = standard_review.get('statistics', {})
    summary_parts = [standard_review.get('summary', 'Automated PR Review')]
    
    # Transform comments
    gitea_comments = []
    for comment in standard_review.get('comments', []):
        gitea_comment = {
            "path": comment.get('path'),
            "new_position": comment.get('line'),  # Gitea uses new_position
            "old_position": 0,  # 0 for new lines
            "body": transform_comment_body(comment)
        }
        gitea_comments.append(gitea_comment)
    
    return {
        "event": 'COMMENT',
        "body": "\n".join(summary_parts),
        "comments": gitea_comments
    }


def post_gitea_review(standard_review: dict, config: dict, dry_run: bool = False) -> dict:
    """Post review to Gitea API."""
    if dry_run:
        gitea_payload = transform_to_gitea_format(standard_review)
        return {"success": True, "dryRun": True, "platform": "gitea", "payload": gitea_payload}
    
    repo_name = config.get('_repoName', 'webAuto')
    resolved = resolve_repo_config(config, repo_name)
    api_url = resolved.get('apiUrl', 'https://gitea.example.com/api/v1')
    owner = resolved.get('owner')
    repo = resolved.get('repo')
    
    if not owner or not repo:
        return {
            "success": False,
            "platform": "gitea",
            "error": f"Owner and repo must be specified in platformConfig or repos.{repo_name}.gitea"
        }
    
    token = os.environ.get('GITEA_TOKEN')
    if not token:
        return {
            "success": False,
            "platform": "gitea",
            "error": "Gitea token not found. Set GITEA_TOKEN environment variable.",
            "skipped": True
        }
    
    pr_number = standard_review.get('prNumber')
    gitea_payload = transform_to_gitea_format(standard_review)
    url = f"{api_url}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'token {token}',
        'Accept': 'application/json'
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(gitea_payload).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        opener = create_no_proxy_opener()

        with opener.open(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return {
                "success": True,
                "platform": "gitea",
                "reviewId": result.get('id'),
                "htmlUrl": result.get('html_url'),
                "state": result.get('state'),
                "commentsPosted": len(gitea_payload.get('comments', []))
            }
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        return {
            "success": False,
            "platform": "gitea",
            "error": f"HTTP {e.code}: {e.reason}",
            "details": error_body
        }
    except urllib.error.URLError as e:
        return {
            "success": False,
            "platform": "gitea",
            "error": f"Connection error: {e.reason}"
        }


# =============================================================================
# Bitbucket Platform Implementation
# =============================================================================

def build_bitbucket_summary(standard_review: dict) -> dict:
    """Build the summary comment payload for Bitbucket."""
    status = standard_review.get('status', 'COMMENT')
    stats = standard_review.get('statistics', {})
    
    status_emoji = {
        'APPROVE': '✅',
        'REQUEST_CHANGES': '⚠️',
        'COMMENT': '💬'
    }.get(status, '💬')
    
    summary_parts = [f"{status_emoji} **Automated PR Review**"]
    summary_parts.append("")
    summary_parts.append(standard_review.get('summary', ''))
    
    if stats:
        summary_parts.append("")
        summary_parts.append("📊 **Statistics**")
        summary_parts.append(f"- Files reviewed: {stats.get('filesReviewed', 0)}")
        summary_parts.append(f"- Critical issues: {stats.get('criticalCount', 0)}")
        summary_parts.append(f"- Warnings: {stats.get('warningCount', 0)}")
        summary_parts.append(f"- Suggestions: {stats.get('suggestionCount', 0)}")
    
    return {
        "content": {
            "raw": "\n".join(summary_parts)
        }
    }


def transform_bitbucket_inline_comment(comment: dict) -> dict:
    """Transform a standard comment to Bitbucket inline comment format."""
    return {
        "content": {
            "raw": transform_comment_body(comment)
        },
        "inline": {
            "path": comment.get('path'),
            "to": comment.get('line')  # Bitbucket uses 'to' for line number
        }
    }


def get_bitbucket_auth_header(platform_config: dict) -> dict:
    """Get authentication header for Bitbucket API. Returns dict with success and auth_header or error."""
    token = os.environ.get('BITBUCKET_TOKEN')
    username = os.environ.get('BITBUCKET_USERNAME')
    
    if token and username:
        # App Password with Basic Auth
        credentials = base64.b64encode(f"{username}:{token}".encode()).decode()
        return {"success": True, "auth_header": f"Basic {credentials}"}
    elif token:
        # OAuth Bearer token
        return {"success": True, "auth_header": f"Bearer {token}"}
    else:
        return {
            "success": False,
            "error": "Bitbucket credentials not found. Set BITBUCKET_TOKEN environment variable.",
            "skipped": True
        }


def post_bitbucket_comment(workspace: str, repo_slug: str, pr_id: int, 
                           payload: dict, api_url: str, auth_header: str) -> dict:
    """Post a comment to Bitbucket PR."""
    url = f"{api_url}/repositories/{workspace}/{repo_slug}/pullrequests/{pr_id}/comments"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth_header
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        opener = create_no_proxy_opener()

        with opener.open(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return {"success": True, "commentId": result.get('id')}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        return {"success": False, "error": f"HTTP {e.code}", "details": error_body}


def approve_bitbucket_pr(workspace: str, repo_slug: str, pr_id: int, 
                         api_url: str, auth_header: str) -> dict:
    """Approve the PR."""
    url = f"{api_url}/repositories/{workspace}/{repo_slug}/pullrequests/{pr_id}/approve"
    
    headers = {'Authorization': auth_header}
    req = urllib.request.Request(url, headers=headers, method='POST')
    
    try:
        opener = create_no_proxy_opener()

        with opener.open(req) as response:
            return {"success": True, "approved": True}
    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP {e.code}: {e.reason}"}


def request_bitbucket_changes(workspace: str, repo_slug: str, pr_id: int,
                              api_url: str, auth_header: str) -> dict:
    """Request changes on the PR."""
    url = f"{api_url}/repositories/{workspace}/{repo_slug}/pullrequests/{pr_id}/request-changes"
    
    headers = {'Authorization': auth_header}
    req = urllib.request.Request(url, headers=headers, method='POST')
    
    try:
        opener = create_no_proxy_opener()

        with opener.open(req) as response:
            return {"success": True, "changesRequested": True}
    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP {e.code}: {e.reason}"}


def post_bitbucket_review(standard_review: dict, config: dict, dry_run: bool = False) -> dict:
    """Post review to Bitbucket API."""
    if dry_run:
        return {
            "success": True,
            "dryRun": True,
            "platform": "bitbucket",
            "summary": build_bitbucket_summary(standard_review),
            "comments": [transform_bitbucket_inline_comment(c) for c in standard_review.get('comments', [])]
        }
    
    repo_name = config.get('_repoName', 'webAuto')
    resolved = resolve_repo_config(config, repo_name)
    api_url = resolved.get('apiUrl', 'https://api.bitbucket.org/2.0')
    workspace = resolved.get('workspace')
    repo_slug = resolved.get('repoSlug')
    
    if not workspace or not repo_slug:
        return {
            "success": False,
            "platform": "bitbucket",
            "error": f"workspace and repoSlug must be specified in platformConfig or repos.{repo_name}.bitbucket"
        }
    
    auth_result = get_bitbucket_auth_header(resolved)
    if not auth_result.get('success'):
        return {
            "success": False,
            "platform": "bitbucket",
            "error": auth_result.get('error'),
            "skipped": True
        }
    
    auth_header = auth_result.get('auth_header')
    
    pr_id = standard_review.get('prNumber')
    status = standard_review.get('status', 'COMMENT')
    
    # Post summary comment
    summary_payload = build_bitbucket_summary(standard_review)
    summary_result = post_bitbucket_comment(workspace, repo_slug, pr_id, summary_payload, api_url, auth_header)
    
    # Post inline comments
    successful = 0
    failed = []
    
    for comment in standard_review.get('comments', []):
        inline_payload = transform_bitbucket_inline_comment(comment)
        result = post_bitbucket_comment(workspace, repo_slug, pr_id, inline_payload, api_url, auth_header)
        
        if result.get('success'):
            successful += 1
        else:
            failed.append({
                "path": comment.get('path'),
                "line": comment.get('line'),
                "error": result.get('error')
            })
    
    # Set approval status
    status_result = None
    if status == 'APPROVE':
        status_result = approve_bitbucket_pr(workspace, repo_slug, pr_id, api_url, auth_header)
    elif status == 'REQUEST_CHANGES':
        status_result = request_bitbucket_changes(workspace, repo_slug, pr_id, api_url, auth_header)
    
    return {
        "success": len(failed) == 0,
        "platform": "bitbucket",
        "prId": pr_id,
        "workspace": workspace,
        "repoSlug": repo_slug,
        "summaryPosted": summary_result.get('success', False),
        "commentsPosted": successful,
        "failedComments": failed if failed else None,
        "statusSet": status_result.get('success') if status_result else None
    }


# =============================================================================
# Platform Script Dispatcher
# =============================================================================

def post_to_platform(platform: str, standard_review: dict, config: dict, dry_run: bool = False) -> dict:
    """
    Post review to the specified platform.
    
    Directly handles transformation and API calls for each platform.
    """
    platform_handlers = {
        'github': post_github_review,
        'gitea': post_gitea_review,
        'gitlab': post_gitlab_review,
        'bitbucket': post_bitbucket_review
    }
    
    if platform not in platform_handlers:
        return {
            "success": False,
            "error": f"Unsupported platform: {platform}",
            "supportedPlatforms": list(platform_handlers.keys())
        }
    
    try:
        return platform_handlers[platform](standard_review, config, dry_run)
    except Exception as e:
        return {
            "success": False,
            "platform": platform,
            "error": f"Exception: {str(e)}"
        }


# =============================================================================
# Notification
# =============================================================================

def fetch_gitea_pr_info(pr_number: int, config: dict) -> dict:
    """Fetch PR information from Gitea API."""
    platform = config.get('platform', '')
    
    if platform != 'gitea':
        return {"success": False, "error": "Not a Gitea platform"}
    
    repo_name = config.get('_repoName', 'webAuto')
    resolved = resolve_repo_config(config, repo_name)
    api_url = resolved.get('apiUrl', '')
    owner = resolved.get('owner', '')
    repo = resolved.get('repo', '')
    
    if not api_url or not owner or not repo:
        return {"success": False, "error": "Missing Gitea configuration"}
    
    token = os.environ.get('GITEA_TOKEN')
    if not token:
        return {"success": False, "error": "GITEA_TOKEN not set"}
    
    url = f"{api_url}/repos/{owner}/{repo}/pulls/{pr_number}"
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/json'
    }
    
    req = urllib.request.Request(url, headers=headers, method='GET')
    
    try:
        opener = create_no_proxy_opener()

        with opener.open(req) as response:
            pr_data = json.loads(response.read().decode('utf-8'))
            return {
                "success": True,
                "data": {
                    "title": pr_data.get('title', ''),
                    "body": pr_data.get('body', ''),
                    "state": pr_data.get('state', ''),
                    "user": pr_data.get('user', {}).get('login', ''),
                    "created_at": pr_data.get('created_at', ''),
                    "updated_at": pr_data.get('updated_at', ''),
                    "html_url": pr_data.get('html_url', ''),
                    "base_branch": pr_data.get('base', {}).get('ref', ''),
                    "head_branch": pr_data.get('head', {}).get('ref', ''),
                    "mergeable": pr_data.get('mergeable', False),
                    "merged": pr_data.get('merged', False),
                    "additions": pr_data.get('additions', 0),
                    "deletions": pr_data.get('deletions', 0),
                    "changed_files": pr_data.get('changed_files', 0)
                }
            }
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        return {
            "success": False,
            "error": f"HTTP {e.code}: {e.reason}",
            "details": error_body
        }
    except urllib.error.URLError as e:
        return {
            "success": False,
            "error": f"Connection error: {e.reason}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }


def generate_summary_file(standard_review: dict, config: dict, output_path: str) -> str:
    """Generate a markdown summary file for notifications."""
    status = standard_review.get('status', 'COMMENT')
    stats = standard_review.get('statistics', {})
    pr_number = standard_review.get('prNumber')
    
    status_emoji = {
        'APPROVE': '✅',
        'REQUEST_CHANGES': '🔴',
        'COMMENT': '💬'
    }.get(status, '💬')
    
    # Fetch PR information from Gitea if available
    pr_info = fetch_gitea_pr_info(pr_number, config)
    pr_data = pr_info.get('data', {}) if pr_info.get('success') else {}
    
    lines = [
        f"# PR Review Report",
        ""
    ]
    
    # Add PR information if available from Gitea
    if pr_data:
        lines.extend([
            f"## Pull Request Information",
            "",
            f"**PR Number**: #{pr_number}",
            f"**Title**: {pr_data.get('title', 'N/A')}",
            f"**Author**: {pr_data.get('user', 'N/A')}",
            f"**Branch**: {pr_data.get('head_branch', 'unknown')} → {pr_data.get('base_branch', 'main')}",
            f"**State**: {pr_data.get('state', 'unknown').upper()}",
            f"**Mergeable**: {'✅ Yes' if pr_data.get('mergeable') else '❌ No'}",
            f"**Changes**: +{pr_data.get('additions', 0)} -{pr_data.get('deletions', 0)} ({pr_data.get('changed_files', 0)} files)",
            f"**Created**: {pr_data.get('created_at', 'N/A')}",
            f"**Updated**: {pr_data.get('updated_at', 'N/A')}",
            ""
        ])
        
        # Add PR description if available
        if pr_data.get('body'):
            lines.extend([
                "### Description",
                "",
                pr_data.get('body'),
                ""
            ])
        
        # Add PR URL if available
        if pr_data.get('html_url'):
            lines.extend([
                f"**🔗 PR Link**: {pr_data.get('html_url')}",
                ""
            ])
    else:
        # Fallback to metadata from standard_review
        lines.extend([
            f"**PR Number**: #{pr_number}",
            f"**Branch**: {standard_review.get('metadata', {}).get('sourceBranch', 'unknown')} → {standard_review.get('metadata', {}).get('baseBranch', 'main')}",
            ""
        ])
    
    lines.extend([
        "---",
        "",
        "## Review Status",
        "",
        f"**Status**: {status_emoji} {status}",
        f"**Files Reviewed**: {stats.get('filesReviewed', 0)}",
        "",
        "---",
        "",
        "## Review Summary",
        "",
        standard_review.get('summary', 'No summary provided.'),
        "",
        "---",
        "",
        f"## Critical Issues ({stats.get('criticalCount', 0)})",
        ""
    ])
    
    critical_comments = [c for c in standard_review.get('comments', []) 
                         if c.get('severity') == 'critical']
    
    if critical_comments:
        for i, c in enumerate(critical_comments, 1):
            lines.append(f"{i}. **[{c.get('category')}]** `{c.get('path')}:{c.get('line')}` - {c.get('title')}")
    else:
        lines.append("✅ No critical issues found.")
    
    lines.extend([
        "",
        "---",
        "",
        f"## Warnings ({stats.get('warningCount', 0)})",
        ""
    ])
    
    warning_comments = [c for c in standard_review.get('comments', []) 
                        if c.get('severity') == 'warning']
    
    if warning_comments:
        for i, c in enumerate(warning_comments, 1):
            lines.append(f"{i}. **[{c.get('category')}]** `{c.get('path')}:{c.get('line')}` - {c.get('title')}")
    else:
        lines.append("✅ No warnings found.")
    
    lines.extend([
        "",
        "---",
        "",
        f"*Generated by PR Review Agent on {datetime.now().isoformat()}*"
    ])
    
    content = "\n".join(lines)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return output_path


def send_notification(summary_file: str, config: dict, standard_review: dict, compact: bool = False) -> dict:
    """Send a Google Chat notification. compact=True sends stats-only card (when comments were posted to Gitea).
    compact=False sends the full rich card with Review Summary, Requirements Coverage, and per-comment sections."""
    webhook_url = os.environ.get('GOOGLE_CHAT_WEBHOOK_URL')
    if not webhook_url:
        return {"success": False, "error": "GOOGLE_CHAT_WEBHOOK_URL not set"}

    if not os.path.isfile(summary_file):
        return {"success": False, "error": f"Summary file not found: {summary_file}"}

    with open(summary_file, 'r', encoding='utf-8') as f:
        content = f.read()

    def _extract(pattern, default=''):
        m = re.search(pattern, content)
        return m.group(1).strip() if m else default

    branch        = _extract(r'\*\*Branch\*\*:\s*(.*)')
    pr_title      = _extract(r'\*\*Title\*\*:\s*(.*)', f"PR #{standard_review.get('prNumber', 'N/A')}")
    author        = _extract(r'\*\*Author\*\*:\s*(.*)', 'Unknown')
    critical_count = int(_extract(r'Critical Issues \(([0-9]*)\)', '0'))
    warning_count  = int(_extract(r'Warnings \(([0-9]*)\)', '0'))

    stats            = standard_review.get('statistics', {})
    suggestion_count = stats.get('suggestionCount', 0)

    review_status = standard_review.get('status', '')
    if review_status == 'REQUEST_CHANGES':
        status, status_short = "Changes Required",    "🔴"
    elif review_status == 'COMMENT':
        status, status_short = "Changes Recommended", "🟡"
    elif review_status == 'APPROVE':
        status, status_short = "Approved",            "✅"
    else:
        status, status_short = "Reviewed",            "💬"

    pr_number        = standard_review.get('prNumber')
    platform         = config.get('platform', 'github')
    config_repo_name = config.get('_repoName', 'webAuto')
    resolved         = resolve_repo_config(config, config_repo_name)
    repo_display     = resolved.get('repo', '') or resolved.get('repoSlug', '') or config_repo_name

    # Build PR URL
    pr_url = None
    if platform == 'github':
        api_url = resolved.get('apiUrl', 'https://api.github.com')
        owner, repo = resolved.get('owner', ''), resolved.get('repo', '')
        if owner and repo:
            base = api_url.replace('api.github.com', 'github.com').replace('/api/v3', '')
            pr_url = f"{base}/{owner}/{repo}/pull/{pr_number}"
    elif platform == 'gitea':
        api_url = resolved.get('apiUrl', '')
        owner, repo = resolved.get('owner', ''), resolved.get('repo', '')
        if api_url and owner and repo:
            pr_url = f"{api_url.replace('/api/v1', '')}/{owner}/{repo}/pulls/{pr_number}"
    elif platform == 'gitlab':
        api_url    = resolved.get('apiUrl', 'https://gitlab.com/api/v4')
        project_id = resolved.get('projectId', '')
        if project_id:
            pr_url = f"{api_url.replace('/api/v4', '')}/merge_requests/{pr_number}"
    elif platform == 'bitbucket':
        workspace = resolved.get('workspace', '')
        repo_slug = resolved.get('repoSlug', '')
        if workspace and repo_slug:
            pr_url = f"https://bitbucket.org/{workspace}/{repo_slug}/pull-requests/{pr_number}"

    comments      = standard_review.get('comments', [])
    comment_count = len(comments)
    unique_files  = len(set(c.get('path') for c in comments if c.get('path')))
    comment_text  = "comment" if comment_count == 1 else "comments"
    file_text     = "file"    if unique_files == 1  else "files"
    review_info   = f"{datetime.now().strftime('%m/%d/%Y %H:%M:%S')} • {comment_count} {comment_text} found at {unique_files} {file_text}"

    # --- Header stats section ---
    widgets = [{"decoratedText": {"text": review_info}}]
    if pr_url:
        widgets.append({"buttonList": {"buttons": [{
            "text": "View Pull Request",
            "onClick": {"openLink": {"url": pr_url}},
        }]}})
    widgets += [
        {"decoratedText": {"topLabel": "📊 Issue Summary"}},
        {"decoratedText": {"topLabel": f"🔴 Critical: {critical_count}"}},
        {"decoratedText": {"topLabel": f"🟡 Warnings: {warning_count}"}},
        {"decoratedText": {"topLabel": f"⚪ Suggestions: {suggestion_count}"}},
        {"decoratedText": {"topLabel": f"🤖 AI Reviewer: {status}"}},
    ]

    # --- Rich sections (only when comments were NOT posted to the platform) ---
    extra_sections = []
    if not compact:
        raw_summary = standard_review.get('summary', '')
        req_marker  = '### ✅ Requirements Coverage'
        narrative   = raw_summary.split(req_marker)[0].strip()
        has_req_table = req_marker in raw_summary

        if narrative:
            extra_sections.append({
                "header": "📝 Review Summary",
                "collapsible": True,
                "uncollapsibleWidgetsCount": 1,
                "widgets": [{"textParagraph": {"text": narrative.replace('\n', '<br>')}}],
            })

        if has_req_table:
            req_block   = raw_summary.split(req_marker, 1)[1]
            req_widgets = []
            for line in req_block.splitlines():
                line = line.strip()
                if line.startswith('|') and not line.startswith('|---') and not line.startswith('| #'):
                    cols = [c.strip() for c in line.strip('|').split('|')]
                    if len(cols) >= 5:
                        num, req, st, confidence, evidence = cols[0], cols[1], cols[2], cols[3], cols[4]
                        req_widgets.append({"textParagraph": {
                            "text": (
                                f"<b>{num}. {st} {req}</b><br>"
                                f"<i>Confidence: {confidence}</i><br>"
                                f"{evidence}"
                            )
                        }})
            if req_widgets:
                extra_sections.append({
                    "header": "✅ Requirements Coverage",
                    "collapsible": True,
                    "uncollapsibleWidgetsCount": 2,
                    "widgets": req_widgets,
                })

        meta        = standard_review.get('metadata', {})
        commit_sha  = meta.get('commitSha', '')
        pr_info     = fetch_gitea_pr_info(pr_number, config) if platform == 'gitea' else {}
        pr_detail   = pr_info.get('data', {}) if pr_info.get('success') else {}
        head_branch = pr_detail.get('head_branch', '')

        platform_label = {
            'gitea': 'Gitea', 'github': 'GitHub',
            'gitlab': 'GitLab', 'bitbucket': 'Bitbucket',
        }.get(platform, platform.capitalize())

        def _file_url(path: str, line: int):
            api_url = resolved.get('apiUrl', '')
            owner   = resolved.get('owner', '')
            repo    = resolved.get('repo', '')
            if not (api_url and owner and repo):
                return None

            if platform == 'github':
                base = api_url.replace('api.github.com', 'github.com')
                if commit_sha:
                    return f"{base}/{owner}/{repo}/blob/{commit_sha}/{path}#L{line}"
                if head_branch:
                    return f"{base}/{owner}/{repo}/blob/{head_branch}/{path}#L{line}"
            elif platform == 'gitlab':
                base = api_url.replace('/api/v4', '')
                if commit_sha:
                    return f"{base}/{owner}/{repo}/-/blob/{commit_sha}/{path}#L{line}"
                if head_branch:
                    return f"{base}/{owner}/{repo}/-/blob/{head_branch}/{path}#L{line}"
            elif platform == 'bitbucket':
                base = api_url.replace('/api/2.0', '').replace('api.bitbucket.org', 'bitbucket.org')
                if commit_sha:
                    return f"{base}/{owner}/{repo}/src/{commit_sha}/{path}#lines-{line}"
                if head_branch:
                    return f"{base}/{owner}/{repo}/src/{head_branch}/{path}#lines-{line}"
            else:
                base = api_url.replace('/api/v1', '')
                if commit_sha:
                    return f"{base}/{owner}/{repo}/src/commit/{commit_sha}/{path}#L{line}"
                if head_branch:
                    return f"{base}/{owner}/{repo}/src/branch/{head_branch}/{path}#L{line}"
            return None

        SEVERITY_META = {
            "critical":   ("🔴 Critical Issues", "🔴"),
            "warning":    ("🟡 Warnings",         "🟡"),
            "suggestion": ("⚪ Suggestions",       "⚪"),
        }

        def _comment_widgets(c: dict) -> list:
            sev_icon  = SEVERITY_META.get(c.get('severity', ''), ('', '❕'))[1]
            category  = c.get('category', '')
            title     = c.get('title', '')
            path      = c.get('path', '')
            line      = c.get('line', '')
            body      = c.get('body', '').replace('\n', '<br>')
            rec       = c.get('recommendation', '')
            snippet   = c.get('codeSnippet', '')
            file_link = _file_url(path, line)

            header_widget = {
                "decoratedText": {
                    "topLabel": f"{sev_icon} [{category}]  ·  {path}:{line}",
                    "text": f"<b>{title}</b>",
                    **({"button": {"text": f"View in {platform_label}", "onClick": {"openLink": {"url": file_link}}}} if file_link else {}),
                }
            }
            w = [header_widget]
            if body:
                w.append({"textParagraph": {"text": body}})
            if rec:
                w.append({"textParagraph": {"text": f"<i>💡 <b>Recommendation:</b> {rec}</i>"}})
            if snippet:
                escaped = snippet.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                w.append({"textParagraph": {
                    "text": f"<i>✏️ <b>Code Suggestion:</b></i><br><code>{escaped}</code>"
                }})
            return w

        for severity in ("critical", "warning", "suggestion"):
            group = [c for c in comments if c.get('severity') == severity]
            if not group:
                continue
            section_header, _ = SEVERITY_META[severity]
            all_widgets = []
            for c in group:
                all_widgets.extend(_comment_widgets(c))
                all_widgets.append({"divider": {}})
            if all_widgets and all_widgets[-1] == {"divider": {}}:
                all_widgets.pop()
            extra_sections.append({
                "header": section_header,
                "collapsible": True,
                "uncollapsibleWidgetsCount": 3,
                "widgets": all_widgets,
            })

    card_title = f"{status_short} [{repo_display}] Code Review Agent ({author}): {pr_title}"
    payload = {
        "text": "<users/all>",
        "cardsV2": [{
            "cardId": "pr-review",
            "card": {
                "header": {"title": card_title, "subtitle": branch},
                "sections": [{"widgets": widgets}] + extra_sections,
            },
        }],
    }

    safe_repo  = re.sub(r'[^a-zA-Z0-9_-]', '-', repo_display) if repo_display else 'repo'
    thread_key = f"pr-{safe_repo}-{pr_number}"
    threaded_url = webhook_url + (
        "&" if "?" in webhook_url else "?"
    ) + urllib.parse.urlencode({
        "threadKey": thread_key,
        "messageReplyOption": "REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD",
    })

    try:
        req = urllib.request.Request(
            threaded_url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST',
        )
        opener = create_no_proxy_opener()
        with opener.open(req) as response:
            if response.status == 200:
                return {"success": True, "sent": True, "threadKey": thread_key}
            return {"success": False, "error": f"HTTP {response.status}"}
    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP {e.code} - {e.reason}"}
    except urllib.error.URLError as e:
        return {"success": False, "error": f"Connection error: {e.reason}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {e}"}



# =============================================================================
# Main
# =============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Post PR review comments to Git platform',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python post-review.py            # Post review using project.config.json
  python post-review.py --dry-run  # Transform only, do not post
        """
    )
    parser.add_argument('--dry-run', '-d', action='store_true',
                        help='Transform and display, do not post')

    args = parser.parse_args()
    
    # Load review.json from project root
    if not os.path.isfile(DEFAULT_REVIEW_FILE):
        print(f"Error: Review file not found: {DEFAULT_REVIEW_FILE}", file=sys.stderr)
        sys.exit(1)
    
    try:
        standard_review = load_json_file(DEFAULT_REVIEW_FILE)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {DEFAULT_REVIEW_FILE}: {e}", file=sys.stderr)
        sys.exit(1)
    
    pr_number = standard_review.get('prNumber')
    if not pr_number:
        print("Error: prNumber is required in review.json", file=sys.stderr)
        sys.exit(1)
    
    # Load config
    try:
        config, config_path = get_config()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Derive repo name from platformConfig for downstream functions
    platform_cfg = config.get('platformConfig', {})
    platform_key = config.get('platform', 'github')
    resolved_cfg = platform_cfg.get(platform_key) or next(iter(platform_cfg.values()), {})
    config['_repoName'] = resolved_cfg.get('repo', 'repo')
    
    print(f"Info: Loaded config from: {config_path}", file=sys.stderr)

    platform = get_platform(config)
    notification_enabled = is_notification_enabled(config)
    comment_posting_enabled = is_comment_posting_enabled(config)
    has_token = has_platform_token(platform)

    if not isinstance(comment_posting_enabled, bool):
        print(
            f"Warning: 'enableCommentPosting' must be a JSON boolean (true/false), "
            f"got {type(comment_posting_enabled).__name__!r} — treating as enabled.",
            file=sys.stderr,
        )
        comment_posting_enabled = bool(comment_posting_enabled)
    
    # Determine operation mode
    if not comment_posting_enabled and not notification_enabled:
        # Both disabled - nothing to do
        print(f"'enableCommentPosting' and 'enableNotification' are disabled - nothing todo.", file=sys.stderr)
        sys.exit(1)
    
    # Post comments (if enabled in config and token available)
    result = {}
    should_post = comment_posting_enabled and (has_token or args.dry_run)
    
    if should_post:
        result = post_to_platform(platform, standard_review, config, args.dry_run)
        
        if not result.get('success') and not result.get('skipped') and not args.dry_run:
            print(f"Error: Failed to post review: {result.get('error', 'Unknown error')}", file=sys.stderr)
            # Don't exit if notifications are enabled - continue to send notification
            if not notification_enabled:
                sys.exit(1)
    else:
        # Determine skip reason
        skip_reasons = []
        if not comment_posting_enabled:
            skip_reasons.append("comment posting disabled in config")
        if comment_posting_enabled and not has_token:
            skip_reasons.append("no git token configured")
        
        skip_reason = " and ".join(skip_reasons)
        
        result = {
            "success": False,
            "platform": platform,
            "skipped": True,
            "reason": f"Skipping inline comments: {skip_reason}"
        }
        
        if notification_enabled:
            print(f"Info: Skipping inline comments ({skip_reason}). Running in notification-only mode.", file=sys.stderr)
        else:
            print(f"Error: Cannot post comments - {skip_reason}.", file=sys.stderr)
            sys.exit(1)
    
    # Send notification if enabled in config
    if notification_enabled and not args.dry_run:
        summary_path = f"/tmp/pr-{pr_number}-summary.md"
        generate_summary_file(standard_review, config, summary_path)
        # compact=True when comments were posted to the platform (details are in Gitea)
        comments_posted = should_post and result.get('success', False)
        notify_result = send_notification(summary_path, config, standard_review, compact=comments_posted)
        result['notification'] = notify_result
    
    # Cleanup: Remove review.json after successful posting or notification
    should_cleanup = False
    if not args.dry_run:
        if result.get('success'):
            # Posting was successful
            should_cleanup = True
        elif result.get('skipped') and notification_enabled:
            # Notification-only mode - cleanup if notification was successful
            notify_result = result.get('notification', {})
            should_cleanup = notify_result.get('success', False)
    
    if should_cleanup:
        try:
            os.remove(DEFAULT_REVIEW_FILE)
            result['cleanup'] = {'reviewFileDeleted': True}
        except Exception as e:
            # Non-critical error, don't fail the whole process
            result['cleanup'] = {'reviewFileDeleted': False, 'error': str(e)}
    
    # Output result as JSON
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
