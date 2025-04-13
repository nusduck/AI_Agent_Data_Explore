import os
import base64
from pathlib import Path

def load_analysis_files(number):
    """
    读取analysis目录下所有文本文件，并合并其内容
    
    Args:
        number (str): 用于构建目录路径的数字
        
    Returns:
        str: 合并后的字符串，格式为"file_name: file_content"
    """
    analysis_path = Path(f"outputs/{number}/analysis")
    print(f"analysis_path: {analysis_path}")
    combined_content = ""
    
    if not analysis_path.exists():
        return combined_content
    
    for file_path in analysis_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in ['.txt', '.md', '.csv', '.json']:
            try:
                content = file_path.read_text(encoding='utf-8')
                combined_content += f"{file_path.name}: {content}\n\n"
            except Exception as e:
                combined_content += f"{file_path.name}: Error reading file: {str(e)}\n\n"
    
    return combined_content

def load_visualization_files(number):
    """
    读取visualization目录下所有图像文件，转换为base64格式
    
    Args:
        number (str): 用于构建目录路径的数字
        
    Returns:
        list: 包含所有图像base64编码的列表
    """
    visualization_path = Path(f"outputs/{number}/visualization")
    base64_images = []
    
    if not visualization_path.exists():
        return base64_images
    
    for file_path in visualization_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
            try:
                with open(file_path, 'rb') as img_file:
                    encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
                base64_images.append({
                    'filename': file_path.name,
                    'base64': encoded_string
                })
            except Exception as e:
                print(f"无法编码图像 {file_path.name}: {str(e)}")
    
    return base64_images
