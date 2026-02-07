"""DeepSeek-OCR 光学字符识别库

基于 deepseek-ai/DeepSeek-OCR-2 的高级封装。

快速开始:
    >>> from ocr import DeepSeekOCR
    >>> ocr = DeepSeekOCR()
    >>> result = ocr.recognize("document.jpg")
"""

from .deepseek_ocr import (
    DeepSeekOCR,
    recognize,
    recognize_pdf,
    SUPPORTED_MODES,
    SUPPORTED_PROMPTS,
    DEFAULT_MODEL_DIR,
)

from .output_formatter import (
    OutputFormatter,
    save_as_markdown,
    save_as_text,
)

__version__ = "0.1.0"
__all__ = [
    "DeepSeekOCR",
    "recognize",
    "recognize_pdf",
    "SUPPORTED_MODES",
    "SUPPORTED_PROMPTS",
    "DEFAULT_MODEL_DIR",
    "OutputFormatter",
    "save_as_markdown",
    "save_as_text",
]
