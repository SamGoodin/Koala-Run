import pygame
import string


class Sprite(pygame.sprite.Sprite):
    
    def __init__(self, imagePath : string, position : tuple, speed : tuple):
        super().__init__()
        if imagePath == None:
            self.image = pygame.image.load("koala_idle.png").convert()
            self.image.set_colorkey((0, 0, 0))
        else:
            self.image = pygame.image.load(imagePath).convert()
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.center = (self.image.get_width() / 2, self.image.get_height() / 2)
        
        # Sets the position of the image by assigning the top left
        # corner to a spot
        self.position = None
        if position == None:
            self.change_position((0,0))
        else:
            self.change_position(position)
            
        self.dx, self.dy = speed[0], speed[1]
        
        self.JUMPING = False
        self.jump_var = 7
        self.is_player = False
        self.is_flipped = False
        
        self.score = 0
        
    def set_colorkey(self, color : tuple):
        # For removing potential background color
        # Color specified will be removed from image
        self.image.set_colorkey(color)
            
    def move(self, scene_bounds : tuple):
        # Not complete moving method
        temp_pos = (self.x + self.dx, self.y + self.dy)
        
        if (temp_pos[0] > scene_bounds[0] or temp_pos[0] < 0):
            self.dx *= -1
        if (temp_pos[1] > scene_bounds[1] or temp_pos[1] < 0):
            self.dy *= -1
        
        self.change_position((self.x + self.dx, self.y + self.dy))
        
    def move_left(self, x_bounds : int):
        if not self.is_flipped:
            self.flip_sprite(True, False)
        self.move_x(self.dx * -1, x_bounds)
        
    def move_right(self, x_bounds : int):
        if self.is_flipped:
            self.flip_sprite(True, False)
        self.move_x(self.dx, x_bounds)
        
    def move_up(self, y_bounds : int):
        self.move_y(self.dy * -1, y_bounds)
        
    def move_down(self, y_bounds : int):
        self.move_y(self.dy, y_bounds)
        
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

    def update(self, bounds : tuple):
        if self.is_player:
            keys = pygame.key.get_pressed()
            if not self.JUMPING:
                if keys[pygame.K_LEFT]:
                    self.move_left(bounds[0])
                if keys[pygame.K_RIGHT]:
                    self.move_right(bounds[0])
                if keys[pygame.K_UP]:
                    self.move_up(bounds[1])
                if keys[pygame.K_DOWN]:
                    self.move_down(bounds[1])
                if keys[pygame.K_SPACE]:
                    self.JUMPING = True
            else:
                # Jumping
                if self.jump_var >= -7:
                    neg = 1
                    if self.jump_var < 0:
                        neg = -1
                    new_y = self.position[1] - (self.jump_var**2 * neg)
                    self.jump_var -= 1
                    self.change_position((self.position[0], new_y))
                else:
                    self.jump_var = 7
                    self.JUMPING = False
    
    def get_x(self):
        return self.position[0]
    
    def get_y(self):
        return self.position[1]
    
    def get_height(self):
        return self.image.get_height()
    
    def get_width(self):
        return self.image.get_width()
        
    def change_size(self, size : tuple):
        self.image = pygame.transform.scale(self.image, (size[0], size[1]))
        self.size = self.image.get_size()
        
    def change_position(self, position : tuple):
        self.rect.topleft = [position[0], position[1]]
        self.position = (self.rect.topleft[0], self.rect.topleft[1])
        self.x, self.y = self.position[0], self.position[1]
        
    def change_speed(self, speed : tuple):
        self.dx, self.dy = speed[0], speed[1]
        
    def rotate_sprite(self):
        rot_img = pygame.transform.rotate(self.image, self.angle)
        rot_rect = rot_img.get_rect(center=self.image.get_rect(center=self.rect.center))
        return rot_img, rot_rect
    
    def flip_sprite(self, horiz : bool, vert : bool):
        self.image = pygame.transform.flip(self.image, horiz, vert)
        if self.is_flipped:
            self.is_flipped = False
        else:
            self.is_flipped = True
        
    def exists(self):
        return self.alive()
    
    def remove(self, allGroups=False):
        if allGroups:
            self.kill()
        else:
            self.remove()
        
    def get_groups(self):
        return self.groups()
    
    
    
class Powerup(Sprite):
    
    def __init__(self, imagePath : string, position : tuple, speed : tuple):
        super().__init__(imagePath, position, speed)
        
    def update(self, screen_bounds : tuple):
        pass
    
    

if __name__ == '__main__':
    pass