#!/usr/bin/env python3
"""OCR 输出格式测试脚本

演示如何使用不同的输出格式和配置。
"""

import sys
sys.path.insert(0, '.')

from ocr import DeepSeekOCR, OutputFormatter, save_as_markdown, save_as_text

def main():
    print("=" * 80)
    print("DeepSeek-OCR-2 输出格式测试")
    print("=" * 80)
    print()
    
    # 测试图像
    image_path = '/Users/lifeng/data/pdfs_images/images/batch_06/page_058.png'
    
    print(f"📄 图像: {image_path}")
    print()
    
    # 初始化 OCR
    print("⏳ 加载模型...")
    ocr = DeepSeekOCR(use_local_model=True)
    print("✅ 模型加载完成")
    print()
    
    # ========================================
    # 测试不同的 prompt_type
    # ========================================
    
    print("🔍 测试 1: Markdown 格式（默认）")
    print("-" * 80)
    result_md = ocr.recognize(image_path, prompt_type='markdown')
    print("✅ 识别完成")
    print()
    
    # 保存原始输出（带标注）
    save_as_markdown(result_md, 'output_raw.md', clean=False)
    
    # 保存清理后的输出（纯净 Markdown）
    save_as_markdown(result_md, 'output_clean.md', clean=True)
    
    # 保存带坐标的输出
    save_as_markdown(result_md, 'output_with_coords.md', clean=True, keep_coordinates=True)
    
    # 保存纯文本
    save_as_text(result_md, 'output_text.txt')
    
    print()
    print("=" * 80)
    print("📁 已生成以下文件:")
    print("=" * 80)
    print("1. output_raw.md          - 原始输出（带标注）")
    print("2. output_clean.md        - 清理后的 Markdown（纯净）")
    print("3. output_with_coords.md  - 带坐标信息的 Markdown")
    print("4. output_text.txt        - 纯文本格式")
    print()
    
    # ========================================
    # 演示结构化输出
    # ========================================
    
    print("=" * 80)
    print("📊 结构化输出分析")
    print("=" * 80)
    structure = OutputFormatter.format_with_structure(result_md)
    
    print(f"\n📌 标题数量: {len(structure['titles'])}")
    for level, title in structure['titles'][:3]:  # 只显示前3个
        print(f"  {'#' * level} {title}")
    if len(structure['titles']) > 3:
        print(f"  ... (共 {len(structure['titles'])} 个标题)")
    
    print(f"\n📋 表格数量: {len(structure['tables'])}")
    
    print(f"\n📄 段落数量: {len(structure['paragraphs'])}")
    if structure['paragraphs']:
        print(f"  第一段预览: {structure['paragraphs'][0][:100]}...")
    
    print()
    print("=" * 80)
    print("✅ 测试完成！")
    print("=" * 80)
    
    # ========================================
    # 测试其他 prompt 类型
    # ========================================
    
    print()
    print("🔍 测试 2: 其他 prompt 类型")
    print("-" * 80)
    
    # OCR 模式
    print("  - 测试 OCR 模式...")
    result_ocr = ocr.recognize(image_path, prompt_type='ocr')
    save_as_markdown(result_ocr, 'output_ocr.md', clean=True)
    print("    ✅ 已保存: output_ocr.md")
    
    # Free OCR 模式
    print("  - 测试 Free OCR 模式...")
    result_free = ocr.recognize(image_path, prompt_type='free_ocr')
    save_as_markdown(result_free, 'output_free_ocr.md', clean=True)
    print("    ✅ 已保存: output_free_ocr.md")
    
    print()
    print("=" * 80)
    print("✅ 所有测试完成！")
    print("=" * 80)


if __name__ == '__main__':
    main()
