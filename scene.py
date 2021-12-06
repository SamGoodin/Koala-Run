import pygame
from sprite import Sprite, Powerup
from background import Background
import string, random


class Scene:
    
    def __init__(self, size=(640, 480), position=(100, 100), frame_rate=30):
        # Initialize the scene
        pygame.init()
        self.size = size
        self.position = position
        self.frame_rate = frame_rate
        self.__game_clock = pygame.time.Clock()
        self.window_icon = None
        self.window_title = None
        self.screen = pygame.display.set_mode(self.size)
        self.background = None
        
        self.sprites = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()
        self.playable_sprites = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.player = None
        self.player_highlight = True
        
        self.font_size = 16
        self.font_name = 'arial'
        self.font = pygame.font.Font(pygame.font.match_font(self.font_name), self.font_size)
        self.score_pos = (500, 50)
        
        self.__running = False      
        
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
                    
        # Draw score
        score = self.font.render("Score: " + str(self.player.score), True, (0, 0, 0))
        score_rect = score.get_rect()
        score_rect.midtop = (500, 50)
        self.screen.blit(score, score_rect)
        
        self.sprites.draw(self.screen)
        
        if self.player_highlight:
            # Red border around player
            pygame.draw.rect(self.screen, (255, 0, 0), [self.player.get_x(), self.player.get_y(), self.player.get_width(), self.player.get_height()], 1)
        
        for npc in self.npc_sprites:
            # Blue border around npc's
            pygame.draw.rect(self.screen, (0, 0, 255), [npc.get_x(), npc.get_y(), npc.get_width(), npc.get_height()], 1)
        
        pygame.display.flip()
        
    def __update(self):
        # All updates every frame
            
        self.sprites.update(self.size)
        
        # Collisions with player and other playable sprites
        playable_collisions = pygame.sprite.spritecollide(self.player, self.playable_sprites, False)
        if playable_collisions:
            # handle playable collision here
            print("Playable Character Collision: " + str(playable_collisions))
        
        # Collisions with player and npc's
        npc_collisions = pygame.sprite.spritecollide(self.player, self.npc_sprites, False)
        if npc_collisions:
            # handle npc collision here
            print("NPC Collision: " + str(npc_collisions))
       
        # Collisions with player and powerups
        pow_collisions = pygame.sprite.spritecollide(self.player, self.powerups, False)
        if pow_collisions:
            # handle powerup collision here
            print("Powerup collision: " + str(pow_collisions))
            pow_collisions[0].remove(True)
            self.player.score += 1
            
            # everytime a coin is hit, a new one spawns
            randx, randy = random.randrange(0, self.size[0]), random.randrange(0, self.size[1])
            pow = Powerup('goldCoin1.png', (randx, randy), (0, 0))
            pow.set_colorkey((255,255,255))
            self.add_powerup(pow)
        
        self.__render()
        
    def check_collision(self, sprite1 : Sprite, sprite2 : Sprite):
        collides = pygame.sprite.collide_rect(sprite1, sprite2)
        return collides
    
    def drop_all_sprites(self):
        for sprite in self.sprites:
            spr_height = sprite.get_height()
            sprite.change_position((sprite.get_x(), self.size[1] - spr_height))
    
    def add_npc_sprite(self, sprite : Sprite):
        self.sprites.add(sprite)
        self.npc_sprites.add(sprite)
        
    def add_playable_sprite(self, sprite : Sprite):
        self.sprites.add(sprite)
        self.playable_sprites.add(sprite)
        
    def add_player_sprite(self, sprite : Sprite):
        self.sprites.add(sprite)
        self.set_player(sprite)
        
    def add_powerup(self, powerup : Powerup):
        self.sprites.add(powerup)
        self.powerups.add(powerup)
        
    def set_player(self, sprite: Sprite):
        if self.player:
            self.player.is_player = False
        self.player = sprite
        self.player.is_player = True
        
    def swap_player(self):
        spriteList = self.playable_sprites.sprites()
        if len(spriteList) > 1:
            idx = spriteList.index(self.player)
            old_player = spriteList[idx]
            if idx + 1 == len(spriteList):
                idx = 0
            else:
                idx += 1
            new_player = spriteList[idx]
            
            self.playable_sprites.add(old_player)
            self.playable_sprites.remove(new_player)
            
            self.set_player(new_player)
        else:
            old_player = self.player
            new_player = spriteList[0]
            self.playable_sprites.add(old_player)
            self.playable_sprites.remove(new_player)
            self.set_player(new_player)
            
    def toggle_player_highlight(self):
        if self.player_highlight:
            self.player_highlight = False
        else:
            self.player_highlight = True
            
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
        self.__running = False
        
    def set_window_title(self, title):
        self.window_title = title
        pygame.display.set_caption(self.window_title)
        
    def hide_scene(self):
        # Minimizes the window
        pygame.display.iconify()
        
if __name__ == '__main__':
    game = scene()
    game.set_window_title("Game")
    game.start_game()
    