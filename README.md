# Agent Tools

AI Agent 工具集合，包含语音识别（ASR）、语音合成（TTS）、光学字符识别（OCR）等功能。

## 📦 项目结构

```
agent-tools/
├── asr/              # 语音识别模块 (Fun-ASR-Nano)
├── tts/              # 语音合成模块 (Qwen3-TTS)
├── deepseek_ocr/     # OCR 模块 (DeepSeek-OCR-2)
├── glm_ocr/          # OCR 模块 (GLM-OCR)
└── requirements.txt  # 全局依赖（不推荐使用）
```

## 🔧 环境说明

**重要**: 每个模块都有独立的虚拟环境，避免依赖冲突！

### 为什么需要独立环境？

不同模块对 `transformers` 版本有不同要求：

| 模块 | transformers 版本 | 虚拟环境 |
|------|------------------|---------|
| ASR | >= 4.40.0 | 使用全局环境 |
| TTS | >= 4.57.3 | 使用全局环境 |
| DeepSeek-OCR | == 4.46.3 | ✅ `deepseek_env` |
| GLM-OCR | >= 5.0.0 (dev) | ✅ `glm_env` |

## 🚀 快速开始

### 1. ASR 语音识别

```bash
cd asr
pip install -r ../requirements.txt  # 或使用全局环境
python examples/demo_basic.py
```

**模型位置**: `/Users/lifeng/data/models/iic/speech_charctc_kws_phone-xiaoyun`

### 2. TTS 语音合成

```bash
cd tts
pip install -r ../requirements.txt  # 或使用全局环境
python examples/demo_basic.py
```

**模型位置**: `/Users/lifeng/data/models/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`

### 3. DeepSeek-OCR 光学字符识别

```bash
cd deepseek_ocr

# 一键安装
bash setup_env.sh

# 激活环境
source deepseek_env/bin/activate

# 运行测试
python examples/demo_basic.py
```

**模型位置**: `/Users/lifeng/data/models/deepseek-ai/DeepSeek-OCR-2`

**重要**: DeepSeek-OCR-2 需要手动修复模型文件才能在 CPU 上运行！详见 [deepseek_ocr/INSTALL.md](./deepseek_ocr/INSTALL.md)

### 4. GLM-OCR 光学字符识别

```bash
cd glm_ocr

# 一键安装
bash setup_env.sh

# 激活环境
source glm_env/bin/activate

# 运行测试
python test_glm_ocr.py
```

**模型位置**: `/Users/lifeng/data/models/GLM-OCR`

## 📊 模块对比

### OCR 模块对比

| 特性 | DeepSeek-OCR-2 | GLM-OCR |
|------|---------------|---------|
| **参数量** | 未知 | 0.9B |
| **加载时间** | 6秒 | **2.2秒** ⚡ |
| **推理速度** | **30秒/页** ⚡ | 82.8秒/页 |
| **准确率** | ⭐⭐⭐⭐ | **⭐⭐⭐⭐⭐** |
| **设备支持** | CPU (需修复) | CPU / GPU |
| **输出格式** | MD / TXT | MD / TXT |
| **安装难度** | ⚠️ 需要修复模型 | ✅ 简单 |
| **推荐场景** | 速度优先 | 准确率优先 |

### 推荐选择

- **速度优先**: DeepSeek-OCR-2（修复后）
- **准确率优先**: GLM-OCR（OmniDocBench V1.5 第一名）
- **生产环境**: GLM-OCR（更稳定）

## 📝 依赖管理

### 全局依赖 (requirements.txt)

适用于 ASR 和 TTS 模块：

```bash
pip install -r requirements.txt
```

### 独立环境依赖

每个 OCR 模块都有独立的 `requirements.txt`：

- `deepseek_ocr/requirements.txt` - DeepSeek-OCR-2 依赖
- `glm_ocr/requirements.txt` - GLM-OCR 依赖

## 🛠️ 安装指南

### 方案 1: 全局安装（ASR + TTS）

```bash
# 创建全局虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 方案 2: 独立安装（推荐用于 OCR）

**DeepSeek-OCR**:
```bash
cd deepseek_ocr
bash setup_env.sh
```

**GLM-OCR**:
```bash
cd glm_ocr
bash setup_env.sh
```

## 📖 详细文档

### DeepSeek-OCR-2

- [README.md](./deepseek_ocr/README.md) - 完整文档
- [INSTALL.md](./deepseek_ocr/INSTALL.md) - 安装指南
- [FIX_GUIDE.md](./deepseek_ocr/FIX_GUIDE.md) - 快速修复指南
- [TROUBLESHOOTING.md](./deepseek_ocr/TROUBLESHOOTING.md) - 故障排查
- [SUMMARY.md](./deepseek_ocr/SUMMARY.md) - CPU 修复总结

### GLM-OCR

- [README.md](./glm_ocr/README.md) - 完整文档

## ⚠️ 重要提示

### DeepSeek-OCR-2 CPU 修复

DeepSeek-OCR-2 官方模型存在 CPU 兼容性问题，需要手动修复：

```bash
# 自动修复（推荐）
bash fix_deepseek_ocr.sh

# 或查看详细修复步骤
cat deepseek_ocr/FIX_GUIDE.md
```

**修复内容**:
1. Flash Attention 2 兼容性
2. CUDA 硬编码问题
3. BFloat16 类型转换
4. Config 配置修正

### 版本冲突处理

如果遇到 `transformers` 版本冲突：

1. 使用独立虚拟环境（已配置）
2. 不要混用全局环境和独立环境
3. 激活正确的环境后再运行代码

## 🔗 参考链接

- [Fun-ASR-Nano](https://modelscope.cn/models/FunAudioLLM/Fun-ASR-Nano-2512)
- [Qwen3-TTS](https://modelscope.cn/models/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice)
- [DeepSeek-OCR-2](https://modelscope.cn/models/deepseek-ai/DeepSeek-OCR-2)
- [GLM-OCR](https://modelscope.cn/models/ZhipuAI/GLM-OCR)

## 📄 License

MIT License
