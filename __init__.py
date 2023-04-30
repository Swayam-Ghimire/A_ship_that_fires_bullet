import game_functions as gf
import pygame
from settings import Settings
from ship import Ship
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    # Initialize game and create a screen object.
    # Creating instance

    setting = Settings()
    pygame.init()

    screen = pygame.display.set_mode((setting.width, setting.height))
    ship = Ship(setting, screen)
    stats = GameStats(setting)
    sb = Scoreboard(setting, screen, stats)
    play_button = Button(screen, setting, 'Tap to play')
    # Make an alien.
    aliens = Group()
    # Create new instance of the Group() class from pygame.sprite module.
    # it is the instance use to store the Alien's sprite and allow us to manage Alien's sprite
    # Make group to store the bullets in.
    bullets = Group()
    gf.create_fleet(setting, screen, aliens, ship)
    pygame.display.set_caption("Alien Invasion")
    play_button.draw_button()
    pygame.display.flip()
    # Start the main loop for the game.
    # bg_color = (100, 100, 100)  # RGB color mixed equally to make a gray color
    while True:
        # Watch for keyboard and mouse events.
        gf.check_events(ship, setting, screen, bullets, stats, play_button, aliens, sb)
        if stats.game_active:
            ship.update()
            """In this case, the bullets group is used to store all the bullets that have been fired by 
            the player's ship, and the update method is used to update the position of each bullet in the
            group on each iteration of the game loop.
            # When the update method is called on the bullets group, it automatically calls the update method
            on each sprite in the group, which in this case is the Bullet class.
            # Therefore, the update method in the Bullet class is called indirectly by calling the update method 
            on the bullets group in the main game loop."""
            bullets.update()
            gf.update_bullets(bullets, aliens, setting, screen, ship, stats, sb)  # deleting bullet
            gf.update_aliens(aliens, setting, ship, stats, bullets, screen, sb) # updating the position of aliens as a whole ie sabai ko position ekaichoti alter gareko
            gf.update_screen(setting, screen, ship, bullets, aliens, play_button, stats, sb)


run_game()
