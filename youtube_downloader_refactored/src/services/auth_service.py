"""
Serviço de autenticação.

Gerencia operações de autenticação com Firebase.
Aplica o princípio de Responsabilidade Única (SRP).
"""

from typing import Optional, Dict, Any
from ..config.firebase_config import firebase_config
from ..models.exceptions import AuthenticationError


class AuthService:
    """Serviço responsável pela autenticação de usuários."""
    
    def __init__(self):
        """Inicializa o serviço de autenticação."""
        self._auth = firebase_config.auth
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Realiza login do usuário.
        
        Args:
            email: Email do usuário
            password: Senha do usuário
            
        Returns:
            Dados do usuário autenticado
            
        Raises:
            AuthenticationError: Se as credenciais forem inválidas
        """
        try:
            user = self._auth.sign_in_with_email_and_password(email, password)
            return user
        except Exception as e:
            raise AuthenticationError("E-mail ou senha incorretos.") from e
    
    def register(self, email: str, password: str) -> Dict[str, Any]:
        """
        Registra um novo usuário.
        
        Args:
            email: Email do usuário
            password: Senha do usuário
            
        Returns:
            Dados do usuário criado
            
        Raises:
            AuthenticationError: Se houver erro no registro
        """
        try:
            user = self._auth.create_user_with_email_and_password(email, password)
            return user
        except Exception as e:
            raise AuthenticationError("Erro ao criar conta. Verifique e-mail e senha.") from e
    
    def reset_password(self, email: str) -> None:
        """
        Envia email de recuperação de senha.
        
        Args:
            email: Email do usuário
            
        Raises:
            AuthenticationError: Se o email não for encontrado
        """
        try:
            self._auth.send_password_reset_email(email)
        except Exception as e:
            raise AuthenticationError("E-mail não encontrado no Firebase.") from e
