import pygame
from scene import Scene
from sprite import Sprite, Powerup
from background import Background


if __name__ == '__main__':
    scene = Scene()
    scene.set_window_title("Demo")
    
    bg = Background(None, scene.size, True)
    scene.set_background(bg)
    scene.set_font_size(20)
    
    # params: imagePath String, position (x, y), speed (dx, dy)
    defaultSprite = Sprite(None, (20, 20), (5, 5))
    scene.add_player_sprite(defaultSprite)
    
    npc = Sprite(None, (200, 150), (1, 1))
    scene.add_npc_sprite(npc)
    
    another_npc = Sprite(None, (150, 10), (2, 2))
    scene.add_npc_sprite(another_npc)
    
    playable_sprite = Sprite(None, (300, 10), (6, 6))
    scene.add_playable_sprite(playable_sprite)
    
    # Start all sprites on the "floor" aka bottom of screen
    scene.drop_all_sprites()
    
    # params: imagePath, position
    for x in range(3):
        pow = Powerup('goldCoin1.png', (x * 100, 50), (0, 0))
        pow.set_colorkey((255,255,255))
        scene.add_powerup(pow)
    
    
    # Starts the game
    scene.start_game()
