#!/bin/bash
#
# Qwen3-TTS 语音合成脚本
# 自动使用独立虚拟环境
#
# 用法：
#   ./tts_speak.sh "你好，世界！" output.wav
#   /path/to/tts_speak.sh "Hello" output.wav Ryan English

# 脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 虚拟环境路径
VENV_PATH="$SCRIPT_DIR/tts_env"

# Python 脚本路径
PYTHON_SCRIPT="$SCRIPT_DIR/tts_speak.py"

# 检查参数
if [ $# -lt 2 ]; then
    echo "用法: $0 <文本> <输出文件> [音色] [语言]"
    echo ""
    echo "示例:"
    echo "  $0 '你好，世界！' output.wav"
    echo "  $0 'Hello World' output.wav Ryan English"
    echo ""
    echo "可用音色:"
    echo "  Vivian, Serena, Uncle_Fu, Dylan, Eric (中文)"
    echo "  Ryan, Aiden (English)"
    echo "  Ono_Anna (Japanese), Sohee (Korean)"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ 错误：虚拟环境不存在: $VENV_PATH"
    echo "请先运行 setup_env.sh 创建虚拟环境"
    exit 1
fi

# 检查 Python 脚本
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ 错误：Python 脚本不存在: $PYTHON_SCRIPT"
    exit 1
fi

# 激活虚拟环境并执行 Python 脚本
source "$VENV_PATH/bin/activate"
python "$PYTHON_SCRIPT" "$@"
exit_code=$?

# 退出虚拟环境
deactivate

exit $exit_code
