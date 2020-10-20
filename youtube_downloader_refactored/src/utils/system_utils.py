"""
Utilitários de sistema.

Funções auxiliares para operações do sistema operacional.
"""

import os
import platform


class FileSystemUtils:
    """Utilitários para operações de sistema de arquivos."""
    
    @staticmethod
    def open_folder(path: str) -> None:
        """
        Abre uma pasta no explorador de arquivos do sistema.
        
        Args:
            path: Caminho da pasta a ser aberta
        """
        system = platform.system()
        
        if system == 'Windows':
            os.startfile(path)
        elif system == 'Darwin':  # macOS
            os.system(f"open '{path}'")
        else:  # Linux e outros
            os.system(f"xdg-open '{path}'")
