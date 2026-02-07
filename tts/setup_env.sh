#!/bin/bash
#
# TTS 独立环境安装脚本
#
# 用法:
#   bash setup_env.sh
#   或
#   ./setup_env.sh

set -e  # 遇到错误立即退出

# 脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "========================================"
echo "TTS 独立环境安装"
echo "========================================"
echo ""

# 1. 创建虚拟环境
echo "⏳ [1/4] 创建虚拟环境..."
if [ -d "tts_env" ]; then
    echo "⚠️  虚拟环境已存在，将删除并重新创建"
    rm -rf tts_env
fi

python3 -m venv tts_env
echo "✅ 虚拟环境创建成功"
echo ""

# 2. 激活虚拟环境
echo "⏳ [2/4] 激活虚拟环境..."
source tts_env/bin/activate
python --version
echo "✅ 虚拟环境激活成功"
echo ""

# 3. 升级 pip
echo "⏳ [3/4] 升级 pip..."
pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
echo "✅ pip 升级完成"
echo ""

# 4. 安装依赖
echo "⏳ [4/4] 安装依赖包..."
echo "   使用清华镜像源加速..."

# 先安装 PyTorch
pip install torch torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple

# 再安装其他依赖
pip install transformers soundfile librosa numpy scipy -i https://pypi.tuna.tsinghua.edu.cn/simple

# 安装 qwen-tts
pip install qwen-tts -i https://pypi.tuna.tsinghua.edu.cn/simple

echo "✅ 所有依赖安装完成"
echo ""

# 5. 验证安装
echo "========================================"
echo "验证安装"
echo "========================================"
python << 'EOF'
import sys
print(f"Python 版本: {sys.version}")

import torch
print(f"PyTorch 版本: {torch.__version__}")

import transformers
print(f"Transformers 版本: {transformers.__version__}")

import soundfile
print(f"SoundFile 版本: {soundfile.__version__}")

try:
    import qwen_tts
    print(f"Qwen-TTS: 已安装")
except ImportError:
    print(f"Qwen-TTS: 未安装（可选）")

print("\n✅ 所有核心依赖验证通过")
EOF

echo ""
echo "========================================"
echo "✅ TTS 环境安装完成！"
echo "========================================"
echo ""
echo "使用方法:"
echo "  source tts_env/bin/activate"
echo "  python examples/demo_basic.py"
echo ""
