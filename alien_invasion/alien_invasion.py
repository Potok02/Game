import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Ogólna klasa przeznaczona do zarzadzania zasobami i sposobem działania gry."""
    def __init__(self):
        """inicjalizacja gry i utowrzenie jej zasobów"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("mini gierka")


        # tryb pelnoekranowy, brak okienka zamykania = dodac menu

        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """rozpoczecie pętli głownej gry."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """reakcja na zdarzenia generowane przez klawiature i mysz."""
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:       
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """reakcja na nacisniecie klawisza."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        
    def _check_keyup_events(self, event):
        """reakcja na zwolnienie klawisza."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        
    def _fire_bullet(self):
        """utworzenie nowego pocisku i dodanie go do grupy pocisków."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """uaktualnienie polozenia pocisków i usuniecie niewidocznych na ekranie"""
        #uaktualnienie polozenia pocisków
        self.bullets.update()
        # usuniecie pociskow z gry gdy przestana byc widoczne
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()
        
    def _check_bullet_alien_collision(self):
        """reakcja na kolizje miedzy pociskiem i obcym."""
        # usuniecie wszystkich pocisków i obcych, miedzy ktorymi doszlo do kolizji
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if not self.aliens:
        #pozbycie sie istniejacych pocisków i utworzenie nowej floty.
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """sprawdzenie czy flota znajduje sie przy krawedzia nastepnie uaktualnienie polozenia obcych we flocie."""
        self._check_fleet_edges()
        self.aliens.update()

        for alien in self.aliens.copy():
            if alien.check_dissapeared():
                self.aliens.remove(alien)

         # Jeśli nie ma więcej obcych, stwórz nową flotę
        if not self.aliens:
            self._create_fleet()
            
    def _create_fleet(self):
        """utworzenie pełnej floty obcych."""
        # utworzenie obcego i dodawanie kolejnych obcych ktorzy zmieszcza sie w rzedzie
        # odległosc miedzy poszczegolnymi obcymi jest równa szerokosci obcego.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            
            # ukonczenie rzedu, wyzerowanie wartosci x oraz inkrementacja wartosci y.
            current_x = alien_width
            current_y += 2 * alien_height

        self.settings.alien_speed *= 1.1  # Zwiększ prędkość o 10% za każdym razem


    def _create_alien(self, x_position, y_position):
        """utworzenie obcego i umieszczenie go w rzędzie."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """odpowiednia reakcja gdy obcy dotrze do krawedzi ekranu"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """przesuniecie calej floty w dol i zmiana kierunku w ktorym sie ona porusza"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
         # odswiezanie ekranu w trakcie kazdej iteracji pętli
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.aliens.draw(self.screen)

        pygame.display.flip()

if __name__ == '__main__':
        # utworzenie egzemplarza gry i jej uruchomienie
    ai = AlienInvasion()
    ai.run_game()
