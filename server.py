import Pyro4
import cv2
import threading

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class VideoServer:
    def __init__(self):
        self.current_video = None
        self.playing = False
        self.lock = threading.Lock()
        self.pause_condition = threading.Condition(self.lock)
        self.client_id = None

    def play_video(self, video_path, client_id):
        with self.lock:
            if self.current_video is not None:
                return "Another video is already playing"
            
            self.current_video = video_path
            self.playing = True
            self.client_id = client_id
            self.thread = threading.Thread(target=self._play_video_thread)
            self.thread.start()
            return "Video started"

    def _play_video_thread(self):
        cap = cv2.VideoCapture(self.current_video)
        
        while True:
            with self.pause_condition:
                while not self.playing:
                    self.pause_condition.wait()
                if self.current_video is None:
                    break

            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow('Video', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                continue
        
        cap.release()
        cv2.destroyAllWindows()
        with self.lock:
            self.current_video = None
            self.playing = False
            self.client_id = None

    def pause_video(self, client_id):
        with self.lock:
            if self.client_id != client_id:
                return "You are not authorized to pause this video"
            if self.playing:
                self.playing = False
                return "Video paused"
            else:
                return "No video is playing"

    def resume_video(self, client_id):
        with self.lock:
            if self.client_id != client_id:
                return "You are not authorized to resume this video"
            if self.current_video is not None and not self.playing:
                self.playing = True
                self.pause_condition.notify()
                return "Video resumed"
            else:
                return "No video to resume"

    def stop_video(self, client_id):
        with self.lock:
            if self.client_id != client_id:
                return "You are not authorized to stop this video"
            if self.current_video is not None:
                self.playing = False
                self.current_video = None
                self.client_id = None
                self.pause_condition.notify()
                return "Video stopped"
            else:
                return "No video to stop"

def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(VideoServer)
    ns.register("example.videoserver", uri)

    print("Video Server is ready.")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
