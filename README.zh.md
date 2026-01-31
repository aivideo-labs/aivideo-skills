# AI 视频技能库（中文）

该仓库存放用于 AI 视频制作的 Codex/Claude 技能，包含任务级技能（图像/视频生成、音频规划、脚本、剪辑）和厂商技能（如百炼 Qwen 图像、Wan 视频、TTS）。每个技能是一个独立目录，至少包含 `SKILL.md`，可选 `scripts/`、`references/`、`assets/`。

## 包含功能

### 任务技能（Category: task）
- **ai-image-generate**：统一图像生成请求与路由。
- **ai-video-generate**：统一视频生成请求与路由。
- **audio-generate**：短视频音频层规划（配音/音乐/音效）。
- **text-to-script**：文本转结构化脚本/镜头。
- **video-edit**：剪辑规范、模板和编辑计划。
- **agent-browser**：浏览器/代理工具类技能。
- **character-bible**：角色设定与剧情一致性模板。
- **bailian-crawl-and-skill**：抓取百炼模型页并生成/更新技能与汇总。

### 阿里云百炼 Model Studio 能力技能（Category: task）
- **aliyun-text-generation**：通义千问/第三方文本生成与对话。
- **aliyun-multimodal**：通义千问 VL/Audio/Omni 多模态理解。
- **aliyun-image-generate**：文生图（Qwen Image/Wanx/FLUX/SD）。
- **aliyun-image-edit**：图像编辑、修复、扩展、试衣、背景/分割。
- **aliyun-tts**：语音合成（实时/离线）。
- **aliyun-asr**：语音识别/翻译（实时/录音文件）。
- **aliyun-video-generate**：文生视频/图生视频。
- **aliyun-video-edit**：视频编辑、视频生视频、风格转换、口型替换。
- **aliyun-embedding-text**：文本向量模型。
- **aliyun-embedding-multimodal**：多模态向量模型。
- **aliyun-rerank**：文本排序（Rerank）。
- **aliyun-opennlu**：文本分类/抽取（OpenNLU）。
- **aliyun-intent-detect**：意图理解模型。
- **aliyun-role-play**：角色扮演对话。
- **aliyun-gui-plus**：GUI-Plus 界面交互能力。
- **aliyun-farui**：通义法睿法律助手。

### 厂商技能（Category: provider）
- **bailian-qwen-image**：百炼 DashScope 图像生成（Qwen）。
- **bailian-wan-video**：百炼 DashScope 视频生成（Wan）。
- **bailian-tts**：百炼 TTS。

## 技能结构

```
<skill-name>/
├── SKILL.md          # 必需：前置元数据 + 使用说明
├── scripts/          # 可选：可执行脚本
├── references/       # 可选：API 文档/模板/提示词指南
└── assets/           # 可选：输出用素材
```

## 数据产物

- `aliyun-model-studio-models.md`：模型列表页面的原始抓取结果。
- `outputs/aliyun-model-studio-models-summary.md`：整理后的模型清单 + API/使用方法链接。

## Skill 使用方式

1. 在 `skills/` 下找到目标技能目录。
2. 阅读 `SKILL.md` 获取流程与规范。
3. 如果有 `scripts/`，可直接运行脚本。
4. 如需细节，阅读 `references/*.md`。

### 鉴权配置

多数脚本会先读取 .env（项目根目录或当前目录），再读取环境变量作为鉴权与端点。常见变量：

- `API_BASE`：接口完整地址
- `API_KEY`：密钥/Token
- `MODEL`：默认模型名
- `TIMEOUT`：超时秒数

示例（bash）：

可参考 `.env.example` 模板。

```bash
export API_BASE="https://api.example.com/v1/generate"
export API_KEY="your_key_here"
export MODEL="your-model-name"
export TIMEOUT="120"
```

部分厂商技能使用特定变量（如 `DASHSCOPE_API_KEY`）。BaiLian 技能鉴权优先使用 `DASHSCOPE_API_KEY`。请以各技能 `SKILL.md` / `references/*.md` 为准。

## 新增或修改 Skill 的规范

### 1）命名
- 小写字母 + 数字 + 连字符
- 目录名必须与 `SKILL.md` 的 `name` 一致

### 2）SKILL.md 要求
- YAML 仅包含：`name` / `description`
- 正文使用命令式描述
- 详细文档放到 `references/`

### 3）推荐实践
- 脚本必须优先从 .env 或环境变量读取鉴权与端点信息。
- 如缺失必填项，需明确提示并给出 .env 配置示例。
- 统一输入输出（normalized interface）
- 厂商差异放到 `references/<provider>.md`
- 可复用逻辑放 `scripts/`
- 素材放 `assets/`，避免多余文档

### 4）验证
- 保证技能自洽、引用路径正确
- 修改后至少跑一次脚本
