"""
Janela de download.

Interface principal para download de vídeos do YouTube.
Aplica princípios de separação de responsabilidades e SOLID.
"""

from typing import Optional, Dict, Any
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QLineEdit, QPushButton, QComboBox, QProgressBar, QFileDialog
)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QIcon, QPainterPath, QRegion, QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from .download_thread import DownloadThread
from .base_components import StatusLabel
from ..models.video_info import DownloadRequest, VideoInfo
from ..services.video_info_service import VideoInfoService, ThumbnailLoader
from ..services.download_service import ProgressParser
from ..utils.validators import URLValidator
from ..utils.system_utils import FileSystemUtils
from ..models.exceptions import InvalidURLError, VideoInfoError, CookiesNotFoundError
from ..config.constants import (
    AppConstants, WindowSize, Colors, Styles, DownloadFormats
)


class DownloaderWindow(QWidget):
    """Janela principal de download de vídeos."""
    
    def __init__(self):
        """Inicializa a janela de download."""
        super().__init__()
        self._is_downloading = False
        self._download_thread: Optional[DownloadThread] = None
        self._save_path: Optional[str] = None
        self._old_pos = self.pos()
        
        self._video_info_service = VideoInfoService()
        
        self._setup_window()
        self._setup_ui()
    
    def _setup_window(self) -> None:
        """Configura propriedades da janela."""
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(WindowSize.DOWNLOADER_WIDTH, WindowSize.DOWNLOADER_HEIGHT)
        self.setWindowIcon(QIcon(AppConstants.WINDOW_ICON))
        self.setAcceptDrops(True)
        
        # Bordas arredondadas
        path = QPainterPath()
        radius = AppConstants.BORDER_RADIUS
        rect = QRectF(self.rect())
        path.addRoundedRect(rect, radius, radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)
        
        self._apply_styles()
    
    def _apply_styles(self) -> None:
        """Aplica estilos CSS à janela."""
        self.setStyleSheet(f"""
            {Styles.BASE_WIDGET}
            {Styles.LINE_EDIT}
            {Styles.PRIMARY_BUTTON}
            QLabel {{
                padding: 4px;
            }}
            {Styles.PROGRESS_BAR}
            {Styles.COMBO_BOX}
        """)
    
    def _setup_ui(self) -> None:
        """Configura a interface do usuário."""
        main_layout = QVBoxLayout(self)
        
        # Barra de título
        main_layout.addWidget(self._create_title_bar())
        main_layout.addStretch()
        
        # Campos de entrada
        self._url_input = QLineEdit()
        self._url_input.setPlaceholderText("Cole o link do vídeo do YouTube...")
        
        self._title_input = QLineEdit()
        self._title_input.setPlaceholderText("Nome do arquivo (opcional)")
        
        self._format_box = QComboBox()
        self._format_box.addItems(DownloadFormats.get_format_keys())
        
        # Botão de download
        self._download_btn = QPushButton("🎬 Baixar Vídeo")
        self._download_btn.clicked.connect(self._handle_download)
        self._add_glow_effect(self._download_btn)
        
        # Barra de progresso e status
        self._progress_bar = QProgressBar()
        self._progress_bar.setValue(0)
        self._progress_bar.setVisible(False)
        self._progress_bar.setFormat("0%")
        
        self._status = StatusLabel()
        self._video_title = QLabel("")
        self._thumbnail_label = QLabel()
        
        # Adicionar widgets ao layout
        main_layout.addWidget(self._url_input)
        main_layout.addWidget(self._title_input)
        main_layout.addWidget(self._format_box)
        main_layout.addWidget(self._download_btn)
        main_layout.addWidget(self._progress_bar)
        main_layout.addWidget(self._status)
        main_layout.addWidget(self._video_title)
        main_layout.addWidget(self._thumbnail_label)
        main_layout.addStretch()
        main_layout.setContentsMargins(20, 20, 20, 20)
    
    def _create_title_bar(self) -> QFrame:
        """Cria a barra de título personalizada."""
        bar = QFrame(self)
        bar.setFixedHeight(36)
        bar.setStyleSheet(f"background-color: {Colors.TOPBAR_BG};")
        
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(10, 0, 10, 0)
        
        title = QLabel("▶ YouTube Gamer DL")
        title.setStyleSheet(f"color: {Colors.ACCENT}; font-size: 16px; font-weight: bold;")
        
        btn_minimize = self._create_window_button("–", self.showMinimized)
        btn_close = self._create_window_button("×", self.close)
        
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(btn_minimize)
        layout.addWidget(btn_close)
        
        return bar
    
    def _create_window_button(self, text: str, callback) -> QPushButton:
        """Cria botão da barra de título."""
        btn = QPushButton(text)
        btn.setFixedSize(30, 30)
        btn.setStyleSheet(Styles.WINDOW_BUTTON)
        btn.clicked.connect(callback)
        return btn
    
    def _add_glow_effect(self, widget: QWidget) -> None:
        """Adiciona efeito de brilho a um widget."""
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(20)
        glow.setColor(QColor(Colors.ACCENT))
        glow.setOffset(0)
        widget.setGraphicsEffect(glow)
    
    def _handle_download(self) -> None:
        """Processa requisição de download."""
        url = self._url_input.text().strip()
        custom_title = self._title_input.text().strip()
        
        # Validações
        if not url or self._is_downloading:
            return
        
        try:
            URLValidator.validate_or_raise(url)
        except InvalidURLError as e:
            self._status.show_error(str(e))
            return
        
        # Selecionar pasta de destino
        save_path = QFileDialog.getExistingDirectory(self, "Escolha a pasta para salvar")
        if not save_path:
            self._status.show_error("Caminho de destino não escolhido.")
            return
        
        self._save_path = save_path
        self._start_download(url, save_path, custom_title)
        self._load_video_info(url)
    
    def _start_download(self, url: str, save_path: str, custom_title: str) -> None:
        """Inicia o processo de download."""
        self._is_downloading = True
        self._download_btn.setEnabled(False)
        self._progress_bar.setVisible(True)
        self._progress_bar.setValue(0)
        self._progress_bar.setFormat("0%")
        self._status.show_info("📥 Preparando...")
        
        request = DownloadRequest(
            url=url,
            save_path=save_path,
            format_choice=self._format_box.currentText(),
            custom_title=custom_title if custom_title else None
        )
        
        self._download_thread = DownloadThread(request)
        self._download_thread.progress_signal.connect(self._update_progress)
        self._download_thread.finished_signal.connect(self._download_finished)
        self._download_thread.start()
    
    def _load_video_info(self, url: str) -> None:
        """Carrega informações do vídeo."""
        try:
            video_info = self._video_info_service.get_video_info(url)
            self._video_title.setText(str(video_info))
            
            if video_info.thumbnail_url:
                pixmap = ThumbnailLoader.load_thumbnail(video_info.thumbnail_url)
                if pixmap:
                    self._thumbnail_label.setPixmap(pixmap)
        except (CookiesNotFoundError, VideoInfoError) as e:
            self._video_title.setText(f"⚠️ {str(e)}")
    
    def _update_progress(self, data: Dict[str, Any]) -> None:
        """Atualiza barra de progresso."""
        progress = ProgressParser.parse(data)
        
        if progress.is_downloading():
            value = int(progress.percent)
            self._progress_bar.setValue(value)
            self._progress_bar.setFormat(f"{value}%")
            
            eta_str = progress.get_formatted_eta()
            if eta_str:
                self._status.show_info(f"📥 Baixando... {value}% - {eta_str} restantes")
            else:
                self._status.show_info(f"📥 Baixando... {value}%")
        elif progress.is_finished():
            self._progress_bar.setValue(100)
            self._progress_bar.setFormat("100%")
            self._status.show_success("Download finalizado!")
    
    def _download_finished(self, result: str) -> None:
        """Processa finalização do download."""
        if result == "success":
            self._status.show_success("Download concluído!")
            if self._save_path:
                FileSystemUtils.open_folder(self._save_path)
        else:
            self._status.show_error(f"Erro: {result}")
        
        self._download_btn.setEnabled(True)
        self._is_downloading = False
    
    # Métodos para movimentação da janela
    def mousePressEvent(self, event) -> None:
        """Captura posição inicial do mouse."""
        if event.button() == Qt.LeftButton:
            self._old_pos = event.globalPos()
    
    def mouseMoveEvent(self, event) -> None:
        """Move a janela junto com o mouse."""
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self._old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self._old_pos = event.globalPos()
