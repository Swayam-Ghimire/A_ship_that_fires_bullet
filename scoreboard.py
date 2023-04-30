import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, setting, screen, stats):
        """Initialize scorekeeping attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.setting = setting
        self.stats = stats
        # Font settings for scoring information.
        self.text_color = (200, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_level(self):
        """Turn the level into rendered image"""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.setting.bg_color)
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.setting.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top + 20

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        """"
The :, inside the format specifier is a formatting option that adds a comma as a thousands separator to the output.
So in the format string "{:,}".format(100000), the : character marks the start of the formatting specifier, ',' inserts
the thousands separator, and the empty string after the colon : means to use the default formatting for a floating-point
number, which in this case is an integer.The resulting output would be the string "100,000".
: The colon character marks the start of the format specifier.
, The comma character is a formatting option that adds a comma as a thousands separator to the output.
        """
        # score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.setting.bg_color)
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.setting, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)


    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # Draw ships.
        self.ships.draw(self.screen)
