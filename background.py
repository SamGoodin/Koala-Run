import pygame
import string

class Background:
    
    def __init__(self, image : string, size : tuple, scrolling : bool):
        self.bg_x1, self.bg_y1, self.bg_x2, self.bg_y2 = None, None, None, None
        if image == None:
            self.image = pygame.image.load('resources/backgrounds/default.png').convert()
        else:
            self.image = pygame.image.load(image).convert()
        if size:
            self.image = pygame.transform.scale(self.image, size)
        if scrolling:
            # Setup for x scrolling
            # Commented code for y scrolling
            self.scrolling = True
            self.scroll = 'x'
            #self.scroll = 'y'
            self.bg_rect = self.image.get_rect()
            self.bg_x1 = 0
            self.bg_y1 = 0
            self.bg_x2 = self.bg_rect.width
            self.bg_y2 = 0
            #self.bg_x2 = 0
            #self.bg_y2 = self.bg_rect.height
            self.moving_speed = 5
        else:
            self.scrolling = False
            self.scroll = None
            
    def render(self):
        if self.bg_x1 != None and self.bg_x2 != None and self.bg_y1 != None and self.bg_y2 != None:
            return self.image, (self.bg_x1, self.bg_y1), (self.bg_x2, self.bg_y2)
        else:    
            return self.image
    
    def scroll_updateX(self):
        self.bg_x1 -= self.moving_speed
        self.bg_x2 -= self.moving_speed
        if self.bg_x1 <= -self.bg_rect.width:
            self.bg_x1 = self.bg_rect.width
        if self.bg_x2 <= -self.bg_rect.width:
            self.bg_x2 = self.bg_rect.width
        
    def scroll_updateY(self):
        self.bg_y1 -= self.moving_speed
        self.bg_y2 -= self.moving_speed
        if self.bg_y1 <= -self.bg_rect.height:
            self.bg_y1 = self.bg_rect.height
        if self.bg_y2 <= -self.bg_rect.height:
            self.bg_y2 = self.bg_rect.height
            
    def scroll_render(self):
        return self.image, (self.bg_x1, self.bg_y1), (self.bg_x2, self.bg_y2)
            
        