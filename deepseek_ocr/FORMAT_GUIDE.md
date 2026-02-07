# DeepSeek-OCR 输出格式指南

本文档介绍 DeepSeek-OCR 的多种输出格式和使用方法。

## 📋 支持的识别模式

DeepSeek-OCR 支持 5 种不同的 `prompt_type`：

| prompt_type | 说明 | 适用场景 |
|------------|------|---------|
| `markdown` | 转换为 Markdown 文档 | 文档 OCR，保留结构 |
| `ocr` | 纯文字识别 | 文本提取 |
| `free_ocr` | 自由文字识别 | 通用 OCR |
| `parse_figure` | 图表解析 | 图表、图形识别 |
| `describe` | 图像描述 | 图像内容理解 |

## 🛠️ 输出格式化工具

### 1. 原始输出（包含标注标签）

```python
from deepseek_ocr import DeepSeekOCR

ocr = DeepSeekOCR(use_local_model=True)
result = ocr.recognize("image.jpg", prompt_type='markdown')
print(result)  # 包含 <|ref|> 和 <|det|> 标签
```

**示例输出**：
```
<|ref|>## （十五）<|/ref|><|det|>[[123,456,789,012]]<|/det|>"三包"赔偿...
```

### 2. 纯净 Markdown（推荐）

使用 `OutputFormatter.clean_markdown()` 移除标注标签：

```python
from deepseek_ocr import DeepSeekOCR, OutputFormatter, save_as_markdown

ocr = DeepSeekOCR(use_local_model=True)
result_raw = ocr.recognize("image.jpg", prompt_type='markdown')

# 清理标签
result_clean = OutputFormatter.clean_markdown(result_raw)
print(result_clean)

# 或直接保存为纯净 Markdown
save_as_markdown(result_raw, 'output.md', clean=True)
```

**示例输出**：
```markdown
## （十五）"三包"赔偿

七、问：货物的生产企业为搞好售后服务...
```

### 3. 纯文本（无格式）

使用 `save_as_text()` 或 `OutputFormatter.to_plain_text()`：

```python
from deepseek_ocr import OutputFormatter, save_as_text

# 方法 1：直接保存
save_as_text(result_raw, 'output.txt')

# 方法 2：获取文本
plain_text = OutputFormatter.to_plain_text(result_raw)
print(plain_text)
```

**示例输出**：
```
（十五）"三包"赔偿

七、问：货物的生产企业为搞好售后服务...
```

### 4. 保留坐标信息

如果需要保留位置坐标（用于后处理）：

```python
result_with_coords = OutputFormatter.clean_markdown(
    result_raw, 
    keep_coordinates=True
)
```

### 5. 结构化输出

提取标题、段落、表格等结构化信息：

```python
structure = OutputFormatter.format_with_structure(result_raw)

print(f"标题: {structure['titles']}")
print(f"表格: {len(structure['tables'])} 个")
print(f"段落: {len(structure['paragraphs'])} 个")
print(f"完整文本: {structure['full_text']}")
```

## 📊 输出大小对比

以 `page_054.png` 为例：

| 格式 | 文件大小 | 说明 |
|-----|---------|------|
| 原始输出 | 3068 字符 | 包含所有标注标签 |
| 纯净 Markdown | 1831 字符 | 移除标签，保留结构 |
| 纯文本 | 1831 字符 | 移除所有格式 |

**清理标签后减少约 40% 的字符**

## 🚀 完整使用示例

### 示例 1：生成多种格式

```python
from deepseek_ocr import DeepSeekOCR, save_as_markdown, save_as_text

ocr = DeepSeekOCR(use_local_model=True)
result = ocr.recognize("document.jpg", prompt_type='markdown')

# 保存 3 种格式
save_as_markdown(result, 'output.md', clean=True)  # 纯净 Markdown
save_as_text(result, 'output.txt')                 # 纯文本
with open('output_raw.txt', 'w') as f:
    f.write(result)                                 # 原始输出
```

### 示例 2：批量处理并格式化

```python
from deepseek_ocr import DeepSeekOCR, OutputFormatter
import os

ocr = DeepSeekOCR(use_local_model=True)
images = ['img1.jpg', 'img2.jpg', 'img3.jpg']

for img in images:
    result_raw = ocr.recognize(img, prompt_type='markdown')
    result_clean = OutputFormatter.clean_markdown(result_raw)
    
    # 保存纯净 Markdown
    output_name = os.path.splitext(img)[0] + '.md'
    with open(output_name, 'w') as f:
        f.write(result_clean)
```

### 示例 3：对比不同 prompt_type

```python
from deepseek_ocr import DeepSeekOCR, OutputFormatter

ocr = DeepSeekOCR(use_local_model=True)
image_path = "test.jpg"

# 测试不同模式
for prompt_type in ['markdown', 'ocr', 'free_ocr']:
    result = ocr.recognize(image_path, prompt_type=prompt_type)
    clean = OutputFormatter.clean_markdown(result)
    
    print(f"\n{'='*60}")
    print(f"模式: {prompt_type}")
    print(f"长度: {len(clean)} 字符")
    print(f"预览: {clean[:200]}...")
```

## 🔧 高级功能

### 提取表格

```python
tables = OutputFormatter.extract_tables(result_raw)
for i, table in enumerate(tables):
    print(f"表格 {i+1}: {table}")
```

### 提取纯文本（不含表格和标题）

```python
text_only = OutputFormatter.extract_text_only(result_raw)
print(text_only)
```

## ⚠️ 注意事项

1. **原始输出 vs 清理后**：
   - 原始输出包含 `<|ref|>` 和 `<|det|>` 标签，用于内部处理
   - **建议使用 `OutputFormatter` 清理后再保存或展示**

2. **Markdown 标题**：
   - 使用 `prompt_type='markdown'` 会自动生成 `##` 标题
   - 使用 `prompt_type='ocr'` 不会生成标题

3. **表格格式**：
   - DeepSeek-OCR 可能输出 HTML 表格格式（`<table>`标签）
   - 建议保持原样或使用专门的表格解析工具

4. **性能优化**：
   - 清理标签操作非常快（正则表达式）
   - 可以先保存原始输出，后续按需清理

## 📚 参考

- [DeepSeek-OCR-2 官方文档](https://modelscope.cn/models/deepseek-ai/DeepSeek-OCR-2)
- [README.md](./README.md) - 安装和基础使用
- [INSTALL.md](./INSTALL.md) - 详细安装指南
- [FIX_GUIDE.md](./FIX_GUIDE.md) - 环境修复指南
