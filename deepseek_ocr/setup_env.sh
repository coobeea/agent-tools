#!/bin/bash
# DeepSeek-OCR-2 环境安装脚本

set -e

echo "=================================="
echo "DeepSeek-OCR-2 环境配置"
echo "=================================="
echo ""

# 检查虚拟环境
if [ ! -d "deepseek_env" ]; then
    echo "⏳ 创建虚拟环境..."
    python3 -m venv deepseek_env
    echo "✅ 虚拟环境创建完成"
fi

# 激活虚拟环境
echo ""
echo "⏳ 激活虚拟环境..."
source deepseek_env/bin/activate

# 升级 pip
echo ""
echo "⏳ 升级 pip..."
pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

# 安装依赖
echo ""
echo "⏳ 安装依赖（使用清华镜像）..."
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo ""
echo "=================================="
echo "✅ 环境安装完成！"
echo "=================================="
echo ""
echo "⚠️  重要: 需要手动修复模型文件"
echo ""
echo "如果模型位于: /Users/lifeng/data/models/deepseek-ai/DeepSeek-OCR-2"
echo "请运行以下命令修复兼容性:"
echo ""
echo "  cd /Users/lifeng/data/models/deepseek-ai/DeepSeek-OCR-2"
echo ""
echo "  # 1. 修复 Flash Attention 兼容性"
echo "  sed -i '' 's/LlamaFlashAttention2/LlamaAttention/g' modeling_deepseekv2.py"
echo ""
echo "  # 2. 修复 CUDA 硬编码"
echo "  sed -i '' 's/\\.cuda()/.to(self.device)/g' modeling_deepseekocr2.py"
echo ""
echo "  # 3. 修复 config.json 数据类型"
echo "  sed -i '' 's/\"torch_dtype\": \"bfloat16\"/\"torch_dtype\": \"float32\"/g' config.json"
echo ""
echo "  # 4. 修复 deepencoderv2.py 类型转换"
echo "  # 在 PatchEmbed.forward() 方法中的 x = self.proj(x) 之前添加:"
echo "  # if x.dtype != self.proj.weight.dtype:"
echo "  #     x = x.to(self.proj.weight.dtype)"
echo ""
echo "  # 5. 清除缓存"
echo "  rm -rf ~/.cache/huggingface/modules/transformers_modules/DeepSeek-OCR-2"
echo ""
echo "或者使用自动修复脚本:"
echo "  bash ../fix_deepseek_ocr.sh"
echo ""
echo "使用方法："
echo "  source deepseek_env/bin/activate"
echo "  python examples/demo_basic.py"
echo ""
