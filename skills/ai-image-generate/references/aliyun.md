# Alibaba Tongyi image generation

## Use when

Use when China-region infra or Ali ecosystem integration is required.

## Model names

- TODO: fill exact model strings for Alibaba Tongyi

## Auth and endpoint

- API_BASE: TODO
- API_KEY: TODO
- MODEL: TODO

## Normalized mapping

Map normalized `image.generate` into provider fields:

- `prompt` -> prompt
- `negative_prompt` -> negative_prompt (if supported)
- `size` -> size (WxH)
- `aspect_ratio` -> aspect_ratio (if supported)
- `style` -> style (if supported)
- `seed` -> seed (if supported)
- `n` -> batch/num outputs (if supported)
- `reference_image` -> provider-specific image field

## Response parsing

Normalize into:

- `image_url`
- `width`
- `height`
- `seed`

If the provider returns base64 blobs, save them to files and return URLs or paths.

## Notes

- Some fields may be ignored; treat them as best-effort.
- Keep request/response samples in `output/images/` for debugging.
