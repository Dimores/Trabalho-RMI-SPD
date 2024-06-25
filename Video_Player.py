import cv2
import threading
import time
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from ffpyplayer.player import MediaPlayer

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Player")
        
        self.panel = tk.Label(root)
        self.panel.pack()

        self.btn_open = tk.Button(root, text="Open Video", command=self.open_video)
        self.btn_open.pack(side="left")

        self.btn_play = tk.Button(root, text="Play", command=self.play_video)
        self.btn_play.pack(side="left")

        self.btn_pause = tk.Button(root, text="Pause", command=self.pause_video)
        self.btn_pause.pack(side="left")

        self.btn_stop = tk.Button(root, text="Stop", command=self.stop_video)
        self.btn_stop.pack(side="left")

        self.cap = None
        self.player = None
        self.playing = False
        self.paused = False
        self.stop = False
        self.fps = 0
        self.frame_time = 0
        self.thread = None

    def open_video(self):
        self.video_path = filedialog.askopenfilename()
        self.cap = cv2.VideoCapture(self.video_path)
        self.player = MediaPlayer(self.video_path)
        if self.cap.isOpened():
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.frame_time = 1 / self.fps

    def play_video(self):
        if not self.cap or not self.cap.isOpened():
            return
        if not self.playing:
            self.playing = True
            self.stop = False
            self.thread = threading.Thread(target=self.update_frame, daemon=True)
            self.thread.start()
        self.paused = False
        if self.player:
            self.player.set_pause(False)

    def pause_video(self):
        self.paused = True
        if self.player:
            self.player.set_pause(True)

    def stop_video(self):
        self.stop = True
        self.playing = False
        self.paused = False
        if self.cap:
            self.cap.release()
        if self.player:
            self.player.close_player()
        self.cap = None
        self.panel.config(image='')

    def update_frame(self):
        while self.playing and not self.stop:
            if self.paused:
                time.sleep(0.1)
                continue

            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(frame)

            self.panel.config(image=frame)
            self.panel.image = frame
            self.root.update()

            time.sleep(self.frame_time)  # Esperar pelo tempo de exibição do frame

        self.playing = False

if __name__ == "__main__":
    root = tk.Tk()
    player = VideoPlayer(root)
    root.mainloop()
