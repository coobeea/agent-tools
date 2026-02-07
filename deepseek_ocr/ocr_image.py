#!/usr/bin/env python3
"""
DeepSeek-OCR 图片识别脚本

简单用法：
    python ocr_image.py input.jpg output.md
"""

import sys
import os

# 添加路径
sys.path.insert(0, '/Users/lifeng/git/git_agents/agent-tools')

from deepseek_ocr import DeepSeekOCR, OutputFormatter


def ocr_image(input_file, output_file):
    """识别图片并保存为 Markdown"""
    
    # 检查输入文件
    if not os.path.exists(input_file):
        print(f"❌ 错误：输入文件不存在: {input_file}")
        return False
    
    # 初始化 OCR
    print(f"⏳ 初始化 DeepSeek-OCR...")
    ocr = DeepSeekOCR(use_local_model=True, model_name='deepseek-ai/DeepSeek-OCR-2')
    
    # 识别
    print(f"⏳ 识别图片: {input_file}")
    result_raw = ocr.recognize(input_file, prompt_type='markdown')
    
    # 清理标注标签
    print(f"⏳ 清理输出...")
    result_clean = OutputFormatter.clean_markdown(result_raw)
    
    # 保存
    print(f"⏳ 保存到: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result_clean)
    
    print(f"✅ 完成！识别了 {len(result_clean)} 字符")
    return True


def main():
    """主函数"""
    
    # 检查参数
    if len(sys.argv) < 3:
        print("用法: python ocr_image.py <输入图片> <输出文件>")
        print()
        print("示例:")
        print("  python ocr_image.py document.jpg output.md")
        print("  python ocr_image.py /path/to/image.png result.md")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # 执行识别
    success = ocr_image(input_file, output_file)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
