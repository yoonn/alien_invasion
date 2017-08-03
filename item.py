import pygame

class Item:
    """아이템 만들기"""

    def __init__(self, ai_settings, screen):

        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('images/fire.png')

        self.speed_factor = self.ai_settings.item_speed_factor
        self.margin = self.ai_settings.item_margin


    def update(self):
        self.y += self.speed_factor
        self.rect.y = self.y