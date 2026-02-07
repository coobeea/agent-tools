#!/usr/bin/env python3
"""GLM-OCR 测试脚本（使用本地模型）"""

import argparse
import time
from PIL import Image
import torch

# 本地模型路径
MODEL_PATH = "/Users/lifeng/data/models/GLM-OCR"

# 默认测试图片
DEFAULT_IMAGE = "/Users/lifeng/data/pdfs_images/images/batch_06/page_058.png"

# 任务提示词
TASK_PROMPTS = {
    "text": "Text Recognition:",
    "formula": "Formula Recognition:",
    "table": "Table Recognition:"
}


def test_glm_ocr(image_path: str, task: str = "text", save_result: bool = True):
    """
    测试 GLM-OCR 模型
    
    Args:
        image_path: 图片路径
        task: 任务类型 (text | formula | table)
        save_result: 是否保存结果
    """
    
    print("=" * 80)
    print("GLM-OCR 测试")
    print("=" * 80)
    print(f"\n📁 模型路径: {MODEL_PATH}")
    print(f"📄 测试图像: {image_path}")
    print(f"🎯 任务类型: {task}")
    print()
    
    start_time = time.time()
    
    # 1. 加载图像
    print("⏳ [1/4] 加载图像...")
    try:
        image = Image.open(image_path).convert("RGB")
        print(f"✅ 图像大小: {image.size}")
    except Exception as e:
        print(f"❌ 加载图像失败: {e}")
        return
    
    # 2. 加载模型
    print("\n⏳ [2/4] 加载模型...")
    try:
        from transformers import AutoProcessor, AutoModelForImageTextToText
        
        # 检测设备
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.bfloat16 if device == "cuda" else torch.float32
        
        print(f"   设备: {device}")
        print(f"   数据类型: {dtype}")
        
        # 加载处理器
        processor = AutoProcessor.from_pretrained(MODEL_PATH)
        print("✅ Processor 加载成功")
        
        # 加载模型（不使用 device_map，手动移动到设备）
        model = AutoModelForImageTextToText.from_pretrained(
            MODEL_PATH,
            torch_dtype=dtype
        )
        model = model.to(device)
        print("✅ 模型加载成功")
        
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    load_time = time.time() - start_time
    print(f"\n⏱️  加载耗时: {load_time:.1f} 秒")
    
    # 3. 准备输入
    print("\n⏳ [3/4] 准备输入...")
    
    # 获取任务提示词
    prompt = TASK_PROMPTS.get(task, "Text Recognition:")
    
    # 构建消息
    messages = [{
        "role": "user",
        "content": [
            {"type": "image", "url": image_path},
            {"type": "text", "text": prompt}
        ]
    }]
    
    try:
        # 应用聊天模板
        inputs = processor.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt"
        ).to(model.device)
        
        # 移除不需要的 token_type_ids
        inputs.pop("token_type_ids", None)
        
        print("✅ 输入准备完成")
        
    except Exception as e:
        print(f"❌ 输入准备失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 4. 推理
    print(f"\n⏳ [4/4] 开始推理（{device.upper()}）...")
    print("   最大生成 tokens: 8192")
    
    infer_start = time.time()
    
    try:
        with torch.no_grad():
            generated_ids = model.generate(**inputs, max_new_tokens=8192)
        
        infer_time = time.time() - infer_start
        print(f"✅ 推理完成（耗时 {infer_time:.1f} 秒）")
        
        # 解码结果
        output_text = processor.decode(
            generated_ids[0][inputs["input_ids"].shape[1]:],
            skip_special_tokens=False
        )
        
        # 显示结果
        print("\n" + "=" * 80)
        print("识别结果:")
        print("=" * 80)
        print(output_text)
        print("=" * 80)
        
        # 保存结果（TXT 和 MD 格式）
        if save_result:
            # 保存为 TXT
            txt_file = f'glm_ocr_result_{task}.txt'
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(output_text)
            print(f"\n💾 结果已保存到: {txt_file}")
            
            # 保存为 MD
            md_file = f'glm_ocr_result_{task}.md'
            with open(md_file, 'w', encoding='utf-8') as f:
                # GLM-OCR 输出通常已经是 Markdown 格式
                f.write(output_text)
            print(f"💾 Markdown 格式已保存到: {md_file}")
        
        # 性能统计
        total_time = time.time() - start_time
        print()
        print("=" * 80)
        print("性能统计:")
        print("=" * 80)
        print(f"  模型加载: {load_time:.1f} 秒")
        print(f"  推理时间: {infer_time:.1f} 秒")
        print(f"  总耗时:   {total_time:.1f} 秒")
        print("=" * 80)
        print("\n✅ 测试完成！")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
    except Exception as e:
        print(f"\n❌ 推理失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GLM-OCR 测试脚本")
    parser.add_argument(
        "--image",
        type=str,
        default=DEFAULT_IMAGE,
        help="图片路径"
    )
    parser.add_argument(
        "--task",
        type=str,
        default="text",
        choices=["text", "formula", "table"],
        help="任务类型 (text | formula | table)"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="不保存结果"
    )
    
    args = parser.parse_args()
    
    test_glm_ocr(
        image_path=args.image,
        task=args.task,
        save_result=not args.no_save
    )
