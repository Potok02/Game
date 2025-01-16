import pygame

class Ship:
    """klasa przeznacozna do zarządzania statkiem kosmicznym."""

    def __init__(self, ai_game):
        """inicjalizacja statku kosmicznego i jego połozenie początkowe"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()


        # wczytanie obrazu statku kosmicznego i pobranie jego prostokąta.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # kazdy nowy statek kosmiczny pojawia sie na dole ekranu
        self.rect.midbottom = self.screen_rect.midbottom

        # połozenie poziome statku jest przechowywane w postaci liczby zmiennoprzecikowej.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # opcje wskazujące na poruszanie sie statku
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
    
    def update(self):
        """uaktualnienie polozenia statku na podstawie opcji wskazującej na jego ruch"""
        # uaktualnienie wartosci wspolrzendej X statku, a nie jego prostokata.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed_fly
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed_fly

        # uaktualnienie obiektu rect na podstawie wartosci self.x  i self.y
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """wyswietlenie statku kosmicznego w jego sktualnym połozeniu."""
        self.screen.blit(self.image, self.rect)