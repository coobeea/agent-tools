"""OCR 输出格式化工具

提供多种输出格式的清理和转换功能。
"""

import re
from typing import Optional


class OutputFormatter:
    """OCR 输出格式化器"""
    
    @staticmethod
    def clean_markdown(text: str, keep_coordinates: bool = False) -> str:
        """清理 Markdown 输出，移除标注标签
        
        参数:
            text: 原始 OCR 输出文本
            keep_coordinates: 是否保留坐标信息
            
        返回:
            清理后的纯净 Markdown 文本
        """
        if not text:
            return ""
        
        # 移除参考标签 <|ref|>...<|/ref|>
        cleaned = re.sub(r'<\|ref\|>.*?<\|/ref\|>', '', text)
        
        # 处理坐标标签 <|det|>[[...]]<|/det|>
        if keep_coordinates:
            # 保留坐标但简化格式
            cleaned = re.sub(r'<\|det\|>(\[\[.*?\]\])<\|/det\|>', r' `\1`', cleaned)
        else:
            # 完全移除坐标
            cleaned = re.sub(r'<\|det\|>\[\[.*?\]\]<\|/det\|>', '', cleaned)
        
        # 移除多余的空行（超过2个连续换行）
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        
        # 移除行首尾空白
        lines = [line.rstrip() for line in cleaned.split('\n')]
        cleaned = '\n'.join(lines)
        
        # 移除开头结尾的空行
        cleaned = cleaned.strip()
        
        return cleaned
    
    @staticmethod
    def extract_tables(text: str) -> list:
        """提取所有表格
        
        参数:
            text: OCR 输出文本
            
        返回:
            表格列表
        """
        tables = re.findall(r'<table>.*?</table>', text, re.DOTALL)
        return tables
    
    @staticmethod
    def extract_text_only(text: str) -> str:
        """提取纯文本（不包含表格和标题）
        
        参数:
            text: OCR 输出文本
            
        返回:
            纯文本内容
        """
        # 先清理标注
        cleaned = OutputFormatter.clean_markdown(text)
        
        # 移除表格
        cleaned = re.sub(r'<table>.*?</table>', '', cleaned, flags=re.DOTALL)
        
        # 移除 Markdown 标题
        cleaned = re.sub(r'^#+\s+.*$', '', cleaned, flags=re.MULTILINE)
        
        # 清理多余空行
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        
        return cleaned.strip()
    
    @staticmethod
    def to_plain_text(text: str) -> str:
        """转换为纯文本（移除所有 Markdown 格式）
        
        参数:
            text: Markdown 文本
            
        返回:
            纯文本
        """
        # 先清理标注
        cleaned = OutputFormatter.clean_markdown(text)
        
        # 移除 Markdown 标题标记
        cleaned = re.sub(r'^#+\s+', '', cleaned, flags=re.MULTILINE)
        
        # 转换表格为文本（简单处理）
        def table_to_text(match):
            table = match.group(0)
            # 移除 HTML 标签
            table = re.sub(r'<[^>]+>', ' | ', table)
            # 清理多余空格
            table = re.sub(r'\s+', ' ', table)
            return table
        
        cleaned = re.sub(r'<table>.*?</table>', table_to_text, cleaned, flags=re.DOTALL)
        
        return cleaned.strip()
    
    @staticmethod
    def format_with_structure(text: str) -> dict:
        """结构化输出（提取标题、段落、表格等）
        
        参数:
            text: OCR 输出文本
            
        返回:
            包含结构化内容的字典
        """
        # 清理标注
        cleaned = OutputFormatter.clean_markdown(text)
        
        # 提取标题
        titles = re.findall(r'^(#+)\s+(.+)$', cleaned, flags=re.MULTILINE)
        
        # 提取表格
        tables = OutputFormatter.extract_tables(text)
        
        # 提取段落（非标题非表格的文本块）
        temp = cleaned
        # 移除标题
        temp = re.sub(r'^#+\s+.*$', '', temp, flags=re.MULTILINE)
        # 移除表格
        temp = re.sub(r'<table>.*?</table>', '', temp, flags=re.DOTALL)
        # 按空行分割段落
        paragraphs = [p.strip() for p in temp.split('\n\n') if p.strip()]
        
        return {
            'titles': [(len(level), title) for level, title in titles],
            'tables': tables,
            'paragraphs': paragraphs,
            'full_text': cleaned
        }


def save_as_markdown(text: str, output_path: str, clean: bool = True, 
                     keep_coordinates: bool = False) -> None:
    """保存为 Markdown 文件
    
    参数:
        text: OCR 输出文本
        output_path: 输出文件路径
        clean: 是否清理标注标签
        keep_coordinates: 是否保留坐标信息
    """
    if clean:
        text = OutputFormatter.clean_markdown(text, keep_coordinates=keep_coordinates)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"✅ 已保存到: {output_path}")


def save_as_text(text: str, output_path: str) -> None:
    """保存为纯文本文件
    
    参数:
        text: OCR 输出文本
        output_path: 输出文件路径
    """
    plain_text = OutputFormatter.to_plain_text(text)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(plain_text)
    
    print(f"✅ 已保存到: {output_path}")


# 导出
__all__ = [
    'OutputFormatter',
    'save_as_markdown',
    'save_as_text',
]
