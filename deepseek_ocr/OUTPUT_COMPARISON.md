# DeepSeek-OCR 输出格式对比

本文档展示 DeepSeek-OCR 原始输出与格式化后输出的区别。

## 📊 对比概览

| 输出类型 | 文件大小 | 标注标签 | Markdown 格式 | 适用场景 |
|---------|---------|---------|--------------|---------|
| 原始输出 | 3068 字符 | ✅ 包含 | ✅ 保留 | 内部处理、调试 |
| 纯净 Markdown | 1831 字符 | ❌ 移除 | ✅ 保留 | 文档展示、编辑 |
| 纯文本 | 1831 字符 | ❌ 移除 | ❌ 移除 | 文本分析、搜索 |

**清理标签后减少约 40% 的字符**

## 🔍 详细对比

### 1. 原始输出（包含标注标签）

**文件**: `deepseek_ocr_result_page054.md`（之前的输出）

```markdown
<|ref|>## （十五）<|/ref|><|det|>[[123,456,789,012]]<|/det|>"三包"赔偿（国税函发 [ 1995 ] 288号）第七条）

<|ref|>七、问：<|/ref|><|det|>[[234,567,890,123]]<|/det|>货物的生产企业为搞好售后服务，支付给经销企业修理费用...
```

**特点**：
- ✅ 包含 `<|ref|>...<|/ref|>` 引用标签
- ✅ 包含 `<|det|>[[x,y,w,h]]<|/det|>` 坐标信息
- ⚠️ 标签干扰可读性
- ⚠️ 文件体积大（3068 字符）

### 2. 纯净 Markdown（推荐）

**文件**: `result_clean.md`（使用 `OutputFormatter.clean_markdown()`）

```markdown
## （十五）"三包"赔偿（国税函发 [ 1995 ] 288号）第七条）

七、问：货物的生产企业为搞好售后服务，支付给经销企业修理费用，作为经销企业为用户提供售后服务的费用支出，对经销企业从货物的生产企业获得的"三包"收入，应如何征税？

答：经销企业从货物的生产企业取得"三包"收入，应按"修理修配"征收增值税。

## （十六）编码中心条形码制作收入（国税函 [ 1997 ] 606号）

中国物品编码中心和新闻出版署条形码中心向用户收取的"条形码胶片研制费"，是制作和销售条码而取得的收入...
```

**特点**：
- ✅ **移除所有标注标签**
- ✅ **保留 Markdown 标题**（`##`）
- ✅ **保留文档结构**
- ✅ **可读性强**
- ✅ **文件体积小**（1831 字符）

### 3. 纯文本输出

**文件**: `result_plain.txt`（使用 `save_as_text()`）

```text
（十五）"三包"赔偿（国税函发 [ 1995 ] 288号）第七条）

七、问：货物的生产企业为搞好售后服务，支付给经销企业修理费用，作为经销企业为用户提供售后服务的费用支出，对经销企业从货物的生产企业获得的"三包"收入，应如何征税？

答：经销企业从货物的生产企业取得"三包"收入，应按"修理修配"征收增值税。

（十六）编码中心条形码制作收入（国税函 [ 1997 ] 606号）

中国物品编码中心和新闻出版署条形码中心向用户收取的"条形码胶片研制费"，是制作和销售条码而取得的收入...
```

**特点**：
- ✅ **移除所有标签和格式**
- ❌ **不保留 Markdown 标题标记**
- ✅ **适合文本分析和搜索**

## 🎯 标注标签说明

### `<|ref|>` 标签（引用标签）

- **作用**: 标记原文引用位置
- **格式**: `<|ref|>文本内容<|/ref|>`
- **示例**: `<|ref|>## （十五）<|/ref|>`

### `<|det|>` 标签（检测标签）

- **作用**: 标记文字在图像中的坐标
- **格式**: `<|det|>[[x1,y1,x2,y2]]<|/det|>`
- **示例**: `<|det|>[[123,456,789,012]]<|/det|>`

**为什么会有这些标签？**

DeepSeek-OCR 内部使用这些标签来：
1. 追踪文本在原始图像中的位置
2. 支持后续的布局分析
3. 方便进行定位和编辑

但对于**最终用户展示**来说，这些标签会干扰阅读，**建议使用 `OutputFormatter` 清理**。

## 💡 使用建议

### 推荐做法（生产环境）

```python
from deepseek_ocr import DeepSeekOCR, save_as_markdown, save_as_text

ocr = DeepSeekOCR(use_local_model=True)
result_raw = ocr.recognize("image.jpg", prompt_type='markdown')

# ✅ 保存纯净 Markdown（推荐用于展示）
save_as_markdown(result_raw, 'output.md', clean=True)

# ✅ 保存纯文本（推荐用于文本分析）
save_as_text(result_raw, 'output.txt')

# 🔧 可选：保存原始输出（用于调试）
with open('output_raw.txt', 'w') as f:
    f.write(result_raw)
```

### 不同场景的选择

| 场景 | 推荐格式 | 原因 |
|-----|---------|------|
| 📄 文档展示 | 纯净 Markdown | 可读性强，保留结构 |
| 📝 文本编辑 | 纯净 Markdown | 易于编辑，标准格式 |
| 🔍 文本搜索 | 纯文本 | 无格式干扰，搜索精确 |
| 📊 数据分析 | 纯文本 | 方便处理，统一格式 |
| 🐛 调试问题 | 原始输出 | 保留完整信息 |
| 📍 位置追踪 | 保留坐标的 Markdown | 需要定位文本位置 |

## 📈 性能对比

### 文件大小（以 page_054.png 为例）

```
原始输出:        3068 字符 ████████████████████████ 100%
纯净 Markdown:   1831 字符 ██████████████            60%
纯文本:          1831 字符 ██████████████            60%
```

### 清理速度

```python
import time
from deepseek_ocr import OutputFormatter

result_raw = ocr.recognize("image.jpg")  # ~51 秒（推理时间）

start = time.time()
result_clean = OutputFormatter.clean_markdown(result_raw)
print(f"清理耗时: {time.time() - start:.3f} 秒")  # ~0.001 秒（几乎瞬时）
```

**结论**: 清理操作非常快，建议总是先保存原始输出，按需清理。

## 🚀 快速上手

### 生成所有格式

```bash
cd /Users/lifeng/git/git_agents/agent-tools/deepseek_ocr
source deepseek_env/bin/activate

python << 'EOF'
import sys
sys.path.insert(0, '/Users/lifeng/git/git_agents/agent-tools')
from deepseek_ocr import DeepSeekOCR, save_as_markdown, save_as_text

ocr = DeepSeekOCR(use_local_model=True)
result = ocr.recognize("test.jpg", prompt_type='markdown')

save_as_markdown(result, 'output.md', clean=True)
save_as_text(result, 'output.txt')
print("✅ 已生成所有格式！")
EOF
```

### 批量转换现有输出

```python
from deepseek_ocr import OutputFormatter
import os

# 读取原始输出
with open('old_output.txt', 'r') as f:
    raw = f.read()

# 清理并保存
clean = OutputFormatter.clean_markdown(raw)
with open('cleaned_output.md', 'w') as f:
    f.write(clean)

print("✅ 清理完成！")
```

## 📚 参考文档

- **[FORMAT_GUIDE.md](./FORMAT_GUIDE.md)** - 完整的输出格式指南
- **[README.md](./README.md)** - 项目使用文档
- **[INSTALL.md](./INSTALL.md)** - 安装指南

## ⚠️ 注意事项

1. **原始输出的价值**:
   - 包含完整的位置信息
   - 便于调试和问题排查
   - 建议保留作为备份

2. **清理后无法还原**:
   - 清理操作是单向的
   - 标签和坐标信息会永久丢失
   - 建议先保存原始输出

3. **Markdown 兼容性**:
   - 清理后的 Markdown 符合标准格式
   - 可在任何 Markdown 编辑器中使用
   - 支持导出为 HTML、PDF 等格式

4. **表格格式**:
   - DeepSeek-OCR 可能输出 HTML 表格（`<table>` 标签）
   - `OutputFormatter` 会保留表格原样
   - 如需转换表格格式，建议使用专门工具
