"""
Thread de download.

Gerencia o download em uma thread separada para não bloquear a UI.
"""

from PyQt5.QtCore import QThread, pyqtSignal
from typing import Dict, Any

from ..models.video_info import DownloadRequest
from ..services.download_service import DownloadService
from ..models.exceptions import DownloadError, CookiesNotFoundError


class DownloadThread(QThread):
    """Thread responsável por executar downloads em background."""
    
    progress_signal = pyqtSignal(dict)
    finished_signal = pyqtSignal(str)
    
    def __init__(self, request: DownloadRequest):
        """
        Inicializa a thread de download.
        
        Args:
            request: Requisição de download
        """
        super().__init__()
        self._request = request
        self._download_service = DownloadService()
    
    def run(self) -> None:
        """Executa o download."""
        try:
            self._download_service.download(
                self._request,
                progress_callback=self._on_progress
            )
            self.finished_signal.emit("success")
        except (CookiesNotFoundError, DownloadError) as e:
            self.finished_signal.emit(str(e))
        except Exception as e:
            self.finished_signal.emit(f"Erro inesperado: {str(e)}")
    
    def _on_progress(self, data: Dict[str, Any]) -> None:
        """
        Callback de progresso.
        
        Args:
            data: Dados de progresso do yt-dlp
        """
        self.progress_signal.emit(data)
