"""
Controlador da aplicação.

Gerencia o ciclo de vida da aplicação e navegação entre janelas.
Aplica o padrão Controller do MVC.
"""

import sys
from typing import Optional
from PyQt5.QtWidgets import QApplication

from .ui.login_window import LoginWindow
from .ui.downloader_window import DownloaderWindow


class AppController:
    """
    Controlador principal da aplicação.
    
    Responsável por inicializar a aplicação e gerenciar
    a transição entre as janelas de login e download.
    """
    
    def __init__(self):
        """Inicializa o controlador da aplicação."""
        self._app = QApplication(sys.argv)
        self._login_window = LoginWindow(self._open_downloader)
        self._downloader_window: Optional[DownloaderWindow] = None
    
    def _open_downloader(self) -> None:
        """Abre a janela de download após login bem-sucedido."""
        if self._downloader_window is None:
            self._downloader_window = DownloaderWindow()
        self._downloader_window.show()
    
    def run(self) -> int:
        """
        Executa a aplicação.
        
        Returns:
            Código de saída da aplicação
        """
        self._login_window.show()
        return self._app.exec_()
