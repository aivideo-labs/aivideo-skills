#!/usr/bin/env python3
"""Generic image generation client (normalized interface).

Reads auth/endpoint from .env or environment variables:
- API_BASE: full endpoint URL (required)
- API_KEY: bearer token (required)
- MODEL: default model name (optional)
- TIMEOUT: request timeout seconds (default 120)
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
    parser.add_argument("--size", default="1024*1024")
    parser.add_argument("--aspect", default="1:1")
    parser.add_argument("--style", default="")
    parser.add_argument("--reference-image", dest="reference_image", default="")
    parser.add_argument("--model", default=os.getenv("MODEL", ""))
    parser.add_argument("--n", type=int, default=1)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--format", default="png")
    parser.add_argument("--out", default="output/images")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    _load_env()
    _require_env(["API_BASE", "API_KEY"])

    req = _load_request(args.request)
    if not req and not args.prompt:
        parser.error("--prompt is required when --request is not provided")

    if req:
        payload = {
            "prompt": req.get("prompt"),
            "negative_prompt": req.get("negative_prompt"),
            "size": req.get("size", args.size),
            "aspect_ratio": req.get("aspect_ratio", args.aspect),
            "style": req.get("style"),
            "seed": req.get("seed"),
            "n": req.get("n", args.n),
            "reference_image": req.get("reference_image"),
            "format": req.get("format", args.format),
            "model": req.get("model", args.model) or None,
        }
    else:
        payload = {
            "prompt": args.prompt,
            "negative_prompt": args.negative or None,
            "size": args.size,
            "aspect_ratio": args.aspect,
            "style": args.style or None,
            "seed": args.seed,
            "n": args.n,
            "reference_image": args.reference_image or None,
            "format": args.format,
            "model": args.model or None,
        }

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    api_base = os.getenv("API_BASE", "").strip()
    api_key = os.getenv("API_KEY", "").strip()
    timeout = int(os.getenv("TIMEOUT", "120"))

    (out_dir / "request.json").write_text(json.dumps(payload, ensure_ascii=True, indent=2))

    if args.dry_run:
        print("Dry run: request written to request.json")
        return 0

    headers = {"Content-Type": "application/json"}
    headers["Authorization"] = f"Bearer {api_key}"

    resp = _post_json(api_base, headers, payload, timeout)
    (out_dir / "response.json").write_text(json.dumps(resp, ensure_ascii=True, indent=2))

    images = resp.get("images") if isinstance(resp, dict) else None
    if images:
        for i, b64_str in enumerate(images, 1):
            _save_b64(b64_str, out_dir / f"image_{i}.{payload['format']}")
        return 0

    data = resp.get("data") if isinstance(resp, dict) else None
    if data:
        for i, item in enumerate(data, 1):
            if isinstance(item, dict) and item.get("b64_json"):
                _save_b64(item["b64_json"], out_dir / f"image_{i}.{payload['format']}")
            elif isinstance(item, dict) and item.get("url"):
                _download(item["url"], out_dir / f"image_{i}.{payload['format']}")
        return 0

    print("No images detected in response. Inspect response.json for provider-specific fields.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
