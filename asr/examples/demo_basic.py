"""Fun-ASR 基础使用示例

演示基本的语音识别功能。
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from asr import FunASR


def main():
    """基础使用示例"""
    
    # 初始化 ASR
    print("正在初始化 Fun-ASR...")
    asr = FunASR(
        model_name="FunAudioLLM/Fun-ASR-Nano-2512",
        # model_dir="/Users/lifeng/data/models",  # 模型存储目录
        # device="cuda:0",  # 或 "mps", "cpu"
        # hub="ms",  # ModelScope，或 "hf" 使用 HuggingFace
    )
    print(f"模型加载完成: {asr}")
    
    # 示例 1: 基本语音识别
    print("\n=== 示例 1: 基本语音识别 ===")
    audio_path = "test.wav"  # 替换为实际音频文件
    if os.path.exists(audio_path):
        result = asr.transcribe(audio_path, language="中文")
        print(f"识别结果: {result}")
    else:
        print(f"请提供音频文件: {audio_path}")
    
    # 示例 2: 使用热词增强
    print("\n=== 示例 2: 使用热词增强 ===")
    hotwords = ["人工智能", "深度学习", "语音识别"]
    if os.path.exists(audio_path):
        result = asr.transcribe(
            audio_path,
            language="中文",
            hotwords=hotwords,
            itn=True,  # 启用文本规整
        )
        print(f"识别结果: {result}")
    
    # 示例 3: 英文识别
    print("\n=== 示例 3: 英文识别 ===")
    english_audio = "english.wav"  # 替换为实际英文音频
    if os.path.exists(english_audio):
        result = asr.transcribe(english_audio, language="英文")
        print(f"英文识别结果: {result}")
    
    # 示例 4: 批量识别
    print("\n=== 示例 4: 批量识别 ===")
    audio_files = ["audio1.wav", "audio2.wav", "audio3.wav"]
    existing_files = [f for f in audio_files if os.path.exists(f)]
    if existing_files:
        results = asr.transcribe(existing_files, language="中文")
        for path, text in zip(existing_files, results):
            print(f"{path}: {text}")
    
    # 显示支持的语言
    print("\n=== 支持的语言 ===")
    for lang in asr.supported_languages:
        print(f"  - {lang}")


if __name__ == "__main__":
    main()
