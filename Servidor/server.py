import sys
import Pyro4
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl

class Video:
    def __init__(self, file_path, player):
        self.file_path = file_path
        self.player = player

    def play(self):
        url = QUrl.fromLocalFile(self.file_path)
        self.player.setMedia(QMediaContent(url))
        self.player.play()

    def pause(self):
        self.player.pause()

    def resume(self):
        self.player.play()

    def stop(self):
        self.player.stop()

class VideoPlayer(QWidget):
    def __init__(self, video_server):
        super().__init__()

        self.video_server = video_server  # Referência ao servidor de vídeo

        self.setWindowTitle("Video Player")
        self.setGeometry(350, 100, 700, 500)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.stateChanged.connect(self.on_state_changed)  # Conectar sinal de mudança de estado
        videoWidget = QVideoWidget()

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        self.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)

    def on_state_changed(self, state):
        if state == QMediaPlayer.StoppedState:
            self.video_server.stop_video()  # Notificar o servidor que o vídeo foi interrompido

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class VideoServer:
    def __init__(self, player):
        self.current_remote = None
        self.videos = {
            "video1": Video("C:\\Users\\diego\\Downloads\\ELDEN RING Official Launch Trailer.webm", player.mediaPlayer),
            "video2": Video("C:\\Users\\diego\\Downloads\\Bloodborne Debut Trailer ｜ Face Your Fears ｜ PlayStation 4 Action RPG.webm", player.mediaPlayer),
            "video3": Video("C:\\Users\\diego\\Downloads\\Demon's Souls - Announcement Trailer ｜ PS5.webm", player.mediaPlayer)
        }
        self.lock = threading.Lock()
        self.player = player
        self.playing = False
        self.video_stopped = False  # Sinalizador para indicar se o vídeo foi interrompido

    def play_video(self, video_key):
        with self.lock:
            if self.current_remote is not None:
                return f"Video is already playing on {self.current_remote}"
            video = self.videos.get(video_key)
            if video is None:
                return "Invalid video key"
            self.current_remote = video_key
            self.video_stopped = False  # Reset the stop flag

            # Execute o vídeo
            video.play()
            self.playing = True

            return "Video started playing = {self.playing}"

    def pause_video(self):
        with self.lock:
            if not self.video_stopped and self.current_remote is not None:
                video = self.videos[self.current_remote]
                video.pause()
                return "Video paused"
            else:
                return "Cannot pause, video has been stopped or not playing"

    def resume_video(self):
        with self.lock:
            if not self.video_stopped and self.current_remote is not None:
                video = self.videos[self.current_remote]
                video.resume()
                return "Video resumed"
            else:
                return "Cannot resume, video has been stopped or not playing"

    def stop_video(self):
        with self.lock:
            if self.current_remote is not None:
                video = self.videos[self.current_remote]
                video.stop()
                self.current_remote = None
                self.video_stopped = True  # Set the stop flag
                self.playing = False
                return "Video stopped"
            else:
                return "No video is currently playing"

    def fullscreen_video(self):
        with self.lock:
            self.player.fullscreen_video()
            return "Fullscreen toggled"

    def get_current_remote(self):
        with self.lock:
            return self.current_remote
        
    def isPlaying(self):
        return self.playing

def main():
    # Inicialize a aplicação Qt e o player
    app = QApplication(sys.argv)

    # Conectar ao servidor Pyro uma vez
    daemon = Pyro4.Daemon(host='192.168.0.5')  # Use a configuração de host padrão
    ns = Pyro4.locateNS()  # Localize o servidor de nomes
    player = VideoPlayer(None)  # Inicialize o player sem o servidor de vídeo por enquanto
    server = VideoServer(player)
    player.video_server = server  # Defina o servidor de vídeo no player
    uri = daemon.register(server)  # Registre a classe VideoServer
    ns.register("videoserver", uri)  # Registre a URI no servidor de nomes

    player.show()

    print("Video Server is ready.")

    # Execute o loop de requisições em uma thread separada
    server_thread = threading.Thread(target=daemon.requestLoop)
    server_thread.daemon = True
    server_thread.start()

    # Execute o loop da aplicação Qt
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
