"""Fun-ASR VAD 示例

演示带有语音端点检测的语音识别。
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from asr import FunASR


def main():
    """VAD 示例"""
    
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("用法: python demo_vad.py <音频文件路径>")
        print("示例: python demo_vad.py meeting_recording.wav")
        return
    
    audio_path = sys.argv[1]
    
    if not os.path.exists(audio_path):
        print(f"错误: 文件不存在 - {audio_path}")
        return
    
    # 初始化带 VAD 的 ASR
    print("正在初始化 Fun-ASR (带 VAD)...")
    asr = FunASR(
        model_name="FunAudioLLM/Fun-ASR-Nano-2512",
        use_vad=True,  # 启用 VAD
        vad_max_segment_time=30000,  # 最大片段时长 30 秒
    )
    print(f"模型加载完成: {asr}")
    
    # 识别
    print(f"\n开始识别: {audio_path}")
    print("-" * 50)
    
    result = asr.transcribe_file(
        audio_path,
        language="中文",
        itn=True,
    )
    
    print(f"音频时长: {result.get('duration', 'N/A'):.2f} 秒")
    print(f"采样率: {result.get('sample_rate', 'N/A')} Hz")
    print(f"\n识别结果:\n{result['text']}")
    
    if "text_tn" in result:
        print(f"\n规整后文本:\n{result['text_tn']}")
    
    print("-" * 50)


if __name__ == "__main__":
    main()
