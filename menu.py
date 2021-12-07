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

    def __init__(self, player_score, lives, shields, slows=0, sound=True):
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
        self.__shields = shields
        self.__slows = slows

        player_data = "Points: {} | Lives: {} | Shields: {}".format(self.__player_score, self.__lives, self.__shields)
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

        if (self.__player_score < 500):
            shield_state = tkinter.DISABLED
            shield_txt = "Need more points"
        else:
            shield_state = tkinter.NORMAL
            shield_txt = "Buy 1 5s shield"

        self.shield_lbl = tkinter.Label(text="Buy a 5 second shield for 500 points")
        self.add_shield = tkinter.Button(self, text=shield_txt, command=self.__buy_shield, state=shield_state)

        self.shield_lbl.pack()
        self.add_shield.pack()

        if (self.__player_score < 500):
            slow_state = tkinter.DISABLED
            slow_txt = "Need more points"
        else:
            slow_state = tkinter.NORMAL
            slow_txt = "Slow down enemies"

        self.slow_lbl = tkinter.Label(text="Slow enemy speed by 1 for 500 points")
        self.slow_btn = tkinter.Button(self, text=slow_txt, command=self.__buy_slow, state=slow_state)

        self.slow_lbl.pack()
        self.slow_btn.pack()

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

    def run(self):
        self.mainloop()

    def hard_update(self, sound=False):
        # This updates the menu and all its elements the hard way
        self.destroy()
        self.__init__(self.__player_score, self.__lives, self.__shields, self.__slows, sound)

    def __buy_life(self):
        self.__player_score -= 100
        self.__lives += 1
        self.hard_update()

    def __buy_shield(self):
        self.__player_score -= 500
        self.__shields += 1
        self.hard_update()
    
    def __buy_slow(self):
        self.__player_score -= 500
        self.__slows += 1
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
        defaultSprite = Player((20, scene.size[1] - 150), self.__lives, self.__shields)
        scene.add_playable_sprite(defaultSprite)
        
        # Starts the game
        scene.start_game(self.__slows)

        print("Score: {}\nLives: {}\nShields: {}".format(defaultSprite.score, defaultSprite.lives, defaultSprite.shields))

        self.__player_score += round(defaultSprite.score)
        self.__shields = defaultSprite.shields
        if (self.__player_score < 100):
            self.__lives = 1

        self.hard_update(True)
