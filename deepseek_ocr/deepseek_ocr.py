"""DeepSeek-OCR 主接口模块

提供简单易用的 OCR 识别功能，支持图像和 PDF 文档。
"""

import os
import logging
from typing import Optional, Union, List, Dict, Any
from pathlib import Path
import torch

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# 默认模型存储路径
DEFAULT_MODEL_DIR = "/Users/lifeng/data/models"

# 支持的分辨率模式
SUPPORTED_MODES = {
    "tiny": {"size": 512, "tokens": 64, "description": "最小模式 512×512"},
    "small": {"size": 640, "tokens": 100, "description": "小型模式 640×640"},
    "base": {"size": 1024, "tokens": 256, "description": "基础模式 1024×1024"},
    "large": {"size": 1280, "tokens": 400, "description": "大型模式 1280×1280"},
}

# 预设提示词模板
SUPPORTED_PROMPTS = {
    "markdown": "<<image>>\n<<|grounding|>>Convert the document to markdown.",
    "ocr": "<<image>>\n<<|grounding|>>OCR this image.",
    "free_ocr": "<<image>>\nFree OCR.",
    "parse_figure": "<<image>>\nParse the figure.",
    "describe": "<<image>>\nDescribe this image in detail.",
}


class DeepSeekOCR:
    """DeepSeek-OCR 主类
    
    提供图像和 PDF 文档的 OCR 识别功能。
    
    参数:
        model_name: 模型名称，默认 'deepseek-ai/DeepSeek-OCR'
        model_dir: 模型缓存目录
        device: 运行设备 ('cuda', 'cpu', 'mps')
        base_size: 基础图像尺寸，默认 1024
        image_size: 图像块尺寸，默认 640
        crop_mode: 是否使用裁剪模式，默认 True
        use_flash_attention: 是否使用 Flash Attention 2
        hub: 模型源 ('modelscope' 或 'huggingface')
    
    示例:
        >>> ocr = DeepSeekOCR()
        >>> result = ocr.recognize("document.jpg")
        >>> print(result)
    """

    def __init__(
        self,
        model_name: str = "deepseek-ai/DeepSeek-OCR-2",
        model_dir: str = DEFAULT_MODEL_DIR,
        device: Optional[str] = None,
        base_size: int = 1024,
        image_size: int = 1024,
        crop_mode: bool = False,
        use_flash_attention: bool = False,
        hub: str = "modelscope",
        use_local_model: bool = True,
    ):
        self.model_dir = model_dir
        self.base_size = base_size
        self.image_size = image_size
        self.crop_mode = crop_mode
        self.use_flash_attention = use_flash_attention
        self.hub = hub
        self.use_local_model = use_local_model
        
        # 如果使用本地模型，直接使用本地路径
        if use_local_model:
            local_path = os.path.join(model_dir, model_name)
            if os.path.exists(local_path):
                self.model_name = local_path
                logging.info(f"使用本地模型: {local_path}")
            else:
                self.model_name = model_name
                logging.warning(f"本地模型不存在: {local_path}，将使用远程模型")
        else:
            self.model_name = model_name
        
        # 自动检测设备 - 优先使用 CPU（MPS 在某些情况下有兼容性问题）
        if device is None:
            if torch.cuda.is_available():
                self.device = "cuda"
            else:
                # 强制使用 CPU，避免 MPS 兼容性问题
                self.device = "cpu"
                logging.info("使用 CPU 设备（避免 MPS 兼容性问题）")
        else:
            self.device = device
            
        self.model = None
        self.tokenizer = None
        
        # 延迟加载模型
        self._load_model()

    def _get_dtype(self):
        """获取数据类型"""
        if self.device == "cuda":
            return torch.bfloat16
        else:
            # CPU 和 MPS 使用 float32
            return torch.float32

    def _load_model(self):
        """加载模型"""
        from transformers import AutoModel, AutoTokenizer
        
        logging.info(f"正在加载模型: {self.model_name}")
        logging.info(f"设备: {self.device}")
        
        # 如果不是本地模型且使用 modelscope，则下载
        if not self.use_local_model or not os.path.exists(self.model_name):
            if self.hub == "modelscope":
                logging.info(f"使用 {self.hub} 下载模型")
                model_local_path = self._download_model_with_modelscope()
            else:
                model_local_path = self.model_name
        else:
            model_local_path = self.model_name
        
        # 加载分词器
        logging.info("加载分词器...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_local_path,
            trust_remote_code=True,
        )
        logging.info("分词器加载成功")
        
        # 加载模型
        logging.info("加载模型...")
        load_kwargs = {
            "trust_remote_code": True,
            "use_safetensors": True,
        }
        
        # 非 CUDA 设备强制使用 float32
        if self.device != "cuda":
            load_kwargs["torch_dtype"] = torch.float32
            logging.info("使用 float32 数据类型")
        
        # 设置 Flash Attention（仅 CUDA）
        if self.use_flash_attention and self.device == "cuda":
            try:
                load_kwargs["_attn_implementation"] = "flash_attention_2"
                logging.info("启用 Flash Attention 2")
            except Exception as e:
                logging.warning(f"Flash Attention 2 不可用: {e}")
        
        self.model = AutoModel.from_pretrained(
            model_local_path,
            **load_kwargs,
        )
        logging.info("模型加载成功")
        
        # 设置为评估模式
        self.model = self.model.eval()
        
        # 对于非 CUDA 设备，强制转换所有参数为 float32
        if self.device != "cuda":
            logging.info("转换模型参数为 float32...")
            def convert_to_float32(module):
                for param in module.parameters():
                    param.data = param.data.to(torch.float32)
                for buffer_name, buffer in module.named_buffers():
                    if buffer is not None:
                        module._buffers[buffer_name] = buffer.to(torch.float32)
            
            convert_to_float32(self.model)
            logging.info("所有模型参数已转换为 float32")
        
        # 移动到目标设备
        logging.info(f"将模型移动到 {self.device} 设备...")
        self.model = self.model.to(self.device)
        
        logging.info("✅ 模型加载完成！")

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
        
        return model_dir

    def recognize(
        self,
        image_path: str,
        prompt: Optional[str] = None,
        prompt_type: str = "markdown",
        output_path: Optional[str] = None,
        save_results: bool = True,
        test_compress: bool = True,
    ) -> str:
        """识别单张图像
        
        参数:
            image_path: 图像文件路径
            prompt: 自定义提示词（可选）
            prompt_type: 预设提示词类型 ('markdown', 'ocr', 'free_ocr', 'parse_figure', 'describe')
            output_path: 输出目录路径（可选）
            save_results: 是否保存结果
            test_compress: 是否测试压缩
        
        Returns:
            str: 识别结果文本
        
        示例:
            >>> ocr = DeepSeekOCR()
            >>> result = ocr.recognize("document.jpg")
            >>> print(result)
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图像文件不存在: {image_path}")
        
        # 使用自定义提示词或预设提示词
        if prompt is None:
            prompt = SUPPORTED_PROMPTS.get(prompt_type, SUPPORTED_PROMPTS["markdown"])
        
        logging.info(f"识别图像: {image_path}")
        logging.info(f"使用提示词类型: {prompt_type}")
        
        # 创建临时输出目录
        import tempfile
        if output_path is None:
            output_path = tempfile.mkdtemp()
            temp_dir_created = True
        else:
            temp_dir_created = False
            os.makedirs(output_path, exist_ok=True)
        
        try:
            # 执行推理
            logging.info("开始推理...")
            result = self.model.infer(
                tokenizer=self.tokenizer,
                prompt=prompt,
                image_file=image_path,
                output_path=output_path,
                base_size=self.base_size,
                image_size=self.image_size,
                crop_mode=self.crop_mode,
                save_results=save_results,
                test_compress=test_compress,
                eval_mode=True,  # 必须设置为 True 才能返回结果
            )
            
            if result is None:
                logging.error("模型返回了 None，可能是推理失败")
                raise RuntimeError("模型推理返回 None")
            
            logging.info("✅ 推理完成")
            return result
            
        finally:
            # 清理临时目录
            if temp_dir_created and os.path.exists(output_path):
                import shutil
                try:
                    shutil.rmtree(output_path)
                    logging.debug(f"已删除临时目录: {output_path}")
                except Exception as e:
                    logging.warning(f"清理临时目录失败: {e}")

    def recognize_pdf(
        self,
        pdf_path: str,
        prompt: Optional[str] = None,
        prompt_type: str = "markdown",
        output_dir: Optional[str] = None,
        save_results: bool = True,
    ) -> List[str]:
        """识别 PDF 文档
        
        参数:
            pdf_path: PDF 文件路径
            prompt: 自定义提示词（可选）
            prompt_type: 预设提示词类型
            output_dir: 输出目录路径（可选）
            save_results: 是否保存结果
        
        Returns:
            List[str]: 每页的识别结果列表
        
        示例:
            >>> ocr = DeepSeekOCR()
            >>> results = ocr.recognize_pdf("document.pdf")
            >>> for i, result in enumerate(results):
            ...     print(f"第 {i+1} 页: {result}")
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF 文件不存在: {pdf_path}")
        
        # 将 PDF 转换为图像
        try:
            from pdf2image import convert_from_path
        except ImportError:
            raise ImportError("请安装 pdf2image: pip install pdf2image")
        
        logging.info(f"转换 PDF: {pdf_path}")
        images = convert_from_path(pdf_path)
        
        results = []
        for i, image in enumerate(images):
            logging.info(f"识别第 {i+1}/{len(images)} 页")
            
            # 保存临时图像
            temp_image_path = f"/tmp/pdf_page_{i}.jpg"
            image.save(temp_image_path, "JPEG")
            
            # 识别
            result = self.recognize(
                temp_image_path,
                prompt=prompt,
                prompt_type=prompt_type,
                output_path=output_dir,
                save_results=save_results,
            )
            results.append(result)
            
            # 删除临时文件
            os.remove(temp_image_path)
        
        logging.info(f"PDF 识别完成，共 {len(results)} 页")
        return results

    def batch_recognize(
        self,
        image_paths: List[str],
        prompt: Optional[str] = None,
        prompt_type: str = "markdown",
        output_dir: Optional[str] = None,
    ) -> List[str]:
        """批量识别图像
        
        参数:
            image_paths: 图像文件路径列表
            prompt: 自定义提示词（可选）
            prompt_type: 预设提示词类型
            output_dir: 输出目录路径（可选）
        
        Returns:
            List[str]: 识别结果列表
        
        示例:
            >>> ocr = DeepSeekOCR()
            >>> images = ["img1.jpg", "img2.jpg", "img3.jpg"]
            >>> results = ocr.batch_recognize(images)
        """
        results = []
        for i, image_path in enumerate(image_paths):
            logging.info(f"批量识别 {i+1}/{len(image_paths)}: {image_path}")
            try:
                result = self.recognize(
                    image_path,
                    prompt=prompt,
                    prompt_type=prompt_type,
                    output_path=output_dir,
                )
                results.append(result)
            except Exception as e:
                logging.error(f"识别失败 {image_path}: {e}")
                results.append(f"ERROR: {e}")
        
        return results

    def __repr__(self):
        return f"DeepSeekOCR(model={self.model_name}, device={self.device})"


def recognize(
    image_path: str,
    prompt_type: str = "markdown",
    **kwargs,
) -> str:
    """快捷函数：识别单张图像
    
    参数:
        image_path: 图像文件路径
        prompt_type: 提示词类型
        **kwargs: 其他参数传递给 DeepSeekOCR
    
    Returns:
        str: 识别结果
    
    示例:
        >>> from ocr import recognize
        >>> result = recognize("document.jpg")
    """
    ocr = DeepSeekOCR(**kwargs)
    return ocr.recognize(image_path, prompt_type=prompt_type)


def recognize_pdf(
    pdf_path: str,
    prompt_type: str = "markdown",
    **kwargs,
) -> List[str]:
    """快捷函数：识别 PDF 文档
    
    参数:
        pdf_path: PDF 文件路径
        prompt_type: 提示词类型
        **kwargs: 其他参数传递给 DeepSeekOCR
    
    Returns:
        List[str]: 识别结果列表
    
    示例:
        >>> from ocr import recognize_pdf
        >>> results = recognize_pdf("document.pdf")
    """
    ocr = DeepSeekOCR(**kwargs)
    return ocr.recognize_pdf(pdf_path, prompt_type=prompt_type)
