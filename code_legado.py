import sys
import os
import re
import platform
import requests
import yt_dlp

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QRectF
from PyQt5.QtGui import QIcon, QPainterPath, QImage, QPixmap, QColor, QRegion

from firebase_config import auth

class LoginWindow(QWidget):
    def __init__(self, open_downloader_callback):
        super().__init__()
        self.open_downloader_callback = open_downloader_callback
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowTitle("Auth - YouTube Gamer DL")
        self.setFixedSize(420, 360)
        self.setStyleSheet("background-color: #1b1c1f; color: white; font-size: 14px; font-family: 'Segoe UI Semibold';")

        self.stack = QStackedWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)
        layout.setContentsMargins(10, 10, 10, 10)

        self.stack.addWidget(self.page_login())
        self.stack.addWidget(self.page_register())
        self.stack.addWidget(self.page_recover())

    # ---------------- LOGIN ----------------
    def page_login(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("🔐 Login")
        title.setStyleSheet("font-size: 24px; color: #f04747; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        self.email_login = QLineEdit()
        self.email_login.setPlaceholderText("E-mail")
        self.senha_login = QLineEdit()
        self.senha_login.setPlaceholderText("Senha")
        self.senha_login.setEchoMode(QLineEdit.Password)

        self.status_login = QLabel("")

        btn_login = QPushButton("Entrar")
        btn_login.clicked.connect(self.do_login)

        btn_register = QPushButton("Criar conta")
        btn_register.setFlat(True)
        btn_register.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        btn_recover = QPushButton("Esqueci minha senha")
        btn_recover.setFlat(True)
        btn_recover.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        for w in (self.email_login, self.senha_login, btn_login, btn_register, btn_recover):
            w.setStyleSheet("padding: 12px; border-radius: 8px; background-color: #2b2d31; color: white;")

        layout.addWidget(title)
        layout.addWidget(self.email_login)
        layout.addWidget(self.senha_login)
        layout.addWidget(btn_login)
        layout.addWidget(btn_register)
        layout.addWidget(btn_recover)
        layout.addWidget(self.status_login)

        return page

    # ---------------- CADASTRO ----------------
    def page_register(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("🆕 Cadastro")
        title.setStyleSheet("font-size: 24px; color: #f04747; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        self.email_reg = QLineEdit()
        self.email_reg.setPlaceholderText("E-mail")

        self.senha_reg = QLineEdit()
        self.senha_reg.setPlaceholderText("Senha")
        self.senha_reg.setEchoMode(QLineEdit.Password)

        self.status_reg = QLabel("")

        btn_create = QPushButton("Criar conta")
        btn_create.clicked.connect(self.do_register)

        btn_back = QPushButton("Voltar")
        btn_back.setFlat(True)
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        for w in (self.email_reg, self.senha_reg, btn_create, btn_back):
            w.setStyleSheet("padding: 12px; border-radius: 8px; background-color: #2b2d31; color: white;")

        layout.addWidget(title)
        layout.addWidget(self.email_reg)
        layout.addWidget(self.senha_reg)
        layout.addWidget(btn_create)
        layout.addWidget(btn_back)
        layout.addWidget(self.status_reg)

        return page

    # ---------------- RECUPERAR SENHA ----------------
    def page_recover(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("🔁 Recuperar Senha")
        title.setStyleSheet("font-size: 24px; color: #f04747; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)

        self.email_rec = QLineEdit()
        self.email_rec.setPlaceholderText("E-mail cadastrado")

        self.status_rec = QLabel("")

        btn_recover = QPushButton("Enviar recuperação")
        btn_recover.clicked.connect(self.do_recover)

        btn_back = QPushButton("Voltar")
        btn_back.setFlat(True)
        btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        for w in (self.email_rec, btn_recover, btn_back):
            w.setStyleSheet("padding: 12px; border-radius: 8px; background-color: #2b2d31; color: white;")

        layout.addWidget(title)
        layout.addWidget(self.email_rec)
        layout.addWidget(btn_recover)
        layout.addWidget(btn_back)
        layout.addWidget(self.status_rec)

        return page

    # ---------------- ACTIONS (FIREBASE) ----------------
    def do_login(self):
        try:
            auth.sign_in_with_email_and_password(self.email_login.text(), self.senha_login.text())
            self.status_login.setText("✔ Login realizado!")
            self.open_downloader_callback()
            self.close()
        except:
            self.status_login.setText("❌ E-mail ou senha incorretos.")

    def do_register(self):
        try:
            auth.create_user_with_email_and_password(self.email_reg.text(), self.senha_reg.text())
            self.status_reg.setText("✔ Conta criada! Agora faça login.")
        except:
            self.status_reg.setText("❌ Erro ao criar conta. Verifique e-mail e senha.")

    def do_recover(self):
        try:
            auth.send_password_reset_email(self.email_rec.text())
            self.status_rec.setText("✔ Link de recuperação enviado para o e-mail!")
        except:
            self.status_rec.setText("❌ E-mail não encontrado no Firebase.")

class DownloadThread(QThread):
    progress_signal = pyqtSignal(dict)
    finished_signal = pyqtSignal(str)

    def __init__(self, url, save_path, format_choice, custom_title):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.format_choice = format_choice
        self.custom_title = custom_title.strip()

    def run(self):
        def hook(d):
            self.progress_signal.emit(d)

        format_map = {
            "Melhor qualidade": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
            "Qualidade até 720p": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]",
            "Áudio MP3": "bestaudio[ext=m4a]",
        }

        cookies_file = 'youtube.com_cookies.txt'

        if not os.path.exists(cookies_file):
            self.finished_signal.emit(f"⚠️ Arquivo de cookies '{cookies_file}' não encontrado.\n"
                                      "Exporte usando a extensão 'Get cookies.txt clean' e salve na pasta do app.")
            return

        filename = self.custom_title if self.custom_title else "%(title)s"

        ydl_opts = {
            'format': format_map.get(self.format_choice, 'best'),
            'outtmpl': os.path.join(self.save_path, f'{filename}.%(ext)s'),
            'merge_output_format': 'mp4',
            'cookiefile': cookies_file,
            'progress_hooks': [hook],
            'quiet': True,
            'noprogress': True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            self.finished_signal.emit("success")
        except Exception as e:
            self.finished_signal.emit(str(e))

class VideoDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(540, 500)
        self.setWindowIcon(QIcon("icon.png"))
        self.setAcceptDrops(True)
        self.is_downloading = False
        self.old_pos = self.pos()

        path = QPainterPath()
        radius = 16
        rect = QRectF(self.rect())
        path.addRoundedRect(rect, radius, radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

        self.setStyleSheet("""
            QWidget {
                background-color: #1b1c1f;
                color: #f2f3f5;
                font-family: 'Segoe UI Semibold';
                font-size: 14px;
            }
            QLineEdit {
                background-color: #2b2d31;
                border: 2px solid #444;
                border-radius: 8px;
                padding: 10px;
            }
            QLineEdit:focus {
                border-color: #f04747;
            }
            QPushButton {
                background-color: #f04747;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #d73737;
            }
            QLabel {
                padding: 4px;
            }
            QProgressBar {
                background-color: #2b2d31;
                border-radius: 6px;
                height: 18px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #f04747;
                border-radius: 6px;
            }
            QComboBox {
                background-color: #2b2d31;
                border: 2px solid #444;
                border-radius: 8px;
                padding: 8px;
                color: #f2f3f5;
            }
        """)

        self.init_ui()

    def init_ui(self):
        bar = QFrame(self)
        bar.setFixedHeight(36)
        bar.setStyleSheet("background-color: #202225;")
        h = QHBoxLayout(bar)
        h.setContentsMargins(10, 0, 10, 0)

        title = QLabel("▶ YouTube Gamer DL")
        title.setStyleSheet("color: #f04747; font-size: 16px; font-weight: bold;")

        btn_min = QPushButton("–")
        btn_min.setFixedSize(30, 30)
        btn_min.clicked.connect(self.showMinimized)

        btn_close = QPushButton("×")
        btn_close.setFixedSize(30, 30)
        btn_close.clicked.connect(self.close)

        for btn in (btn_min, btn_close):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #f04747;
                    font-size: 16px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #3c3f45;
                    border-radius: 5px;
                }
            """)

        h.addWidget(title)
        h.addStretch()
        h.addWidget(btn_min)
        h.addWidget(btn_close)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Cole o link do vídeo do YouTube...")

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Nome do arquivo (opcional)")

        self.format_box = QComboBox()
        self.format_box.addItems(["Melhor qualidade", "Qualidade até 720p", "Áudio MP3"])

        self.download_btn = QPushButton("🎬 Baixar Vídeo")
        self.download_btn.clicked.connect(self.download_video)

        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(20)
        glow.setColor(QColor("#f04747"))
        glow.setOffset(0)
        self.download_btn.setGraphicsEffect(glow)

        self.status = QLabel("")
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.progress_bar.setFormat("0%")

        self.video_title = QLabel("")
        self.thumbnail_label = QLabel()

        v = QVBoxLayout(self)
        v.addWidget(bar)
        v.addStretch()
        v.addWidget(self.url_input)
        v.addWidget(self.title_input)
        v.addWidget(self.format_box)
        v.addWidget(self.download_btn)
        v.addWidget(self.progress_bar)
        v.addWidget(self.status)
        v.addWidget(self.video_title)
        v.addWidget(self.thumbnail_label)
        v.addStretch()
        v.setContentsMargins(20, 20, 20, 20)

    def download_video(self):
        url = self.url_input.text().strip()
        custom_title = self.title_input.text().strip()

        if not re.match(r"^https?://(www\.)?(youtube\.com|youtu\.be)/", url):
            self.status.setText("❌ URL inválida.")
            return

        if not url or self.is_downloading:
            return

        save_path = QFileDialog.getExistingDirectory(self, "Escolha a pasta para salvar")
        if not save_path:
            self.status.setText("❌ Caminho de destino não escolhido.")
            return

        self.is_downloading = True
        self.download_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("0%")
        self.status.setText("📥 Preparando...")

        format_choice = self.format_box.currentText()

        self.download_thread = DownloadThread(url, save_path, format_choice, custom_title)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.finished_signal.connect(self.download_finished)
        self.download_thread.start()
        self.save_path = save_path

        self.get_video_info(url)

    def get_video_info(self, url):
        cookies_file = 'youtube.com_cookies.txt'

        if not os.path.exists(cookies_file):
            self.video_title.setText("⚠️ Cookies ausentes para obter título e thumbnail.")
            return

        ydl_opts = {
            'quiet': True,
            'cookiefile': cookies_file,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Título não disponível')
                thumb = info.get('thumbnail', '')
                self.video_title.setText(f"📹 {title}")
                if thumb:
                    self.load_thumbnail(thumb)
        except Exception as e:
            print("Erro ao obter info:", e)
            self.video_title.setText("❌ Não foi possível obter informações do vídeo.")

    def load_thumbnail(self, url):
        try:
            img = requests.get(url).content
            image = QImage()
            image.loadFromData(img)
            pixmap = QPixmap(image)
            self.thumbnail_label.setPixmap(pixmap.scaled(200, 150, Qt.KeepAspectRatio))
        except Exception as e:
            print("Erro ao carregar thumbnail:", e)

    def update_progress(self, d):
        if d['status'] == 'downloading':
            percent_str = d.get('_percent_str', '').strip()
            percent_clean = re.sub(r'\x1b\[[0-9;]*m', '', percent_str).replace('%', '')

            if percent_clean:
                try:
                    value = int(float(percent_clean))
                    self.progress_bar.setValue(value)
                    self.progress_bar.setFormat(f"{value}%")
                    eta = d.get('eta')
                    if eta:
                        mins, secs = divmod(eta, 60)
                        self.status.setText(f"📥 Baixando... {value}% - {int(mins):02d}:{int(secs):02d} restantes")
                    else:
                        self.status.setText(f"📥 Baixando... {value}%")
                except ValueError as e:
                    print("Erro ao converter percent:", e)
                    self.status.setText("⚠️ Erro ao processar progresso.")
            else:
                self.status.setText("🔄 Iniciando download...")
        elif d['status'] == 'finished':
            self.progress_bar.setValue(100)
            self.progress_bar.setFormat("100%")
            self.status.setText("✅ Download finalizado!")

    def download_finished(self, result):
        if result == "success":
            self.status.setText("✅ Download concluído!")
            if platform.system() == 'Windows':
                os.startfile(self.save_path)
            elif platform.system() == 'Darwin':
                os.system(f"open {self.save_path}")
            else:
                os.system(f"xdg-open {self.save_path}")
        else:
            self.status.setText(f"❌ Erro: {result}")
        self.download_btn.setEnabled(True)
        self.is_downloading = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()
    def _banco_de_dados(self):
        # Espaço reservado para integração futura com banco de dados
        pass


class AppController:
    """Controlador simples que inicializa a aplicação e alterna janelas.

    Mantém referências às janelas para evitar coleta pelo GC do PyQt.
    """

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_window = LoginWindow(self.open_downloader)
        self.downloader = None

    def open_downloader(self):
        if self.downloader is None:
            self.downloader = VideoDownloader()
        self.downloader.show()

    def run(self):
        self.login_window.show()
        return self.app.exec_()


if __name__ == "__main__":
    controller = AppController()
    sys.exit(controller.run())


