"""Fun-ASR 语音识别封装库

基于 FunAudioLLM/Fun-ASR-Nano-2512 的高级封装，提供简洁易用的语音识别接口。

支持特性:
- 中文、英文、日文语音识别
- 中文 7 种方言和 26 种地域口音支持
- 热词增强
- 实时流式识别
- VAD 语音端点检测

使用示例:
    >>> from asr import FunASR
    >>> asr = FunASR()
    >>> result = asr.transcribe("audio.wav", language="中文")
    >>> print(result)
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
    "中文", "英文", "日文",
]

# 多语言版本支持的语言
SUPPORTED_LANGUAGES_MLT = [
    "中文", "英文", "粤语", "日文", "韩文", "越南语", "印尼语", "泰语", "马来语",
    "菲律宾语", "阿拉伯语", "印地语", "保加利亚语", "克罗地亚语", "捷克语",
    "丹麦语", "荷兰语", "爱沙尼亚语", "芬兰语", "希腊语", "匈牙利语", "爱尔兰语",
    "拉脱维亚语", "立陶宛语", "马耳他语", "波兰语", "葡萄牙语", "罗马尼亚语",
    "斯洛伐克语", "斯洛文尼亚语", "瑞典语",
]


class FunASR:
    """Fun-ASR 语音识别类
    
    基于通义实验室推出的端到端语音识别大模型，具备强大的上下文理解能力与行业适应性。
    
    Attributes:
        model_name: 模型名称
        device: 运行设备 (cuda/mps/cpu)
        model_dir: 模型存储目录
        use_vad: 是否启用 VAD
    """
    
    def __init__(
        self,
        model_name: str = "FunAudioLLM/Fun-ASR-Nano-2512",
        device: Optional[str] = None,
        model_dir: str = DEFAULT_MODEL_DIR,
        use_vad: bool = False,
        vad_max_segment_time: int = 30000,
        hub: str = "ms",
    ):
        """初始化 Fun-ASR
        
        Args:
            model_name: 模型名称，可选:
                - "FunAudioLLM/Fun-ASR-Nano-2512": 基础版，支持中英日
                - "FunAudioLLM/Fun-ASR-MLT-Nano-2512": 多语言版，支持 31 种语言
            device: 运行设备，默认自动选择 (cuda > mps > cpu)
            model_dir: 模型存储目录
            use_vad: 是否启用 VAD（语音活动检测）
            vad_max_segment_time: VAD 最大片段时长（毫秒）
            hub: 模型下载源，"ms" 为 ModelScope，"hf" 为 HuggingFace
        """
        self.model_name = model_name
        self.model_dir = model_dir
        self.use_vad = use_vad
        self.vad_max_segment_time = vad_max_segment_time
        self.hub = hub
        
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
        self.model_direct = None
        self.kwargs = None
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
        
    def _load_model(self):
        """加载模型"""
        from funasr import AutoModel
        
        # 获取当前脚本目录，用于加载 model.py
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_py_path = os.path.join(current_dir, "model.py")
        
        logging.info(f"正在加载模型: {self.model_name}")
        logging.info(f"设备: {self.device}")
        
        if self.use_vad:
            self.model = AutoModel(
                model=self.model_name,
                trust_remote_code=True,
                vad_model="fsmn-vad",
                vad_kwargs={"max_single_segment_time": self.vad_max_segment_time},
                remote_code=model_py_path,
                device=self.device,
                hub=self.hub,
            )
        else:
            self.model = AutoModel(
                model=self.model_name,
                trust_remote_code=True,
                remote_code=model_py_path,
                device=self.device,
                hub=self.hub,
            )
            
        logging.info("模型加载完成")
        
    def transcribe(
        self,
        audio: Union[str, np.ndarray, torch.Tensor, List[str]],
        language: str = "中文",
        hotwords: Optional[List[str]] = None,
        itn: bool = True,
        batch_size: int = 1,
    ) -> Union[str, List[str]]:
        """语音转文字
        
        Args:
            audio: 音频输入，支持:
                - 文件路径 (str)
                - 文件路径列表 (List[str])
                - numpy 数组
                - torch 张量
            language: 目标语言，默认 "中文"
                - Fun-ASR-Nano: 支持 "中文"、"英文"、"日文"
                - Fun-ASR-MLT-Nano: 支持 31 种语言
            hotwords: 热词列表，用于提高特定词汇的识别准确率
            itn: 是否进行文本规整（数字、日期等标准化）
            batch_size: 批处理大小
            
        Returns:
            识别结果文本，如果输入是列表则返回列表
        """
        if hotwords is None:
            hotwords = []
            
        # 处理输入
        if isinstance(audio, str):
            inputs = [audio]
            single_input = True
        elif isinstance(audio, list):
            inputs = audio
            single_input = False
        else:
            # numpy 或 torch 张量
            inputs = [audio]
            single_input = True
            
        # 执行识别
        results = self.model.generate(
            input=inputs,
            cache={},
            batch_size=batch_size,
            hotwords=hotwords,
            language=language,
            itn=itn,
        )
        
        # 提取文本
        texts = [r["text"] for r in results]
        
        if single_input:
            return texts[0]
        return texts
    
    def transcribe_stream(
        self,
        audio_path: str,
        chunk_size: float = 0.72,
        language: str = "中文",
        hotwords: Optional[List[str]] = None,
        itn: bool = True,
    ):
        """流式语音识别
        
        对长音频进行分块流式识别，适用于实时转写场景。
        
        Args:
            audio_path: 音频文件路径
            chunk_size: 每次处理的音频块大小（秒）
            language: 目标语言
            hotwords: 热词列表
            itn: 是否进行文本规整
            
        Yields:
            每个音频块的识别结果
        """
        from .model import FunASRNano
        from .tools.utils import load_audio
        
        if hotwords is None:
            hotwords = []
            
        # 加载直接推理模型（如果尚未加载）
        if self.model_direct is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.model_direct, self.kwargs = FunASRNano.from_pretrained(
                model=self.model_name,
                device=self.device,
            )
            self.model_direct.eval()
            
        tokenizer = self.kwargs.get("tokenizer", None)
        
        # 获取音频时长
        duration = sf.info(audio_path).duration
        cum_durations = np.arange(chunk_size, duration + chunk_size, chunk_size)
        
        prev_text = ""
        for idx, cum_duration in enumerate(cum_durations):
            audio, rate = load_audio(audio_path, 16000, duration=round(cum_duration, 3))
            
            result = self.model_direct.inference(
                [torch.tensor(audio)],
                prev_text=prev_text,
                hotwords=hotwords,
                language=language,
                itn=itn,
                **self.kwargs,
            )
            
            prev_text = result[0][0]["text"]
            
            # 处理中间结果
            if idx != len(cum_durations) - 1:
                prev_text = tokenizer.decode(tokenizer.encode(prev_text)[:-5]).replace("", "")
                
            if prev_text:
                yield prev_text
                
    def transcribe_file(
        self,
        audio_path: str,
        language: str = "中文",
        hotwords: Optional[List[str]] = None,
        itn: bool = True,
    ) -> dict:
        """转写音频文件（返回详细结果）
        
        Args:
            audio_path: 音频文件路径
            language: 目标语言
            hotwords: 热词列表
            itn: 是否进行文本规整
            
        Returns:
            dict: 包含以下字段:
                - text: 识别文本
                - text_tn: 规整后的文本
                - duration: 音频时长
        """
        if hotwords is None:
            hotwords = []
            
        # 获取音频信息
        info = sf.info(audio_path)
        
        # 执行识别
        results = self.model.generate(
            input=[audio_path],
            cache={},
            batch_size=1,
            hotwords=hotwords,
            language=language,
            itn=itn,
        )
        
        result = results[0]
        result["duration"] = info.duration
        result["sample_rate"] = info.samplerate
        
        return result
    
    @property
    def supported_languages(self) -> List[str]:
        """获取支持的语言列表"""
        if "MLT" in self.model_name:
            return SUPPORTED_LANGUAGES_MLT
        return SUPPORTED_LANGUAGES
    
    def __repr__(self):
        return f"FunASR(model={self.model_name}, device={self.device}, vad={self.use_vad})"


def transcribe(
    audio: Union[str, np.ndarray, torch.Tensor],
    language: str = "中文",
    hotwords: Optional[List[str]] = None,
    itn: bool = True,
    device: Optional[str] = None,
) -> str:
    """便捷函数：语音转文字
    
    Args:
        audio: 音频输入（文件路径、numpy 数组或 torch 张量）
        language: 目标语言
        hotwords: 热词列表
        itn: 是否进行文本规整
        device: 运行设备
        
    Returns:
        识别结果文本
    """
    asr = FunASR(device=device)
    return asr.transcribe(audio, language=language, hotwords=hotwords, itn=itn)


if __name__ == "__main__":
    # 简单测试
    import sys
    
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
        asr = FunASR()
        result = asr.transcribe(audio_path, language="中文")
        print(f"识别结果: {result}")
    else:
        print("用法: python fun_asr.py <音频文件路径>")
        print("\n支持的语言:")
        for lang in SUPPORTED_LANGUAGES:
            print(f"  - {lang}")
