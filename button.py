"""Python doesn't have a builtin method for making buttons."""
import pygame.font


class Button:
    def __init__(self, screen, setting, msg):
        """Initializes the button attribute"""
        self.screen = screen
        self.setting = setting
        # Set the dimensions and properties of the button
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = 200, 50
        self.text_color = (0, 0, 0)
        self.button_color = (150, 200, 100)
        self.font = pygame.font.SysFont(None, 36) # None is a default font and 48 is the font size
        # To make the font of desired format and size
        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        # The button message needs to be prepped only once.
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
    # The call to font.render() turns the text stored in msg into an image, which we then store in msg_image
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
