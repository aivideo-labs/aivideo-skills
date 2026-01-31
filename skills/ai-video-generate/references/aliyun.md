# Alibaba Tongyi video generation

## Use when

Use when China-region infra or Ali ecosystem integration is required.

## Model names

- TODO: fill exact model strings for Alibaba Tongyi

## Auth and endpoint

- API_BASE: TODO
- API_KEY: TODO
- MODEL: TODO

## Normalized mapping

Map normalized `video.generate` into provider fields:

- `prompt` -> prompt
- `negative_prompt` -> negative_prompt (if supported)
- `duration` -> duration seconds
- `fps` -> fps
- `size` -> size (WxH)
- `aspect_ratio` -> aspect_ratio (if supported)
- `seed` -> seed (if supported)
- `reference_image` -> provider-specific image field
- `motion_strength` -> motion control field (if supported)

## Response parsing

Normalize into:

- `video_url`
- `duration`
- `fps`
- `seed`

If the provider returns base64 blobs, save them to files and return URLs or paths.

## Notes

- Many providers are async; handle task IDs and polling.
- Keep request/response samples in `output/videos/` for debugging.
