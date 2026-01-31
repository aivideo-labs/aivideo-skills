#!/usr/bin/env python3
"""Rebuild the cleaned summary from the models page crawl."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "aliyun-model-studio-models.md"
OUT = ROOT / "outputs/aliyun-model-studio-models-summary.md"

if not RAW.exists():
    raise SystemExit(f"Missing raw crawl: {RAW}")

text = RAW.read_text()

# Extract API/usage links from the page content
link_re = re.compile(r"\[([^\]]+?)\]\(([^)]+)\)")
links = []
for t, u in link_re.findall(text):
    t = t.strip()
    u = u.strip()
    if "model-studio" in u:
        if (
            "api" in u
            or "reference" in u
            or "capability" in u
            or "usage" in u
            or "get-started" in u
            or "API" in t
            or "使用方法" in t
            or "API参考" in t
            or "API 参考" in t
            or "API详情" in t
        ):
            links.append((t, u))

# Deduplicate while preserving order
seen = set()
api_links = []
for t, u in links:
    if (t, u) in seen:
        continue
    seen.add((t, u))
    api_links.append((t, u))

# Model IDs (versioned strings)
model_id_re = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{2,}$")
model_ids = set()
for line in text.splitlines():
    s = line.strip()
    if not s or "http" in s or "/" in s:
        continue
    if model_id_re.match(s):
        model_ids.add(s)

# Model names from link texts
keywords = [
    "通义",
    "Qwen",
    "万相",
    "DeepSeek",
    "Kimi",
    "GLM",
    "FLUX",
    "Stable Diffusion",
    "CosyVoice",
    "Sambert",
    "Paraformer",
    "SenseVoice",
    "Gummy",
    "Fun-ASR",
    "AnimateAnyone",
    "VideoRetalk",
    "LivePortrait",
    "EMO",
    "FaceChain",
    "WordArt",
    "Z-Image",
    "QVQ",
    "Omni",
    "Omni-Realtime",
    "GUI-Plus",
    "OpenNLU",
    "Rerank",
    "法睿",
    "意图理解",
    "角色扮演",
    "通义法睿",
]
model_names = set()
for t, _ in link_re.findall(text):
    t = t.strip()
    if any(k in t for k in keywords):
        model_names.add(t)

# Group model IDs by prefix
prefix_groups = {}
for mid in sorted(model_ids):
    prefix = mid.split("-")[0]
    prefix_groups.setdefault(prefix, []).append(mid)

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w") as f:
    f.write("# 阿里云百炼 Model Studio 模型与 API 用法（整理版）\n\n")
    f.write("来源：`https://help.aliyun.com/zh/model-studio/models`\n\n")
    f.write("## API 与使用方法链接\n\n")
    for t, u in api_links:
        f.write(f"- {t}: {u}\n")
    f.write("\n")
    f.write("## 模型名称（页面出现的中文/产品名）\n\n")
    for n in sorted(model_names):
        f.write(f"- {n}\n")
    f.write("\n")
    f.write("## 模型 ID（页面出现的英文/版本号）\n\n")
    for prefix in sorted(prefix_groups):
        f.write(f"### {prefix}\n")
        for mid in prefix_groups[prefix]:
            f.write(f"- {mid}\n")
        f.write("\n")

print(f"Wrote summary: {OUT}")
