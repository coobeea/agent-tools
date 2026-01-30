"""Fun-ASR 语音识别库

基于 FunAudioLLM/Fun-ASR-Nano-2512 的高级封装。

快速开始:
    >>> from asr import FunASR
    >>> asr = FunASR()
    >>> result = asr.transcribe("audio.wav", language="中文")
"""

from .fun_asr import (
    FunASR,
    transcribe,
    SUPPORTED_LANGUAGES,
    SUPPORTED_LANGUAGES_MLT,
    DEFAULT_MODEL_DIR,
)

__version__ = "0.1.0"
__all__ = [
    "FunASR",
    "transcribe",
    "SUPPORTED_LANGUAGES",
    "SUPPORTED_LANGUAGES_MLT",
    "DEFAULT_MODEL_DIR",
]
