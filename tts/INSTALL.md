# TTS 独立环境安装指南

## 🎯 为什么需要独立环境

TTS 使用 `transformers>=4.57.3`，而 DeepSeek-OCR 需要 `transformers==4.46.3`，两者不兼容，因此需要独立的虚拟环境。

## 📦 安装步骤

### 1. 创建独立环境

```bash
cd /Users/lifeng/git/git_agents/agent-tools/tts
bash setup_env.sh
```

这会：
- 创建 `tts_env` 虚拟环境
- 安装 PyTorch, Transformers, SoundFile 等
- 安装 qwen-tts 库

### 2. 验证安装

```bash
source tts_env/bin/activate
python -c "import torch; import transformers; print('✅ 安装成功')"
```

## 🚀 快速使用

安装完成后，直接调用脚本即可（不需要手动激活环境）：

```bash
/Users/lifeng/git/git_agents/agent-tools/tts/tts_speak.sh "你好，世界！" output.wav
```

## 📝 依赖说明

- **PyTorch**: 深度学习框架
- **Transformers >= 4.57.3**: Qwen3-TTS 需要较新版本
- **SoundFile**: 音频文件读写
- **Librosa**: 音频处理（可选）
- **qwen-tts**: Qwen3-TTS 核心库

## ⚠️ 注意事项

1. **不要与 OCR 环境混用**：TTS 和 DeepSeek-OCR 的 transformers 版本冲突
2. **使用独立脚本**：通过 `tts_speak.sh` 调用，会自动使用正确的环境
3. **首次下载模型**：首次运行会下载约 3-4GB 的模型文件

## 🔧 故障排查

### 问题：环境安装失败

```bash
# 删除并重新安装
cd /Users/lifeng/git/git_agents/agent-tools/tts
rm -rf tts_env
bash setup_env.sh
```

### 问题：找不到 qwen-tts

```bash
source tts_env/bin/activate
pip install qwen-tts -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## ✅ 完成

安装完成后，参考 `使用说明.txt` 开始使用！
