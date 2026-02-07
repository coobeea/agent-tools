#!/usr/bin/env python3
"""
GLM-OCR 图片识别脚本

简单用法：
    python ocr_image.py input.jpg output.md
"""

import sys
import os
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForImageTextToText


def ocr_image(input_file, output_file):
    """识别图片并保存为 Markdown"""
    
    # 检查输入文件
    if not os.path.exists(input_file):
        print(f"❌ 错误：输入文件不存在: {input_file}")
        return False
    
    # 模型路径
    model_path = "/Users/lifeng/data/models/GLM-OCR"
    
    # 检测设备
    if torch.cuda.is_available():
        device = "cuda"
        dtype = torch.bfloat16
    else:
        device = "cpu"
        dtype = torch.float32
    
    print(f"⏳ 使用设备: {device}")
    
    # 加载模型
    print(f"⏳ 加载 GLM-OCR 模型...")
    processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForImageTextToText.from_pretrained(
        model_path,
        torch_dtype=dtype,
        trust_remote_code=True
    )
    model.to(device)
    model.eval()
    print(f"✅ 模型加载完成")
    
    # 读取图片
    print(f"⏳ 识别图片: {input_file}")
    image = Image.open(input_file).convert('RGB')
    
    # 准备消息（使用 GLM-OCR 的标准格式）
    messages = [{
        "role": "user",
        "content": [
            {"type": "image", "url": input_file},
            {"type": "text", "text": "Text Recognition:"}
        ]
    }]
    
    # 应用模板并生成输入
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt"
    ).to(device)
    
    # 识别
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=2048)
    
    # 解码（跳过输入部分）
    result = processor.decode(outputs[0][inputs['input_ids'].shape[-1]:], skip_special_tokens=True)
    
    # 保存
    print(f"⏳ 保存到: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"✅ 完成！识别了 {len(result)} 字符")
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
