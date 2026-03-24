---
name: doubao-tts
description: 使用豆包语音合成 2.0 将文本转换为语音音频。
---

# 豆包语音合成技能

将文本转换为高质量的中文语音音频。

## 何时使用
当用户需要文本转语音、生成音频、TTS 合成、朗读文本、创建配音时使用此技能。

## 支持功能
- 单个文本生成单个音频文件
- 多个文本片段批量生成多个音频文件
- 可选择不同音色（默认：zh_female_xiaohe_uranus_bigtts）
- 输出 MP3 格式，24000Hz 采样率

## 示例用法
- "用豆包TTS把这段文字转成语音：你好世界"
- "把这个脚本转成音频，保存到 output.mp3"
- "生成这些段落的语音文件"

## 快速开始

### 单个文本生成音频

使用 `scripts/tts_single.py` 生成单个音频文件：

```bash
python3 scripts/tts_single.py "要合成的文本" -o output.mp3
```

参数：
- 第一个参数：要合成的文本（必需）
- `-o, --output`：输出文件路径（默认：`output.mp3`）
- `-v, --voice`：音色类型（默认：`zh_female_xiaohe_uranus_bigtts`）

### 多个片段批量生成

使用 `scripts/tts_batch.py` 批量生成多个音频文件：

```bash
python3 scripts/tts_batch.py -c segments.json -o ./audio_output/
```

或直接在命令行指定：

```bash
python3 scripts/tts_batch.py \
  -s "第一段文本" scene1.mp3 \
  -s "第二段文本" scene2.mp3 \
  -o ./audio_output/
```

参数：
- `-c, --config`：JSON 配置文件路径
- `-s, --segment`：文本和文件名对（可多次使用）
- `-o, --output-dir`：输出目录（默认：当前目录）
- `-v, --voice`：音色类型（默认：`zh_female_xiaohe_uranus_bigtts`）

## 可用音色

常用音色选项：

| 音色 ID | 描述 |
|---------|------|
| `zh_female_xiaohe_uranus_bigtts` | 女声 - 小荷（默认，自然流畅） |
| `zh_male_m191_uranus_bigtts` | 男声 - 云舟 |
| `zh_female_vv_uranus_bigtts` | 女声 - Vivi |

更多音色请参考[豆包语音合成模型2.0音色列表](https://www.volcengine.com/docs/6561/1257544?lang=zh#豆包语音合成模型2-0-音色列表)


## 配置文件格式

批量生成时，可使用 JSON 配置文件：

```json
[
  {"text": "第一段要合成的文本", "filename": "scene1.mp3"},
  {"text": "第二段要合成的文本", "filename": "scene2.mp3"}
]
```

## 使用示例

### 示例 1：生成单个语音文件

用户请求：
> 把这段文字转成语音："欢迎观看本期视频，今天我们聊聊人工智能。"

执行：
```bash
python3 scripts/tts_single.py "欢迎观看本期视频，今天我们聊聊人工智能。" -o intro.mp3
```

### 示例 2：批量生成视频配音

用户请求：
> 为我的视频生成配音，有三个场景...

执行：
```bash
python3 scripts/tts_batch.py \
  -s "场景一的文本内容" scene1.mp3 \
  -s "场景二的文本内容" scene2.mp3 \
  -s "场景三的文本内容" scene3.mp3 \
  -o ./public/audio/my-video/
```

### 示例 3：指定音色

用户请求：
> 用男声朗读这段文字

执行：
```bash
python3 scripts/tts_single.py "要朗读的内容" -v zh_male_chunhou_uranus_bigtts -o male_voice.mp3
```

## 依赖

- Python 3.7+
- websockets 库

安装依赖：
```bash
pip3 install websockets
```

## 环境变量配置

使用前需要设置以下环境变量：

```bash
export DOUBAO_TTS_APP_ID="your_app_id"
export DOUBAO_TTS_ACCESS_TOKEN="your_access_token"
```

可选环境变量：
```bash
export DOUBAO_TTS_ENDPOINT="wss://openspeech.bytedance.com/api/v3/tts/bidirection"  # API 端点
export DOUBAO_TTS_DEFAULT_VOICE="zh_female_xiaohe_uranus_bigtts"  # 默认音色
```

建议将环境变量添加到 `~/.zshrc` 或 `~/.bashrc` 中：
```bash
# 豆包 TTS 配置
export DOUBAO_TTS_APP_ID="your_app_id"
export DOUBAO_TTS_ACCESS_TOKEN="your_access_token"
```

## 技术细节

- 使用火山引擎豆包语音合成 2.0 API
- 输出格式：MP3
- 采样率：24000Hz
- 通过 WebSocket 流式传输文本，实时接收音频