---
name: bailian-crawl-and-skill
description: Crawl Alibaba Bailian Model Studio models page and generate/update Claude skills + summary artifacts.
---

Category: task

# 阿里云百炼抓取与 Skills 生成

## When to use

- Use when you need to refresh the models page crawl and regenerate the derived summary and `skills/aliyun-*` skill files.

## Workflow

1) Crawl models page (raw markdown)

```bash
npx -y @just-every/crawl \"https://help.aliyun.com/zh/model-studio/models\" > aliyun-model-studio-models.md
```

2) Rebuild summary (models + API/usage links)

```bash
python3 scripts/bailian/refresh_models_summary.py
```

3) Regenerate skills (creates/updates `skills/aliyun-*`)

```bash
python3 scripts/bailian/refresh_bailian_skills.py
```

## Outputs

- `aliyun-model-studio-models.md`: raw crawl output
- `outputs/aliyun-model-studio-models-summary.md`: cleaned summary
- `skills/aliyun-*/*`: generated skills

## Notes

- Do not invent model IDs or API endpoints; only use links present on the models page.
- After regeneration, update `README.en.md` and `README.zh.md` if skills list changed.
