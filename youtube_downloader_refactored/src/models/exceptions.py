"""
Exceções personalizadas da aplicação.

Define exceções específicas para melhor tratamento de erros.
"""


class AuthenticationError(Exception):
    """Erro de autenticação."""
    pass


class InvalidURLError(Exception):
    """URL inválida fornecida."""
    pass


class DownloadError(Exception):
    """Erro durante o download."""
    pass


class CookiesNotFoundError(Exception):
    """Arquivo de cookies não encontrado."""
    pass


class VideoInfoError(Exception):
    """Erro ao obter informações do vídeo."""
    pass
