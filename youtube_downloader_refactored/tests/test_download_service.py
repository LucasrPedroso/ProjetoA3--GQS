"""
Testes unitários para o serviço de download.

Valida o comportamento do DownloadService e ProgressParser.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.download_service import DownloadService, ProgressParser
from src.models.video_info import DownloadRequest, DownloadProgress
from src.models.exceptions import DownloadError, CookiesNotFoundError


class TestDownloadService:
    """Testes para a classe DownloadService."""
    
    @pytest.fixture
    def download_service(self):
        """Fixture que retorna uma instância do DownloadService."""
        return DownloadService(cookies_file="test_cookies.txt")
    
    @pytest.fixture
    def download_request(self):
        """Fixture que retorna uma requisição de download de teste."""
        return DownloadRequest(
            url="https://www.youtube.com/watch?v=test123",
            save_path="/tmp/downloads",
            format_choice="Melhor qualidade",
            custom_title="Test Video"
        )
    
    def test_download_without_cookies(self, download_service, download_request):
        """Testa download sem arquivo de cookies."""
        # Arrange
        with patch('os.path.exists', return_value=False):
            # Act & Assert
            with pytest.raises(CookiesNotFoundError) as exc_info:
                download_service.download(download_request)
            
            assert "Arquivo de cookies" in str(exc_info.value)
    
    def test_download_success(self, download_service, download_request):
        """Testa download bem-sucedido."""
        # Arrange
        with patch('os.path.exists', return_value=True), \
             patch('yt_dlp.YoutubeDL') as mock_ydl_class:
            
            mock_ydl = MagicMock()
            mock_ydl_class.return_value.__enter__.return_value = mock_ydl
            mock_ydl.download.return_value = None
            
            # Act
            download_service.download(download_request)
            
            # Assert
            mock_ydl.download.assert_called_once_with([download_request.url])
    
    def test_download_failure(self, download_service, download_request):
        """Testa falha no download."""
        # Arrange
        with patch('os.path.exists', return_value=True), \
             patch('yt_dlp.YoutubeDL') as mock_ydl_class:
            
            mock_ydl = MagicMock()
            mock_ydl_class.return_value.__enter__.return_value = mock_ydl
            mock_ydl.download.side_effect = Exception("Download failed")
            
            # Act & Assert
            with pytest.raises(DownloadError) as exc_info:
                download_service.download(download_request)
            
            assert "Erro durante o download" in str(exc_info.value)
    
    def test_build_download_options(self, download_service, download_request):
        """Testa construção de opções de download."""
        # Arrange
        callback = Mock()
        
        # Act
        options = download_service._build_download_options(download_request, callback)
        
        # Assert
        assert 'format' in options
        assert 'outtmpl' in options
        assert 'cookiefile' in options
        assert 'progress_hooks' in options
        assert callback in options['progress_hooks']


class TestProgressParser:
    """Testes para a classe ProgressParser."""
    
    def test_parse_downloading_status(self):
        """Testa parsing de status de download em progresso."""
        # Arrange
        data = {
            'status': 'downloading',
            '_percent_str': '45.5%',
            'eta': 120,
            'speed': '1.5MB/s'
        }
        
        # Act
        progress = ProgressParser.parse(data)
        
        # Assert
        assert progress.status == 'downloading'
        assert progress.percent == 45.5
        assert progress.eta == 120
        assert progress.is_downloading()
        assert not progress.is_finished()
    
    def test_parse_finished_status(self):
        """Testa parsing de status finalizado."""
        # Arrange
        data = {
            'status': 'finished'
        }
        
        # Act
        progress = ProgressParser.parse(data)
        
        # Assert
        assert progress.status == 'finished'
        assert progress.percent == 100.0
        assert progress.is_finished()
        assert not progress.is_downloading()
    
    def test_parse_with_ansi_codes(self):
        """Testa parsing com códigos ANSI na porcentagem."""
        # Arrange
        data = {
            'status': 'downloading',
            '_percent_str': '\x1b[31m75.3%\x1b[0m'
        }
        
        # Act
        progress = ProgressParser.parse(data)
        
        # Assert
        assert progress.percent == 75.3
    
    def test_get_formatted_eta(self):
        """Testa formatação do ETA."""
        # Arrange
        progress = DownloadProgress(status='downloading', eta=125)
        
        # Act
        formatted = progress.get_formatted_eta()
        
        # Assert
        assert formatted == "02:05"
    
    def test_get_formatted_eta_none(self):
        """Testa formatação do ETA quando None."""
        # Arrange
        progress = DownloadProgress(status='downloading', eta=None)
        
        # Act
        formatted = progress.get_formatted_eta()
        
        # Assert
        assert formatted == ""
