"""
Utilitários de validação.

Funções auxiliares para validação de dados.
"""

import re
from ..models.exceptions import InvalidURLError


class URLValidator:
    """Validador de URLs do YouTube."""
    
    YOUTUBE_PATTERN = r"^https?://(www\.)?(youtube\.com|youtu\.be)/"
    
    @classmethod
    def validate(cls, url: str) -> bool:
        """
        Valida se uma URL é do YouTube.
        
        Args:
            url: URL a ser validada
            
        Returns:
            True se válida, False caso contrário
        """
        return bool(re.match(cls.YOUTUBE_PATTERN, url))
    
    @classmethod
    def validate_or_raise(cls, url: str) -> None:
        """
        Valida URL ou lança exceção.
        
        Args:
            url: URL a ser validada
            
        Raises:
            InvalidURLError: Se a URL for inválida
        """
        if not cls.validate(url):
            raise InvalidURLError("URL inválida. Use uma URL do YouTube.")


class EmailValidator:
    """Validador de emails."""
    
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    @classmethod
    def validate(cls, email: str) -> bool:
        """
        Valida formato de email.
        
        Args:
            email: Email a ser validado
            
        Returns:
            True se válido, False caso contrário
        """
        return bool(re.match(cls.EMAIL_PATTERN, email))
