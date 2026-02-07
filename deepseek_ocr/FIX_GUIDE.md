# DeepSeek-OCR-2 CPU 修复指南

## 问题

DeepSeek-OCR-2 在 CPU 上运行时会遇到数据类型不匹配错误：
```
RuntimeError: Input type (c10::BFloat16) and bias type (float) should be the same
```

## 根本原因

1. 模型权重文件（safetensors）以 **bfloat16** 格式保存
2. config.json 中配置的 `torch_dtype` 为 `"bfloat16"`  
3. deepencoderv2.py 中的 patch_embed 层输入数据为 bfloat16，但 bias 为 float32

## 完整修复步骤

### 1. 修复 transformers API 兼容性

```bash
cd /Users/lifeng/data/models/deepseek-ai/DeepSeek-OCR-2

# 修复 LlamaFlashAttention2 → LlamaAttention
sed -i '' 's/LlamaFlashAttention2/LlamaAttention/g' modeling_deepseekv2.py

# 修复硬编码 CUDA → 设备无关
sed -i '' 's/\.cuda()/.to(self.device)/g' modeling_deepseekocr2.py
```

### 2. 修改 config.json

```bash
# 将 torch_dtype 从 bfloat16 改为 float32
sed -i '' 's/"torch_dtype": "bfloat16"/"torch_dtype": "float32"/g' config.json
```

### 3. 修复 deepencoderv2.py 的数据类型匹配

在 `deepencoderv2.py` 的 `PatchEmbed` 类的 `forward` 方法中（约第956行）添加类型转换：

```python
def forward(self, x: torch.Tensor) -> torch.Tensor:
    # 强制转换输入为与权重相同的 dtype
    if x.dtype != self.proj.weight.dtype:
        x = x.to(self.proj.weight.dtype)
    x = self.proj(x)
    # B C H W -> B H W C
    x = x.permute(0, 2, 3, 1)
    return x
```

### 4. 清除缓存

```bash
rm -rf ~/.cache/huggingface/modules/transformers_modules/DeepSeek-OCR-2
```

### 5. 安装正确的 transformers 版本

```bash
pip install transformers==4.46.3
```

**注意**: 这会与 qwen-tts 的 transformers==4.57.3 冲突，建议创建独立环境。

## 验证

修复后可以正常在 CPU 上运行：

```python
from transformers import AutoModel, AutoTokenizer
import torch

MODEL_PATH = '/Users/lifeng/data/models/deepseek-ai/DeepSeek-OCR-2'

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
model = AutoModel.from_pretrained(
    MODEL_PATH,
    trust_remote_code=True,
    torch_dtype=torch.float32,
)
model = model.eval().to('cpu')

result = model.infer(
    tokenizer=tokenizer,
    prompt='<<image>>\n<<|grounding|>>Convert the document to markdown.',
    image_file='document.png',
    output_path='/tmp/ocr_output',
    base_size=1024,
    image_size=1024,
    crop_mode=False,
    eval_mode=True,
)
print(result)
```

## 性能

在 Apple M2 Max (CPU) 上：
- 单页文档识别：约 50-60 秒
- 精确识别表格、文字、布局结构
- 支持 Markdown 格式输出

## 参考

修复参考自：/Users/lifeng/git/git_skills/deepseekocrGradio
