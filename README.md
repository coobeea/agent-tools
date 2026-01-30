# Agent Tools

AI Agent 工具集，包含语音识别（ASR）和语音合成（TTS）模块。

## 模块

### ASR - 语音识别

基于 [Fun-ASR-Nano-2512](https://modelscope.cn/models/FunAudioLLM/Fun-ASR-Nano-2512) 的语音识别模块。

**特性:**
- 中文、英文、日文语音识别
- 中文 7 种方言和 26 种地域口音支持
- 热词增强
- 实时流式识别
- VAD 语音端点检测

```python
from asr import FunASR

asr = FunASR()
result = asr.transcribe("audio.wav", language="中文")
print(result)
```

详细文档: [asr/README.md](asr/README.md)

### TTS - 语音合成

基于 [Qwen3-TTS-12Hz-1.7B-CustomVoice](https://modelscope.cn/models/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice) 的语音合成模块。

**特性:**
- 9 种预设音色
- 10 种语言支持
- 指令控制（情感、语速、音调等）
- 超低延迟流式生成

```python
from tts import QwenTTS

tts = QwenTTS()
tts.speak("你好，世界！", speaker="Vivian", output_path="output.wav")
```

详细文档: [tts/README.md](tts/README.md)

## 安装

### 环境要求

- Python 3.12（推荐使用虚拟环境）
- macOS / Linux / Windows
- GPU（可选，推荐用于加速）

### 创建虚拟环境

```bash
# 使用 pyenv
pyenv install 3.12.12
cd /path/to/agent-tools
~/.pyenv/versions/3.12.12/bin/python -m venv .venv
source .venv/bin/activate

# 或使用 conda
conda create -n agent-tools python=3.12 -y
conda activate agent-tools
```

### 安装依赖

```bash
pip install -r requirements.txt
```

## 模型存储

所有模型默认下载到 `/Users/lifeng/data/models` 目录：

```
/Users/lifeng/data/models/
├── models/
│   └── FunAudioLLM/
│       └── Fun-ASR-Nano-2512/     # ASR 模型
└── Qwen/
    ├── Qwen3-TTS-12Hz-1.7B-CustomVoice/  # TTS 模型
    └── Qwen3-TTS-Tokenizer-12Hz/          # TTS Tokenizer
```

## 项目结构

```
agent-tools/
├── README.md
├── requirements.txt
├── .venv/                 # Python 3.12 虚拟环境
├── asr/                   # 语音识别模块
│   ├── __init__.py
│   ├── fun_asr.py         # 主接口
│   ├── model.py           # 核心模型
│   ├── ctc.py
│   ├── tools/
│   │   └── utils.py
│   └── examples/
│       ├── demo_basic.py
│       ├── demo_stream.py
│       └── demo_vad.py
└── tts/                   # 语音合成模块
    ├── __init__.py
    ├── qwen_tts.py        # 主接口
    ├── README.md
    └── examples/
        └── demo_basic.py
```

## 快速开始

### 语音识别

```python
from asr import FunASR

# 初始化
asr = FunASR()

# 识别音频
result = asr.transcribe("audio.wav", language="中文")
print(result)

# 使用热词
result = asr.transcribe(
    "meeting.wav",
    language="中文",
    hotwords=["人工智能", "深度学习"],
)
```

### 语音合成

```python
from tts import QwenTTS

# 初始化
tts = QwenTTS()

# 生成语音
tts.speak(
    text="你好，我是语音合成模型！",
    speaker="Vivian",
    language="Chinese",
    output_path="output.wav",
)

# 带情感控制
tts.speak_with_emotion(
    text="今天真是太开心了！",
    emotion="开心",
    speaker="Serena",
    output_path="happy.wav",
)
```

## 参考

- [Fun-ASR GitHub](https://github.com/FunAudioLLM/Fun-ASR)
- [Qwen3-TTS GitHub](https://github.com/QwenLM/Qwen3-TTS)
- [ModelScope](https://modelscope.cn)

## 许可证

本项目遵循原始项目的许可证。
