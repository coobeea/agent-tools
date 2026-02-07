#!/bin/bash
# DeepSeek-OCR-2 自动修复脚本

MODEL_PATH="${1:-/Users/lifeng/data/models/deepseek-ai/DeepSeek-OCR-2}"

echo "========================================="
echo "DeepSeek-OCR-2 自动修复工具"
echo "========================================="
echo ""
echo "目标模型: $MODEL_PATH"
echo ""

if [ ! -d "$MODEL_PATH" ]; then
    echo "❌ 错误: 模型目录不存在: $MODEL_PATH"
    exit 1
fi

cd "$MODEL_PATH" || exit 1

# 1. 修复 API 兼容性
echo "🔧 [1/4] 修复 transformers API 兼容性..."
if grep -q "LlamaFlashAttention2" modeling_deepseekv2.py 2>/dev/null; then
    sed -i '' 's/LlamaFlashAttention2/LlamaAttention/g' modeling_deepseekv2.py
    echo "   ✅ 已修复 LlamaFlashAttention2 → LlamaAttention"
else
    echo "   ⏭️  modeling_deepseekv2.py 已修复或不存在，跳过"
fi

if grep -q "\.cuda()" modeling_deepseekocr2.py 2>/dev/null; then
    sed -i '' 's/\.cuda()/.to(self.device)/g' modeling_deepseekocr2.py
    echo "   ✅ 已修复硬编码 .cuda() 调用"
else
    echo "   ⏭️  modeling_deepseekocr2.py 已修复或不存在，跳过"
fi

# 2. 修改 config.json
echo ""
echo "🔧 [2/4] 修改 config.json..."
if grep -q '"torch_dtype": "bfloat16"' config.json 2>/dev/null; then
    cp config.json config.json.bak
    sed -i '' 's/"torch_dtype": "bfloat16"/"torch_dtype": "float32"/g' config.json
    echo "   ✅ 已修改 torch_dtype: bfloat16 → float32"
    echo "   📦 备份已保存: config.json.bak"
else
    echo "   ⏭️  config.json 已修复，跳过"
fi

# 3. 修复 deepencoderv2.py
echo ""
echo "🔧 [3/4] 修复 deepencoderv2.py 数据类型匹配..."
if [ -f "deepencoderv2.py" ]; then
    if ! grep -q "if x.dtype != self.proj.weight.dtype:" deepencoderv2.py; then
        # 找到正确的插入位置（def forward 之后的第一行）
        sed -i '' '/def forward(self, x: torch.Tensor) -> torch.Tensor:/a\
        # 强制转换输入为与权重相同的 dtype\
        if x.dtype != self.proj.weight.dtype:\
            x = x.to(self.proj.weight.dtype)
' deepencoderv2.py
        echo "   ✅ 已添加类型转换补丁到 PatchEmbed.forward()"
    else
        echo "   ⏭️  deepencoderv2.py 已包含修复，跳过"
    fi
else
    echo "   ⚠️  deepencoderv2.py 不存在，跳过"
fi

# 4. 清除缓存
echo ""
echo "🔧 [4/4] 清除 transformers 缓存..."
CACHE_DIR="$HOME/.cache/huggingface/modules/transformers_modules/DeepSeek-OCR-2"
if [ -d "$CACHE_DIR" ]; then
    rm -rf "$CACHE_DIR"
    echo "   ✅ 已清除缓存: $CACHE_DIR"
else
    echo "   ⏭️  缓存已清除或不存在，跳过"
fi

echo ""
echo "========================================="
echo "✅ 修复完成！"
echo "========================================="
echo ""
echo "📌 下一步操作:"
echo "  1. 确保安装正确版本: pip install transformers==4.46.3"
echo "  2. 运行测试验证:      python test_ocr_result.py"
echo ""
