# Agents Instructions (aivideo-skills)

## Purpose
Keep this repo’s skills and documentation aligned with Alibaba Bailian Model Studio capabilities and the existing video-creation skills.

## Canonical Sources
- Models page crawl: `aliyun-model-studio-models.md`
- Cleaned summary: `outputs/aliyun-model-studio-models-summary.md`
- Skills root: `skills/`

## When Updating Bailian/Model Studio Skills
1. Re-crawl the models page if needed and refresh `aliyun-model-studio-models.md`.
2. Update `outputs/aliyun-model-studio-models-summary.md` with the latest models + API/usage links.
3. Ensure each `skills/aliyun-*` skill lists:
   - Models (names + IDs)
   - API/usage links (from the models page)
4. Keep skill `name` in `SKILL.md` aligned with the folder name.

Tip: Use `skills/bailian-crawl-and-skill/SKILL.md` for the step-by-step commands.

## Documentation
- Keep `README.en.md` and `README.zh.md` in sync with the actual skill folders.
- List new skills under the correct section (task vs provider).
- Mention data artifacts when applicable.

## Guardrails
- Do not invent model IDs or API endpoints.
- Prefer official Model Studio docs linked from the models page.
- Keep edits minimal and structured; avoid duplicating long lists in multiple files.
