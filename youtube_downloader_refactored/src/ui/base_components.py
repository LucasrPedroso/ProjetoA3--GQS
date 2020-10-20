"""
Componentes base de UI.

Componentes reutilizáveis para a interface gráfica.
Aplica o princípio DRY (Don't Repeat Yourself).
"""

from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from ..config.constants import Styles, Colors


class TitleLabel(QLabel):
    """Label de título estilizado."""
    
    def __init__(self, text: str):
        """
        Inicializa o label de título.
        
        Args:
            text: Texto do título
        """
        super().__init__(text)
        self.setStyleSheet(Styles.TITLE_LABEL)
        self.setAlignment(Qt.AlignCenter)


class StyledLineEdit(QLineEdit):
    """Campo de entrada de texto estilizado."""
    
    def __init__(self, placeholder: str = "", password: bool = False):
        """
        Inicializa o campo de entrada.
        
        Args:
            placeholder: Texto placeholder
            password: Se True, oculta o texto digitado
        """
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet(Styles.LINE_EDIT)
        if password:
            self.setEchoMode(QLineEdit.Password)


class PrimaryButton(QPushButton):
    """Botão primário estilizado."""
    
    def __init__(self, text: str):
        """
        Inicializa o botão primário.
        
        Args:
            text: Texto do botão
        """
        super().__init__(text)
        self.setStyleSheet(Styles.PRIMARY_BUTTON)


class FlatButton(QPushButton):
    """Botão flat estilizado."""
    
    def __init__(self, text: str):
        """
        Inicializa o botão flat.
        
        Args:
            text: Texto do botão
        """
        super().__init__(text)
        self.setFlat(True)
        self.setStyleSheet(Styles.FLAT_BUTTON)


class StatusLabel(QLabel):
    """Label para exibição de status."""
    
    def __init__(self):
        """Inicializa o label de status."""
        super().__init__("")
        self.setAlignment(Qt.AlignCenter)
    
    def show_success(self, message: str) -> None:
        """
        Exibe mensagem de sucesso.
        
        Args:
            message: Mensagem a ser exibida
        """
        self.setText(f"✔ {message}")
        self.setStyleSheet(f"color: #43b581; padding: 4px;")
    
    def show_error(self, message: str) -> None:
        """
        Exibe mensagem de erro.
        
        Args:
            message: Mensagem a ser exibida
        """
        self.setText(f"❌ {message}")
        self.setStyleSheet(f"color: {Colors.ACCENT}; padding: 4px;")
    
    def show_info(self, message: str) -> None:
        """
        Exibe mensagem informativa.
        
        Args:
            message: Mensagem a ser exibida
        """
        self.setText(message)
        self.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; padding: 4px;")
    
    def clear(self) -> None:
        """Limpa o label."""
        self.setText("")
