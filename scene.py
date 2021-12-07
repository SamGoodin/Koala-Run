import pygame
from sprite import *
from background import Background
import string, random
import time


class Scene:
    
    def __init__(self, size=(640, 480), position=(100, 100), frame_rate=30):
        # Initialize the scene
        pygame.init()

        # Start music
        pygame.mixer.music.load("resources/music/song1.wav")
        pygame.mixer.music.play(-1)

        self.sfx = pygame.mixer.Channel(2)
        self.coin_sfx = pygame.mixer.Channel(3)
        self.hit = pygame.mixer.Sound("resources/music/hit.wav")
        self.gain = pygame.mixer.Sound("resources/music/coin.wav")

        self.size = size
        self.position = position
        self.frame_rate = frame_rate
        self.__game_clock = pygame.time.Clock()
        self.window_icon = None
        self.window_title = None
        self.screen = pygame.display.set_mode(self.size)
        self.background = None
        
        self.sprites = pygame.sprite.Group() # all enemies
        self.coins = pygame.sprite.Group() # all coins
        self.playable_sprites = pygame.sprite.Group() # just player
        self.player = None
        
        self.font_size = 16
        self.font_name = 'arial'
        self.font = pygame.font.Font(pygame.font.match_font(self.font_name), self.font_size)
        self.score_pos = (500, 50)
        
        self.__running = False   

        self.enemy_num = 3
        self.enemy_time_int = 2

        self.__totaltime = time.time()
        self.__enemytime = self.__totaltime
        # Used to track timing of enemy spawns
        self.__timestart = self.__totaltime  
        # Used to track coin spawns
        self.__cointime = self.__totaltime
        
    def set_font_size(self, size : int):
        self.font_size = size
        self.font = pygame.font.Font(pygame.font.match_font(self.font_name), self.font_size)
        
    def set_font_name(self, name : string):
        self.font_name = name
        self.font = pygame.font.Font(pygame.font.match_font(self.font_name), self.font_size)
        
    def set_font(self, font: pygame.font.Font):
        self.font = font
        
    def set_background(self, background : Background): 
        self.background = background     
        
    def get_player(self):
        return self.player
        
    def __cleanup(self):
        pygame.quit()
        
    def __event(self, event):
        # event handling will happen here
        if event.type == pygame.QUIT:
            # Window exit
            self.__running = False
        if event.type == pygame.KEYDOWN:
            # Single action
            print(pygame.key.name(event.key))
            if event.key == pygame.K_m:
                # Toggle bg scrolling
                if self.background:
                    if self.background.scrolling:
                        self.background.scrolling = False
                    else:
                        self.background.scrolling = True
            if event.key == pygame.K_p:
                # Player becomes next available sprite
                print(len(self.playable_sprites))
                if self.player:
                    self.swap_player()
            if event.key == pygame.K_q:
                # Position each sprite at bottom of screen
                self.drop_all_sprites()
            if event.key == pygame.K_b:
                # Toggle red border around player
                self.toggle_player_highlight()
                
    
    def __render(self):
        # Draw everything to the screen
        
        # Draw background
        if self.background:
            if self.background.scrolling and self.background.scroll == 'x':
                self.background.scroll_updateX()
                bg_img, bg_pos1, bg_pos2 = self.background.scroll_render()
                self.screen.blit(bg_img, bg_pos1)
                self.screen.blit(bg_img, bg_pos2)
            elif self.background.scrolling and self.background.scroll == 'y':
                self.background.scroll_updateY()
                bg_img, bg_pos1, bg_pos2 = self.background.scroll_render()
                self.screen.blit(bg_img, bg_pos1)
                self.screen.blit(bg_img, bg_pos2)
            else:
                bg_img, bg_pos1, bg_pos2 = self.background.render()
                if bg_pos1 == None or bg_pos2 == None:
                    self.screen.blit(self.background.render(), (0, 0))
                else:
                    self.screen.blit(bg_img, bg_pos1)
                    self.screen.blit(bg_img, bg_pos2)
                    
        # Draw scorebox
        pygame.draw.rect(self.screen, (0, 0, 0), [self.screen.get_width() - 200, 0, self.screen.get_width(), 100], 0)

        # Draw score
        score = self.font.render("Distance: " + str(round(self.player.score, 1)) + "m", True, (255, 255, 255))
        score_rect = score.get_rect()
        score_rect.midtop = (self.screen.get_width() - 125, 10)
        self.screen.blit(score, score_rect)

        # Draw lives
        lives = self.font.render("Lives: " + str(self.player.lives), True, (255, 255, 255))
        lives_rect = lives.get_rect()
        lives_rect.midtop = (self.screen.get_width() - 125, 30)
        self.screen.blit(lives, lives_rect)

        # Draw enemy spawn interval
        enemy_spawn_int = self.font.render("Enemy spawn: " + str(round(self.enemy_time_int, 1)) + "s", True, (255, 255, 255))
        spawn_rect = enemy_spawn_int.get_rect()
        spawn_rect.midtop = (self.screen.get_width() - 100, 50)
        self.screen.blit(enemy_spawn_int, spawn_rect)

        # Draw time elapsed
        elapsed = self.font.render("Time running: " + str(round(time.time() - self.__totaltime, 1)) + "s", True, (255, 255, 255))
        time_rect = elapsed.get_rect()
        time_rect.midtop = (self.screen.get_width() - 100, 75)
        self.screen.blit(elapsed, time_rect)

        self.playable_sprites.draw(self.screen)
        self.coins.draw(self.screen)
        self.sprites.draw(self.screen)
        
        pygame.display.flip()

    def create_owl(self):
        enemy = Owl(self.size[0], self.position[1])
        self.add_npc_sprite(enemy)
        print("Owl enemy spawned")
        self.__timestart = time.time()
    
    def create_snake(self):
        enemy = Snake(self.size[0])
        self.add_npc_sprite(enemy)
        print("Snake enemy spawned")
        self.__timestart = time.time()

    def create_coin(self):
        coin = Coin(self.size[0])
        self.coins.add(coin)
        print("Coin spawned")
        self.__cointime = time.time()
        
    def __update(self):
        # All updates every frame
        self.player.add_score(.1)

        self.coins.update(self.size)
        self.playable_sprites.update(self.size)
        self.sprites.update(self.size)

        # Enemy spawns every two seconds
        if ((time.time() - self.__timestart >= self.enemy_time_int)):

            # Val represents our randomness for enemy spawns
            # Stored once so enemies multiple enemies don't spawn simultaneously
            # Range is numbers 1-25
            val = random.randrange(1, 26)

            # Logic for creating owls
            if ((val % 2 == 0) and len(self.sprites) < self.enemy_num):
                self.create_owl()

            # Logic for creating snakes
            if ((val % 2 == 1) and len(self.sprites) < self.enemy_num):
                self.create_snake()

        if ((time.time() - self.__cointime >= 5)):
            # Logic for creating coins
            val = random.randrange(1, 11)
            if (val % 5 == 0):
                self.create_coin()
        
        # Logic for removing enemies offscreen
        for enemy in self.sprites:
            if enemy.offscreen:
                enemy.kill()
                print("Enemy offscreen removed.\nSprites: {}".format(len(self.sprites)))

        npc_collision = pygame.sprite.groupcollide(self.playable_sprites, self.sprites, False, False)
        for player, enemies in npc_collision.items():
            for enemy in enemies:
                self.sfx.play(self.hit)
                enemy.kill()
                player.add_lives(-1)
                print("Enemy collided removed.\nSprites: {}".format(len(self.sprites)))
        
        coin_collision = pygame.sprite.groupcollide(self.playable_sprites, self.coins, False, False)
        for player, coins in coin_collision.items():
            for coin in coins:
                self.coin_sfx.play(self.gain)
                coin.kill()
                player.add_score(50)
                print("Coin collided removed.")

        if (self.player.lives <= 0):
            self.stop_game()

        if ((time.time() - self.__enemytime) >= 10):
            # Increase enemy spawn time
            self.enemy_time_int -= .2
            print("Enemy spawn time: {}".format(self.enemy_time_int))
            self.__enemytime = time.time()
            

        self.__render()
        
    def check_collision(self, sprite1, sprite2):
        collides = pygame.sprite.collide_rect(sprite1, sprite2)
        return collides
    
    def drop_all_sprites(self):
        for sprite in self.sprites:
            spr_height = sprite.get_height()
            sprite.change_position((sprite.get_x(), self.size[1] - spr_height))
    
    def add_npc_sprite(self, sprite):
        self.sprites.add(sprite)
        
    def add_playable_sprite(self, sprite):
        self.playable_sprites.add(sprite)
        self.add_player_sprite(sprite)
        
    def add_player_sprite(self, sprite):
        self.set_player(sprite)
        
    def set_player(self, sprite):
        if self.player:
            self.player.is_player = False
        self.player = sprite
        self.player.is_player = True
            
    def start_game(self):
        # Main game loop
        self.__running = True
        while self.__running:
            self.__game_clock.tick(self.frame_rate)
            for event in pygame.event.get():
                self.__event(event)
            
            
            # Updates to happen
            self.__update()
        
        # After the game loop breaks, we clean things up on
        # pygame's end
        self.__cleanup()
            
    def stop_game(self):
        pygame.mixer.music.stop()

        sfx = pygame.mixer.Channel(1)
        death = pygame.mixer.Sound("resources/music/death.wav")
        sfx.play(death)
        while sfx.get_busy():
            # Waiting until sfx are done
            pass
        self.__running = False
        
    def set_window_title(self, title):
        self.window_title = title
        pygame.display.set_caption(self.window_title)