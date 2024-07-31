import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pygame
import os

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("800x500")

        self.icon = tk.PhotoImage(file=r"C:/Users/ARAVIND/Documents/Music player/appicon.png")
        self.root.iconphoto(False, self.icon)

        self.current_song = ""
        self.paused = False
        self.playlist = []
        self.current_index = -1
        self.playing = False  

        self.background_image = ImageTk.PhotoImage(Image.open(r"C:/Users/ARAVIND/Documents/Music player/background.png").resize((750,
                                                                                                                                 750), Image.Resampling.LANCZOS))
        self.play_image = ImageTk.PhotoImage(Image.open(r"C:/Users/ARAVIND/Documents/Music player/play.png").resize((50, 50), Image.Resampling.LANCZOS))
        self.pause_image = ImageTk.PhotoImage(Image.open(r"C:/Users/ARAVIND/Documents/Music player/pause.png").resize((50, 50), Image.Resampling.LANCZOS))
        self.next_image = ImageTk.PhotoImage(Image.open(r"C:/Users/ARAVIND/Documents/Music player/next.png").resize((50, 50), Image.Resampling.LANCZOS))
        self.prev_image = ImageTk.PhotoImage(Image.open(r"C:/Users/ARAVIND/Documents/Music player/previous.png").resize((50, 50), Image.Resampling.LANCZOS))
        self.volume_image = ImageTk.PhotoImage(Image.open(r"C:/Users/ARAVIND/Documents/Music player/volume.png").resize((50, 50), Image.Resampling.LANCZOS))
        self.browse_image = ImageTk.PhotoImage(Image.open(r"C:/Users/ARAVIND/Documents/Music player/browse.png").resize((50, 50), Image.Resampling.LANCZOS))

       
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        
        self.widget_frame = tk.Frame(self.root, bg='black', bd=0)
        self.widget_frame.place(relwidth=1, relheight=1)

        self.song_label = tk.Label(self.widget_frame, text="No song selected", bg="black", fg="white")
        self.song_label.pack(pady=10)

        self.control_frame = tk.Frame(self.widget_frame, bg='black')
        self.control_frame.pack(side=tk.BOTTOM, pady=20)

        self.volume_button = tk.Button(self.control_frame, image=self.volume_image, bg="yellow", command=self.adjust_volume)
        self.volume_button.pack(side=tk.LEFT, padx=10)

        self.play_pause_button = tk.Button(self.control_frame, image=self.play_image, bg="green", command=self.play_pause)
        self.play_pause_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(self.control_frame, image=self.next_image, bg="purple", command=self.play_next)
        self.next_button.pack(side=tk.LEFT, padx=10)

        self.prev_button = tk.Button(self.control_frame, image=self.prev_image, bg="purple", command=self.play_previous)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.browse_button = tk.Button(self.control_frame, image=self.browse_image, bg="orange", command=self.browse_file)
        self.browse_button.pack(side=tk.LEFT, padx=10)

        self.seek_bar = tk.Scale(self.widget_frame, from_=0, to=100, orient=tk.HORIZONTAL, bg="blue", command=self.seek_update)
        self.seek_bar.pack(pady=10, fill=tk.X, padx=20)
        self.seek_bar.pack(side=tk.BOTTOM, pady=10)

        pygame.init()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

    def browse_file(self):
        song = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if song:
            try:
                self.playlist.append(song)
                if not self.playing:
                    self.play_next()
            except Exception as e:
                print("Error loading song:", e)

    def play_song(self, song):
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        self.playing = True
        self.update_seek_bar()

    def update_seek_bar(self):
        if self.playing:
            position = pygame.mixer.music.get_pos() / 1000  
            length = self.get_song_length(self.current_song)
            if length:
                progress = (position / length) * 100
                self.seek_bar.set(progress)
            self.root.after(100, self.update_seek_bar)

    def seek_update(self, value):
        if self.playing:
            length = self.get_song_length(self.current_song)
            position = (float(value) / 100) * length
            pygame.mixer.music.set_pos(position)

    def adjust_volume(self):
        volume = pygame.mixer.music.get_volume()
        if volume >= 1.0:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(min(volume + 0.1, 1.0))

    def play_pause(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.play_pause_button.config(image=self.pause_image, bg="green")
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.play_pause_button.config(image=self.play_image, bg="red")
            self.paused = True

    def play_next(self):
        if len(self.playlist) > 0:
            self.current_index = (self.current_index + 1) % len(self.playlist)  
            self.current_song = self.playlist[self.current_index]
            self.song_label.config(text=os.path.basename(self.current_song))
            self.play_song(self.current_song)

    def play_previous(self):
        if len(self.playlist) > 0:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.current_song = self.playlist[self.current_index]
            self.song_label.config(text=os.path.basename(self.current_song))
            self.play_song(self.current_song)

    def get_song_length(self, song):
        try:
            audio = pygame.mixer.Sound(song)
            length = audio.get_length()
            return length
        except Exception as e:
            print("Error getting song length:", e)
            return None

root = tk.Tk()
app = MusicPlayer(root)
root.mainloop()
