# 环境管理指南

Agent Tools 项目环境配置总览。

## 📦 环境架构

```
agent-tools/
├── .venv/                    # 全局环境 (ASR + TTS)
├── deepseek_ocr/
│   ├── deepseek_env/        # DeepSeek-OCR 独立环境
│   ├── requirements.txt     # DeepSeek-OCR 依赖清单
│   └── setup_env.sh         # 一键安装脚本
├── glm_ocr/
│   ├── glm_env/             # GLM-OCR 独立环境
│   ├── requirements.txt     # GLM-OCR 依赖清单
│   └── setup_env.sh         # 一键安装脚本
└── requirements.txt          # 全局依赖清单
```

## 🔧 环境配置表

| 模块 | 虚拟环境 | 依赖文件 | 安装脚本 | transformers 版本 |
|------|---------|---------|---------|------------------|
| **ASR** | 全局 `.venv` | `requirements.txt` | 手动安装 | >= 4.40.0 |
| **TTS** | 全局 `.venv` | `requirements.txt` | 手动安装 | >= 4.57.3 |
| **DeepSeek-OCR** | `deepseek_env` | `deepseek_ocr/requirements.txt` | `setup_env.sh` | == 4.46.3 |
| **GLM-OCR** | `glm_env` | `glm_ocr/requirements.txt` | `setup_env.sh` | >= 5.0.0 (dev) |

## 🚀 快速安装

### 方案 1: 全局环境 (ASR + TTS)

```bash
# 在项目根目录
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 方案 2: DeepSeek-OCR 独立环境

```bash
cd deepseek_ocr
bash setup_env.sh
```

### 方案 3: GLM-OCR 独立环境

```bash
cd glm_ocr
bash setup_env.sh
```

## 📋 依赖清单详情

### 全局依赖 (`requirements.txt`)

适用模块: **ASR + TTS**

```text
# 基础依赖
torch>=2.0.0
torchaudio>=2.0.0
transformers>=4.40.0
soundfile
numpy

# ASR 依赖
funasr>=1.3.0
zhconv
openai-whisper

# TTS 依赖
qwen-tts>=0.0.5
modelscope

# OCR 基础依赖（可选）
pdf2image
pillow
addict
easydict
matplotlib
torchvision
timm
```

### DeepSeek-OCR 依赖 (`deepseek_ocr/requirements.txt`)

```text
torch>=2.0.0
torchvision>=0.15.0
torchaudio>=2.0.0
transformers==4.46.3      # 固定版本！
pillow>=9.0.0
pdf2image>=1.16.0
modelscope>=1.9.0
numpy>=1.21.0
```

### GLM-OCR 依赖 (`glm_ocr/requirements.txt`)

```text
torch>=2.0.0
torchvision>=0.15.0
torchaudio>=2.0.0
transformers>=5.0.0       # 需要开发版
accelerate>=0.20.0        # 必需
pillow>=9.0.0
numpy>=1.21.0
```

## ⚙️ 使用方法

### ASR 语音识别

```bash
# 激活全局环境
source .venv/bin/activate

# 运行示例
cd asr
python examples/demo_basic.py
```

### TTS 语音合成

```bash
# 激活全局环境
source .venv/bin/activate

# 运行示例
cd tts
python examples/demo_basic.py
```

### DeepSeek-OCR

```bash
# 激活 DeepSeek-OCR 环境
cd deepseek_ocr
source deepseek_env/bin/activate

# 运行示例
python examples/demo_basic.py
```

### GLM-OCR

```bash
# 激活 GLM-OCR 环境
cd glm_ocr
source glm_env/bin/activate

# 运行测试
python test_glm_ocr.py
```

## ⚠️ 版本冲突说明

### 为什么需要独立环境？

**transformers 版本冲突**:

| 模块 | 版本要求 | 原因 |
|------|---------|------|
| TTS | >= 4.57.3 | 需要新版 API |
| DeepSeek-OCR | == 4.46.3 | 模型在此版本训练 |
| GLM-OCR | >= 5.0.0 | 需要最新特性 |

**解决方案**:
- ✅ ASR + TTS 共享全局环境（版本兼容）
- ✅ DeepSeek-OCR 使用 `deepseek_env`（固定 4.46.3）
- ✅ GLM-OCR 使用 `glm_env`（开发版）

### 常见错误

❌ **错误做法**:
```bash
# 在全局环境安装 OCR 模块
source .venv/bin/activate
pip install transformers==4.46.3  # 会破坏 TTS！
```

✅ **正确做法**:
```bash
# 使用独立环境
cd deepseek_ocr
bash setup_env.sh
source deepseek_env/bin/activate
```

## 🧹 环境清理

### 清理所有虚拟环境

```bash
# 在项目根目录
rm -rf .venv
rm -rf deepseek_ocr/deepseek_env
rm -rf glm_ocr/glm_env
```

### 重新安装

```bash
# 全局环境
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# DeepSeek-OCR
cd deepseek_ocr && bash setup_env.sh && cd ..

# GLM-OCR
cd glm_ocr && bash setup_env.sh && cd ..
```

## 📊 磁盘空间占用

| 环境 | 大小（估算） |
|------|------------|
| 全局 `.venv` | ~2GB |
| `deepseek_env` | ~2GB |
| `glm_env` | ~2GB |
| **总计** | **~6GB** |

## 🔍 环境检查

### 检查当前激活的环境

```bash
which python
# /Users/lifeng/git/git_agents/agent-tools/.venv/bin/python           # 全局
# /Users/lifeng/git/git_agents/agent-tools/deepseek_ocr/deepseek_env/bin/python  # DeepSeek
# /Users/lifeng/git/git_agents/agent-tools/glm_ocr/glm_env/bin/python           # GLM
```

### 检查 transformers 版本

```bash
python -c "import transformers; print(transformers.__version__)"
```

### 检查依赖完整性

```bash
# 全局环境
source .venv/bin/activate
pip list | grep -E "torch|transformers|funasr|qwen"

# DeepSeek-OCR 环境
source deepseek_ocr/deepseek_env/bin/activate
pip list | grep -E "torch|transformers|pillow"

# GLM-OCR 环境
source glm_ocr/glm_env/bin/activate
pip list | grep -E "torch|transformers|accelerate"
```

## 📚 相关文档

- [README.md](./README.md) - 项目总览
- [deepseek_ocr/INSTALL.md](./deepseek_ocr/INSTALL.md) - DeepSeek-OCR 详细安装
- [deepseek_ocr/FIX_GUIDE.md](./deepseek_ocr/FIX_GUIDE.md) - DeepSeek-OCR 修复指南
- [glm_ocr/README.md](./glm_ocr/README.md) - GLM-OCR 使用文档

## 💡 最佳实践

1. **始终检查当前环境**: 运行代码前确认激活了正确的虚拟环境
2. **不要混用环境**: 不要在全局环境安装 OCR 模块的依赖
3. **使用安装脚本**: 优先使用 `setup_env.sh` 自动配置环境
4. **定期更新**: 定期运行 `pip install --upgrade` 更新依赖（但保持 transformers 版本）
5. **记录版本**: 如果修改了依赖，更新 `requirements.txt`

## 🆘 故障排查

### 问题 1: 找不到模块

**症状**: `ModuleNotFoundError: No module named 'xxx'`

**解决**:
```bash
# 1. 确认已激活正确环境
which python

# 2. 重新安装依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题 2: transformers 版本错误

**症状**: `ImportError: cannot import name 'xxx' from 'transformers'`

**解决**:
```bash
# 检查版本
python -c "import transformers; print(transformers.__version__)"

# DeepSeek-OCR: 必须是 4.46.3
# GLM-OCR: 必须是 5.x (dev)
```

### 问题 3: 环境混乱

**症状**: 各种奇怪的版本冲突

**解决**: 清理并重装所有环境
```bash
cd /Users/lifeng/git/git_agents/agent-tools
rm -rf .venv deepseek_ocr/deepseek_env glm_ocr/glm_env

# 重新安装...
```

## 📝 更新记录

- 2026-01-30: 创建独立环境配置
- 之前: 使用全局环境（已废弃）
