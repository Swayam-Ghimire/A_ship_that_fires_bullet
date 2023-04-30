import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, setting, screen):
        """Initialize the ship and set its starting position."""
        super().__init__()
        # calls __init__() method of parent class "Sprite"
        self.screen = screen
        self.setting = setting
        # Load the ship image and get its rect.
        self.image = pygame.image.load('ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # self.rect.centerx -= 60
        # Movement flag
        # Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)
        self.center1 = float(self.rect.centery)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # self.rect.right vaneko ship ko x-coordinate ho.
            # yesle check garxa if ship ko x-coordinate chai less than screen ko x-coordinate ko antim vaagh
            self.center += self.setting.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.setting.ship_speed_factor
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.center1 -= self.setting.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.center1 += self.setting.ship_speed_factor
        self.rect.centerx = self.center
        self.rect.centery = self.center1
        # updating new position of the ship

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
    def center_ship(self):
        self.center = self.screen_rect.centerx
        self.center1 = self.screen_rect.bottom - 60
        # self.rect.bottom = self.screen_rect.bottom
# ship_explained
