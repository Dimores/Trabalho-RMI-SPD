import Pyro4
import threading
import subprocess
import psutil

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class RemoteVideoClient:
    def __init__(self):
        self.current_video = None
        self.process = None
        self.lock = threading.Lock()

    def play_video(self, video_path):
        with self.lock:
            if self.process is not None:
                return "Another video is already playing"
            
            self.current_video = video_path
            self.process = subprocess.Popen(["ffplay", "-autoexit", video_path])
            return "Video started"

    def pause_video(self):
        with self.lock:
            if self.process is not None:
                psutil.Process(self.process.pid).suspend()
                return "Video paused"
            else:
                return "No video is playing"

    def resume_video(self):
        with self.lock:
            if self.process is not None:
                psutil.Process(self.process.pid).resume()
                return "Video resumed"
            else:
                return "No video to resume"

    def stop_video(self):
        with self.lock:
            if self.process is not None:
                self.process.terminate()
                self.process = None
                self.current_video = None
                return "Video stopped"
            else:
                return "No video to stop"

def main():
    daemon = Pyro4.Daemon(host='172.25.9.70')  # Use o endereço IP da máquina onde está o servidor de nomes
    ns = Pyro4.locateNS(host='172.25.8.196', port=9090)  # Certifique-se de que o host e a porta estão corretos
    remote_id = "remote1"  # Substitua pelo ID correto para cada cliente remoto
    uri = daemon.register(RemoteVideoClient)
    ns.register(f"example.{remote_id}", uri)

    print(f"Remote Video Client {remote_id} is ready.")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
