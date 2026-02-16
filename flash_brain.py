#!/usr/bin/env python3
"""Fast Gemini CLI bridge for low-friction async cognitive offloading.

Usage examples:
  python flash_brain.py ask "сделай скелет модуля памяти для LAM"
  python flash_brain.py ask --prompt-file notes/raw.txt --save drafts/memory_skeleton.md
  python flash_brain.py offload --input-dir notes/inbox --output-dir notes/outbox
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Iterable

DEFAULT_MODEL_CHAIN = ("gemini-3-flash", "gemini-2.5-flash")
DEFAULT_SYSTEM_PROMPT = (
    "You are Fast-Thought assistant for asynchronous development. "
    "Transform rough notes into concise, implementation-ready drafts."
)


def _load_google_genai_client():
    try:
        from google import genai  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "google-genai is not installed. Run: pip install -q -U google-genai"
        ) from exc

    if not (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
        raise RuntimeError(
            "Missing API key. Set GEMINI_API_KEY or GOOGLE_API_KEY in environment."
        )
    return genai.Client()


def _resolve_models(cli_models: str | None) -> list[str]:
    if cli_models:
        return [m.strip() for m in cli_models.split(",") if m.strip()]
    env_models = os.getenv("GEMINI_FLASH_MODELS")
    if env_models:
        return [m.strip() for m in env_models.split(",") if m.strip()]
    return list(DEFAULT_MODEL_CHAIN)


def _response_text(response: object) -> str:
    text = getattr(response, "text", None)
    if text:
        return str(text).strip()
    return str(response)


def _generate_text(
    prompt: str,
    models: Iterable[str],
    system_prompt: str,
    temperature: float,
    max_output_tokens: int,
) -> tuple[str, str]:
    client = _load_google_genai_client()
    errors: list[str] = []

    for model in models:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config={
                    "system_instruction": system_prompt,
                    "temperature": temperature,
                    "max_output_tokens": max_output_tokens,
                },
            )
            text = _response_text(response)
            if not text:
                raise RuntimeError("Model returned empty response")
            return model, text
        except Exception as exc:  # pragma: no cover
            errors.append(f"{model}: {exc}")

    raise RuntimeError(
        "All configured models failed. Tried: "
        + ", ".join(models)
        + "\n"
        + "\n".join(errors)
    )


def _read_prompt(args: argparse.Namespace) -> str:
    if args.prompt:
        return args.prompt
    if args.prompt_file:
        return Path(args.prompt_file).read_text(encoding="utf-8")
    data = sys.stdin.read()
    if data.strip():
        return data
    raise RuntimeError("Prompt is empty. Use positional prompt, --prompt-file, or stdin.")


def cmd_ask(args: argparse.Namespace) -> int:
    prompt = _read_prompt(args)
    models = _resolve_models(args.models)

    model_used, text = _generate_text(
        prompt=prompt,
        models=models,
        system_prompt=args.system,
        temperature=args.temperature,
        max_output_tokens=args.max_output_tokens,
    )

    output = f"[model: {model_used}]\n\n{text}\n"
    if args.save:
        out = Path(args.save)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(output, encoding="utf-8")
        print(f"Saved: {out}")
        return 0

    print(output)
    return 0


def cmd_offload(args: argparse.Namespace) -> int:
    src_dir = Path(args.input_dir)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not src_dir.exists() or not src_dir.is_dir():
        raise RuntimeError(f"Input directory not found: {src_dir}")

    files = sorted(p for p in src_dir.iterdir() if p.is_file())
    if not files:
        print(f"No files to process in {src_dir}")
        return 0

    models = _resolve_models(args.models)

    for path in files:
        raw = path.read_text(encoding="utf-8", errors="replace")
        prompt = (
            f"{args.instruction}\n\n"
            "Return sections: summary, candidate_tasks, draft_artifacts.\n\n"
            f"SOURCE_FILE: {path.name}\n"
            f"SOURCE_TEXT:\n{raw}"
        )
        model_used, text = _generate_text(
            prompt=prompt,
            models=models,
            system_prompt=args.system,
            temperature=args.temperature,
            max_output_tokens=args.max_output_tokens,
        )

        out_file = out_dir / f"{path.stem}.flash.md"
        out_file.write_text(f"[model: {model_used}]\n\n{text}\n", encoding="utf-8")
        print(f"Processed: {path.name} -> {out_file.name}")

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Gemini Flash bridge for LAM-Codex_Agent")
    parser.add_argument(
        "--models",
        default=None,
        help="Comma-separated model fallback chain. Default: gemini-3-flash,gemini-2.5-flash",
    )
    parser.add_argument(
        "--system",
        default=DEFAULT_SYSTEM_PROMPT,
        help="System prompt used for generation",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Sampling temperature",
    )
    parser.add_argument(
        "--max-output-tokens",
        type=int,
        default=2048,
        help="Max output tokens",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    ask = sub.add_parser("ask", help="Single fast prompt")
    ask.add_argument("prompt", nargs="?", help="Prompt text")
    ask.add_argument("--prompt-file", help="Path to file with prompt text")
    ask.add_argument("--save", help="Write output to file instead of stdout")
    ask.set_defaults(func=cmd_ask)

    offload = sub.add_parser(
        "offload",
        help="Batch-process notes/logs into structured drafts",
    )
    offload.add_argument("--input-dir", required=True, help="Directory with raw notes/logs")
    offload.add_argument("--output-dir", required=True, help="Directory for generated drafts")
    offload.add_argument(
        "--instruction",
        default="Convert raw operational notes into actionable development draft.",
        help="Transformation instruction",
    )
    offload.set_defaults(func=cmd_offload)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
