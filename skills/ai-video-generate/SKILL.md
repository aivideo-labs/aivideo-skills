---
name: ai-video-generate
description: Generate videos with multiple providers (OpenAI, Alibaba Tongyi, Volcengine, Midjourney). Use when implementing or documenting video.generate requests/responses, mapping prompts/negative prompts/duration/fps/size/seed/reference image, or integrating video generation into a creative pipeline.
---

Category: task

# AI Video Generate

Standardize `video.generate` across providers by using a normalized request/response shape and provider-specific mappings.

## Critical model names

Use ONLY exact model strings defined in each provider reference:
- OpenAI: `references/openai.md`
- Alibaba Tongyi: `references/aliyun.md`
- Volcengine: `references/volcengine.md`
- Midjourney: `references/midjourney.md`

Do not invent aliases or date suffixes.

## Normalized interface (video.generate)

### Request
- `prompt` (string, required)
- `negative_prompt` (string, optional)
- `duration` (number, required) seconds
- `fps` (number, required)
- `size` (string, required) e.g. `1280*720`
- `aspect_ratio` (string, optional) e.g. `16:9`
- `seed` (int, optional)
- `reference_image` (string | bytes, optional)
- `motion_strength` (number, optional)

### Response
- `video_url` (string)
- `duration` (number)
- `fps` (number)
- `seed` (int)

## Quick start (normalized request + script)

Minimal normalized request body:

```json
{
  "prompt": "a wide drone shot over a coastal road at golden hour",
  "duration": 4,
  "fps": 24,
  "size": "1280*720"
}
```

Local helper script (JSON request -> video file):

```bash
python skills/ai-video-generate/scripts/openai/generate.py \
  --request '{"prompt":"a neon-lit alley in the rain","duration":4,"fps":24,"size":"1280*720"}' \
  --out output/videos/neon \
  --dry-run
```

## Parameters at a glance

| Field | Required | Notes |
|------|----------|-------|
| `prompt` | yes | Describe motion and scene. |
| `negative_prompt` | no | Best-effort; may be ignored. |
| `duration` | yes | Seconds. |
| `fps` | yes | Frames per second. |
| `size` | yes | `WxH` format, e.g. `1280*720`. |
| `aspect_ratio` | no | Use if provider expects ratio. |
| `seed` | no | Reproducibility when supported. |
| `reference_image` | no | URL/file/bytes, provider-specific. |
| `motion_strength` | no | Use for i2v or motion control if supported. |

## Error handling

| Error | Likely cause | Action |
|------|--------------|--------|
| 401/403 | Missing or invalid API key | Check env var and access policy. |
| 400 | Unsupported size or bad request | Validate fields and use common sizes. |
| 429 | Rate limit or quota | Retry with backoff or reduce concurrency. |
| 5xx | Transient backend errors | Retry once or twice with backoff. |

## Output location

- Save generated videos under `output/videos/` by default.

## Operational guidance

- Video generation can take minutes; expose progress and allow cancel/retry.
- Cache by `(prompt, negative_prompt, duration, fps, size, seed, reference_image hash, motion_strength)`.
- Store video assets in object storage and persist only URLs in metadata.
- If the provider is async, poll until completion and handle timeouts explicitly.

## Size notes

- Use `WxH` format (e.g. `1280*720`).
- Prefer common sizes; unsupported sizes can return 400.

## Anti-patterns

- Do not invent model names or aliases; use only provider references.
- Do not block the UI without progress updates.
- Do not retry blindly on 4xx; handle validation failures explicitly.

## References

- Provider selection: `references/selection.md`
- Prompt guide: `references/prompt-guide.md`
- OpenAI: `references/openai.md`
- Alibaba Tongyi: `references/aliyun.md`
- Volcengine: `references/volcengine.md`
- Midjourney: `references/midjourney.md`