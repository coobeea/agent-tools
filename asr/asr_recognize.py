#!/usr/bin/env python3
"""
Fun-ASR 语音识别脚本

简单用法：
    python asr_recognize.py audio.wav output.txt
"""

import sys
import os

# 添加路径
sys.path.insert(0, '/Users/lifeng/git/git_agents/agent-tools')

from asr import FunASR


def recognize_audio(input_file, output_file, language="中文"):
    """识别音频并保存文本"""
    
    # 检查输入文件
    if not os.path.exists(input_file):
        print(f"❌ 错误：输入文件不存在: {input_file}")
        return False
    
    # 初始化 ASR
    print(f"⏳ 初始化 Fun-ASR...")
    asr = FunASR()
    print(f"✅ 模型加载完成")
    
    # 识别
    print(f"⏳ 识别音频: {input_file}")
    print(f"   语言: {language}")
    
    result = asr.transcribe(input_file, language=language)
    
    # 提取文本
    if isinstance(result, dict):
        text = result.get('text', str(result))
    else:
        text = str(result)
    
    # 保存
    print(f"⏳ 保存到: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"✅ 完成！识别了 {len(text)} 字符")
    print(f"\n识别结果:")
    print(text)
    
    return True


def main():
    """主函数"""
    
    # 检查参数
    if len(sys.argv) < 3:
        print("用法: python asr_recognize.py <输入音频> <输出文件> [语言]")
        print()
        print("示例:")
        print("  python asr_recognize.py audio.wav output.txt")
        print("  python asr_recognize.py audio.wav output.txt 英文")
        print()
        print("支持语言:")
        print("  中文（默认）, 英文, 日文")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    language = sys.argv[3] if len(sys.argv) > 3 else "中文"
    
    # 执行识别
    success = recognize_audio(input_file, output_file, language)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
