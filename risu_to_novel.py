#!/usr/bin/env python3
"""
RisuAI chat JSON → novel-format Markdown converter.

Usage:
    python risu_to_novel.py <input.json> [output.md]

If output path is omitted, writes to <input_stem>.md in the same directory.
"""

import json
import re
import sys
from pathlib import Path


# ── helpers ──────────────────────────────────────────────────────────────────

def strip_abp_block(text: str) -> str:
    """Remove the <details>…</details> header and the following --- divider."""
    # Remove <details> block (non-greedy, handles multiline)
    text = re.sub(r"<details>.*?</details>", "", text, flags=re.DOTALL)
    # Remove leading --- separator (may have surrounding whitespace/newlines)
    text = re.sub(r"^\s*---\s*\n", "", text.lstrip())
    return text.strip()


def format_message(role: str, content: str) -> str:
    """Return the message as a novel paragraph block."""
    if role == "char":
        return strip_abp_block(content)
    else:  # user / human turn
        return content.strip()


# ── main ──────────────────────────────────────────────────────────────────────

def convert(input_path: Path, output_path: Path) -> None:
    raw = input_path.read_text(encoding="utf-8")
    data = json.loads(raw)

    if data.get("type") != "risuAllChats":
        print(f"[warn] Unexpected type: {data.get('type')}", file=sys.stderr)

    chats = data.get("data", [])
    if not chats:
        print("[warn] No chat data found.", file=sys.stderr)
        return

    # Each element in data[] is a chat session (could be multiple).
    # We flatten all messages in chronological order.
    blocks: list[str] = []

    for session in chats:
        messages = session.get("message", [])
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("data", "")
            if not content.strip():
                continue
            block = format_message(role, content)
            if block:
                blocks.append(block)

    # Join with double newline to separate paragraphs
    novel_text = "\n\n".join(blocks)

    output_path.write_text(novel_text, encoding="utf-8")
    print(f"[ok] Written to: {output_path}")
    print(f"     {len(blocks)} message blocks → {len(novel_text):,} characters")


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = Path(sys.argv[1]).expanduser().resolve()
    if not input_path.exists():
        print(f"[error] File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2]).expanduser().resolve()
    else:
        output_path = input_path.with_suffix(".md")

    convert(input_path, output_path)


if __name__ == "__main__":
    main()
