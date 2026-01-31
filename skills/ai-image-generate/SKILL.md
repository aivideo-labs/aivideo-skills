---
name: ai-image-generate
description: Generate images with multiple providers (OpenAI, Alibaba Tongyi, Volcengine, Midjourney). Use when implementing or documenting image.generate requests/responses, mapping prompts/negative prompts/size/seed/reference image, or integrating image generation into a video/creative pipeline.
---

Category: task

# AI Image Generate

Standardize `image.generate` across providers by using a normalized request/response shape and provider-specific mappings.

## Critical model names

Use ONLY exact model strings defined in each provider reference:
- OpenAI: `references/openai.md`
- Alibaba Tongyi: `references/aliyun.md`
- Volcengine: `references/volcengine.md`
- Midjourney: `references/midjourney.md`

Do not invent aliases or date suffixes.

## Normalized interface (image.generate)

### Request
- `prompt` (string, required)
- `negative_prompt` (string, optional)
- `size` (string, required) e.g. `1024*1024`, `768*1024`
- `aspect_ratio` (string, optional) e.g. `1:1`, `3:4`
- `style` (string, optional)
- `seed` (int, optional)
- `n` (int, optional)
- `reference_image` (string | bytes, optional)

### Response
- `image_url` (string)
- `width` (int)
- `height` (int)
- `seed` (int)

## Quick start (normalized request + script)

Minimal normalized request body:

```json
{
  "prompt": "a cinematic portrait of a cyclist at dusk, soft rim light, shallow depth of field",
  "negative_prompt": "blurry, low quality, watermark",
  "size": "1024*1024",
  "seed": 1234
}
```

Local helper script (JSON request -> image file):

```bash
python skills/ai-image-generate/scripts/openai/generate.py \
  --request '{"prompt":"a studio product photo of headphones","size":"1024*1024"}' \
  --out output/images/headphones \
  --dry-run
```

## Parameters at a glance

| Field | Required | Notes |
|------|----------|-------|
| `prompt` | yes | Describe a scene, not just keywords. |
| `negative_prompt` | no | Best-effort, may be ignored by backend. |
| `size` | yes | `WxH` format, e.g. `1024*1024`. |
| `aspect_ratio` | no | Use if the provider expects ratio. |
| `style` | no | Optional stylistic hint. |
| `seed` | no | Use for reproducibility when supported. |
| `n` | no | Number of outputs. |
| `reference_image` | no | URL/file/bytes, provider-specific. |

## Error handling

| Error | Likely cause | Action |
|------|--------------|--------|
| 401/403 | Missing or invalid API key | Check env var and access policy. |
| 400 | Unsupported size or bad request | Validate fields and use common sizes. |
| 429 | Rate limit or quota | Retry with backoff or reduce concurrency. |
| 5xx | Transient backend errors | Retry once or twice with backoff. |

## Output location

- Save generated images under `output/images/` by default.

## Operational guidance

- Cache by `(prompt, negative_prompt, size, seed, reference_image hash)` to avoid duplicate costs.
- Store images in object storage and persist only URLs in metadata.
- Some backends ignore `negative_prompt`, `style`, or `seed`; treat them as best-effort inputs.
- If no image URL is returned, surface a clear error and retry with a simplified prompt.

## Size notes

- Use `WxH` format (e.g. `1024*1024`, `768*1024`).
- Prefer common sizes; unsupported sizes can return 400.

## Anti-patterns

- Do not invent model names or aliases; use only provider references.
- Do not store large base64 blobs in DB rows; use object storage.
- Do not omit user-visible progress for long generations.

## References

- Provider selection: `references/selection.md`
- Prompt guide: `references/prompt-guide.md`
- OpenAI: `references/openai.md`
- Alibaba Tongyi: `references/aliyun.md`
- Volcengine: `references/volcengine.md`
- Midjourney: `references/midjourney.md`