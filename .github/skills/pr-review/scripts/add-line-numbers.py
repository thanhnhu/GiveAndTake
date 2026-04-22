#!/usr/bin/env python3
"""Add explicit line numbers to unified diff format for easier parsing"""

import sys
import re

def add_line_numbers(input_file, output_file):
    """
    Parse unified diff and add explicit line numbers to each line.

    Example:
    Input:  @@ -10,5 +10,7 @@
            function login() {
            -  const token = secret;
            +  const token = process.env.TOKEN;

    Output: @@ -10,5 +10,7 @@
            10 | function login() {
            11 | -  const token = secret;
            11 | +  const token = process.env.TOKEN;
    """

    with open(input_file, 'r') as f:
        lines = f.readlines()

    numbered_lines = []
    current_new_line = None  # Track line numbers for new/context lines

    for line in lines:
        # Parse hunk header: @@ -old_start,old_count +new_start,new_count @@
        hunk_match = re.match(r'@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@', line)

        if hunk_match:
            # Hunk header - extract starting line number for new file
            current_new_line = int(hunk_match.group(1))
            numbered_lines.append(line)  # Keep hunk header as-is
        elif current_new_line is not None:
            if line.startswith('+'):
                # Added line - add line number and increment
                numbered_lines.append(f"{current_new_line} | {line}")
                current_new_line += 1
            elif line.startswith('-'):
                # Deleted line - add line number but don't increment (only context/added lines count)
                numbered_lines.append(f"{current_new_line} | {line}")
            elif line.startswith('\\'):
                # "\ No newline at end of file" marker - keep as-is
                numbered_lines.append(line)
            else:
                # Context line (space prefix) - add line number and increment
                numbered_lines.append(f"{current_new_line} | {line}")
                current_new_line += 1
        else:
            # Before first hunk (file headers, metadata) - keep as-is
            numbered_lines.append(line)

    # Write output
    with open(output_file, 'w') as f:
        f.writelines(numbered_lines)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: add-line-numbers.py <input.diff> <output.diff>")
        sys.exit(1)

    try:
        add_line_numbers(sys.argv[1], sys.argv[2])
        print(f"✅ Line numbers added: {sys.argv[2]}")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
