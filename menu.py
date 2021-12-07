from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter
import pygame
from scene import Scene
from sprite import Player
from background import Background
from menu import *
import json



class Store(Tk):

    def __init__(self, player_score, lives, sound=True):
        super().__init__()
        if sound:
            pygame.mixer.init()
            pygame.mixer.music.load("resources/music/menu.wav")
            pygame.mixer.music.play(-1)
        self.winfo_toplevel().title("Koala Run - Menu")
        self.geometry("300x300")
        screen_width = self.winfo_reqwidth()
        screen_height = self.winfo_reqheight()
        self.x = int(self.winfo_screenwidth()/2 - screen_width/2)
        self.y = int(self.winfo_screenheight()/2 - screen_height/2)
        self.geometry("+{}+{}".format(self.x, self.y))

        self.__player_score = player_score
        self.__lives = lives

        player_data = "Points: {} | Lives: {}".format(player_score, lives)
        self.player_data = tkinter.Label(text=player_data, bg="black", fg="white")
        self.player_data.pack()

        if (self.__player_score < 100):
            life_state = tkinter.DISABLED
            life_txt = "Need more points"
        else:
            life_state = tkinter.NORMAL
            life_txt = "Buy 1 Life"

        self.life_label = tkinter.Label(text="Buy an additional life for 100 points")
        self.add_lives = tkinter.Button(self, text=life_txt, command=self.__buy_life, state=life_state)

        self.life_label.pack()
        self.add_lives.pack()

        self.bg_label = tkinter.Label(text="Select a custom background to play on")
        self.bg_pick = tkinter.Button(self, text="Select a background", command=self.pick_background)
        self.background_file = "resources/backgrounds/default.png"

        self.bg_label.pack()
        self.bg_pick.pack()

        playx = self.winfo_screenheight()
        self.play_button = tkinter.Button(self, text="Start Game", command=self.__start_game)
        #self.play_button.place(x=self.winfo_reqwidth()/2 + 10, y=self.winfo_reqheight() - 50)
        self.play_button.pack()

        self.running = True
        self.focus_force()
        self.attributes('-topmost', True)
        self.update()

    def pick_background(self):
        self.background_file = askopenfilename(initialdir="resources/backgrounds", filetypes=[("png Files", "*.png")])

    def write_data(self, data):
        with open('data.txt', 'w') as output:
            json.dump(data, output)

    def __on_close(self):
        pass

    def run(self):
        self.mainloop()

    def hard_update(self, sound=False):
        self.destroy()
        self.__init__(self.__player_score, self.__lives, sound)

    def __buy_life(self):
        self.__player_score -= 100
        self.__lives += 1
        self.hard_update()

    def __start_game(self):
        # Hide menu
        self.withdraw()

        pygame.mixer.music.stop()

        scene = Scene()
        scene.set_window_title("Koala Run - Game")
        
        bg = Background(self.background_file, scene.size, True)
        scene.set_background(bg) 
        scene.set_font_size(20)
        
        # params: position (x, y), lives
        defaultSprite = Player((20, scene.size[1] - 150), self.__lives)
        scene.add_playable_sprite(defaultSprite)
        
        # Starts the game
        scene.start_game()

        print("Score: {}\nLives: {}".format(defaultSprite.score, defaultSprite.lives))

        self.__player_score += round(defaultSprite.score)
        if (self.__player_score < 100):
            self.__lives = 1

        self.hard_update(True)
