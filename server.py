import Pyro4
import threading

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class VideoServer:
    def __init__(self):
        self.current_remote = None
        self.videos = {
            "example.remote1": "C:\\Users\\Arthur Aguiar\\Desktop\\SPD\\Atividade Avaliativa 2\\VideoPlayer\\BM.mp4",
            "example.remote2": "C:\\Users\\diego\\OneDrive\\Documentos\\SPD\\Trabalho 2\\videos\\BM.mp4"
        }
        self.lock = threading.Lock()

    def play_video(self, remote_id):
        with self.lock:
            if self.current_remote is not None:
                return f"Video is already playing on {self.current_remote}"
            video_path = self.videos.get(remote_id)
            if video_path is None:
                return "Invalid remote ID"
            self.current_remote = remote_id
            remote = Pyro4.Proxy(f"PYRONAME:{remote_id}")
            response = remote.play_video(video_path)
            return response

    def pause_video(self, remote_id):
        with self.lock:
            if self.current_remote != remote_id:
                return "Video is not playing on this remote"
            remote = Pyro4.Proxy(f"PYRONAME:{remote_id}")
            response = remote.pause_video()
            return response

    def resume_video(self, remote_id):
        with self.lock:
            if self.current_remote != remote_id:
                return "Video is not playing on this remote"
            remote = Pyro4.Proxy(f"PYRONAME:{remote_id}")
            response = remote.resume_video()
            return response

    def stop_video(self, remote_id):
        with self.lock:
            if self.current_remote != remote_id:
                return "Video is not playing on this remote"
            remote = Pyro4.Proxy(f"PYRONAME:{remote_id}")
            response = remote.stop_video()
            self.current_remote = None
            return response

def main():
    daemon = Pyro4.Daemon(host='192.168.0.5')  # Use o endereço IP da máquina onde está o servidor de nomes
    uri = daemon.register(VideoServer)
    ns = Pyro4.locateNS(host='192.168.0.5', port=9090)  # Certifique-se de que o host e a porta estão corretos
    ns.register("example.videoserver", uri)

    print("Video Server is ready.")
    daemon.requestLoop()

if __name__ == "__main__":
    main()

