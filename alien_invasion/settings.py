class Settings:
    """klasa przeznaczona do przechowywania wszystkich ustawien gry"""

    def __init__(self):
        """inicjalizacja ustawień gry"""
        # ustawienia ekranu
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        # ustawienia dotyczace statku
        self.ship_speed = 2.5
        self.ship_speed_fly = 1.5

        # ustawienia dotyczace pocisku
        self.bullet_speed = 5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (22.4, 100, 7.8)
        self.bullets_allowed = 10

        #ustawienia dotyczace obcego
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # wartosc fleet_direction wynoszaca 1 oznacza w prawo, a -1 w lewo.
        self.fleet_direction = 1