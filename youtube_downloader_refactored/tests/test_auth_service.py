"""
Testes unitários para o serviço de autenticação.

Valida o comportamento do AuthService em diferentes cenários.
"""

import pytest
from unittest.mock import Mock, patch
from src.services.auth_service import AuthService
from src.models.exceptions import AuthenticationError


class TestAuthService:
    """Testes para a classe AuthService."""
    
    @pytest.fixture
    def auth_service(self):
        """Fixture que retorna uma instância do AuthService."""
        with patch('src.services.auth_service.firebase_config') as mock_config:
            mock_auth = Mock()
            mock_config.auth = mock_auth
            service = AuthService()
            service._auth = mock_auth
            return service
    
    def test_login_success(self, auth_service):
        """Testa login bem-sucedido."""
        # Arrange
        email = "test@example.com"
        password = "password123"
        expected_user = {"localId": "123", "email": email}
        auth_service._auth.sign_in_with_email_and_password.return_value = expected_user
        
        # Act
        result = auth_service.login(email, password)
        
        # Assert
        assert result == expected_user
        auth_service._auth.sign_in_with_email_and_password.assert_called_once_with(email, password)
    
    def test_login_failure(self, auth_service):
        """Testa falha no login com credenciais inválidas."""
        # Arrange
        email = "test@example.com"
        password = "wrongpassword"
        auth_service._auth.sign_in_with_email_and_password.side_effect = Exception("Invalid credentials")
        
        # Act & Assert
        with pytest.raises(AuthenticationError) as exc_info:
            auth_service.login(email, password)
        
        assert "E-mail ou senha incorretos" in str(exc_info.value)
    
    def test_register_success(self, auth_service):
        """Testa registro bem-sucedido."""
        # Arrange
        email = "newuser@example.com"
        password = "password123"
        expected_user = {"localId": "456", "email": email}
        auth_service._auth.create_user_with_email_and_password.return_value = expected_user
        
        # Act
        result = auth_service.register(email, password)
        
        # Assert
        assert result == expected_user
        auth_service._auth.create_user_with_email_and_password.assert_called_once_with(email, password)
    
    def test_register_failure(self, auth_service):
        """Testa falha no registro."""
        # Arrange
        email = "invalid-email"
        password = "123"
        auth_service._auth.create_user_with_email_and_password.side_effect = Exception("Invalid email")
        
        # Act & Assert
        with pytest.raises(AuthenticationError) as exc_info:
            auth_service.register(email, password)
        
        assert "Erro ao criar conta" in str(exc_info.value)
    
    def test_reset_password_success(self, auth_service):
        """Testa envio de email de recuperação bem-sucedido."""
        # Arrange
        email = "test@example.com"
        auth_service._auth.send_password_reset_email.return_value = None
        
        # Act
        auth_service.reset_password(email)
        
        # Assert
        auth_service._auth.send_password_reset_email.assert_called_once_with(email)
    
    def test_reset_password_failure(self, auth_service):
        """Testa falha no envio de email de recuperação."""
        # Arrange
        email = "nonexistent@example.com"
        auth_service._auth.send_password_reset_email.side_effect = Exception("Email not found")
        
        # Act & Assert
        with pytest.raises(AuthenticationError) as exc_info:
            auth_service.reset_password(email)
        
        assert "E-mail não encontrado" in str(exc_info.value)
