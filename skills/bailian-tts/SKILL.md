---
name: bailian-tts
description: Generate human-like speech audio with BaiLian DashScope Qwen TTS (qwen3-tts-flash). Use when converting text to speech, producing voice lines for short drama/news videos, or documenting TTS request/response fields for DashScope.
---

Category: provider

# BaiLian Qwen TTS

## Critical model name

Use the recommended model:
- `qwen3-tts-flash`

## Normalized interface (tts.generate)

### Request
- `text` (string, required)
- `voice` (string, required)
- `language_type` (string, optional; default `Auto`)
- `stream` (bool, optional; default false)

### Response
- `audio_url` (string, when stream=false)
- `audio_base64_pcm` (string, when stream=true)
- `sample_rate` (int, 24000)
- `format` (string, wav or pcm depending on mode)

## Quick start (Python + DashScope SDK)

```python
import os
import dashscope

# Beijing region; for Singapore use: https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

text = "Hello, this is a short voice line."
response = dashscope.MultiModalConversation.call(
    model="qwen3-tts-flash",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    text=text,
    voice="Cherry",
    language_type="English",
    stream=False,
)

audio_url = response.output.audio.url
print(audio_url)
```

## Streaming notes

- `stream=True` returns Base64-encoded PCM chunks at 24kHz.
- Decode chunks and play or concatenate to a pcm buffer.
- The response contains `finish_reason == "stop"` when the stream ends.

## Operational guidance

- Keep text short per request (doc limit is 600 characters for qwen3-tts-flash).
- Use `language_type` consistent with the text to improve pronunciation.
- Cache by `(text, voice, language_type)` to avoid repeat costs.

## Output location

- Save generated audio under `output/audio/` by default.

## References

- `references/api_reference.md` for parameter mapping and streaming example.