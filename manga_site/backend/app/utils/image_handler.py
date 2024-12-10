from PIL import Image
import os
from fastapi import UploadFile
from typing import Tuple
import aiofiles
import logging

logger = logging.getLogger(__name__)

class ImageHandler:
    def __init__(self):
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.webp'}

    async def save_image(
        self,
        upload_file: UploadFile,
        save_path: str,
        optimize: bool = True,
        max_size: Tuple[int, int] = (1920, None)
    ) -> str:
        """
        保存并优化上传的图片
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # 保存原始文件
            async with aiofiles.open(save_path, 'wb') as out_file:
                content = await upload_file.read()
                await out_file.write(content)
            
            if optimize:
                # 优化图片
                with Image.open(save_path) as img:
                    # 转换为RGB模式（如果是RGBA）
                    if img.mode == 'RGBA':
                        img = img.convert('RGB')
                    
                    # 调整大小
                    if max_size[0] and img.size[0] > max_size[0]:
                        ratio = max_size[0] / img.size[0]
                        new_height = int(img.size[1] * ratio)
                        img = img.resize((max_size[0], new_height), Image.Resampling.LANCZOS)
                    
                    # 保存优化后的图片
                    img.save(
                        save_path,
                        'JPEG',
                        quality=85,
                        optimize=True,
                        progressive=True
                    )
            
            return save_path
            
        except Exception as e:
            logger.error(f"Error processing image {upload_file.filename}: {str(e)}")
            if os.path.exists(save_path):
                os.remove(save_path)
            raise

    def is_valid_image(self, filename: str) -> bool:
        """
        检查文件是否是支持的图片格式
        """
        ext = os.path.splitext(filename.lower())[1]
        return ext in self.supported_formats

    async def create_thumbnail(
        self,
        source_path: str,
        thumb_path: str,
        size: Tuple[int, int] = (300, 300)
    ) -> str:
        """
        创建缩略图
        """
        try:
            os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
            
            with Image.open(source_path) as img:
                # 转换为RGB模式（如果是RGBA）
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                
                # 创建缩略图
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                # 保存缩略图
                img.save(
                    thumb_path,
                    'JPEG',
                    quality=85,
                    optimize=True
                )
                
            return thumb_path
            
        except Exception as e:
            logger.error(f"Error creating thumbnail for {source_path}: {str(e)}")
            if os.path.exists(thumb_path):
                os.remove(thumb_path)
            raise