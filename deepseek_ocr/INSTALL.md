# DeepSeek-OCR-2 安装指南

## 快速开始

### 1. 创建独立虚拟环境

```bash
cd /Users/lifeng/git/git_agents/agent-tools/deepseek_ocr

# 使用自动安装脚本（推荐）
bash setup_env.sh
```

### 2. 手动安装（可选）

如果需要手动安装：

```bash
# 1. 创建虚拟环境
python3 -m venv deepseek_env

# 2. 激活环境
source deepseek_env/bin/activate

# 3. 升级 pip
pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

# 4. 安装依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 修复模型文件（重要！）

DeepSeek-OCR-2 模型需要手动修复才能在 CPU 上运行：

```bash
cd /Users/lifeng/data/models/deepseek-ai/DeepSeek-OCR-2

# 方法1: 使用自动修复脚本（推荐）
bash /Users/lifeng/git/git_agents/agent-tools/fix_deepseek_ocr.sh

# 方法2: 手动执行修复命令
# 1. 修复 Flash Attention 兼容性
sed -i '' 's/LlamaFlashAttention2/LlamaAttention/g' modeling_deepseekv2.py

# 2. 修复 CUDA 硬编码
sed -i '' 's/\.cuda()/.to(self.device)/g' modeling_deepseekocr2.py

# 3. 修复 config.json 数据类型
sed -i '' 's/"torch_dtype": "bfloat16"/"torch_dtype": "float32"/g' config.json

# 4. 清除缓存
rm -rf ~/.cache/huggingface/modules/transformers_modules/DeepSeek-OCR-2
```

**关键修复（手动）**:

如果自动脚本未能修复 `deepencoderv2.py`，需要手动编辑：

打开 `/Users/lifeng/data/models/deepseek-ai/DeepSeek-OCR-2/deepencoderv2.py`

找到 `PatchEmbed` 类的 `forward` 方法（约 956 行），在 `x = self.proj(x)` 之前添加：

```python
def forward(self, x: torch.Tensor) -> torch.Tensor:
    # 添加这两行
    if x.dtype != self.proj.weight.dtype:
        x = x.to(self.proj.weight.dtype)
    
    x = self.proj(x)
    x = x.permute(0, 2, 3, 1)
    return x
```

### 4. 测试安装

```bash
# 激活环境
source deepseek_env/bin/activate

# 运行基础示例
python examples/demo_basic.py
```

## 依赖说明

### requirements.txt

```
torch>=2.0.0
torchvision>=0.15.0
torchaudio>=2.0.0
transformers==4.46.3  # 重要: 固定版本
pillow>=9.0.0
pdf2image>=1.16.0
modelscope>=1.9.0
numpy>=1.21.0
```

### 版本要求

- **Python**: 3.8+
- **transformers**: 必须使用 `4.46.3`（不要升级！）
- **PyTorch**: 2.0.0+
- **系统**: macOS / Linux / Windows

### 版本冲突说明

⚠️ **重要**: DeepSeek-OCR-2 和 TTS 模块使用不同的 transformers 版本：

- DeepSeek-OCR-2: `transformers==4.46.3`
- TTS: `transformers>=4.57.3`

**解决方案**: 使用独立虚拟环境（已配置）

## 设备支持

### CPU（推荐）
- ✅ 已完全测试
- ✅ 推理速度: ~30秒/页
- ✅ 内存需求: ~4GB

### CUDA GPU
- ✅ 支持（需修复模型文件）
- ⚡ 推理速度: ~5-10秒/页
- 💾 显存需求: ~6GB

### MPS (Apple Silicon)
- ⚠️ 官方模型存在兼容性问题
- 建议使用 CPU 模式

## 常见问题

### 1. `RuntimeError: Input type (c10::BFloat16) and bias type (float) should be the same`

**原因**: 模型文件未修复

**解决**: 按照"步骤3"修复模型文件，特别是 `deepencoderv2.py`

### 2. `ImportError: cannot import name 'LlamaFlashAttention2'`

**原因**: transformers 版本不兼容

**解决**: 
```bash
pip install transformers==4.46.3
sed -i '' 's/LlamaFlashAttention2/LlamaAttention/g' /Users/lifeng/data/models/deepseek-ai/DeepSeek-OCR-2/modeling_deepseekv2.py
```

### 3. 推理速度慢

**原因**: CPU 推理本身较慢

**优化**:
- 使用 GPU（如果有）
- 减小图片分辨率
- 使用 `crop_mode=False`（默认）

## 参考文档

- [FIX_GUIDE.md](./FIX_GUIDE.md) - 快速修复指南
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) - 详细故障排查
- [SUMMARY.md](./SUMMARY.md) - CPU 兼容性修复总结
- [README.md](./README.md) - 完整文档
