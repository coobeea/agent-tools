# Qwen3-TTS 语音合成库

基于 [Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice](https://modelscope.cn/models/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice) 的高级封装，提供简洁易用的语音合成接口。

## 特性

- **9 种预设音色**: 覆盖中文、英文、日语、韩语
- **10 种语言支持**: 中、英、日、韩、德、法、俄、葡、西、意
- **指令控制**: 支持情感、语速、音调等多维度控制
- **超低延迟**: 首包延迟仅 97ms，支持流式生成
- **本地部署**: 模型完全本地运行

## 环境要求

**重要**: 由于依赖限制，需要使用 Python 3.12 环境。

```bash
# 创建 Python 3.12 环境
conda create -n qwen3-tts python=3.12 -y
conda activate qwen3-tts

# 安装依赖
pip install -U qwen-tts soundfile

# 可选：安装 FlashAttention 加速（仅 CUDA）
pip install -U flash-attn --no-build-isolation
```

## 支持的音色

| 音色 | 描述 | 母语 |
|------|------|------|
| Vivian | 明亮、略带锐利的年轻女声 | 中文 |
| Serena | 温暖、温柔的年轻女声 | 中文 |
| Uncle_Fu | 成熟男声，低沉圆润 | 中文 |
| Dylan | 年轻的北京男声，清晰自然 | 中文(北京话) |
| Eric | 活泼的成都男声，略带沙哑 | 中文(四川话) |
| Ryan | 动感男声，节奏感强 | 英文 |
| Aiden | 阳光美式男声，中音清晰 | 英文 |
| Ono_Anna | 俏皮日本女声，轻盈灵动 | 日语 |
| Sohee | 温暖韩国女声，情感丰富 | 韩语 |

## 快速开始

### 基本使用

```python
from tts import QwenTTS

# 初始化
tts = QwenTTS()

# 文字转语音
tts.speak(
    text="你好，我是 Qwen3 语音合成模型！",
    speaker="Vivian",
    language="Chinese",
    output_path="output.wav",
)
```

### 带情感控制

```python
from tts import QwenTTS

tts = QwenTTS()

# 使用情感控制
tts.speak_with_emotion(
    text="今天真是太开心了！",
    emotion="开心",
    speaker="Serena",
    output_path="happy.wav",
)
```

### 指令控制

```python
from tts import QwenTTS

tts = QwenTTS()

# 使用指令控制语音风格
tts.speak(
    text="这件事情让我非常生气！",
    speaker="Uncle_Fu",
    language="Chinese",
    instruct="用愤怒的语气说，说话速度稍快",
    output_path="angry.wav",
)
```

### 英文语音

```python
from tts import QwenTTS

tts = QwenTTS()

tts.speak(
    text="Hello! Nice to meet you!",
    speaker="Ryan",
    language="English",
    instruct="Very friendly and energetic",
    output_path="english.wav",
)
```

## API 参考

### QwenTTS 类

```python
QwenTTS(
    model_name: str = "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    device: str = None,  # 自动选择: cuda > mps > cpu
    model_dir: str = "/Users/lifeng/data/models",
    dtype: str = "bfloat16",
    use_flash_attention: bool = False,
)
```

### speak 方法

```python
tts.speak(
    text,           # 要合成的文本
    speaker="Vivian",  # 音色名称
    language="Chinese",  # 语言
    instruct=None,   # 指令控制
    output_path=None,  # 输出文件路径
)
```

### speak_with_emotion 方法

```python
tts.speak_with_emotion(
    text,            # 要合成的文本
    emotion,         # 情感：开心/愤怒/悲伤/惊讶/温柔
    speaker="Vivian",
    language="Chinese",
    output_path=None,
)
```

## 模型存储

默认情况下，模型会下载到 `/Users/lifeng/data/models` 目录。

## 参考

- [Qwen3-TTS GitHub](https://github.com/QwenLM/Qwen3-TTS)
- [ModelScope 模型页](https://modelscope.cn/models/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice)
- [HuggingFace 模型页](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice)
- [DashScope API](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime)

## 引用

```bibtex
@article{Qwen3-TTS,
    title={Qwen3-TTS Technical Report},
    author={Hangrui Hu and others},
    journal={arXiv preprint arXiv:2601.15621},
    year={2026}
}
```
