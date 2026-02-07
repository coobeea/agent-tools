#!/bin/bash
#
# Fun-ASR 语音识别脚本
# 自动使用独立虚拟环境
#
# 用法：
#   ./asr_recognize.sh audio.wav output.txt
#   /path/to/asr_recognize.sh audio.wav output.txt 英文

# 脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 虚拟环境路径
VENV_PATH="$SCRIPT_DIR/asr_env"

# Python 脚本路径
PYTHON_SCRIPT="$SCRIPT_DIR/asr_recognize.py"

# 检查参数
if [ $# -lt 2 ]; then
    echo "用法: $0 <输入音频> <输出文件> [语言]"
    echo ""
    echo "示例:"
    echo "  $0 audio.wav output.txt"
    echo "  $0 audio.wav output.txt 英文"
    echo ""
    echo "支持语言:"
    echo "  中文（默认）, 英文, 日文"
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
