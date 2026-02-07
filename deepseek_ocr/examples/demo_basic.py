#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""DeepSeek-OCR 基础使用示例

演示如何使用 DeepSeek-OCR 进行图像文字识别。
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from deepseek_ocr import DeepSeekOCR, SUPPORTED_PROMPTS


def demo_basic_ocr():
    """基础 OCR 识别示例"""
    print("=" * 60)
    print("基础 OCR 识别示例")
    print("=" * 60)
    
    # 初始化 OCR
    print("\n正在初始化 DeepSeek-OCR...")
    ocr = DeepSeekOCR()
    print(f"模型加载完成: {ocr}")
    
    # 测试图像路径（需要准备一张测试图像）
    image_path = "test_image.jpg"
    
    if not os.path.exists(image_path):
        print(f"\n请准备一张测试图像并保存为: {image_path}")
        return
    
    # 识别图像
    print(f"\n识别图像: {image_path}")
    result = ocr.recognize(image_path, prompt_type="ocr")
    print("\n识别结果:")
    print("-" * 60)
    print(result)
    print("-" * 60)


def demo_markdown_conversion():
    """文档转 Markdown 示例"""
    print("\n" + "=" * 60)
    print("文档转 Markdown 示例")
    print("=" * 60)
    
    # 初始化 OCR
    ocr = DeepSeekOCR()
    
    # 测试文档图像
    document_path = "test_document.jpg"
    
    if not os.path.exists(document_path):
        print(f"\n请准备一张文档图像并保存为: {document_path}")
        return
    
    # 转换为 Markdown
    print(f"\n转换文档为 Markdown: {document_path}")
    result = ocr.recognize(document_path, prompt_type="markdown")
    print("\nMarkdown 结果:")
    print("-" * 60)
    print(result)
    print("-" * 60)


def demo_figure_parsing():
    """图表解析示例"""
    print("\n" + "=" * 60)
    print("图表解析示例")
    print("=" * 60)
    
    # 初始化 OCR
    ocr = DeepSeekOCR()
    
    # 测试图表图像
    figure_path = "test_figure.jpg"
    
    if not os.path.exists(figure_path):
        print(f"\n请准备一张图表图像并保存为: {figure_path}")
        return
    
    # 解析图表
    print(f"\n解析图表: {figure_path}")
    result = ocr.recognize(figure_path, prompt_type="parse_figure")
    print("\n解析结果:")
    print("-" * 60)
    print(result)
    print("-" * 60)


def demo_batch_recognition():
    """批量识别示例"""
    print("\n" + "=" * 60)
    print("批量识别示例")
    print("=" * 60)
    
    # 初始化 OCR
    ocr = DeepSeekOCR()
    
    # 准备多张图像
    image_paths = ["image1.jpg", "image2.jpg", "image3.jpg"]
    
    # 检查文件是否存在
    existing_paths = [p for p in image_paths if os.path.exists(p)]
    
    if not existing_paths:
        print("\n请准备测试图像:")
        for path in image_paths:
            print(f"  - {path}")
        return
    
    # 批量识别
    print(f"\n批量识别 {len(existing_paths)} 张图像...")
    results = ocr.batch_recognize(existing_paths)
    
    print("\n批量识别结果:")
    for i, (path, result) in enumerate(zip(existing_paths, results)):
        print(f"\n图像 {i+1}: {path}")
        print("-" * 60)
        print(result[:200] + "..." if len(result) > 200 else result)
        print("-" * 60)


def demo_custom_prompt():
    """自定义提示词示例"""
    print("\n" + "=" * 60)
    print("自定义提示词示例")
    print("=" * 60)
    
    # 初始化 OCR
    ocr = DeepSeekOCR()
    
    # 测试图像
    image_path = "test_image.jpg"
    
    if not os.path.exists(image_path):
        print(f"\n请准备一张测试图像并保存为: {image_path}")
        return
    
    # 使用自定义提示词
    custom_prompt = "<<image>>\nDescribe this image in detail, focusing on text content."
    
    print(f"\n使用自定义提示词识别: {image_path}")
    print(f"提示词: {custom_prompt}")
    result = ocr.recognize(image_path, prompt=custom_prompt)
    print("\n识别结果:")
    print("-" * 60)
    print(result)
    print("-" * 60)


def demo_supported_prompts():
    """显示所有支持的提示词模板"""
    print("\n" + "=" * 60)
    print("支持的提示词模板")
    print("=" * 60)
    
    for key, prompt in SUPPORTED_PROMPTS.items():
        print(f"\n{key}:")
        print(f"  {prompt}")


def main():
    """主函数"""
    print("\nDeepSeek-OCR 基础使用示例\n")
    
    # 显示支持的提示词
    demo_supported_prompts()
    
    # 运行基础示例（需要准备测试图像）
    print("\n提示: 请准备测试图像后运行以下示例:")
    print("  - test_image.jpg (普通图像)")
    print("  - test_document.jpg (文档图像)")
    print("  - test_figure.jpg (图表图像)")
    print("  - image1.jpg, image2.jpg, image3.jpg (批量测试)")
    
    # 如果有测试图像，可以取消注释运行
    # demo_basic_ocr()
    # demo_markdown_conversion()
    # demo_figure_parsing()
    # demo_batch_recognition()
    # demo_custom_prompt()


if __name__ == "__main__":
    main()
