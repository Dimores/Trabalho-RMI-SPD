import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QPushButton
from PyQt5.QtGui import QFont, QFontDatabase, QPalette, QColor, QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import Pyro4

class PlayWindow(QWidget):
    closed_signal = pyqtSignal()  # Sinal para indicar que a janela foi fechada

    def __init__(self, title, server):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(200, 200, 300, 200)
        self.server = server
        self.initUI()
        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.check_video_status)
        self.check_timer.start(1000)  # Verificar a cada 1 segundo

    def initUI(self):
        main_layout = QVBoxLayout()

        # Título
        title_label = QLabel(self.windowTitle())
        title_font = QFont("Montserrat", 24, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        title_label.setStyleSheet("color: white;")
        main_layout.addWidget(title_label)

        # Layout para os botões
        button_layout = QVBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)  # Remover margens internas

        # Botões
        self.pause_button = QPushButton("PAUSE", self)
        self.resume_button = QPushButton("RESUME", self)
        self.stop_button = QPushButton("STOP", self)

        for button in [self.pause_button, self.resume_button, self.stop_button]:
            button.setFont(QFont("Montserrat", 12))
            button.setStyleSheet("background-color: #333333; color: white; border-radius: 10px;")
            button.setFixedSize(100, 40)
            button.clicked.connect(self.handleButtonClick)
            button_layout.addWidget(button, alignment=Qt.AlignHCenter)
            button_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Adiciona espaçamento entre os botões

        button_layout.addStretch()  # Adiciona um espaço flexível antes dos botões

        # Layout centralizado
        central_layout = QVBoxLayout()
        central_layout.addStretch()  # Adiciona um espaço flexível acima dos botões
        central_layout.addLayout(button_layout)
        central_layout.addStretch()  # Adiciona um espaço flexível abaixo dos botões

        main_layout.addLayout(central_layout)
        self.setLayout(main_layout)
        self.setStyleSheet("background-color: black;")  # Cor de fundo preta

        self.current_button = None

        # Impedir que a janela seja fechada manualmente
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

    def handleButtonClick(self):
        sender = self.sender()

        if sender == self.pause_button:
            response = self.server.pause_video()
        elif sender == self.resume_button:
            response = self.server.resume_video()
        elif sender == self.stop_button:
            response = self.server.stop_video()
            self.close()  # Fechar a janela ao clicar em STOP
        
        self.updateButtonStyles(sender)
        print(response)

    def updateButtonStyles(self, clicked_button):
        buttons = [self.pause_button, self.resume_button, self.stop_button]
        for button in buttons:
            if button == clicked_button:
                button.setStyleSheet("background-color: #333333; color: white; border-radius: 10px; border: 2px solid #E50914;")
            else:
                button.setStyleSheet("background-color: #333333; color: white; border-radius: 10px; border: none;")

    def check_video_status(self):
        if not self.server.isPlaying():
            self.close()

    def closeEvent(self, event):
        self.check_timer.stop()
        self.closed_signal.emit()
        super().closeEvent(event)

class HoverLabel(QWidget):
    playClicked = pyqtSignal(str)  # Sinal para emitir o título do jogo

    def __init__(self, image_path, button_text, audio_path, title, video_name, server):
        super().__init__()
        self.image_path = image_path
        self.button_text = button_text
        self.audio_path = audio_path
        self.title = title  # Título do jogo
        self.video_name = video_name
        self.server = server
        self.initUI()
        self.initAudio()

    def initUI(self):
        self.setFixedSize(200, 200)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.image_label = QLabel(self)
        self.pixmap = QPixmap(self.image_path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        final_image = QImage(200, 200, QImage.Format_ARGB32)
        final_image.fill(Qt.transparent)
        painter = QPainter(final_image)
        x_offset = (200 - self.pixmap.width()) // 2
        y_offset = (200 - self.pixmap.height()) // 2
        painter.drawPixmap(x_offset, y_offset, self.pixmap)
        painter.end()
        self.image_label.setPixmap(QPixmap.fromImage(final_image))
        layout.addWidget(self.image_label)

        self.button = QPushButton(self.button_text, self)
        self.button.setFont(QFont("Montserrat", 12))
        self.button.setStyleSheet("background-color: black; color: white; border-radius: 10px;")
        self.button.setFixedSize(100, 40)
        self.button.move(50, 80)
        self.button.setVisible(False)  # Inicialmente invisível
        self.button.clicked.connect(self.onPlayClicked)  # Conectar o botão Play ao slot

    def initAudio(self):
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.audio_path)))
        self.player.setPlaybackRate(1.0)  # Normal playback rate
        self.player.stateChanged.connect(self.checkIfFinished)  # Connect signal to check when audio ends

    def checkIfFinished(self, state):
        if state == QMediaPlayer.StoppedState:
            self.player.stop()  # Ensure player stops when audio ends

    def enterEvent(self, event):
        self.set_image_with_overlay(150)
        self.button.setVisible(True)
        self.player.play()  # Iniciar a reprodução do áudio

    def leaveEvent(self, event):
        self.set_image_with_overlay(0)
        self.button.setVisible(False)
        self.player.stop()  # Parar a reprodução do áudio

    def set_image_with_overlay(self, darkness):
        final_image = QImage(200, 200, QImage.Format_ARGB32)
        final_image.fill(Qt.transparent)
        painter = QPainter(final_image)
        painter.drawPixmap(0, 0, self.pixmap)
        if darkness > 0:
            painter.fillRect(final_image.rect(), QColor(0, 0, 0, darkness))
        painter.end()
        self.image_label.setPixmap(QPixmap.fromImage(final_image))

    def onPlayClicked(self):
        # Parar a música antes de abrir a nova janela
        self.player.stop()
        if not self.server.isPlaying():
            # Emitir o sinal para abrir a nova janela
            self.playClicked.emit(self.title)
            # Tocar o vídeo correspondente
            response = self.server.play_video(self.video_name)
            print(response)

class FromSoftwareGamesWindow(QWidget):
    def __init__(self, server):
        super().__init__()
        self.server = server
        self.play_window = None  # Referência à janela de reprodução
        self.initUI()

    def initUI(self):
        self.setWindowTitle("3 melhores jogos da FromSoftware")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()

        # Título
        title = QLabel("3 melhores jogos da FromSoftware")
        title_font = QFont("Montserrat", 24, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        title.setStyleSheet("color: white;")
        main_layout.addWidget(title)

        # Adicionar espaçamento entre o título e os jogos
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Layout horizontal para os jogos
        games_layout = QHBoxLayout()
        games_layout.setSpacing(20)  # Ajustar o espaçamento entre os jogos

        games = [
            ("Elden Ring", "96", "Imgs/EldenRing.jpg", "audios/EldenRing.mp3", "video1"),
            ("Bloodborne", "92", "Imgs/Bloodborne.jpg", "audios/Bloodborne.mp3", "video2"),
            ("Demon's Souls", "92", "Imgs/DemonSouls.jpg", "audios/DemonsSouls.mp3", "video3")
        ]

        for game, rating, image_path, audio_path, video_name in games:
            game_layout = QVBoxLayout()

            game_label = QLabel(game)
            game_font = QFont("Montserrat", 18)
            game_label.setFont(game_font)
            game_label.setAlignment(Qt.AlignCenter)
            game_label.setStyleSheet("color: white;")
            game_layout.addWidget(game_label)

            image_label = HoverLabel(image_path, "Play", audio_path, game, video_name, self.server)
            game_layout.addWidget(image_label, alignment=Qt.AlignCenter)

            rating_label = QLabel(rating)
            rating_font = QFont("Montserrat", 16)
            rating_label.setFont(rating_font)
            rating_label.setAlignment(Qt.AlignCenter)
            rating_label.setStyleSheet("color: green;")
            game_layout.addWidget(rating_label)

            games_layout.addLayout(game_layout)

        main_layout.addLayout(games_layout)

        # Adicionar espaçamento na parte inferior
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(main_layout)

        # Paleta de cores
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))  # Cor de fundo preta
        self.setPalette(palette)

        # Conectar sinal para abrir a nova janela
        self.hover_labels = [widget for widget in self.findChildren(HoverLabel)]
        for hover_label in self.hover_labels:
            hover_label.playClicked.connect(self.openPlayWindow)

    @pyqtSlot()
    def onPlayWindowClosed(self):
        self.play_window = None  # Resetar a referência da janela de reprodução
        self.setEnabled(True)  # Reativar a tela de início

    def openPlayWindow(self, title):
        if self.play_window is None:  # Verificar se a janela já está aberta
            self.play_window = PlayWindow(title, self.server)
            self.play_window.closed_signal.connect(self.onPlayWindowClosed)  # Conectar o sinal de fechamento
            self.play_window.show()
            self.setEnabled(False)  # Desativar a tela de início

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Carregar fonte Montserrat
    QFontDatabase.addApplicationFont("fonts/Montserrat-Regular.ttf")
    QFontDatabase.addApplicationFont("fonts/Montserrat-Bold.ttf")

    # Conectar ao servidor Pyro uma vez
    server = Pyro4.Proxy("PYRONAME:videoserver")

    window = FromSoftwareGamesWindow(server)
    window.show()
    sys.exit(app.exec_())
