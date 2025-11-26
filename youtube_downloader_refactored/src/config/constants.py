"""
Constantes e estilos da aplicação.

Centraliza todas as constantes, estilos CSS e configurações visuais
para facilitar manutenção e evitar repetição.
"""

from typing import Dict


class AppConstants:
    """Constantes gerais da aplicação."""
    
    WINDOW_ICON = "icon.png"
    COOKIES_FILE = "youtube.com_cookies.txt"
    BORDER_RADIUS = 16
    

class WindowSize:
    """Dimensões das janelas."""
    
    LOGIN_WIDTH = 420
    LOGIN_HEIGHT = 360
    DOWNLOADER_WIDTH = 540
    DOWNLOADER_HEIGHT = 500


class Colors:
    """Paleta de cores da aplicação."""
    
    BACKGROUND = "#1b1c1f"
    SECONDARY_BG = "#2b2d31"
    TOPBAR_BG = "#202225"
    TEXT_PRIMARY = "#f2f3f5"
    TEXT_WHITE = "white"
    ACCENT = "#f04747"
    ACCENT_HOVER = "#d73737"
    BORDER = "#444"
    HOVER_BG = "#3c3f45"


class Styles:
    """Estilos CSS reutilizáveis."""
    
    BASE_WIDGET = f"""
        QWidget {{
            background-color: {Colors.BACKGROUND};
            color: {Colors.TEXT_PRIMARY};
            font-family: 'Segoe UI Semibold';
            font-size: 14px;
        }}
    """
    
    LINE_EDIT = f"""
        QLineEdit {{
            background-color: {Colors.SECONDARY_BG};
            border: 2px solid {Colors.BORDER};
            border-radius: 8px;
            padding: 10px;
        }}
        QLineEdit:focus {{
            border-color: {Colors.ACCENT};
        }}
    """
    
    PRIMARY_BUTTON = f"""
        QPushButton {{
            background-color: {Colors.ACCENT};
            border: none;
            border-radius: 8px;
            padding: 12px;
            font-size: 16px;
            font-weight: bold;
            color: {Colors.TEXT_WHITE};
        }}
        QPushButton:hover {{
            background-color: {Colors.ACCENT_HOVER};
        }}
    """
    
    FLAT_BUTTON = f"""
        padding: 12px;
        border-radius: 8px;
        background-color: {Colors.SECONDARY_BG};
        color: {Colors.TEXT_WHITE};
    """
    
    WINDOW_BUTTON = f"""
        QPushButton {{
            background-color: transparent;
            color: {Colors.ACCENT};
            font-size: 16px;
            border: none;
        }}
        QPushButton:hover {{
            background-color: {Colors.HOVER_BG};
            border-radius: 5px;
        }}
    """
    
    PROGRESS_BAR = f"""
        QProgressBar {{
            background-color: {Colors.SECONDARY_BG};
            border-radius: 6px;
            height: 18px;
            text-align: center;
            color: {Colors.TEXT_WHITE};
        }}
        QProgressBar::chunk {{
            background-color: {Colors.ACCENT};
            border-radius: 6px;
        }}
    """
    
    COMBO_BOX = f"""
        QComboBox {{
            background-color: {Colors.SECONDARY_BG};
            border: 2px solid {Colors.BORDER};
            border-radius: 8px;
            padding: 8px;
            color: {Colors.TEXT_PRIMARY};
        }}
    """
    
    TITLE_LABEL = f"""
        font-size: 24px;
        color: {Colors.ACCENT};
        font-weight: bold;
    """


class DownloadFormats:
    """Formatos de download disponíveis."""
    
    FORMATS: Dict[str, str] = {
        "Melhor qualidade": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "Qualidade até 720p": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]",
        "Áudio MP3": "bestaudio[ext=m4a]",
    }
    
    @classmethod
    def get_format_keys(cls):
        """Retorna lista de nomes dos formatos."""
        return list(cls.FORMATS.keys())
    
    @classmethod
    def get_format_string(cls, format_name: str) -> str:
        """Retorna a string de formato do yt-dlp."""
        return cls.FORMATS.get(format_name, 'best')
