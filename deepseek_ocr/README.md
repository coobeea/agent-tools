# DeepSeek-OCR 光学字符识别库

基于 [DeepSeek-OCR](https://modelscope.cn/models/deepseek-ai/DeepSeek-OCR) 的高级封装，提供简单易用的 OCR 识别功能。

## 特性

- ✅ **图像 OCR**: 支持各种图像格式的文字识别
- ✅ **PDF 识别**: 支持 PDF 文档的文字提取
- ✅ **文档转 Markdown**: 将文档图像转换为结构化 Markdown
- ✅ **图表解析**: 解析图表、表格等复杂结构
- ✅ **批量处理**: 支持批量图像识别
- ✅ **多种输出格式**: 支持 Markdown、纯文本、结构化输出（见 [FORMAT_GUIDE.md](./FORMAT_GUIDE.md)）
- ✅ **5 种识别模式**: markdown、ocr、free_ocr、parse_figure、describe
- ✅ **输出格式化工具**: 自动清理标注标签，生成纯净输出
- ✅ **多种分辨率模式**: Tiny/Small/Base/Large 四种模式
- ✅ **自定义提示词**: 灵活的提示词控制
- ✅ **GPU 加速**: 支持 CUDA/MPS 加速
- ✅ **Flash Attention 2**: 支持高效注意力机制

## 环境要求

- Python 3.12+
- PyTorch 2.6.0+
- **Transformers 4.46.3**（重要：TTS 模块需要 4.57.3，存在版本冲突）
- CPU/CUDA GPU（已修复 MPS 兼容性）
- 至少 16GB RAM

### ⚠️ 重要说明

**transformers 版本冲突**:
- DeepSeek-OCR-2 需要 `transformers==4.46.3`
- TTS 模块需要 `transformers==4.57.3`
- 建议为 OCR 创建独立的虚拟环境

**设备支持**:
- ✅ CPU（已测试，推荐）
- ✅ CUDA GPU（需修复模型文件中的硬编码）
- ⚠️ MPS（Apple Silicon）：官方模型存在兼容性问题

### 快速修复（已下载模型）

如果您已下载 DeepSeek-OCR-2 到 `/Users/lifeng/data/models/deepseek-ai/DeepSeek-OCR-2`：

```bash
cd /Users/lifeng/data/models/deepseek-ai/DeepSeek-OCR-2

# 修复 LlamaFlashAttention2 兼容性
sed -i '' 's/LlamaFlashAttention2/LlamaAttention/g' modeling_deepseekv2.py

# 修复硬编码 CUDA（如需 CPU/MPS 支持）
sed -i '' 's/\.cuda()/.to(self.device)/g' modeling_deepseekocr2.py

# 清除缓存
rm -rf ~/.cache/huggingface/modules/transformers_modules/DeepSeek_hyphen_OCR_hyphen_2
```

### 推荐的替代方案

由于兼容性问题，推荐使用以下成熟的 OCR 方案：
- **PaddleOCR**: 完善的跨平台 OCR 库，支持多语言
- **EasyOCR**: 支持 80+ 语言的 OCR
- **Tesseract OCR**: 开源 OCR 引擎
- **Azure Computer Vision**: 云端 OCR API

## 安装

### 1. 安装依赖

```bash
# 激活虚拟环境
source .venv/bin/activate

# 安装 PyTorch（根据系统选择）
# macOS (MPS)
pip install torch torchvision torchaudio

# Linux (CUDA 11.8)
pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu118

# 安装其他依赖
pip install transformers>=4.51.1 modelscope pdf2image pillow
```

### 2. 可选：安装 Flash Attention 2（提升性能）

```bash
pip install flash-attn==2.7.3 --no-build-isolation
```

## 支持的分辨率模式

| 模式 | 尺寸 | 视觉 Tokens | 适用场景 |
|------|------|-------------|----------|
| Tiny | 512×512 | 64 | 低分辨率图像 |
| Small | 640×640 | 100 | 一般图像 |
| Base | 1024×1024 | 256 | 标准文档（默认）|
| Large | 1280×1280 | 400 | 高清文档 |

## 支持的提示词类型

| 类型 | 描述 | 提示词 |
|------|------|--------|
| markdown | 转换为 Markdown | `<<image>>\n<<\|grounding\|>>Convert the document to markdown.` |
| ocr | 普通 OCR | `<<image>>\n<<\|grounding\|>>OCR this image.` |
| free_ocr | 无布局 OCR | `<<image>>\nFree OCR.` |
| parse_figure | 图表解析 | `<<image>>\nParse the figure.` |
| describe | 详细描述 | `<<image>>\nDescribe this image in detail.` |

## 快速开始

### 基本使用

```python
from ocr import DeepSeekOCR

# 初始化（首次运行会自动下载模型）
ocr = DeepSeekOCR()

# 识别图像
result = ocr.recognize("document.jpg")
print(result)
```

### 文档转 Markdown

```python
from ocr import DeepSeekOCR

ocr = DeepSeekOCR()

# 将文档图像转换为 Markdown
result = ocr.recognize(
    "document.jpg",
    prompt_type="markdown",
    output_path="output/",
)
print(result)
```

### 识别 PDF 文档

```python
from ocr import DeepSeekOCR

ocr = DeepSeekOCR()

# 识别 PDF 每一页
results = ocr.recognize_pdf(
    "document.pdf",
    prompt_type="markdown",
    output_dir="output/",
)

# 输出每页结果
for i, result in enumerate(results):
    print(f"第 {i+1} 页:\n{result}\n")
```

### 批量识别

```python
from ocr import DeepSeekOCR

ocr = DeepSeekOCR()

# 批量识别多张图像
images = ["img1.jpg", "img2.jpg", "img3.jpg"]
results = ocr.batch_recognize(images, prompt_type="ocr")

for img, result in zip(images, results):
    print(f"{img}: {result}")
```

### 解析图表

```python
from ocr import DeepSeekOCR

ocr = DeepSeekOCR()

# 解析图表
result = ocr.recognize(
    "chart.jpg",
    prompt_type="parse_figure",
)
print(result)
```

### 自定义提示词

```python
from ocr import DeepSeekOCR

ocr = DeepSeekOCR()

# 使用自定义提示词
custom_prompt = "<<image>>\nExtract all table data from this image."
result = ocr.recognize("table.jpg", prompt=custom_prompt)
print(result)
```

### 快捷函数

```python
from ocr import recognize, recognize_pdf

# 快速识别单张图像
result = recognize("image.jpg", prompt_type="markdown")

# 快速识别 PDF
results = recognize_pdf("document.pdf", prompt_type="ocr")
```

## API 参考

### DeepSeekOCR 类

```python
DeepSeekOCR(
    model_name: str = "deepseek-ai/DeepSeek-OCR",
    model_dir: str = "/Users/lifeng/data/models",
    device: Optional[str] = None,  # 自动检测 'cuda', 'mps', 'cpu'
    base_size: int = 1024,
    image_size: int = 640,
    crop_mode: bool = True,
    use_flash_attention: bool = True,
    hub: str = "modelscope",  # 'modelscope' 或 'huggingface'
)
```

### 主要方法

#### recognize()

识别单张图像。

```python
recognize(
    image_path: str,
    prompt: Optional[str] = None,
    prompt_type: str = "markdown",
    output_path: Optional[str] = None,
    save_results: bool = True,
    test_compress: bool = True,
) -> str
```

#### recognize_pdf()

识别 PDF 文档。

```python
recognize_pdf(
    pdf_path: str,
    prompt: Optional[str] = None,
    prompt_type: str = "markdown",
    output_dir: Optional[str] = None,
    save_results: bool = True,
) -> List[str]
```

#### batch_recognize()

批量识别图像。

```python
batch_recognize(
    image_paths: List[str],
    prompt: Optional[str] = None,
    prompt_type: str = "markdown",
    output_dir: Optional[str] = None,
) -> List[str]
```

## 模型存储

模型默认下载到 `/Users/lifeng/data/models` 目录：

```
/Users/lifeng/data/models/
└── deepseek-ai/
    └── DeepSeek-OCR/
        ├── config.json
        ├── model.safetensors
        ├── tokenizer.json
        └── ...
```

## 性能优化

### 1. 使用 GPU 加速

```python
# CUDA
ocr = DeepSeekOCR(device="cuda")

# MPS (Apple Silicon)
ocr = DeepSeekOCR(device="mps")
```

### 2. 启用 Flash Attention 2

```python
ocr = DeepSeekOCR(use_flash_attention=True)
```

### 3. 调整分辨率模式

```python
# 低分辨率快速识别
ocr = DeepSeekOCR(base_size=640, image_size=512)

# 高分辨率精确识别
ocr = DeepSeekOCR(base_size=1280, image_size=1024)
```

## 示例

查看 `ocr/examples/` 目录获取更多示例：

- `demo_basic.py`: 基础使用示例

## 性能指标

在 Apple M2 Max (38-core GPU, 64GB RAM) 上测试：

| 任务类型 | 分辨率 | 处理速度 | 备注 |
|---------|--------|---------|------|
| 普通 OCR | 1024×1024 | ~3s/张 | MPS 加速 |
| 文档转 Markdown | 1024×1024 | ~4s/张 | 包含布局分析 |
| PDF 识别 | 多页 | ~3-5s/页 | 自动分页 |

## 常见问题

### 1. 内存不足

- 降低 `base_size` 和 `image_size`
- 使用 CPU 模式（虽然较慢）
- 关闭其他应用释放内存

### 2. GPU 显存不足

- 减小图像尺寸
- 关闭 `crop_mode`
- 使用更小的分辨率模式

### 3. 识别结果不准确

- 尝试不同的提示词类型
- 使用自定义提示词
- 增加图像分辨率
- 确保图像清晰度

### 4. 首次运行很慢

首次运行需要从 ModelScope 下载模型（约 3-4GB），请耐心等待。后续运行会直接加载本地缓存的模型。

## 参考

### 📚 项目文档

- **[FORMAT_GUIDE.md](./FORMAT_GUIDE.md)** - 输出格式完整指南（Markdown、纯文本、结构化输出）
- **[INSTALL.md](./INSTALL.md)** - 详细安装指南
- **[FIX_GUIDE.md](./FIX_GUIDE.md)** - 环境修复指南
- **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** - 常见问题排查

### 🔗 外部资源

- [DeepSeek-OCR ModelScope](https://modelscope.cn/models/deepseek-ai/DeepSeek-OCR)
- [DeepSeek-OCR GitHub](https://github.com/deepseek-ai/DeepSeek-OCR)
- [Transformers 文档](https://huggingface.co/docs/transformers)

## 许可证

本项目遵循 DeepSeek-OCR 的原始许可证。
