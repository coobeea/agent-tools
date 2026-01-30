# Fun-ASR 语音识别库

基于 [FunAudioLLM/Fun-ASR-Nano-2512](https://modelscope.cn/models/FunAudioLLM/Fun-ASR-Nano-2512) 的高级封装，提供简洁易用的语音识别接口。

## 特性

- **高精度识别**: 基于数千万小时真实语音数据训练，识别准确率高达 93%
- **多语言支持**: 支持中文、英文、日文，以及 7 种中文方言和 26 种地域口音
- **热词增强**: 支持自定义热词，提高特定词汇识别准确率
- **实时转写**: 支持低延迟流式识别
- **VAD 支持**: 内置语音端点检测，自动切分长音频
- **本地部署**: 模型完全本地运行，保护隐私

## 支持的语言

### Fun-ASR-Nano (基础版)
- 中文、英文、日文
- 中文方言: 吴语、粤语、闽语、客家话、赣语、湘语、晋语
- 中文口音: 河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西等 26 个地区

### Fun-ASR-MLT-Nano (多语言版)
- 支持 31 种语言: 中文、英文、粤语、日文、韩文、越南语、印尼语、泰语、马来语、菲律宾语、阿拉伯语、印地语等

## 安装

```bash
# 安装依赖
pip install -r requirements.txt
```

## 快速开始

### 基本使用

```python
from asr import FunASR

# 初始化
asr = FunASR()

# 语音转文字
result = asr.transcribe("audio.wav", language="中文")
print(result)
```

### 使用热词增强

```python
from asr import FunASR

asr = FunASR()

# 设置热词提高识别准确率
result = asr.transcribe(
    "meeting.wav",
    language="中文",
    hotwords=["人工智能", "深度学习", "语音识别"],
    itn=True,  # 启用文本规整
)
```

### 流式识别

```python
from asr import FunASR

asr = FunASR()

# 流式识别长音频
for partial_result in asr.transcribe_stream("long_audio.wav", chunk_size=0.72):
    print(partial_result)
```

### 使用 VAD

```python
from asr import FunASR

# 启用 VAD
asr = FunASR(use_vad=True, vad_max_segment_time=30000)

# 识别带静音的音频
result = asr.transcribe("meeting_recording.wav")
```

### 便捷函数

```python
from asr import transcribe

# 一行代码完成识别
text = transcribe("audio.wav", language="中文")
```

## API 参考

### FunASR 类

```python
FunASR(
    model_name: str = "FunAudioLLM/Fun-ASR-Nano-2512",
    device: str = None,  # 自动选择: cuda > mps > cpu
    model_dir: str = "/Users/lifeng/data/models",
    use_vad: bool = False,
    vad_max_segment_time: int = 30000,
    hub: str = "ms",  # "ms" 或 "hf"
)
```

### transcribe 方法

```python
asr.transcribe(
    audio,           # 音频输入: 文件路径、numpy 数组或 torch 张量
    language="中文", # 目标语言
    hotwords=None,   # 热词列表
    itn=True,        # 是否进行文本规整
    batch_size=1,    # 批处理大小
)
```

### transcribe_stream 方法

```python
asr.transcribe_stream(
    audio_path,       # 音频文件路径
    chunk_size=0.72,  # 音频块大小（秒）
    language="中文",
    hotwords=None,
    itn=True,
)
```

## 模型存储

默认情况下，模型会下载到 `/Users/lifeng/data/models` 目录。可以通过 `model_dir` 参数自定义：

```python
asr = FunASR(model_dir="/path/to/models")
```

## 示例

查看 `asr/examples/` 目录获取更多示例：

- `demo_basic.py`: 基础使用示例
- `demo_stream.py`: 流式识别示例
- `demo_vad.py`: VAD 使用示例

## 性能参考

| 测试集 | Fun-ASR-Nano WER |
|--------|------------------|
| AIShell1 | 1.80% |
| AIShell2 | 2.75% |
| Fleurs-zh | 2.56% |
| Fleurs-en | 5.96% |
| WenetSpeech Meeting | 6.60% |

## 参考

- [Fun-ASR GitHub](https://github.com/FunAudioLLM/Fun-ASR)
- [ModelScope 模型页](https://modelscope.cn/models/FunAudioLLM/Fun-ASR-Nano-2512)
- [HuggingFace 模型页](https://huggingface.co/FunAudioLLM/Fun-ASR-Nano-2512)

## 引用

```bibtex
@misc{an2025funasrtechnicalreport,
    title={Fun-ASR Technical Report},
    author={Keyu An and Yanni Chen and others},
    year={2025},
    eprint={2509.12508},
    archivePrefix={arXiv},
}
```

## 许可证

本项目遵循原始 Fun-ASR 项目的许可证。
