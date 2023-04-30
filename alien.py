import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, setting, screen, ship):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.ship = ship
        self.screen = screen
        self.setting = setting
        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('alien.png')
        self.rect = self.image.get_rect()
        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Store the alien's exact position.
        self.x = float(self.rect.x)
        # self.rect.x is the distance between the screen left end and the left edge of alien.
        # In this case self.rect.x is equal to the width of the alien object.
        # float here is used for smooth animation.
        # By setting self.x to a floating-point value, we can move the alien in small increments,
        # allowing for smooth movement across the screen.

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien to the right and left"""
        self.x += (self.setting.alien_speed_factor * self.setting.fleet_direction)
        self.rect.x = self.x
