#!/usr/bin/env python3
"""保存上一次 OCR 识别结果为 Markdown 文件"""

import sys
sys.path.insert(0, '.')

from ocr import DeepSeekOCR, save_as_markdown, save_as_text

def main():
    # 识别图像
    image_path = '/Users/lifeng/data/pdfs_images/images/batch_06/page_058.png'
    
    print("🔍 识别图像...")
    ocr = DeepSeekOCR(use_local_model=True)
    result = ocr.recognize(image_path, prompt_type='markdown')
    
    print()
    print("=" * 80)
    print("💾 保存结果为不同格式")
    print("=" * 80)
    print()
    
    # 1. 保存清理后的 Markdown（推荐）
    save_as_markdown(result, 'page_058_clean.md', clean=True)
    
    # 2. 保存原始 Markdown（带标注）
    save_as_markdown(result, 'page_058_raw.md', clean=False)
    
    # 3. 保存纯文本
    save_as_text(result, 'page_058.txt')
    
    print()
    print("=" * 80)
    print("✅ 完成！生成了以下文件:")
    print("=" * 80)
    print("📄 page_058_clean.md  - 推荐：清理后的 Markdown")
    print("📄 page_058_raw.md    - 原始输出（带标注）")
    print("📄 page_058.txt       - 纯文本")
    print()

if __name__ == '__main__':
    main()
