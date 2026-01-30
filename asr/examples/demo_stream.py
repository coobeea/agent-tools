"""Fun-ASR 流式识别示例

演示实时流式语音识别功能。
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from asr import FunASR


def main():
    """流式识别示例"""
    
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("用法: python demo_stream.py <音频文件路径>")
        print("示例: python demo_stream.py long_audio.wav")
        return
    
    audio_path = sys.argv[1]
    
    if not os.path.exists(audio_path):
        print(f"错误: 文件不存在 - {audio_path}")
        return
    
    # 初始化 ASR
    print("正在初始化 Fun-ASR...")
    asr = FunASR(
        model_name="FunAudioLLM/Fun-ASR-Nano-2512",
    )
    print(f"模型加载完成: {asr}")
    
    # 流式识别
    print(f"\n开始流式识别: {audio_path}")
    print("-" * 50)
    
    for idx, partial_result in enumerate(asr.transcribe_stream(
        audio_path,
        chunk_size=0.72,  # 每 0.72 秒处理一次
        language="中文",
    )):
        print(f"[{idx + 1}] {partial_result}")
    
    print("-" * 50)
    print("识别完成")


if __name__ == "__main__":
    main()
