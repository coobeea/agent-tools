"""Qwen3-TTS 语音合成封装库

基于 Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice 的高级封装，提供简洁易用的语音合成接口。

支持特性:
- 9 种预设音色
- 10 种语言支持
- 指令控制（情感、语速、音调等）
- 流式生成，低延迟

使用示例:
    >>> from tts import QwenTTS
    >>> tts = QwenTTS()
    >>> tts.speak("你好，世界！", speaker="Vivian", output_path="output.wav")
"""

import os
import logging
from typing import List, Optional, Union
from pathlib import Path

import torch
import numpy as np
import soundfile as sf

# 默认模型存储路径
DEFAULT_MODEL_DIR = "/Users/lifeng/data/models"

# 支持的语言列表
SUPPORTED_LANGUAGES = [
    "Chinese", "English", "Japanese", "Korean",
    "German", "French", "Russian", "Portuguese",
    "Spanish", "Italian",
]

# 支持的预设音色
SUPPORTED_SPEAKERS = {
    "Vivian": {"description": "明亮、略带锐利的年轻女声", "language": "Chinese"},
    "Serena": {"description": "温暖、温柔的年轻女声", "language": "Chinese"},
    "Uncle_Fu": {"description": "成熟男声，低沉圆润", "language": "Chinese"},
    "Dylan": {"description": "年轻的北京男声，清晰自然", "language": "Chinese"},
    "Eric": {"description": "活泼的成都男声，略带沙哑", "language": "Chinese"},
    "Ryan": {"description": "动感男声，节奏感强", "language": "English"},
    "Aiden": {"description": "阳光美式男声，中音清晰", "language": "English"},
    "Ono_Anna": {"description": "俏皮日本女声，轻盈灵动", "language": "Japanese"},
    "Sohee": {"description": "温暖韩国女声，情感丰富", "language": "Korean"},
}


class QwenTTS:
    """Qwen3-TTS 语音合成类
    
    基于阿里千问团队开源的语音合成大模型，支持多语言、多音色、指令控制。
    
    Attributes:
        model_name: 模型名称
        device: 运行设备 (cuda/mps/cpu)
        model_dir: 模型存储目录
    """
    
    def __init__(
        self,
        model_name: str = "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
        device: Optional[str] = None,
        model_dir: str = DEFAULT_MODEL_DIR,
        dtype: str = "bfloat16",
        use_flash_attention: bool = False,
    ):
        """初始化 Qwen3-TTS
        
        Args:
            model_name: 模型名称，可选:
                - "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice": 自定义音色版（推荐）
                - "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign": 语音设计版
                - "Qwen/Qwen3-TTS-12Hz-1.7B-Base": 基础版（支持语音克隆）
                - "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice": 轻量版
            device: 运行设备，默认自动选择 (cuda > mps > cpu)
            model_dir: 模型存储目录
            dtype: 数据类型，"bfloat16" 或 "float16" 或 "float32"
            use_flash_attention: 是否使用 FlashAttention2 加速（需要安装 flash-attn）
        """
        self.model_name = model_name
        self.model_dir = model_dir
        self.dtype = dtype
        self.use_flash_attention = use_flash_attention
        
        # 自动选择设备
        if device is None:
            if torch.cuda.is_available():
                self.device = "cuda:0"
            elif torch.backends.mps.is_available():
                self.device = "mps"
            else:
                self.device = "cpu"
        else:
            self.device = device
            
        # 设置模型缓存目录
        self._setup_model_dir()
        
        # 加载模型
        self.model = None
        self.sample_rate = 24000  # Qwen3-TTS 输出采样率
        self._load_model()
        
    def _setup_model_dir(self):
        """设置模型存储目录"""
        os.makedirs(self.model_dir, exist_ok=True)
        
        # 设置 ModelScope 缓存目录
        os.environ["MODELSCOPE_CACHE"] = self.model_dir
        # 设置 HuggingFace 缓存目录
        os.environ["HF_HOME"] = self.model_dir
        os.environ["HUGGINGFACE_HUB_CACHE"] = os.path.join(self.model_dir, "hub")
        
        logging.info(f"模型将存储到: {self.model_dir}")
        
    def _get_dtype(self):
        """获取 torch 数据类型"""
        dtype_map = {
            "bfloat16": torch.bfloat16,
            "float16": torch.float16,
            "float32": torch.float32,
        }
        return dtype_map.get(self.dtype, torch.bfloat16)
        
    def _load_model(self):
        """加载模型"""
        from qwen_tts import Qwen3TTSModel
        
        logging.info(f"正在加载模型: {self.model_name}")
        logging.info(f"设备: {self.device}")
        
        # 首先使用 modelscope 下载模型到本地
        model_local_path = self._download_model_with_modelscope()
        
        # 使用 qwen_tts 包加载本地模型
        load_kwargs = {
            "device_map": self.device,
            "dtype": self._get_dtype(),
        }
        
        if self.use_flash_attention and self.device.startswith("cuda"):
            load_kwargs["attn_implementation"] = "flash_attention_2"
            
        self.model = Qwen3TTSModel.from_pretrained(
            model_local_path,
            **load_kwargs,
        )
        self._use_qwen_tts = True
            
        logging.info("模型加载完成")
    
    def _download_model_with_modelscope(self) -> str:
        """使用 modelscope 下载模型
        
        Returns:
            str: 本地模型路径
        """
        from modelscope import snapshot_download
        
        # 下载模型
        model_dir = snapshot_download(
            self.model_name,
            cache_dir=self.model_dir,
        )
        logging.info(f"模型已下载到: {model_dir}")
        
        # 同时下载 Tokenizer
        tokenizer_name = "Qwen/Qwen3-TTS-Tokenizer-12Hz"
        tokenizer_dir = snapshot_download(
            tokenizer_name,
            cache_dir=self.model_dir,
        )
        logging.info(f"Tokenizer 已下载到: {tokenizer_dir}")
        
        return model_dir
        
    def speak(
        self,
        text: Union[str, List[str]],
        speaker: str = "Vivian",
        language: str = "Chinese",
        instruct: Optional[Union[str, List[str]]] = None,
        output_path: Optional[str] = None,
    ) -> tuple:
        """文字转语音
        
        Args:
            text: 要合成的文本，支持单条或批量
            speaker: 音色名称，可选:
                - 中文: Vivian, Serena, Uncle_Fu, Dylan, Eric
                - 英文: Ryan, Aiden
                - 日语: Ono_Anna
                - 韩语: Sohee
            language: 语言，如 "Chinese", "English", "Japanese" 等
            instruct: 指令控制，如 "用愤怒的语气说", "Very happy", "说话速度快一些" 等
            output_path: 输出文件路径，如果提供则保存到文件
            
        Returns:
            tuple: (音频数据列表, 采样率)
        """
        if not self._use_qwen_tts:
            raise RuntimeError(
                "qwen_tts 包不可用。请使用 Python 3.12 环境安装: pip install qwen-tts\n"
                "或者使用 DashScope API: https://help.aliyun.com/zh/model-studio/qwen-tts-realtime"
            )
        
        # 处理输入
        if isinstance(text, str):
            texts = [text]
            languages = [language]
            speakers = [speaker]
            instructs = [instruct or ""]
        else:
            texts = text
            languages = [language] * len(texts) if isinstance(language, str) else language
            speakers = [speaker] * len(texts) if isinstance(speaker, str) else speaker
            instructs = [instruct or ""] * len(texts) if isinstance(instruct, str) or instruct is None else instruct
        
        # 生成语音
        wavs, sr = self.model.generate_custom_voice(
            text=texts if len(texts) > 1 else texts[0],
            language=languages if len(languages) > 1 else languages[0],
            speaker=speakers if len(speakers) > 1 else speakers[0],
            instruct=instructs if len(instructs) > 1 else instructs[0],
        )
        
        self.sample_rate = sr
        
        # 如果提供了输出路径，保存文件
        if output_path:
            sf.write(output_path, wavs[0], sr)
            logging.info(f"音频已保存到: {output_path}")
            
        return wavs, sr
    
    def speak_with_emotion(
        self,
        text: str,
        emotion: str,
        speaker: str = "Vivian",
        language: str = "Chinese",
        output_path: Optional[str] = None,
    ) -> tuple:
        """带情感控制的语音合成
        
        Args:
            text: 要合成的文本
            emotion: 情感，如 "开心", "愤怒", "悲伤", "惊讶", "温柔" 等
            speaker: 音色名称
            language: 语言
            output_path: 输出文件路径
            
        Returns:
            tuple: (音频数据列表, 采样率)
        """
        # 构建情感指令
        emotion_instructs = {
            "开心": "用开心愉快的语气说",
            "愤怒": "用愤怒的语气说",
            "悲伤": "用悲伤的语气说",
            "惊讶": "用惊讶的语气说",
            "温柔": "用温柔的语气说",
            "兴奋": "用兴奋的语气说",
            "平静": "用平静的语气说",
            "happy": "Very happy",
            "angry": "Very angry",
            "sad": "Very sad",
            "surprised": "Very surprised",
            "gentle": "Very gentle",
        }
        
        instruct = emotion_instructs.get(emotion, f"用{emotion}的语气说")
        
        return self.speak(
            text=text,
            speaker=speaker,
            language=language,
            instruct=instruct,
            output_path=output_path,
        )
    
    def list_speakers(self) -> dict:
        """获取所有支持的音色
        
        Returns:
            dict: 音色信息字典
        """
        return SUPPORTED_SPEAKERS
    
    @property
    def supported_languages(self) -> List[str]:
        """获取支持的语言列表"""
        return SUPPORTED_LANGUAGES
    
    def __repr__(self):
        return f"QwenTTS(model={self.model_name}, device={self.device})"


def speak(
    text: str,
    speaker: str = "Vivian",
    language: str = "Chinese",
    instruct: Optional[str] = None,
    output_path: Optional[str] = None,
    device: Optional[str] = None,
) -> tuple:
    """便捷函数：文字转语音
    
    Args:
        text: 要合成的文本
        speaker: 音色名称
        language: 语言
        instruct: 指令控制
        output_path: 输出文件路径
        device: 运行设备
        
    Returns:
        tuple: (音频数据列表, 采样率)
    """
    tts = QwenTTS(device=device)
    return tts.speak(
        text=text,
        speaker=speaker,
        language=language,
        instruct=instruct,
        output_path=output_path,
    )


if __name__ == "__main__":
    import sys
    
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) > 1:
        text = sys.argv[1]
        output = sys.argv[2] if len(sys.argv) > 2 else "output.wav"
        
        tts = QwenTTS()
        tts.speak(text, output_path=output)
        print(f"音频已保存到: {output}")
    else:
        print("用法: python qwen_tts.py <文本> [输出文件路径]")
        print("\n支持的音色:")
        for name, info in SUPPORTED_SPEAKERS.items():
            print(f"  - {name}: {info['description']} ({info['language']})")
