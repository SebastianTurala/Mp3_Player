import tkinter as tk
from tkinter import filedialog
from pygame import mixer
import time
import sys

class App(tk.Tk):
    def __init__(self):
        super(App, self).__init__()
        mixer.init()

        # window config
        self.title('Mp3Player')

        # dictionary with titles and directories
        self.library = {}

        # library display
        self.frame_display = tk.Frame(self)
        self.frame_display.grid(row=0, column=0)

        self.library_scrollbar = tk.Scrollbar(self.frame_display)
        self.library_scrollbar.pack(side='right')

        self.library_display_background_colors = ["#69FFFC", "#FF0000", "#84FF47", "#D3A1FF", "#FFFC2A"]
        self.library_display = tk.Listbox(self.frame_display, width=32, height=4, yscrollcommand=self.library_scrollbar.set)
        self.library_display.pack()

        # library buttons
        self.library_buttons_frame = tk.Frame(self)
        self.library_buttons_frame.grid(row=0, column=1)

        self.add_song_button = tk.Button(self.library_buttons_frame, text='Add songs', width=10, command=self.song_add)
        self.add_song_button.grid(row=0, column=0)

        self.delete_song_button = tk.Button(self.library_buttons_frame, text= "Delete song", width=10, command=self.delete_song)
        self.delete_song_button.grid(row=1,column=0)

        # music buttons
        self.music_buttons_frame = tk.Frame(self)
        self.music_buttons_frame.grid(row=1,columnspan=1)

        self.play_button = tk.Button(self.music_buttons_frame, text='Play', command=self.play_song)
        self.play_button.grid(row=0,column=2)

        self.next_song_button = tk.Button(self.music_buttons_frame, text='|>', width=2, command= self.next_song)
        self.next_song_button.grid(row=0, column=3)

        self.previously_song_button = tk.Button(self.music_buttons_frame, text='<|', width=2, command= self.previously_song)
        self.previously_song_button.grid(row=0,column=1)

        self.music_volume = 1.0
        self.min_volume_button = tk.Button(self.music_buttons_frame, text='Vol -', command=self.min_volume)
        self.min_volume_button.grid(row=0,column=4)
        self.add_volume_button = tk.Button(self.music_buttons_frame, text='Vol +', command=self.add_volume)
        self.add_volume_button.grid(row=0,column=5)

        self.color_change_button = tk.Button(self.music_buttons_frame, text="C", command=self.color_change)
        self.color_change_button.grid(row=0, column=0)

        self.col = 0
    def color_change(self):
        if self.col < len(self.library_display_background_colors):
            self.library_display.configure(background=self.library_display_background_colors[self.col])
            self.col += 1
        else:
            self.col = 0
            self.library_display.configure(background="#FFFFFF")

    def min_volume(self):
        self.music_volume -= 0.1
        mixer.music.set_volume(self.music_volume)

    def add_volume(self):
        self.music_volume += 0.1
        mixer.music.set_volume(self.music_volume)

    # add title and directory to library
    def song_add(self):
        # extract title from directory
        def title_finder(directory):
            return directory.split('/')[-1]
        song = filedialog.askopenfilename(filetypes=[('MP3 files', '*mp3')])
        self.library[title_finder(song)] = song
        self.library_display.insert('end', title_finder(song))

    def delete_song(self):
        if self.library_display.size() == 0:
            pass
        else:
            song = self.library_display.curselection()
            self.library.pop(self.library_display.get(song))
            self.library_display.delete(song)

    def play_song(self):
        if mixer.music.get_busy():
            mixer.music.pause()
            self.play_button.config(text="Play")
        else:
            song = self.library_display.curselection()
            mixer.music.load(self.library[self.library_display.get(song)])
            mixer.music.play()
            self.play_button.config(text="Stop")

    def next_song(self):
        try:
            if mixer.music.get_busy():
                song = self.library_display.curselection()[0] + 1
                self.library_display.selection_set(song)
                self.library_display.select_clear(song - 1)
                mixer.music.load(self.library[self.library_display.get(song)])
                mixer.music.play()
            else:
                pass
        except:
            if mixer.music.get_busy():
                self.library_display.selection_set(0)
                mixer.music.load(self.library[self.library_display.get(0)])
                mixer.music.play()


    def previously_song(self):
        if self.library_display.curselection() == (0,):
            pass
        elif mixer.music.get_busy():
            song = self.library_display.curselection()[0] - 1
            self.library_display.selection_set(song)
            self.library_display.select_clear(song + 1)
            mixer.music.load(self.library[self.library_display.get(song)])
            mixer.music.play()
        else:
            pass

if __name__ == '__main__':
    app = App()
    app.mainloop()