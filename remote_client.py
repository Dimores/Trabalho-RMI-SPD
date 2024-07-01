import Pyro4
import cv2
import threading

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class RemoteVideoClient:
    def __init__(self):
        self.current_video = None
        self.playing = False
        self.paused = False
        self.lock = threading.Lock()
        self.thread = None

    def play_video(self, video_path):
        with self.lock:
            if self.current_video is not None:
                return "Another video is already playing"
            
            self.current_video = video_path
            self.playing = True
            self.paused = False
            self.thread = threading.Thread(target=self._play_video_thread)
            self.thread.start()
            return "Video started"

    def _play_video_thread(self):
        cap = cv2.VideoCapture(self.current_video)
        
        while self.playing and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow('Video', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

            while self.paused:
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
        
        cap.release()
        cv2.destroyAllWindows()
        with self.lock:
            self.current_video = None
            self.playing = False
            self.paused = False

    def pause_video(self):
        with self.lock:
            if self.playing and not self.paused:
                self.paused = True
                return "Video paused"
            elif self.paused:
                return "Video is already paused"
            else:
                return "No video is playing"

    def resume_video(self):
        with self.lock:
            if self.current_video is not None and self.paused:
                self.paused = False
                return "Video resumed"
            else:
                return "No video to resume"

    def stop_video(self):
        with self.lock:
            if self.current_video is not None:
                self.playing = False
                self.current_video = None
                return "Video stopped"
            else:
                return "No video to stop"

def main():
    daemon = Pyro4.Daemon(host='192.168.0.5')  # Use o endereço IP da máquina onde está o servidor de nomes
    ns = Pyro4.locateNS(host='192.168.0.5', port=9090)  # Certifique-se de que o host e a porta estão corretos
    remote_id = "remote2"  # Substitua pelo ID correto para cada cliente remoto
    uri = daemon.register(RemoteVideoClient)
    ns.register(f"example.{remote_id}", uri)

    print(f"Remote Video Client {remote_id} is ready.")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
