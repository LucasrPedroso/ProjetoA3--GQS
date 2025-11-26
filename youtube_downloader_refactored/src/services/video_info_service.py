"""
Serviço de informações de vídeo.

Obtém metadados de vídeos do YouTube.
Aplica o princípio de Responsabilidade Única (SRP).
"""

import os
from typing import Optional
import yt_dlp
import requests
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

from ..models.video_info import VideoInfo
from ..models.exceptions import VideoInfoError, CookiesNotFoundError
from ..config.constants import AppConstants


class VideoInfoService:
    """Serviço responsável por obter informações de vídeos."""
    
    def __init__(self, cookies_file: str = AppConstants.COOKIES_FILE):
        """
        Inicializa o serviço de informações.
        
        Args:
            cookies_file: Caminho para o arquivo de cookies
        """
        self._cookies_file = cookies_file
    
    def get_video_info(self, url: str) -> VideoInfo:
        """
        Obtém informações de um vídeo.
        
        Args:
            url: URL do vídeo
            
        Returns:
            Objeto VideoInfo com as informações
            
        Raises:
            CookiesNotFoundError: Se o arquivo de cookies não existir
            VideoInfoError: Se houver erro ao obter informações
        """
        if not os.path.exists(self._cookies_file):
            raise CookiesNotFoundError("Cookies ausentes para obter informações do vídeo.")
        
        ydl_opts = {
            'quiet': True,
            'cookiefile': self._cookies_file,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return VideoInfo(
                    title=info.get('title', 'Título não disponível'),
                    thumbnail_url=info.get('thumbnail'),
                    duration=info.get('duration')
                )
        except Exception as e:
            raise VideoInfoError("Não foi possível obter informações do vídeo.") from e


class ThumbnailLoader:
    """Carregador de thumbnails de vídeos."""
    
    @staticmethod
    def load_thumbnail(url: str, width: int = 200, height: int = 150) -> Optional[QPixmap]:
        """
        Carrega uma thumbnail de uma URL.
        
        Args:
            url: URL da thumbnail
            width: Largura desejada
            height: Altura desejada
            
        Returns:
            QPixmap com a imagem ou None se houver erro
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            image = QImage()
            image.loadFromData(response.content)
            pixmap = QPixmap(image)
            return pixmap.scaled(width, height, Qt.KeepAspectRatio)
        except Exception as e:
            print(f"Erro ao carregar thumbnail: {e}")
            return None
