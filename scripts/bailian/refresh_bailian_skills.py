#!/usr/bin/env python3
"""Regenerate skills/aliyun-* skill files from the models page crawl."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "aliyun-model-studio-models.md"

if not RAW.exists():
    raise SystemExit(f"Missing raw crawl: {RAW}")

text = RAW.read_text()

# Extract model IDs
model_id_re = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{2,}$")
model_ids = set()
for line in text.splitlines():
    s = line.strip()
    if not s or "http" in s or "/" in s:
        continue
    if model_id_re.match(s):
        model_ids.add(s)

# Extract model names from link texts
link_re = re.compile(r"\[([^\]]+?)\]\(([^)]+)\)")
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
links = []
for t, u in link_re.findall(text):
    t = t.strip()
    u = u.strip()
    if any(k in t for k in keywords):
        model_names.add(t)
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

# Deduplicate links
seen = set()
api_links = []
for t, u in links:
    if (t, u) in seen:
        continue
    seen.add((t, u))
    api_links.append((t, u))


def docs_by_url_substr(*subs):
    out = []
    for t, u in api_links:
        if any(s in u for s in subs):
            out.append((t, u))
    return out


def filter_ids(prefixes=(), substr=()):
    out = []
    for mid in sorted(model_ids):
        if prefixes and any(mid.startswith(p) for p in prefixes):
            out.append(mid)
            continue
        if substr and any(s in mid for s in substr):
            out.append(mid)
            continue
    return out


def filter_names(words):
    return sorted([n for n in model_names if any(w in n for w in words)])


skills = [
    {
        "name": "aliyun-text-generation",
        "title": "阿里云百炼 - 文本生成",
        "desc": "Alibaba Bailian text generation (通义千问/第三方文本大模型). Use for text generation/chat/completion and Qwen API usage.",
        "model_words": [
            "通义千问",
            "Qwen",
            "DeepSeek",
            "Kimi",
            "GLM",
            "零一万物",
            "Llama",
            "百川",
            "ChatGLM",
            "Dolly",
            "姜子牙",
            "BELLE",
            "元语",
        ],
        "model_prefixes": [
            "qwen",
            "qwen2",
            "qwen2.5",
            "qwen3",
            "deepseek",
            "kimi",
            "glm",
            "yi",
            "llama",
            "baichuan",
            "chatglm",
            "dolly",
            "ziya",
            "belle",
            "chatyuan",
            "billa",
        ],
        "docs": docs_by_url_substr(
            "qwen-api-reference",
            "deepseek-api",
            "kimi-api",
            "minimax",
            "use-open-source-qwen",
            "siliconflow-deepseek",
        ),
    },
    {
        "name": "aliyun-multimodal",
        "title": "阿里云百炼 - 多模态理解",
        "desc": "Multimodal understanding with Qwen VL/Audio/Omni/Omni-Realtime and related APIs.",
        "model_words": ["通义千问VL", "通义千问Audio", "通义千问Omni", "Omni-Realtime", "QVQ"],
        "model_prefixes": [
            "qwen-vl",
            "qwen3-vl",
            "qwen2.5-vl",
            "qwen-audio",
            "qwen3-omni",
            "qwen3-asr",
            "qwen3-audio",
            "qwen3-omni",
        ],
        "docs": docs_by_url_substr("qwen-vl-ocr-api-reference", "qwen-deep-research-api"),
    },
    {
        "name": "aliyun-image-generate",
        "title": "阿里云百炼 - 文生图/图像生成",
        "desc": "Image generation with Tongyi Qwen Image, Wanx, Stable Diffusion, FLUX, Z-Image, WordArt.",
        "model_words": [
            "通义千问文生图",
            "通义万相",
            "通义-文生图-Z-Image",
            "Stable Diffusion",
            "FLUX",
            "WordArt",
            "创意海报生成",
        ],
        "model_prefixes": ["wanx", "wordart", "sd", "flux", "z-image"],
        "docs": docs_by_url_substr(
            "qwen-image-api",
            "text-to-image",
            "wan-image-generation",
            "z-image",
            "stable-diffusion",
            "flux-api-reference",
            "creative-poster-generation",
        ),
    },
    {
        "name": "aliyun-image-edit",
        "title": "阿里云百炼 - 图像编辑",
        "desc": "Image edit, inpaint, outpaint, translate, background, segmentation, virtual model/try-on.",
        "model_words": [
            "通义千问图像编辑",
            "通义万相图像编辑",
            "图像翻译",
            "涂鸦作画",
            "图像局部重绘",
            "人像风格重绘",
            "图像背景生成",
            "图像画面扩展",
            "人物实例分割",
            "图像擦除补全",
            "虚拟模特",
            "鞋靴模特",
            "FaceChain",
            "AI试衣",
        ],
        "model_prefixes": ["wanx", "qwen-image", "facechain"],
        "docs": docs_by_url_substr(
            "qwen-image-edit",
            "qwen-mt-image",
            "wan2-5-image-edit",
            "wanx-image-edit",
            "wanx-sketch-to-image",
            "vary-region",
            "portrait-style-redraw",
            "wanx-background-generation",
            "image-scaling",
            "image-instance-segmentation",
            "image-erase-completion",
            "virtual-model",
            "shoe-model",
            "facechain",
            "fill-texture-effect",
            "outfitanyone",
            "aitryon",
            "ai-fitting-picture-finishing",
        ),
    },
    {
        "name": "aliyun-tts",
        "title": "阿里云百炼 - 语音合成 (TTS)",
        "desc": "Text-to-speech and real-time TTS with Qwen/CosyVoice/Sambert.",
        "model_words": ["通义千问实时语音合成", "通义千问语音合成", "CosyVoice语音合成", "Sambert语音合成"],
        "model_prefixes": ["cosyvoice", "sambert", "qwen-tts"],
        "docs": docs_by_url_substr("qwen-tts-api", "qwen-tts-realtime"),
    },
    {
        "name": "aliyun-asr",
        "title": "阿里云百炼 - 语音识别/翻译 (ASR)",
        "desc": "Speech-to-text and speech translation with Qwen, Fun-ASR, Gummy, Paraformer, SenseVoice.",
        "model_words": ["通义千问实时语音识别", "通义千问录音文件识别", "Fun-ASR", "Gummy", "Paraformer", "SenseVoice"],
        "model_prefixes": ["funasr", "gummy", "paraformer", "sensevoice", "qwen-audio-asr"],
        "docs": docs_by_url_substr(
            "qwen-asr",
            "real-time-speech-recognition",
            "sentence-recognition",
            "fun-asr",
            "paraformer",
            "sensevoice",
            "live-translator",
            "qwen3-livetranslate",
        ),
    },
    {
        "name": "aliyun-video-generate",
        "title": "阿里云百炼 - 视频生成",
        "desc": "Text-to-video and image-to-video generation (first frame/first+last/multi-image) and avatar video.",
        "model_words": [
            "文生视频",
            "首帧生视频",
            "首尾帧生视频",
            "多图生视频",
            "AnimateAnyone",
            "通义万相-数字人",
            "悦动人像EMO",
            "灵动人像LivePortrait",
            "表情包Emoji",
        ],
        "model_prefixes": ["animate", "emo", "liveportrait", "wanx", "video"],
        "docs": docs_by_url_substr(
            "text-to-video",
            "image-to-video",
            "first-and-last-frame",
            "wan-s2v",
            "wan-animate",
            "animate-anyone",
            "animateanyone",
            "emo",
            "liveportrait",
            "emoji",
            "wanx-vace",
        ),
    },
    {
        "name": "aliyun-video-edit",
        "title": "阿里云百炼 - 视频编辑/视频生视频",
        "desc": "Video editing, video-to-video reference, lip sync replacement, and style transfer.",
        "model_words": ["通用视频编辑", "VideoRetalk", "视频风格重绘", "参考生视频"],
        "model_prefixes": ["videoretalk", "video"],
        "docs": docs_by_url_substr("videoretalk", "video-style-transform", "wan-video-to-video"),
    },
    {
        "name": "aliyun-embedding-text",
        "title": "阿里云百炼 - 文本向量",
        "desc": "Text embedding models for search, clustering, and retrieval.",
        "model_words": ["文本向量"],
        "model_prefixes": ["text-embedding", "bge", "gte-embedding", "tongyi-embedding"],
        "docs": docs_by_url_substr("text-embedding-synchronous", "text-embedding-batch"),
    },
    {
        "name": "aliyun-embedding-multimodal",
        "title": "阿里云百炼 - 多模态向量",
        "desc": "Multimodal embeddings for text/image/video retrieval and classification.",
        "model_words": ["多模态向量"],
        "model_prefixes": ["qwen3-vl-embedding", "qwen2.5-vl-embedding", "tongyi-embedding-vision", "multimodal-embedding"],
        "docs": docs_by_url_substr("multimodal-embedding-api-reference"),
    },
    {
        "name": "aliyun-rerank",
        "title": "阿里云百炼 - 文本排序 (Rerank)",
        "desc": "Semantic reranking models for retrieval.",
        "model_words": ["文本排序", "Rerank"],
        "model_prefixes": ["qwen3-rerank", "gte-rerank"],
        "docs": docs_by_url_substr("text-rerank-api"),
    },
    {
        "name": "aliyun-opennlu",
        "title": "阿里云百炼 - OpenNLU",
        "desc": "OpenNLU for text classification and extraction.",
        "model_words": ["OpenNLU"],
        "model_prefixes": ["opennlu"],
        "docs": docs_by_url_substr("opennlu-api"),
    },
    {
        "name": "aliyun-intent-detect",
        "title": "阿里云百炼 - 意图理解",
        "desc": "Intent detection capability for tool selection and routing.",
        "model_words": ["意图理解"],
        "model_prefixes": ["tongyi-intent-detect"],
        "docs": docs_by_url_substr("intent-detect-capability"),
    },
    {
        "name": "aliyun-role-play",
        "title": "阿里云百炼 - 角色扮演",
        "desc": "Role-play / persona chat models.",
        "model_words": ["角色扮演"],
        "model_prefixes": ["qwen-plus-character", "qwen-flash-character"],
        "docs": docs_by_url_substr("role-play"),
    },
    {
        "name": "aliyun-gui-plus",
        "title": "阿里云百炼 - GUI-Plus 界面交互",
        "desc": "GUI-Plus for screenshot-based UI action planning.",
        "model_words": ["GUI-Plus"],
        "model_prefixes": ["gui-plus"],
        "docs": docs_by_url_substr("gui-automation", "gui-plus-interface-interaction-model"),
    },
    {
        "name": "aliyun-farui",
        "title": "阿里云百炼 - 通义法睿",
        "desc": "Legal reasoning and document drafting with Farui.",
        "model_words": ["通义法睿"],
        "model_prefixes": ["farui"],
        "docs": docs_by_url_substr("tongyi-farui-api"),
    },
]

skills_dir = ROOT / "skills"

for sk in skills:
    name = sk["name"]
    path = skills_dir / name
    path.mkdir(parents=True, exist_ok=True)

    ids = filter_ids(prefixes=tuple(sk["model_prefixes"]))
    names = filter_names(sk["model_words"])

    skill_md = path / "SKILL.md"
    with skill_md.open("w") as f:
        f.write("---\n")
        f.write(f"name: {name}\n")
        f.write(f"description: {sk['desc']}\n")
        f.write("---\n\n")
        f.write("Category: task\n\n")
        f.write(f"# {sk['title']}\n\n")
        f.write("## When to use\n\n")
        f.write("- Use when implementing or documenting this capability in Alibaba Bailian (Model Studio).\n")
        f.write("- Prefer official API references linked below; do not guess parameter names.\n\n")

        f.write("## Models (from the models page)\n\n")
        if names:
            f.write("### 中文/产品名\n")
            for n in names:
                f.write(f"- {n}\n")
            f.write("\n")
        if ids:
            f.write("### 模型 ID\n")
            for mid in ids:
                f.write(f"- {mid}\n")
            f.write("\n")
        if not names and not ids:
            f.write("- See `outputs/aliyun-model-studio-models-summary.md` for the full list.\n\n")

        f.write("## API 参考与使用方法\n\n")
        docs = sk["docs"]
        if docs:
            for t, u in docs:
                label = t if t else u
                f.write(f"- {label}: {u}\n")
        else:
            f.write("- See `outputs/aliyun-model-studio-models-summary.md` for available API/usage links.\n")
        f.write("\n")

        f.write("## Notes\n\n")
        f.write("- Model availability can differ by deployment region (中国内地/全球/国际/美国).\n")
        f.write("- Use exact model strings as listed in the models page; avoid inventing aliases.\n")
        f.write("- For a complete list of models and links, see `outputs/aliyun-model-studio-models-summary.md`.\n")

print("Skills updated:", len(skills))
