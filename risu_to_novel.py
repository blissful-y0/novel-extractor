#!/usr/bin/env python3
"""
RisuAI chat JSON → novel-format Markdown converter.
Enhanced version with multi-session support and tag cleanup.
"""

import json
import re
import sys
from pathlib import Path

# ── helpers ──────────────────────────────────────────────────────────────────

def clean_tags(text: str) -> str:
    """Remove RisuAI metadata blocks and XML-like tags."""
    # Remove <details>…</details> header (non-greedy)
    text = re.sub(r"<details>.*?</details>", "", text, flags=re.DOTALL)
    
    # Remove XML-like tags (narrative, psyche-status, etc)
    # We keep the content inside <narrative> but remove the tag itself
    text = re.sub(r"</?narrative>", "", text)
    # Remove tags that usually contain metadata or system info
    text = re.sub(r"<(psyche-status|world-info|summary|details)>.*?</\1>", "", text, flags=re.DOTALL)
    # Generic cleanup for any remaining <tag>...</tag> or <tag/>
    # (Optional: use if we want to be aggressive)
    # text = re.sub(r"<[^>]+>.*?</[^>]+>", "", text, flags=re.DOTALL)
    
    # Remove leading --- separator
    text = re.sub(r"^\s*---\s*\n", "", text.lstrip())
    
    return text.strip()

def format_message(role: str, content: str) -> str:
    """Return the message as a novel paragraph block."""
    if role == "char":
        return clean_tags(content)
    else:  # user / human turn
        return content.strip()

# ── main ──────────────────────────────────────────────────────────────────────

def convert(input_path: Path, output_path: Path) -> None:
    try:
        raw = input_path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except Exception as e:
        print(f"[error] Failed to read/parse JSON: {e}", file=sys.stderr)
        return

    chats = data.get("data", [])
    if not chats:
        print("[warn] No chat data found.", file=sys.stderr)
        return

    all_output: list[str] = []

    for i, session in enumerate(chats, 1):
        messages = session.get("message", [])
        if not messages:
            continue
            
        session_blocks: list[str] = []
        # Add a session header if multiple exist
        if len(chats) > 1:
            session_blocks.append(f"--- SESSION {i} ---")
            
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("data", "")
            if not content or not str(content).strip():
                continue
            block = format_message(role, content)
            if block:
                session_blocks.append(block)
        
        if session_blocks:
            all_output.append("\n\n".join(session_blocks))

    final_text = "\n\n\n\n".join(all_output)

    output_path.write_text(final_text, encoding="utf-8")
    print(f"[ok] Written to: {output_path}")
    print(f"     {len(chats)} sessions, total message blocks processed.")

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python risu_to_novel.py <input.json> [output.md]")
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
