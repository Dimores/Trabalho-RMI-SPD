import tkinter as tk
from tkinter import font as tkfont
import Pyro4
from tkinter import messagebox

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Escolha uma máquina")
        self.configure(bg='#000000')
        self.geometry("400x300")

        self.title_font = tkfont.Font(family="Montserrat", size=18, weight="bold")
        self.button_font = tkfont.Font(family="Montserrat", size=12, weight="bold")

        self.title_label = tk.Label(self, text="Escolha uma máquina", bg='#000000', fg='#FFFFFF', font=self.title_font)
        self.title_label.pack(pady=20)

        self.button_frame = tk.Frame(self, bg='#000000')
        self.button_frame.pack(pady=20)

        self.buttons = []
        self.borders = []  # Store the borders to manipulate later
        for i in range(1, 4):
            button, border = self.create_round_button(f"Máquina {i}", 100, 50, i)
            button.grid(row=0, column=i-1, padx=10)
            self.buttons.append(button)
            self.borders.append(border)

        self.selected_button = None
        self.command_windows = {}  # Dictionary to store command windows

    def create_round_button(self, text, width, height, index):
        canvas = tk.Canvas(self.button_frame, width=width, height=height, bg='#000000', highlightthickness=0)
        radius = 10
        x0, y0, x1, y1 = 10, 10, width-10, height-10
        
        # Draw the button
        button = canvas.create_oval(x0, y0, x1, y1, fill='#333333', outline='#333333')
        
        text_id = canvas.create_text(width//2, height//2, text=text, fill='#FFFFFF', font=self.button_font)
        
        # Draw an invisible border initially
        border = canvas.create_oval(x0-2, y0-2, x1+2, y1+2, outline='#000000', width=2)

        canvas.tag_bind(button, "<Button-1>", lambda event, idx=index: self.on_button_click(idx))
        canvas.tag_bind(text_id, "<Button-1>", lambda event, idx=index: self.on_button_click(idx))
        canvas.bind("<Button-1>", lambda event, idx=index: self.on_button_click(idx))
        
        return canvas, border

    def on_button_click(self, button_index):
        if self.selected_button is not None:
            self.remove_red_border(self.selected_button - 1)
        self.selected_button = button_index
        self.add_red_border(button_index - 1)
        
        # Open a new command window if not already open
        remote_id = f"remote{button_index}"
        if remote_id not in self.command_windows or not self.command_windows[remote_id].winfo_exists():
            self.command_windows[remote_id] = CommandWindow(self, remote_id)

    def add_red_border(self, index):
        canvas = self.buttons[index]
        border = self.borders[index]
        canvas.itemconfig(border, outline='#E50914')

    def remove_red_border(self, index):
        canvas = self.buttons[index]
        border = self.borders[index]
        canvas.itemconfig(border, outline='#000000')

class CommandWindow(tk.Toplevel):
    def __init__(self, master, remote_id):
        super().__init__(master)

        self.title("Escolha um comando")
        self.configure(bg='#000000')
        self.geometry("400x300")

        self.remote_name = f"example.{remote_id}"
        self.video_server = Pyro4.Proxy("PYRONAME:example.videoserver")

        self.title_font = tkfont.Font(family="Montserrat", size=18, weight="bold")
        self.button_font = tkfont.Font(family="Montserrat", size=12, weight="bold")

        self.title_label = tk.Label(self, text="Escolha um comando", bg='#000000', fg='#FFFFFF', font=self.title_font)
        self.title_label.pack(pady=20)

        self.button_frame = tk.Frame(self, bg='#000000')
        self.button_frame.pack(pady=20)

        self.create_command_button("Play", self.button_font, self.play_video).pack(pady=5)
        self.create_command_button("Pause", self.button_font, self.pause_video).pack(pady=5)
        self.create_command_button("Resume", self.button_font, self.resume_video).pack(pady=5)
        self.create_command_button("Stop", self.button_font, self.stop_video).pack(pady=5)
        self.create_command_button("Exit", self.button_font, self.destroy).pack(pady=5)

    def create_command_button(self, text, font, command):
        button = tk.Button(self.button_frame, text=text, font=font, bg='#333333', fg='#FFFFFF', activebackground='#555555', activeforeground='#FFFFFF', command=command)
        button.configure(width=10, height=2)
        return button

    def show_response(self, response):
        messagebox.showinfo("Response", response)

    def play_video(self):
        response = self.video_server.play_video(self.remote_name)
        self.show_response(response)

    def pause_video(self):
        response = self.video_server.pause_video(self.remote_name)
        self.show_response(response)

    def resume_video(self):
        response = self.video_server.resume_video(self.remote_name)
        self.show_response(response)

    def stop_video(self):
        response = self.video_server.stop_video(self.remote_name)
        self.show_response(response)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
