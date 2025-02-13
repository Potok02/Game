import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """klasa przedstawiająca pojedynczego obcego we flocie."""

    def __init__(self, ai_game):
        """inicjalizacja obcego i zdefiniowanie jego polozenia poczatkowego."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #wczytanie obrazu obcego i zdefiniowanie jego atrybutu rect
        self.image = pygame.image.load(get_random_alien_image())
        self.rect = self.image.get_rect()

        # umieszczenie nowego obcego w poblizu lewego gornego rogu ekranu.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # przechowywanie dokladnego poziomego polozenia obcego.
        self.x = float(self.rect.x)

    def check_edges(self):
        """zwraca wartosc True, jesli obcy znajduje sie przy krawedzi ekranu."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
    
    def check_dissapeared(self):
        """sprawdzenie czy flota dotarła za dolną krawedz ekranu"""
        if self.rect.top > self.screen.get_rect().bottom:
            return True
        else:
            return False
    
    def update(self):
        """przesuniecie obcego w prawo lub w lewo"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
    