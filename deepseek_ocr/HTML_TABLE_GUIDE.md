# DeepSeek-OCR HTML 表格输出指南

## 🎯 关键发现

**DeepSeek-OCR-2 确实可以输出 HTML 表格！**

关键是使用正确的 prompt：

```python
prompt = "<<image>>\n<<|grounding|>>Convert to HTML format with tables."
```

## ✅ 成功测试

### 测试结果

| Prompt | HTML 表格 | 输出质量 |
|--------|-----------|---------|
| `<<image>>\nConvert this document to HTML table format.` | ❌ 否 | 纯文本 |
| **`<<image>>\n<<|grounding|>>Convert to HTML format with tables.`** | **✅ 是** | **包含 `<table>` 标签** |
| `<<image>>\nExtract tables from this image and output as HTML.` | ❌ 否 | 纯文本 |

### 成功的输出示例

```markdown
<|ref|>sub_title<|/ref|><|det|>[[111, 70, 521, 87]]<|/det|>
## （十五）"三包"赔偿（国税函发 [ 1995 ] 288号）第七条）

<|ref|>table<|/ref|><|det|>[[76, 96, 908, 147]]<|/det|>
<table><tr><td>七、问：货物的生产企业为搞好售后服务，支付给经销企业修理费用，作为经销企业为用户提供售后服务的费用支出，对经销企业从货物的生产企业获得的"三包"收入，应如何征税？</td><td>答：经销企业从货物的生产企业取得"三包"收入，应按"修理修配"征收增值税。</td></tr></table>

<|ref|>sub_title<|/ref|><|det|>[[111, 161, 557, 177]]<|/det|>
## （十六）编码中心条形码制作收入（国税函 [ 1997 ] 606号）
```

## 🔑 关键要素

### 1. `<<|grounding|>>` 标记

这个标记似乎触发了模型的**结构化输出模式**，使其能够识别表格布局。

### 2. 明确的指令

`"Convert to HTML format with tables"` 明确告诉模型：
- 输出格式：HTML
- 包含结构：tables（表格）

### 3. 完整的 Prompt 格式

```python
"<<image>>\n<<|grounding|>>Convert to HTML format with tables."
```

- `<<image>>`: 图像占位符
- `\n`: 换行符
- `<<|grounding|>>`: 结构化标记
- `Convert to HTML format with tables.`: 具体指令

## 💡 使用方法

### 基础用法

```python
from deepseek_ocr import DeepSeekOCR

ocr = DeepSeekOCR(use_local_model=True)

# 使用 HTML 表格 prompt
html_prompt = "<<image>>\n<<|grounding|>>Convert to HTML format with tables."
result = ocr.recognize("image.jpg", prompt=html_prompt)

# 输出包含 HTML 表格
print(result)
```

### 清理标注标签

```python
from deepseek_ocr import OutputFormatter

# 原始输出
result_raw = ocr.recognize("image.jpg", prompt=html_prompt)

# 清理标注标签，保留 HTML 表格
result_clean = OutputFormatter.clean_markdown(result_raw)

# 现在 result_clean 包含纯净的 HTML 表格
with open('output.html', 'w', encoding='utf-8') as f:
    f.write(result_clean)
```

### 提取纯 HTML 表格

```python
import re

def extract_html_tables(text):
    """提取所有 HTML 表格"""
    # 清理标注标签
    cleaned = OutputFormatter.clean_markdown(text)
    
    # 提取所有 <table>...</table>
    tables = re.findall(r'<table>.*?</table>', cleaned, re.DOTALL)
    return tables

# 使用
tables = extract_html_tables(result_raw)
for i, table in enumerate(tables, 1):
    print(f"表格 {i}:")
    print(table)
    print()
```

## 📊 输出格式对比

### 标准 Markdown 模式

```python
result = ocr.recognize("image.jpg", prompt_type='markdown')
```

**输出**：
```markdown
## （十五）"三包"赔偿

七、问：...

答：...
```

### HTML 表格模式

```python
result = ocr.recognize("image.jpg", 
                       prompt="<<image>>\n<<|grounding|>>Convert to HTML format with tables.")
```

**输出**：
```html
## （十五）"三包"赔偿

<table><tr><td>七、问：...</td><td>答：...</td></tr></table>
```

## ⚠️ 注意事项

### 1. 表格识别取决于布局

模型会根据**文本的布局**判断是否输出为表格：
- ✅ 左右分栏的文字 → 可能输出为 `<tr><td>...</td><td>...</td></tr>`
- ❌ 单列文字 → 不会输出为表格

### 2. 并非所有内容都会变成表格

只有模型判断为"表格结构"的内容才会输出为 HTML 表格，其他内容仍然是 Markdown 标题和文本。

### 3. 标注标签需要清理

原始输出仍然包含 `<|ref|>` 和 `<|det|>` 标签，需要使用 `OutputFormatter.clean_markdown()` 清理。

### 4. HTML 样式

默认输出的 `<table>` 标签**不包含样式**：
```html
<table><tr><td>内容</td></tr></table>
```

如果需要样式（如边框、居中），需要手动添加：
```html
<table border="1" style="margin: auto; width: 100%;">
  <tr><td>内容</td></tr>
</table>
```

## 🎨 高级用法

### 添加 HTML 样式

```python
import re

def add_table_style(html_text):
    """为 HTML 表格添加样式"""
    # 替换 <table> 标签
    styled = re.sub(
        r'<table>',
        r'<table border="1" style="margin: auto; word-wrap: break-word; width: 100%;">',
        html_text
    )
    # 为 <td> 添加样式
    styled = re.sub(
        r'<td>',
        r'<td style="padding: 5px; text-align: left;">',
        styled
    )
    return styled

# 使用
result = ocr.recognize("image.jpg", 
                       prompt="<<image>>\n<<|grounding|>>Convert to HTML format with tables.")
result_clean = OutputFormatter.clean_markdown(result)
result_styled = add_table_style(result_clean)

with open('output_styled.html', 'w', encoding='utf-8') as f:
    # 添加 HTML 头部
    f.write('<!DOCTYPE html>\n<html><head><meta charset="UTF-8"></head><body>\n')
    f.write(result_styled)
    f.write('\n</body></html>')
```

### 转换为完整 HTML 文档

```python
def to_html_document(ocr_result, title="OCR Result"):
    """转换为完整的 HTML 文档"""
    # 清理标注
    cleaned = OutputFormatter.clean_markdown(ocr_result)
    
    # 添加样式
    styled = add_table_style(cleaned)
    
    # 将 Markdown 标题转换为 HTML
    styled = re.sub(r'^## (.+)$', r'<h2>\1</h2>', styled, flags=re.MULTILINE)
    styled = re.sub(r'^### (.+)$', r'<h3>\1</h3>', styled, flags=re.MULTILINE)
    
    # 包装为完整 HTML
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        table {{
            border-collapse: collapse;
            margin: 20px 0;
            width: 100%;
        }}
        td {{
            border: 1px solid #ddd;
            padding: 8px;
        }}
        h2 {{
            color: #333;
            border-bottom: 2px solid #007bff;
        }}
    </style>
</head>
<body>
{styled}
</body>
</html>'''
    return html

# 使用
result = ocr.recognize("image.jpg", 
                       prompt="<<image>>\n<<|grounding|>>Convert to HTML format with tables.")
html_doc = to_html_document(result, title="增值税政策文档")

with open('output.html', 'w', encoding='utf-8') as f:
    f.write(html_doc)
```

## 📝 最佳实践

### 1. 对比不同模式

```python
# 测试同一张图片的不同输出
ocr = DeepSeekOCR(use_local_model=True)

# Markdown 模式
result_md = ocr.recognize("image.jpg", prompt_type='markdown')

# HTML 表格模式
result_html = ocr.recognize("image.jpg", 
                           prompt="<<image>>\n<<|grounding|>>Convert to HTML format with tables.")

# 对比
print("Markdown 模式包含 <table>:", '<table>' in result_md)
print("HTML 模式包含 <table>:", '<table>' in result_html)
```

### 2. 根据需求选择模式

| 需求 | 推荐模式 | Prompt |
|-----|---------|--------|
| 纯文本识别 | `ocr` | `prompt_type='ocr'` |
| 文档结构 | `markdown` | `prompt_type='markdown'` |
| **HTML 表格** | **自定义** | **`"<<image>>\n<<|grounding|>>Convert to HTML format with tables."`** |
| 图表解析 | `parse_figure` | `prompt_type='parse_figure'` |

### 3. 批量处理

```python
import os
from pathlib import Path

def batch_convert_to_html(image_dir, output_dir):
    """批量转换图片为 HTML 表格格式"""
    ocr = DeepSeekOCR(use_local_model=True)
    html_prompt = "<<image>>\n<<|grounding|>>Convert to HTML format with tables."
    
    os.makedirs(output_dir, exist_ok=True)
    
    for img_file in Path(image_dir).glob('*.{jpg,jpeg,png}'):
        print(f"处理: {img_file.name}")
        
        # 识别
        result = ocr.recognize(str(img_file), prompt=html_prompt)
        
        # 清理并转换
        html_doc = to_html_document(result, title=img_file.stem)
        
        # 保存
        output_file = Path(output_dir) / f"{img_file.stem}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_doc)
        
        print(f"  ✅ 已保存: {output_file}")

# 使用
batch_convert_to_html('/path/to/images', '/path/to/output')
```

## 🔗 相关文档

- [FORMAT_GUIDE.md](./FORMAT_GUIDE.md) - 输出格式完整指南
- [PROMPT_TYPES_TEST_SUMMARY.md](./PROMPT_TYPES_TEST_SUMMARY.md) - 5种模式测试总结
- [OUTPUT_COMPARISON.md](./OUTPUT_COMPARISON.md) - 格式对比详情
- [README.md](./README.md) - 项目使用文档

## 🎉 总结

1. **DeepSeek-OCR-2 支持 HTML 表格输出**
2. **关键是使用 `<<|grounding|>>` 标记**
3. **明确指定 "Convert to HTML format with tables"**
4. **输出仍需清理标注标签**
5. **可以自定义 HTML 样式**

现在您可以使用这个方法获得类似历史文件的 HTML 表格输出了！
