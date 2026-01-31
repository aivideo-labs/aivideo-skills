#!/usr/bin/env python3
"""Generic video generation client (normalized interface).

Reads auth/endpoint from .env or environment variables:
- API_BASE: full endpoint URL (required)
- API_KEY: bearer token (required)
- MODEL: default model name (optional)
- TIMEOUT: request timeout seconds (default 300)
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
from pathlib import Path


def _find_repo_root(start: Path) -> Path | None:
    for parent in [start] + list(start.parents):
        if (parent / ".git").exists():
            return parent
    return None


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _load_env() -> None:
    _load_dotenv(Path.cwd() / ".env")
    repo_root = _find_repo_root(Path(__file__).resolve())
    if repo_root:
        _load_dotenv(repo_root / ".env")


def _require_env(keys: list[str]) -> None:
    missing = [key for key in keys if not os.environ.get(key)]
    if not missing:
        return
    msg = [
        "Error: missing required environment variables: " + ", ".join(missing),
        "Configure them in your shell or .env file.",
        "Example .env:",
        "  API_BASE=https://api.example.com/v1/generate",
        "  API_KEY=your_key_here",
        "  MODEL=your-model-name",
    ]
    print("\n".join(msg), file=sys.stderr)
    raise SystemExit(1)


def _post_json(url, headers, payload, timeout):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _download(url, out_path):
    urllib.request.urlretrieve(url, out_path)


def _save_b64(b64_str, out_path):
    Path(out_path).write_bytes(base64.b64decode(b64_str))


def _load_request(arg):
    if not arg:
        return None
    path = Path(arg)
    if path.exists():
        return json.loads(path.read_text())
    return json.loads(arg)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", default="", help="JSON string or path to JSON file")
    parser.add_argument("--prompt", default="")
    parser.add_argument("--negative", default="")
    parser.add_argument("--duration", type=float, default=4)
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--size", default="1280*720")
    parser.add_argument("--resolution", default="")
    parser.add_argument("--aspect", default="16:9")
    parser.add_argument("--reference-image", dest="reference_image", default="")
    parser.add_argument("--motion-strength", dest="motion_strength", type=float, default=None)
    parser.add_argument("--model", default=os.getenv("MODEL", ""))
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--format", default="mp4")
    parser.add_argument("--out", default="output/videos")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    _load_env()
    _require_env(["API_BASE", "API_KEY"])

    req = _load_request(args.request)
    if not req and not args.prompt:
        parser.error("--prompt is required when --request is not provided")

    size = args.size if args.size else args.resolution

    if req:
        payload = {
            "prompt": req.get("prompt"),
            "negative_prompt": req.get("negative_prompt"),
            "duration": req.get("duration", args.duration),
            "fps": req.get("fps", args.fps),
            "size": req.get("size", size),
            "aspect_ratio": req.get("aspect_ratio", args.aspect),
            "seed": req.get("seed"),
            "reference_image": req.get("reference_image"),
            "motion_strength": req.get("motion_strength"),
            "format": req.get("format", args.format),
            "model": req.get("model", args.model) or None,
        }
    else:
        payload = {
            "prompt": args.prompt,
            "negative_prompt": args.negative or None,
            "duration": args.duration,
            "fps": args.fps,
            "size": size,
            "aspect_ratio": args.aspect,
            "seed": args.seed,
            "reference_image": args.reference_image or None,
            "motion_strength": args.motion_strength,
            "format": args.format,
            "model": args.model or None,
        }

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    api_base = os.getenv("API_BASE", "").strip()
    api_key = os.getenv("API_KEY", "").strip()
    timeout = int(os.getenv("TIMEOUT", "300"))

    (out_dir / "request.json").write_text(json.dumps(payload, ensure_ascii=True, indent=2))

    if args.dry_run:
        print("Dry run: request written to request.json")
        return 0

    headers = {"Content-Type": "application/json"}
    headers["Authorization"] = f"Bearer {api_key}"

    resp = _post_json(api_base, headers, payload, timeout)
    (out_dir / "response.json").write_text(json.dumps(resp, ensure_ascii=True, indent=2))

    videos = resp.get("videos") if isinstance(resp, dict) else None
    if videos:
        for i, b64_str in enumerate(videos, 1):
            _save_b64(b64_str, out_dir / f"video_{i}.{payload['format']}")
        return 0

    data = resp.get("data") if isinstance(resp, dict) else None
    if data:
        for i, item in enumerate(data, 1):
            if isinstance(item, dict) and item.get("b64_json"):
                _save_b64(item["b64_json"], out_dir / f"video_{i}.{payload['format']}")
            elif isinstance(item, dict) and item.get("url"):
                _download(item["url"], out_dir / f"video_{i}.{payload['format']}")
        return 0

    print("No videos detected in response. Inspect response.json for provider-specific fields.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
