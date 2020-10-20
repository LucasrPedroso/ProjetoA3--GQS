"""
Serviço de download de vídeos.

Gerencia o download de vídeos do YouTube usando yt-dlp.
Aplica o princípio de Responsabilidade Única (SRP).
"""

import os
import re
from typing import Callable, Optional, Dict, Any
import yt_dlp

from ..models.video_info import DownloadRequest, DownloadProgress
from ..models.exceptions import DownloadError, CookiesNotFoundError
from ..config.constants import AppConstants, DownloadFormats


class DownloadService:
    """Serviço responsável pelo download de vídeos."""
    
    def __init__(self, cookies_file: str = AppConstants.COOKIES_FILE):
        """
        Inicializa o serviço de download.
        
        Args:
            cookies_file: Caminho para o arquivo de cookies
        """
        self._cookies_file = cookies_file
    
    def download(
        self,
        request: DownloadRequest,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ) -> None:
        """
        Realiza o download de um vídeo.
        
        Args:
            request: Requisição de download
            progress_callback: Callback para atualização de progresso
            
        Raises:
            CookiesNotFoundError: Se o arquivo de cookies não existir
            DownloadError: Se houver erro no download
        """
        if not os.path.exists(self._cookies_file):
            raise CookiesNotFoundError(
                f"Arquivo de cookies '{self._cookies_file}' não encontrado.\n"
                "Exporte usando a extensão 'Get cookies.txt clean' e salve na pasta do app."
            )
        
        ydl_opts = self._build_download_options(request, progress_callback)
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([request.url])
        except Exception as e:
            raise DownloadError(f"Erro durante o download: {str(e)}") from e
    
    def _build_download_options(
        self,
        request: DownloadRequest,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]]
    ) -> Dict[str, Any]:
        """
        Constrói as opções de download para o yt-dlp.
        
        Args:
            request: Requisição de download
            progress_callback: Callback para progresso
            
        Returns:
            Dicionário de opções para o yt-dlp
        """
        format_string = DownloadFormats.get_format_string(request.format_choice)
        filename = request.get_filename()
        
        options = {
            'format': format_string,
            'outtmpl': os.path.join(request.save_path, f'{filename}.%(ext)s'),
            'merge_output_format': 'mp4',
            'cookiefile': self._cookies_file,
            'quiet': True,
            'noprogress': True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }
        
        if progress_callback:
            options['progress_hooks'] = [progress_callback]
        
        return options


class ProgressParser:
    """Parser para informações de progresso do yt-dlp."""
    
    @staticmethod
    def parse(data: Dict[str, Any]) -> DownloadProgress:
        """
        Converte dados do yt-dlp em objeto DownloadProgress.
        
        Args:
            data: Dados de progresso do yt-dlp
            
        Returns:
            Objeto DownloadProgress
        """
        status = data.get('status', 'unknown')
        percent = 0.0
        eta = data.get('eta')
        speed = data.get('speed')
        
        if status == 'downloading':
            percent_str = data.get('_percent_str', '').strip()
            percent_clean = re.sub(r'\x1b\[[0-9;]*m', '', percent_str).replace('%', '')
            
            if percent_clean:
                try:
                    percent = float(percent_clean)
                except ValueError:
                    percent = 0.0
        elif status == 'finished':
            percent = 100.0
        
        return DownloadProgress(
            status=status,
            percent=percent,
            eta=eta,
            speed=speed
        )
