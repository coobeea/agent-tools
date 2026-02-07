#!/usr/bin/env python3
"""DeepSeek-OCR-2 识别测试脚本"""

import sys
sys.path.insert(0, '.')

from ocr import DeepSeekOCR

def main():
    print("=" * 80)
    print("DeepSeek-OCR-2 图像识别测试")
    print("=" * 80)
    print()
    
    # 图像路径
    image_path = '/Users/lifeng/data/pdfs_images/images/batch_06/page_053.png'
    
    print(f"📄 图像文件: {image_path}")
    print()
    
    # 初始化 OCR
    print("🔄 正在加载模型（首次加载需要几秒）...")
    ocr = DeepSeekOCR(use_local_model=True)
    print("✅ 模型加载完成！")
    print()
    
    # 识别图像
    print("🔍 开始识别图像（CPU 推理约需 50-60 秒，请耐心等待）...")
    print()
    result = ocr.recognize(image_path, prompt_type='markdown')
    
    # 显示结果
    print()
    print("=" * 80)
    print("📋 识别结果")
    print("=" * 80)
    print()
    print(result)
    print()
    print("=" * 80)
    print("✅ 识别完成！")
    print("=" * 80)
    
    # 保存结果到文件
    output_file = 'ocr_result.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    print()
    print(f"💾 识别结果已保存到: {output_file}")

if __name__ == '__main__':
    main()
