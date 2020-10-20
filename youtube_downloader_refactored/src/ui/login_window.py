"""
Janela de login.

Interface de autenticação do usuário.
Aplica princípios de separação de responsabilidades.
"""

from typing import Callable
from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from PyQt5.QtGui import QIcon

from .base_components import TitleLabel, StyledLineEdit, PrimaryButton, FlatButton, StatusLabel
from ..services.auth_service import AuthService
from ..models.exceptions import AuthenticationError
from ..config.constants import AppConstants, WindowSize, Colors


class LoginWindow(QWidget):
    """Janela principal de autenticação."""
    
    def __init__(self, on_login_success: Callable[[], None]):
        """
        Inicializa a janela de login.
        
        Args:
            on_login_success: Callback executado após login bem-sucedido
        """
        super().__init__()
        self._on_login_success = on_login_success
        self._auth_service = AuthService()
        self._setup_window()
        self._setup_ui()
    
    def _setup_window(self) -> None:
        """Configura propriedades da janela."""
        self.setWindowIcon(QIcon(AppConstants.WINDOW_ICON))
        self.setWindowTitle("Auth - YouTube Gamer DL")
        self.setFixedSize(WindowSize.LOGIN_WIDTH, WindowSize.LOGIN_HEIGHT)
        self.setStyleSheet(
            f"background-color: {Colors.BACKGROUND}; "
            f"color: white; "
            f"font-size: 14px; "
            f"font-family: 'Segoe UI Semibold';"
        )
    
    def _setup_ui(self) -> None:
        """Configura a interface do usuário."""
        self._stack = QStackedWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self._stack)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self._stack.addWidget(self._create_login_page())
        self._stack.addWidget(self._create_register_page())
        self._stack.addWidget(self._create_recovery_page())
    
    def _create_login_page(self) -> QWidget:
        """Cria a página de login."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = TitleLabel("🔐 Login")
        
        self._email_login = StyledLineEdit("E-mail")
        self._password_login = StyledLineEdit("Senha", password=True)
        self._status_login = StatusLabel()
        
        btn_login = PrimaryButton("Entrar")
        btn_login.clicked.connect(self._handle_login)
        
        btn_register = FlatButton("Criar conta")
        btn_register.clicked.connect(lambda: self._stack.setCurrentIndex(1))
        
        btn_recover = FlatButton("Esqueci minha senha")
        btn_recover.clicked.connect(lambda: self._stack.setCurrentIndex(2))
        
        layout.addWidget(title)
        layout.addWidget(self._email_login)
        layout.addWidget(self._password_login)
        layout.addWidget(btn_login)
        layout.addWidget(btn_register)
        layout.addWidget(btn_recover)
        layout.addWidget(self._status_login)
        
        return page
    
    def _create_register_page(self) -> QWidget:
        """Cria a página de cadastro."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = TitleLabel("🆕 Cadastro")
        
        self._email_register = StyledLineEdit("E-mail")
        self._password_register = StyledLineEdit("Senha", password=True)
        self._status_register = StatusLabel()
        
        btn_create = PrimaryButton("Criar conta")
        btn_create.clicked.connect(self._handle_register)
        
        btn_back = FlatButton("Voltar")
        btn_back.clicked.connect(lambda: self._stack.setCurrentIndex(0))
        
        layout.addWidget(title)
        layout.addWidget(self._email_register)
        layout.addWidget(self._password_register)
        layout.addWidget(btn_create)
        layout.addWidget(btn_back)
        layout.addWidget(self._status_register)
        
        return page
    
    def _create_recovery_page(self) -> QWidget:
        """Cria a página de recuperação de senha."""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = TitleLabel("🔁 Recuperar Senha")
        
        self._email_recovery = StyledLineEdit("E-mail cadastrado")
        self._status_recovery = StatusLabel()
        
        btn_recover = PrimaryButton("Enviar recuperação")
        btn_recover.clicked.connect(self._handle_recovery)
        
        btn_back = FlatButton("Voltar")
        btn_back.clicked.connect(lambda: self._stack.setCurrentIndex(0))
        
        layout.addWidget(title)
        layout.addWidget(self._email_recovery)
        layout.addWidget(btn_recover)
        layout.addWidget(btn_back)
        layout.addWidget(self._status_recovery)
        
        return page
    
    def _handle_login(self) -> None:
        """Processa tentativa de login."""
        email = self._email_login.text().strip()
        password = self._password_login.text()
        
        try:
            self._auth_service.login(email, password)
            self._status_login.show_success("Login realizado!")
            self._on_login_success()
            self.close()
        except AuthenticationError as e:
            self._status_login.show_error(str(e))
    
    def _handle_register(self) -> None:
        """Processa tentativa de cadastro."""
        email = self._email_register.text().strip()
        password = self._password_register.text()
        
        try:
            self._auth_service.register(email, password)
            self._status_register.show_success("Conta criada! Agora faça login.")
        except AuthenticationError as e:
            self._status_register.show_error(str(e))
    
    def _handle_recovery(self) -> None:
        """Processa recuperação de senha."""
        email = self._email_recovery.text().strip()
        
        try:
            self._auth_service.reset_password(email)
            self._status_recovery.show_success("Link de recuperação enviado para o e-mail!")
        except AuthenticationError as e:
            self._status_recovery.show_error(str(e))
