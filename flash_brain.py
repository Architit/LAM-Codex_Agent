#!/usr/bin/env python3
# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
"""Fast Codex Bridge for low-friction cognitive offloading.
Unified version using src.codex_agent.gate.
"""

import argparse
import os
import re
import sys
from pathlib import Path

# Setup path to include src
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from codex_agent.gate import CodexGate

DEFAULT_SYSTEM_PROMPT = (
    "You are Fast-Thought assistant for asynchronous development. "
    "Transform rough notes into concise, implementation-ready drafts."
)

def _read_prompt(args):
    if args.prompt: return args.prompt
    if args.prompt_file: return Path(args.prompt_file).read_text(encoding="utf-8")
    return sys.stdin.read()

def _slug(value: str, limit: int = 40) -> str:
    cleaned = re.sub(r"\s+", "_", value.strip())
    cleaned = re.sub(r"[^0-9A-Za-z_-]+", "", cleaned)
    return (cleaned[:limit] or "thought_dump").strip("_") or "thought_dump"

def main():
    parser = argparse.ArgumentParser(description="Codex Flash Bridge")
    parser.add_argument("--models", default="auto", help="Model hint")
    parser.add_argument("--system", default=DEFAULT_SYSTEM_PROMPT, help="System prompt")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-output-tokens", type=int, default=2048)
    
    sub = parser.add_subparsers(dest="command", required=True)
    
    ask = sub.add_parser("ask")
    ask.add_argument("prompt", nargs="?")
    ask.add_argument("--prompt-file")
    ask.add_argument("--save")
    
    hib = sub.add_parser("hibernate")
    hib.add_argument("prompt", nargs="?")
    hib.add_argument("--output-dir", default="thoughts")
    
    args = parser.parse_args()
    gate = CodexGate()
    prompt = _read_prompt(args)
    
    if args.command == "ask":
        res = gate.ask(prompt, model_hint=args.models, sys_prompt=args.system, 
                      temperature=args.temperature, max_tokens=args.max_output_tokens)
        if args.save:
            Path(args.save).write_text(res, encoding="utf-8")
            print(f"Saved: {args.save}")
        else:
            print(res)
            
    elif args.command == "hibernate":
        full_prompt = f"Transform this thought into a structured draft:\n\n{prompt}"
        res = gate.ask(full_prompt, model_hint=args.models, sys_prompt=args.system,
                      temperature=args.temperature, max_tokens=args.max_output_tokens)
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"{_slug(prompt)}.md"
        out_file.write_text(res, encoding="utf-8")
        print(f"Saved: {out_file}")

if __name__ == "__main__":
    main()
