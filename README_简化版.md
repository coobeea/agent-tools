# Agent Tools 简单使用指南

## 📋 OCR 工具快速调用

### DeepSeek-OCR（推荐，已测试通过）

```bash
# 在任何目录下直接调用
/Users/lifeng/git/git_agents/agent-tools/deepseek_ocr/ocr_image.sh 输入图片.jpg 输出.md
```

**示例**：
```bash
/Users/lifeng/git/git_agents/agent-tools/deepseek_ocr/ocr_image.sh \
  /Users/lifeng/data/images/test.png \
  result.md
```

**特点**：
- ✅ 自动激活虚拟环境
- ✅ 输出纯净 Markdown
- ✅ 识别质量优秀
- ⏱️  耗时约 45 秒

---

### GLM-OCR（脚本已创建，需要进一步测试）

```bash
# 在任何目录下直接调用
/Users/lifeng/git/git_agents/agent-tools/glm_ocr/ocr_image.sh 输入图片.jpg 输出.md
```

**注意**：此脚本可能需要进一步调试才能正常使用。

---

## 📝 就这两个命令！

不需要看其他复杂的文档，记住这两个路径就够了：

1. **DeepSeek-OCR**：`/Users/lifeng/git/git_agents/agent-tools/deepseek_ocr/ocr_image.sh`
2. **GLM-OCR**：`/Users/lifeng/git/git_agents/agent-tools/glm_ocr/ocr_image.sh`

在任何地方都能调用，自动处理虚拟环境！
