"""
Modelos de dados para informações de vídeo.

Define as estruturas de dados usadas na aplicação.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class VideoInfo:
    """Informações de um vídeo do YouTube."""
    
    title: str
    thumbnail_url: Optional[str] = None
    duration: Optional[int] = None
    
    def __str__(self) -> str:
        """Representação em string do vídeo."""
        return f"📹 {self.title}"


@dataclass
class DownloadProgress:
    """Informações de progresso de download."""
    
    status: str
    percent: float = 0.0
    eta: Optional[int] = None
    speed: Optional[str] = None
    
    def is_downloading(self) -> bool:
        """Verifica se está em processo de download."""
        return self.status == 'downloading'
    
    def is_finished(self) -> bool:
        """Verifica se o download foi finalizado."""
        return self.status == 'finished'
    
    def get_formatted_eta(self) -> str:
        """Retorna o tempo estimado formatado."""
        if self.eta is None:
            return ""
        mins, secs = divmod(self.eta, 60)
        return f"{int(mins):02d}:{int(secs):02d}"


@dataclass
class DownloadRequest:
    """Requisição de download de vídeo."""
    
    url: str
    save_path: str
    format_choice: str
    custom_title: Optional[str] = None
    
    def get_filename(self) -> str:
        """Retorna o nome do arquivo a ser usado."""
        return self.custom_title.strip() if self.custom_title else "%(title)s"
