#!/usr/bin/env python3
"""
Qwen3-TTS 语音合成脚本

简单用法：
    python tts_speak.py "你好，世界！" output.wav
"""

import sys
import os

# 添加路径
sys.path.insert(0, '/Users/lifeng/git/git_agents/agent-tools')

from tts.tts_wrapper import QwenTTS


def text_to_speech(text, output_file, speaker="Vivian", language="Chinese"):
    """文字转语音"""
    
    # 初始化 TTS
    print(f"⏳ 初始化 Qwen3-TTS...")
    tts = QwenTTS()
    print(f"✅ 模型加载完成")
    
    # 合成语音
    print(f"⏳ 合成语音: {text[:50]}...")
    print(f"   音色: {speaker}")
    print(f"   语言: {language}")
    
    wavs, sr = tts.speak(
        text=text,
        speaker=speaker,
        language=language,
        output_path=output_file
    )
    
    print(f"✅ 语音已保存到: {output_file}")
    print(f"   采样率: {sr} Hz")
    print(f"   时长: {len(wavs[0]) / sr:.2f} 秒")
    
    return True


def main():
    """主函数"""
    
    # 检查参数
    if len(sys.argv) < 3:
        print("用法: python tts_speak.py <文本> <输出文件> [音色] [语言]")
        print()
        print("示例:")
        print("  python tts_speak.py '你好，世界！' output.wav")
        print("  python tts_speak.py 'Hello World' output.wav Ryan English")
        print()
        print("可用音色:")
        print("  Vivian, Serena, Uncle_Fu, Dylan, Eric")
        print("  Ryan, Aiden (English)")
        print("  Ono_Anna (Japanese), Sohee (Korean)")
        sys.exit(1)
    
    text = sys.argv[1]
    output_file = sys.argv[2]
    speaker = sys.argv[3] if len(sys.argv) > 3 else "Vivian"
    language = sys.argv[4] if len(sys.argv) > 4 else "Chinese"
    
    # 执行合成
    success = text_to_speech(text, output_file, speaker, language)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
