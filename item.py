import pygame
from pygame.sprite import Sprite

class Item(Sprite):
    """아이템 만들기"""

    def __init__(self, ai_settings, screen):

        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.flag = False

        self.image = pygame.image.load('images/fire.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.margin = self.ai_settings.item_margin


    def update(self):
        """아이템을 바닥을 향해 떨어트린다."""
        self.y += self.speed_factor
        self.rect.y = self.y