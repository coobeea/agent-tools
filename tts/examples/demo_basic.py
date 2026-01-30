"""Qwen3-TTS 基础使用示例

演示基本的语音合成功能。
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tts import QwenTTS, SUPPORTED_SPEAKERS


def main():
    """基础使用示例"""
    
    # 初始化 TTS
    print("正在初始化 Qwen3-TTS...")
    tts = QwenTTS()
    print(f"模型加载完成: {tts}")
    
    # 示例 1: 基本语音合成
    print("\n=== 示例 1: 基本语音合成 ===")
    wavs, sr = tts.speak(
        text="你好，我是 Qwen3 语音合成模型，很高兴为你服务！",
        speaker="Vivian",
        language="Chinese",
        output_path="output_basic.wav",
    )
    print(f"采样率: {sr} Hz")
    print("音频已保存到: output_basic.wav")
    
    # 示例 2: 带情感控制
    print("\n=== 示例 2: 带情感控制 ===")
    tts.speak_with_emotion(
        text="今天真是太开心了！",
        emotion="开心",
        speaker="Serena",
        output_path="output_happy.wav",
    )
    print("开心语气音频已保存到: output_happy.wav")
    
    # 示例 3: 英文语音
    print("\n=== 示例 3: 英文语音合成 ===")
    tts.speak(
        text="Hello! I am Qwen3 Text-to-Speech model. Nice to meet you!",
        speaker="Ryan",
        language="English",
        instruct="Very friendly and energetic",
        output_path="output_english.wav",
    )
    print("英文音频已保存到: output_english.wav")
    
    # 示例 4: 指令控制
    print("\n=== 示例 4: 指令控制 ===")
    tts.speak(
        text="这件事情让我非常生气！",
        speaker="Uncle_Fu",
        language="Chinese",
        instruct="用愤怒的语气说，说话速度稍快",
        output_path="output_angry.wav",
    )
    print("愤怒语气音频已保存到: output_angry.wav")
    
    # 显示支持的音色
    print("\n=== 支持的音色 ===")
    for name, info in SUPPORTED_SPEAKERS.items():
        print(f"  - {name}: {info['description']} ({info['language']})")


if __name__ == "__main__":
    main()
