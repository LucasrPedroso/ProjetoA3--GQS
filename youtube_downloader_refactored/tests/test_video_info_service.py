"""
Testes unitários para o serviço de informações de vídeo.

Valida o comportamento do VideoInfoService e ThumbnailLoader.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.video_info_service import VideoInfoService, ThumbnailLoader
from src.models.video_info import VideoInfo
from src.models.exceptions import VideoInfoError, CookiesNotFoundError


class TestVideoInfoService:
    """Testes para a classe VideoInfoService."""
    
    @pytest.fixture
    def video_info_service(self):
        """Fixture que retorna uma instância do VideoInfoService."""
        return VideoInfoService(cookies_file="test_cookies.txt")
    
    def test_get_video_info_without_cookies(self, video_info_service):
        """Testa obtenção de informações sem arquivo de cookies."""
        # Arrange
        url = "https://www.youtube.com/watch?v=test123"
        
        with patch('os.path.exists', return_value=False):
            # Act & Assert
            with pytest.raises(CookiesNotFoundError) as exc_info:
                video_info_service.get_video_info(url)
            
            assert "Cookies ausentes" in str(exc_info.value)
    
    def test_get_video_info_success(self, video_info_service):
        """Testa obtenção bem-sucedida de informações do vídeo."""
        # Arrange
        url = "https://www.youtube.com/watch?v=test123"
        mock_info = {
            'title': 'Test Video Title',
            'thumbnail': 'https://example.com/thumb.jpg',
            'duration': 300
        }
        
        with patch('os.path.exists', return_value=True), \
             patch('yt_dlp.YoutubeDL') as mock_ydl_class:
            
            mock_ydl = MagicMock()
            mock_ydl_class.return_value.__enter__.return_value = mock_ydl
            mock_ydl.extract_info.return_value = mock_info
            
            # Act
            result = video_info_service.get_video_info(url)
            
            # Assert
            assert isinstance(result, VideoInfo)
            assert result.title == 'Test Video Title'
            assert result.thumbnail_url == 'https://example.com/thumb.jpg'
            assert result.duration == 300
    
    def test_get_video_info_failure(self, video_info_service):
        """Testa falha ao obter informações do vídeo."""
        # Arrange
        url = "https://www.youtube.com/watch?v=invalid"
        
        with patch('os.path.exists', return_value=True), \
             patch('yt_dlp.YoutubeDL') as mock_ydl_class:
            
            mock_ydl = MagicMock()
            mock_ydl_class.return_value.__enter__.return_value = mock_ydl
            mock_ydl.extract_info.side_effect = Exception("Video not found")
            
            # Act & Assert
            with pytest.raises(VideoInfoError) as exc_info:
                video_info_service.get_video_info(url)
            
            assert "Não foi possível obter informações" in str(exc_info.value)
    
    def test_get_video_info_missing_fields(self, video_info_service):
        """Testa obtenção de informações com campos faltando."""
        # Arrange
        url = "https://www.youtube.com/watch?v=test123"
        mock_info = {}  # Sem informações
        
        with patch('os.path.exists', return_value=True), \
             patch('yt_dlp.YoutubeDL') as mock_ydl_class:
            
            mock_ydl = MagicMock()
            mock_ydl_class.return_value.__enter__.return_value = mock_ydl
            mock_ydl.extract_info.return_value = mock_info
            
            # Act
            result = video_info_service.get_video_info(url)
            
            # Assert
            assert result.title == 'Título não disponível'
            assert result.thumbnail_url is None


class TestThumbnailLoader:
    """Testes para a classe ThumbnailLoader."""
    
    def test_load_thumbnail_success(self):
        """Testa carregamento bem-sucedido de thumbnail."""
        # Arrange
        url = "https://example.com/thumb.jpg"
        mock_image_data = b'\x89PNG\r\n\x1a\n'  # Dados de imagem fake
        
        with patch('requests.get') as mock_get, \
             patch('src.services.video_info_service.QImage') as mock_qimage, \
             patch('src.services.video_info_service.QPixmap') as mock_qpixmap:
            
            mock_response = Mock()
            mock_response.content = mock_image_data
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            mock_image = Mock()
            mock_qimage.return_value = mock_image
            
            mock_pixmap = Mock()
            mock_scaled = Mock()
            mock_pixmap.scaled.return_value = mock_scaled
            mock_qpixmap.return_value = mock_pixmap
            
            # Act
            result = ThumbnailLoader.load_thumbnail(url)
            
            # Assert
            mock_get.assert_called_once_with(url, timeout=10)
            assert result == mock_scaled
    
    def test_load_thumbnail_failure(self):
        """Testa falha no carregamento de thumbnail."""
        # Arrange
        url = "https://example.com/invalid.jpg"
        
        with patch('requests.get', side_effect=Exception("Connection error")):
            # Act
            result = ThumbnailLoader.load_thumbnail(url)
            
            # Assert
            assert result is None
