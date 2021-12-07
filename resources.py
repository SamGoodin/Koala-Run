# Class that contains all resources
# Resources class stores sub classes per resource
# Each sub class contains dict {file : filepath}
# so upon get, must load

class Resources:

    def __init__(self):
        self.Player = self.Player()
        self.Background = self.Background()
        self.Other = self.Other()

    class Player:

        def __init__(self) -> None:
            self.resources = {}
            self.resources['idle'] = "resources/player/koala_idle.png"
            self.resources['jump'] = "resources/player/koala_jump.png"
            self.resources['walk1'] = "resources/player/koala_walk01.png"
            self.resources['walk2'] = "resources/player/koala_walk02.png"
            self.resources['walk3'] = "resources/player/koala_walk03.png"

    class Background:

        def __init__(self) -> None:
            self.resources = {}
            self.resources['default'] = "resources/backgrounds/default.png"

    class Other:

        def __init__(self) -> None:
            self.resources = {}
            self.resources['coin'] = "resources/other/goldCoin1.png"