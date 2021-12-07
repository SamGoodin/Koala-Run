import pygame
import random
import string
import time

class Player(pygame.sprite.Sprite):

    def __init__(self, position : tuple, lives, shields):
        super().__init__()
        self.walking = [
                "resources/player/koala_walk01.png",
                "resources/player/koala_walk02.png",
                "resources/player/koala_walk03.png"
            ]
        self.walking_idx = 0
        # Delay on walk
        self.walking_counter = 0
        self.image = pygame.image.load(self.walking[self.walking_idx]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (42, 72))
        #self.image.set_colorkey((0, 0, 0))

        self.name = "player"

        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.center = (self.image.get_width() / 2, self.image.get_height() / 2)

        self.change_position(position)

        self.dx, self.dy = 7, 12

        self.JUMPING = False

        self.score = 0
        self.lives = lives

        # Used for managing shield
        self.shields = shields
        self.invincible = False
        self.shieldtimer = -1

    def add_lives(self, amount):
        self.lives += amount

    def add_score(self, amount):
        self.score += amount

    def move_left(self, x_bounds : int):
        self.move_x(self.dx * -1, x_bounds)
        
    def move_right(self, x_bounds : int):
        self.move_x(self.dx, x_bounds)

    def move_x(self, distance : int, x_bounds = int):
        if distance == None:
            temp_pos = (self.x + self.dx, self.y)
        else:
            temp_pos = (self.x + distance, self.y)
            
        if (temp_pos[0] > x_bounds - self.image.get_width() or temp_pos[0] < 0):
            print("X BOUND")
            temp_pos = (self.x, self.y)
            
        self.change_position(temp_pos)
        
    def move_y(self, distance : int, y_bounds : int):
        if distance == None:
            temp_pos = (self.x, self.y + self.dy)
        else:
            temp_pos = (self.x, self.y + distance)
            
        if (temp_pos[1] > y_bounds - self.image.get_height() or temp_pos[1] < 0):
            print("Y BOUND")
            temp_pos = (self.x, self.y)
        self.change_position(temp_pos)

    def change_position(self, position : tuple):
        self.rect.topleft = [position[0], position[1]]
        self.position = (self.rect.topleft[0], self.rect.topleft[1])
        self.x, self.y = self.position[0], self.position[1]
    
    def get_x(self):
        return self.position[0]
    
    def get_y(self):
        return self.position[1]
    
    def get_height(self):
        return self.image.get_height()
    
    def get_width(self):
        return self.image.get_width()

    def update(self, bounds : tuple):
        if self.shieldtimer != -1:
            # Shield is active
            if (time.time() - self.shieldtimer >= 5):
                # Turn off shield
                self.invincible = False
                self.shieldtimer = -1

        if self.is_player:
            keys = pygame.key.get_pressed()
            # Shield
            if keys[pygame.K_f]:
                # Attempting to use shield
                if ((self.shields > 0) and (not self.invincible)):
                    self.invincible = True
                    self.shields -= 1
                    self.shieldtimer = time.time()

            if not self.JUMPING:
                if self.walking_counter == 5:
                    self.walking_idx += 1
                    if self.walking_idx > len(self.walking) - 1:
                        self.walking_idx = 0
                    self.image = pygame.image.load(self.walking[self.walking_idx]).convert_alpha()
                    self.image = pygame.transform.scale(self.image, (42, 72))
                    
                    #self.image.set_colorkey((0, 0, 0))
                    self.walking_counter = 0
                else:
                    self.walking_counter += 1
                if keys[pygame.K_LEFT]:
                    self.move_left(bounds[0])
                if keys[pygame.K_RIGHT]:
                    self.move_right(bounds[0])
                if keys[pygame.K_SPACE]:
                    self.JUMPING = True
            else:
                # Jumping
                self.image = pygame.image.load("resources/player/koala_jump.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (42, 72))
                if keys[pygame.K_LEFT]:
                    self.move_left(bounds[0])
                if keys[pygame.K_RIGHT]:
                    self.move_right(bounds[0])
                y = self.dy * 4
                self.dy -= 1
                self.change_position((self.position[0], self.position[1] - y))
                if self.dy < -12:
                    self.JUMPING = False
                    self.dy = 12


class Coin(pygame.sprite.Sprite):

    def __init__(self, x_pos):
        super().__init__()
        self.image = pygame.image.load("resources/other/goldCoin1.png").convert_alpha()
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.center = (self.image.get_width() / 2, self.image.get_height() / 2)

        self.name = "coin"

        self.min_y = 100
        self.max_y = 275

        self.x_pos = x_pos
        self.y_pos = random.randrange(self.min_y, self.max_y)

        self.position = (self.x_pos, self.y_pos)
        self.rect.topleft = self.position

        self.x_move = -1

        # Used for removal of sprites as they pass player
        self.offscreen = False

    def __offscreen(self):
        self.offscreen = True

    def move(self):
        self.rect.topleft = [self.position[0] + self.x_move, self.position[1]]
        self.position = (self.rect.topleft[0], self.rect.topleft[1])
        self.x_pos, self.y_pos = self.position[0], self.position[1]
        if (self.rect.topright[0] < 0):
            self.__offscreen()

    def update(self, *args):
        self.move()

    def get_x(self):
        return self.x_pos
    
    def get_y(self):
        return self.y_pos
    
    def get_height(self):
        return self.image.get_height()
    
    def get_width(self):
        return self.image.get_width()


class Owl(pygame.sprite.Sprite):

    def __init__(self, x_pos, slows):
        super().__init__()
        self.image = pygame.image.load("resources/enemies/owl.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.image.set_colorkey((255,255,255))
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.center = (self.image.get_width() / 2, self.image.get_height() / 2)
        
        self.name = "owl"

        self.min_y = 100
        self.max_y = 275

        self.x_pos = x_pos
        self.y_pos = random.randrange(self.min_y, self.max_y)

        self.position = (self.x_pos, self.y_pos)
        print(self.position)

        self.rect.topleft = self.position

        self.x_move = 8 - slows
        self.y_move = -3

        # Used for removal of sprites as they pass player
        self.offscreen = False

    def __offscreen(self):
        self.offscreen = True

    def move(self):
        if (self.position[1] + self.y_move > self.max_y or self.position[1] + self.y_move < self.min_y):
            self.y_move *= -1
        self.rect.topleft = [self.position[0] - self.x_move, self.position[1] + self.y_move]
        self.position = (self.rect.topleft[0], self.rect.topleft[1])
        self.x_pos, self.y_pos = self.position[0], self.position[1]
        if (self.rect.topright[0] < 0):
            self.__offscreen()

    def update(self, *args):
        self.move()

    def get_x(self):
        return self.x_pos
    
    def get_y(self):
        return self.y_pos
    
    def get_height(self):
        return self.image.get_height()
    
    def get_width(self):
        return self.image.get_width()
    

class Snake(pygame.sprite.Sprite):

    def __init__(self, x_pos, slows):
        super().__init__()
        self.image = pygame.image.load("resources/enemies/snake.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (125, 125))
        #self.image.set_colorkey((255,255,255))
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.center = (self.image.get_width() / 2, self.image.get_height() / 2)

        self.name = "snake"

        self.x_pos = x_pos
        self.y_pos = 325

        self.x_move = 8 - slows

        self.position = (self.x_pos, self.y_pos)

        self.rect.topleft = self.position

        # Used for removal of enemies as they pass player
        self.offscreen = False

    def __offscreen(self):
        self.offscreen = True

    def move(self):
        self.rect.topleft = [self.position[0] - self.x_move, self.position[1]]
        self.position = (self.rect.topleft[0], self.rect.topleft[1])
        self.x_pos, self.y_pos = self.position[0], self.position[1]
        if (self.rect.topright[0] < 0):
            self.__offscreen()

    def update(self, *args):
        self.move()

    def get_x(self):
        return self.x_pos
    
    def get_y(self):
        return self.y_pos
    
    def get_height(self):
        return self.image.get_height()
    
    def get_width(self):
        return self.image.get_width()

    
    