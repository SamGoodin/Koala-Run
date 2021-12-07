import pygame
from scene import Scene
from sprite import Player
from background import Background
from menu import *
#import resources
import json


if __name__ == '__main__':
    #game_resources = resources.Resources()

    """ JSON Game Data
    player_name = input("Enter the name of your player: ")
    
    # Get score data
    score_data, lives_data = None, None
    create = False
    with open('data.txt') as json_file:
        data = json.load(json_file)
        if data:
            try:
                score_data = data['players'][player_name]['score']
                lives_data = data['players'][player_name]['lives']
            except:
                print("Couldn't load data. Creating new profile.")
                create = True
                score_data = 0
                lives_data = 0
        else:
            create = True
            score_data = 0
            lives_data = 0
    if create:
        if not data:
            data = {}

        data['players'].append({
            player_name: {
                'score': score_data,
                'lives': lives_data
            }
        }) 
    """

    #menu = Store(int(input("Score: ")), int(input("Lives: ")))
    menu = Store(500, 3)
    menu.run()

    print("Game closed")
    
    
