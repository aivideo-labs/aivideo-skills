# Provider selection (image)

## Default decision flow

1. If user explicitly names a provider, use it.
2. If user wants stylized / artistic / illustrative output, prefer **Midjourney**.
3. If user needs strict prompt adherence or safety constraints, prefer **OpenAI**.
4. If user requires China-region infra or Ali ecosystem integration, prefer **Alibaba Tongyi**.
5. If user needs fast batch generation in China, prefer **Volcengine**.
6. If requirements are unclear, ask a single clarifying question: "Do you have a preferred provider?"

## Comparison factors to mention

- Prompt adherence vs stylization
- Latency and batch size
- Regional compliance / data residency
- Cost and quota
- Feature availability (masking, inpainting, variations)

## Fallback

If the chosen provider fails or is unavailable, fall back in this order:
OpenAI -> Alibaba Tongyi -> Volcengine -> Midjourney
