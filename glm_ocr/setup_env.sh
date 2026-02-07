#!/bin/bash
# GLM-OCR 环境安装脚本

set -e

echo "=================================="
echo "GLM-OCR 环境配置"
echo "=================================="
echo ""

# 检查虚拟环境
if [ ! -d "glm_env" ]; then
    echo "⏳ 创建虚拟环境..."
    python3 -m venv glm_env
    echo "✅ 虚拟环境创建完成"
fi

# 激活虚拟环境
echo ""
echo "⏳ 激活虚拟环境..."
source glm_env/bin/activate

# 升级 pip
echo ""
echo "⏳ 升级 pip..."
pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

# 安装基础依赖
echo ""
echo "⏳ 安装基础依赖（使用清华镜像）..."
pip install torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install accelerate pillow numpy -i https://pypi.tuna.tsinghua.edu.cn/simple

# 安装 transformers 最新开发版（GLM-OCR 必需）
echo ""
echo "⏳ 安装 transformers 最新开发版..."
echo "   (GLM-OCR 需要最新的 transformers，从 GitHub 安装)"
pip install git+https://github.com/huggingface/transformers.git

echo ""
echo "=================================="
echo "✅ 环境安装完成！"
echo "=================================="
echo ""
echo "模型信息："
echo "  模型路径: /Users/lifeng/data/models/GLM-OCR"
echo "  参数量: 0.9B"
echo "  支持设备: CPU / CUDA GPU"
echo ""
echo "使用方法："
echo "  source glm_env/bin/activate"
echo "  python test_glm_ocr.py"
echo ""
echo "高级用法："
echo "  # 指定图片"
echo "  python test_glm_ocr.py --image /path/to/image.png"
echo ""
echo "  # 指定任务类型"
echo "  python test_glm_ocr.py --task formula  # text | formula | table"
echo ""
