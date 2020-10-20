"""
Testes unitários para validadores.

Valida o comportamento dos validadores de URL e email.
"""

import pytest
from src.utils.validators import URLValidator, EmailValidator
from src.models.exceptions import InvalidURLError


class TestURLValidator:
    """Testes para a classe URLValidator."""
    
    def test_validate_valid_youtube_url(self):
        """Testa validação de URL válida do YouTube."""
        # Arrange
        valid_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "http://youtube.com/watch?v=test123",
            "https://youtu.be/dQw4w9WgXcQ",
            "http://www.youtu.be/test123"
        ]
        
        # Act & Assert
        for url in valid_urls:
            assert URLValidator.validate(url) is True
    
    def test_validate_invalid_url(self):
        """Testa validação de URL inválida."""
        # Arrange
        invalid_urls = [
            "not a url",
            "https://vimeo.com/123456",
            "ftp://youtube.com/video",
            "youtube.com/watch?v=test",
            ""
        ]
        
        # Act & Assert
        for url in invalid_urls:
            assert URLValidator.validate(url) is False
    
    def test_validate_or_raise_valid_url(self):
        """Testa validate_or_raise com URL válida."""
        # Arrange
        url = "https://www.youtube.com/watch?v=test123"
        
        # Act & Assert
        try:
            URLValidator.validate_or_raise(url)
        except InvalidURLError:
            pytest.fail("validate_or_raise lançou exceção para URL válida")
    
    def test_validate_or_raise_invalid_url(self):
        """Testa validate_or_raise com URL inválida."""
        # Arrange
        url = "https://vimeo.com/123456"
        
        # Act & Assert
        with pytest.raises(InvalidURLError) as exc_info:
            URLValidator.validate_or_raise(url)
        
        assert "URL inválida" in str(exc_info.value)


class TestEmailValidator:
    """Testes para a classe EmailValidator."""
    
    def test_validate_valid_email(self):
        """Testa validação de email válido."""
        # Arrange
        valid_emails = [
            "user@example.com",
            "test.user@domain.co.uk",
            "user+tag@example.com",
            "123@test.com",
            "user_name@example.org"
        ]
        
        # Act & Assert
        for email in valid_emails:
            assert EmailValidator.validate(email) is True
    
    def test_validate_invalid_email(self):
        """Testa validação de email inválido."""
        # Arrange
        invalid_emails = [
            "not an email",
            "@example.com",
            "user@",
            "user@domain",
            "user domain@example.com",
            "",
            "user@.com"
        ]
        
        # Act & Assert
        for email in invalid_emails:
            assert EmailValidator.validate(email) is False
