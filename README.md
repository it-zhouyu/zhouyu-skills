# ZhouYu Skills

语音合成技能集合，为 Claude Code 提供文本转语音能力。

## 包含技能

### 豆包语音合成 (doubao-tts)

使用火山引擎豆包语音合成 2.0 将文本转换为高质量的中文语音音频。

**特性：**
- 单个文本生成单个音频文件
- 多个文本片段批量生成
- 支持多种中文音色
- 输出 MP3 格式，24000Hz 采样率

**快速开始：**

```bash
# 安装依赖
cd skills/doubao-tts
pip install -r requirements.txt

# 设置环境变量
export DOUBAO_TTS_APP_ID="your_app_id"
export DOUBAO_TTS_ACCESS_TOKEN="your_access_token"

# 生成单个音频
python3 scripts/tts_single.py "你好世界" -o output.mp3

# 批量生成
python3 scripts/tts_batch.py \
  -s "第一段文本" scene1.mp3 \
  -s "第二段文本" scene2.mp3 \
  -o ./audio/
```

详细文档请查看 [skills/doubao-tts/SKILL.md](skills/doubao-tts/SKILL.md)。

## 技能使用方式

在 Claude Code 中，可以通过以下方式使用技能：

- "用豆包TTS把这段文字转成语音：你好世界"
- "把这个脚本转成音频，保存到 output.mp3"
- "生成这些段落的语音文件"

## 获取 API 凭证

使用豆包 TTS 需要火山引擎的 API 凭证：

1. 访问 [火山引擎控制台](https://console.volcengine.com/)
2. 开通语音技术服务
3. 获取 APP ID 和 Access Token

## 项目结构

```
zhouyu-skills/
├── README.md
└── skills/
    └── doubao-tts/
        ├── SKILL.md           # 技能详细文档
        ├── requirements.txt   # Python 依赖
        ├── scripts/
        │   ├── tts_single.py  # 单文本生成
        │   └── tts_batch.py   # 批量生成
        └── lib/
            ├── __init__.py
            └── protocols.py   # WebSocket 协议实现
```

## 许可证

MIT