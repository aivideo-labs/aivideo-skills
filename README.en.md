# AI Video Skills

This repository contains a curated set of Codex/Claude skills for AI-assisted video creation. It includes task-level skills (image/video generation, audio planning, script writing, editing) and provider-specific skills (e.g., BaiLian/Qwen image, Wan video, TTS). Each skill is a self-contained folder with a required `SKILL.md` and optional `scripts/`, `references/`, and `assets/`.

## Contents

### Task Skills (Category: task)
- **ai-image-generate**: Normalize image generation requests and routing across providers.
- **ai-video-generate**: Normalize video generation requests and routing across providers.
- **audio-generate**: Plan voice/music/SFX layers for short videos.
- **text-to-script**: Convert text into structured shot/script output.
- **video-edit**: Editing guidance, templates, and edit plans.
- **agent-browser**: Browser/agent helper skills.
- **character-bible**: Character sheets and story consistency templates.
- **bailian-crawl-and-skill**: Crawl Alibaba Model Studio models page and regenerate skills/summary.

### Alibaba Bailian Model Studio Skills (Category: task)
- **aliyun-text-generation**: Qwen/third-party text generation and chat.
- **aliyun-multimodal**: Qwen VL/Audio/Omni multimodal understanding.
- **aliyun-image-generate**: Text-to-image generation (Qwen Image/Wanx/FLUX/SD).
- **aliyun-image-edit**: Image edit, inpaint/outpaint, try-on, background, segmentation.
- **aliyun-tts**: Text-to-speech (real-time + batch).
- **aliyun-asr**: Speech recognition/translation (real-time + file).
- **aliyun-video-generate**: Text-to-video & image-to-video generation.
- **aliyun-video-edit**: Video editing, video-to-video, style transfer, lip sync.
- **aliyun-embedding-text**: Text embedding models.
- **aliyun-embedding-multimodal**: Multimodal embedding models.
- **aliyun-rerank**: Text rerank models for retrieval.
- **aliyun-opennlu**: Text classification/extraction (OpenNLU).
- **aliyun-intent-detect**: Intent detection routing models.
- **aliyun-role-play**: Role-play/persona chat.
- **aliyun-gui-plus**: GUI-Plus UI action planning.
- **aliyun-farui**: Legal assistant (Farui).

### Provider Skills (Category: provider)
- **bailian-qwen-image**: BaiLian DashScope image generation (Qwen Image).
- **bailian-wan-video**: BaiLian DashScope video generation (Wan).
- **bailian-tts**: BaiLian TTS.

## Skill Structure

Each skill follows this structure:

```
<skill-name>/
├── SKILL.md          # Required: frontmatter + instructions
├── scripts/          # Optional: runnable helpers
├── references/       # Optional: API docs, templates, prompt guides
└── assets/           # Optional: files used in output
```

## Data Artifacts

- `aliyun-model-studio-models.md`: Raw crawl of the Alibaba Model Studio models page.
- `outputs/aliyun-model-studio-models-summary.md`: Cleaned model list + API/usage links.

## How to Use Skills

1. Identify the skill folder under `skills/`.
2. Open `SKILL.md` for workflow and guidance.
3. If a skill includes scripts, run them directly.
4. If a skill references `references/*.md`, read those for API mappings and examples.

### Authentication Configuration

Most generation scripts read credentials and endpoints from a .env file (repo root or current directory) or environment variables. Typical variables:

- `API_BASE`: Full endpoint URL
- `API_KEY`: API token / bearer key
- `MODEL`: Default model name
- `TIMEOUT`: Request timeout seconds

Example (bash):

See `.env.example` for a template.

```bash
export API_BASE="https://api.example.com/v1/generate"
export API_KEY="your_key_here"
export MODEL="your-model-name"
export TIMEOUT="120"
```

Some provider-specific skills use other names (e.g., `DASHSCOPE_API_KEY`). For BaiLian skills, prefer `DASHSCOPE_API_KEY` for auth. Follow each skill’s `SKILL.md` and `references/*.md`.

## How to Add or Modify a Skill (规范)

### 1) Naming
- Use lowercase letters, digits, and hyphens.
- Folder name must match `name` in `SKILL.md` frontmatter.

### 2) Required SKILL.md Format
- YAML frontmatter with only:
  - `name`
  - `description`
- Clear, imperative instructions in the body.
- Keep the body concise; move detailed docs to `references/`.

### 3) Recommended Practices
- Scripts must load auth/endpoint info from .env or environment variables.
- If required values are missing, exit with clear guidance and a .env example.
- Standardize inputs/outputs with a normalized interface.
- Keep provider-specific details in `references/<provider>.md`.
- Put deterministic or reusable logic in `scripts/`.
- Keep assets in `assets/` and avoid extra docs.

### 4) Validation
- Ensure each skill is self-contained and references are correct.
- Run scripts once after changes to ensure they work.
