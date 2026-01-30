"""Qwen3-TTS 语音合成库

基于 Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice 的高级封装。

快速开始:
    >>> from tts import QwenTTS
    >>> tts = QwenTTS()
    >>> tts.speak("你好，世界！", output_path="output.wav")
"""

from .qwen_tts import (
    QwenTTS,
    speak,
    SUPPORTED_SPEAKERS,
    SUPPORTED_LANGUAGES,
    DEFAULT_MODEL_DIR,
)

__version__ = "0.1.0"
__all__ = [
    "QwenTTS",
    "speak",
    "SUPPORTED_SPEAKERS",
    "SUPPORTED_LANGUAGES",
    "DEFAULT_MODEL_DIR",
]
