# DeepSeek-OCR 5种识别模式测试总结

## 🎯 测试目标

验证 DeepSeek-OCR 的 5 种 `prompt_type` 是否能输出 HTML 表格格式。

## 📋 测试图片

- **图片路径**: `/Users/lifeng/data/pdfs_images/images/batch_06/page_054.png`
- **内容**: 增值税政策文档（文字内容，无明显表格）

## ✅ 测试结果汇总

| prompt_type | 输出格式 | HTML 表格 | 文件大小 | 识别质量 | 说明 |
|------------|---------|----------|---------|---------|------|
| `markdown` | ✅ Markdown 标题 + 文本 | ❌ 无 | 3068 字符（原始）<br>1831 字符（清理后） | ⭐⭐⭐⭐⭐ 优秀 | **推荐**：保留文档结构，清晰易读 |
| `ocr` | ✅ 纯文本 + 坐标 | ❌ 无 | 9328 字符（原始） | ⭐⭐⭐ 一般 | 带详细坐标，但输出混乱 |
| `free_ocr` | ⭐ 纯文本（有重复） | ❌ 无 | ~2000 字符 | ⭐⭐ 较差 | 识别错误多，有大量重复内容 |
| `parse_figure` | ❌ 英文描述 | ❌ 无 | ~1500 字符 | ❌ 不适用 | 错误理解为知识产权文档 |
| `describe` | ❌ 英文描述 | ❌ 无 | ~1500 字符 | ❌ 不适用 | 错误理解为信用评级文档 |

## 🔍 关键发现

### ❌ **所有 5 种模式都没有输出 HTML 表格！**

但是，用户提供的历史文件 `/Users/lifeng/data/pdfs_images/images/batch_06/page_054.md` **确实包含大量 HTML 表格标签**：

```html
<table border=1 style='margin: auto; word-wrap: break-word;'>
<tr><td colspan="2">（十五）"三包"赔偿...</td></tr>
...
</table>
```

## 🤔 为什么会出现这种差异？

### 可能的原因：

1. **不同的模型版本**
   - 历史文件可能是用 DeepSeek-OCR v1 生成的
   - 当前测试使用的是 DeepSeek-OCR-2（新版本）
   - **新版本可能移除了 HTML 表格输出功能**

2. **不同的参数配置**
   - 历史版本可能有 `output_format='html'` 或类似参数
   - 当前代码中没有这个参数

3. **不同的 prompt**
   - 可能存在未公开的 prompt 能触发 HTML 输出
   - 当前的 5 种 prompt 都不会触发 HTML 表格

4. **图片内容差异**
   - 如果图片中包含**明显的表格结构**（比如带边框的表格），可能会触发 HTML 输出
   - 当前测试的图片是纯文本文档，没有表格

## 📊 各模式详细对比

### 1. `markdown` 模式（推荐）

**原始输出**：
```markdown
<|ref|>sub_title<|/ref|><|det|>[[111, 70, 521, 87]]<|/det|>
## （十五）"三包"赔偿（国税函发 [ 1995 ] 288号）第七条）

<|ref|>text<|/ref|><|det|>[[80, 99, 910, 145]]<|/det|>
七、问：货物的生产企业为搞好售后服务...
```

**清理后输出**：
```markdown
## （十五）"三包"赔偿（国税函发 [ 1995 ] 288号）第七条）

七、问：货物的生产企业为搞好售后服务，支付给经销企业修理费用...

答：经销企业从货物的生产企业取得"三包"收入，应按"修理修配"征收增值税。
```

**特点**：
- ✅ 保留标题结构（`##`）
- ✅ 段落清晰
- ✅ 易读性强
- ✅ 识别准确

### 2. `ocr` 模式

**原始输出**：
```
<|ref|>32<|/ref|><|det|>[[78, 37, 104, 49]]<|/det|>
<|ref|>增值税新政策新业务大全<|/ref|><|det|>[[133, 37, 309, 51]]<|/det|>
<|ref|>（十五）"三包"赔偿（国税函发[1995]288号第七条）<|/ref|><|det|>[[113, 70, 518, 86]]<|/det|>
...
```

**特点**：
- ✅ 包含详细坐标信息
- ❌ 输出冗长（9328 字符）
- ❌ 每个文本块都有单独的标签
- ⚠️ 适合需要精确定位的场景

**清理后为空**：因为清理工具移除了所有标签，但没有合并文本。

### 3. `free_ocr` 模式（质量差）

**输出示例**：
```
（十五）"三包"赔偿（国税函发[1995]288号 第七条）

七、同、货物的生产企业为赔偿而服务...（错误识别）

（二十）不征收增值税的部分货物

（1）基本建设单位和从事建筑安装业务的企业向建设工广...（错误）

（2）应按规定缴纳增值税的货物，应按以下规定缴纳增值税：（重复内容）
（3）对自建自用房屋、自建自用房屋的建筑物，应按以下规定缴纳增值税：（重复）
...（大量重复的(4)-(23)）
```

**问题**：
- ❌ 识别错误多（"搞好售后服务" → "赔偿而服务"）
- ❌ 大量重复内容（(2)-(23)都是相同的句子）
- ❌ 不推荐使用

### 4. `parse_figure` 模式（不适用）

**输出**：
```
This image appears to display several sections related to financial regulations 
concerning intellectual property rights management within China's context.

### Section Breakdown:
1. **Title**: "《中国专利法》" (Chinese Patent Law)...
```

**问题**：
- ❌ **完全错误理解了图片内容**（明明是增值税文档，理解成了知识产权文档）
- ❌ 输出英文描述
- ❌ 不适合中文文档 OCR

### 5. `describe` 模式（不适用）

**输出**：
```
This image appears to display several pages extracted from what seems like legal 
documents related to financial regulations concerning credit ratings.

**Page Layout Description**
1. **Header Section**: Title: Credit Rating System Reform Office
...
```

**问题**：
- ❌ **完全错误理解**（理解成信用评级文档）
- ❌ 输出英文描述
- ❌ 不适合文字识别

## 🎯 推荐使用方案

### 方案 1：Markdown 模式（最佳）

```python
from deepseek_ocr import DeepSeekOCR, save_as_markdown

ocr = DeepSeekOCR(use_local_model=True)
result = ocr.recognize("image.jpg", prompt_type='markdown')
save_as_markdown(result, 'output.md', clean=True)
```

**适用场景**：
- ✅ 文档 OCR
- ✅ 保留标题结构
- ✅ 需要清晰易读的输出

### 方案 2：OCR 模式 + 自定义处理

```python
result = ocr.recognize("image.jpg", prompt_type='ocr')
# 需要自己解析坐标和文本
```

**适用场景**：
- ✅ 需要精确定位
- ✅ 后续需要根据坐标做处理

### ❌ 不推荐的模式

- `free_ocr`: 识别质量差，有大量错误
- `parse_figure`: 适合图表，不适合文字文档
- `describe`: 适合图像描述，不适合 OCR

## 🔬 关于 HTML 表格输出

### 现状

当前 DeepSeek-OCR-2 的所有 5 种 prompt_type **都不会输出 HTML 表格**。

### 可能的解决方案

1. **查看 DeepSeek-OCR v1 文档**
   - 检查旧版本是否有 HTML 输出功能
   - 查看是否有特殊参数

2. **使用自定义 prompt**
   ```python
   custom_prompt = "<<image>>\nConvert this document to HTML table format."
   result = ocr.recognize(image_path, prompt=custom_prompt)
   ```

3. **检查模型配置**
   - 可能需要特定的模型配置
   - 或者需要不同的 DeepSeek-OCR 版本

4. **后处理转换**
   - 使用 Markdown 输出
   - 用脚本将 Markdown 转换为 HTML 表格

## 📝 建议

1. **如果需要 HTML 表格输出**：
   - 检查是否有 DeepSeek-OCR v1 或其他版本
   - 尝试自定义 prompt
   - 或者使用其他 OCR 工具（如 PaddleOCR）

2. **如果 Markdown 格式够用**：
   - 使用 `prompt_type='markdown'` + `OutputFormatter.clean_markdown()`
   - 输出质量优秀，结构清晰

3. **如果需要表格识别**：
   - 使用专门的表格识别模型
   - 或者使用 PaddleOCR 的表格识别功能

## 📚 测试文件位置

所有测试输出文件位于：
```
/Users/lifeng/git/git_agents/agent-tools/deepseek_ocr/
├── test_markdown_raw.txt
├── test_markdown_clean.md
├── test_ocr_raw.txt
├── test_ocr_clean.md
├── test_free_ocr_raw.txt
├── test_free_ocr_clean.md
├── test_parse_figure_raw.txt
├── test_parse_figure_clean.md
├── test_describe_raw.txt
└── test_describe_clean.md
```

## 🔗 相关文档

- [FORMAT_GUIDE.md](./FORMAT_GUIDE.md) - 输出格式完整指南
- [OUTPUT_COMPARISON.md](./OUTPUT_COMPARISON.md) - 格式对比详情
- [README.md](./README.md) - 项目使用文档
