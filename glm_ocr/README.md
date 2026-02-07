# GLM-OCR 测试项目

基于智谱 GLM-OCR 模型的 OCR 测试环境。

## 模型信息

- **模型**: GLM-OCR (0.9B 参数)
- **开发者**: ZhipuAI
- **本地路径**: `/Users/lifeng/data/models/GLM-OCR`
- **参考**: https://www.modelscope.cn/models/ZhipuAI/GLM-OCR

## 特性

- ✅ 多模态 OCR 模型
- ✅ 支持文本、公式、表格识别
- ✅ 支持信息提取（JSON 格式）
- ✅ 0.9B 参数，推理速度快
- ✅ OmniDocBench V1.5 排名第一（94.62 分）

## 环境要求

- Python 3.8+
- transformers (最新开发版)
- torch
- Pillow

## 安装

```bash
# 1. 创建虚拟环境
cd /Users/lifeng/git/git_agents/agent-tools/glm_ocr
python3 -m venv glm_env

# 2. 激活环境
source glm_env/bin/activate

# 3. 安装依赖
bash setup_env.sh
```

## 快速开始

### Python API

```python
from transformers import AutoProcessor, AutoModelForImageTextToText
import torch

MODEL_PATH = "/Users/lifeng/data/models/GLM-OCR"

# 加载模型
processor = AutoProcessor.from_pretrained(MODEL_PATH)
model = AutoModelForImageTextToText.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float32,  # CPU 使用 float32
    device_map="cpu"
)

# 准备输入
messages = [{
    "role": "user",
    "content": [
        {"type": "image", "url": "test.png"},
        {"type": "text", "text": "Text Recognition:"}
    ]
}]

# 推理
inputs = processor.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_dict=True,
    return_tensors="pt"
).to(model.device)

inputs.pop("token_type_ids", None)
generated_ids = model.generate(**inputs, max_new_tokens=8192)
output_text = processor.decode(
    generated_ids[0][inputs["input_ids"].shape[1]:],
    skip_special_tokens=False
)
print(output_text)
```

### 命令行测试

```bash
# 基础 OCR
python test_glm_ocr.py

# 指定图片
python test_glm_ocr.py --image /path/to/image.png

# 指定任务类型
python test_glm_ocr.py --task formula  # text | formula | table
```

## 支持的任务

### 1. 文档解析

- **Text Recognition** - 文本识别
  ```python
  prompt = "Text Recognition:"
  ```

- **Formula Recognition** - 公式识别
  ```python
  prompt = "Formula Recognition:"
  ```

- **Table Recognition** - 表格识别
  ```python
  prompt = "Table Recognition:"
  ```

### 2. 信息提取

使用 JSON 格式定义提取的结构：

```python
prompt = """请按下列JSON格式输出图中信息:
{
    "field1": "",
    "field2": ""
}"""
```

## 性能

- **速度**: 1.86 页/秒 (PDF), 0.67 张/秒 (图片)
- **准确率**: OmniDocBench V1.5 第一名（94.62）
- **参数量**: 0.9B（小巧高效）

## 对比其他模型

| 模型 | 参数量 | 加载时间 | 推理速度 | 准确率 |
|------|--------|---------|---------|--------|
| GLM-OCR | 0.9B | ? | ? | ⭐⭐⭐⭐⭐ |
| DeepSeek-OCR-2 | 未知 | 6秒 | 30秒/页 | ⭐⭐⭐⭐ |
| PaddleOCR-VL-1.5 | 0.9B | >2.5分钟 | 未知 | ⭐⭐⭐⭐ |

## 参考

- [ModelScope 模型主页](https://www.modelscope.cn/models/ZhipuAI/GLM-OCR)
- [GitHub SDK](https://github.com/zai-org/GLM-OCR)
- [官方文档](https://docs.z.ai/guides/vlm/glm-ocr)

## License

MIT License
