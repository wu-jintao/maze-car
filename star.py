import pygame


class Star(pygame.sprite.Sprite):
    # pygame.mixer.init()
    # eat_stars_sound = pygame.mixer.Sound("static/sounds/eat_stars.wav")
    # eat_stars_sound.set_volume(0.3)

    def __init__(self, center_x, center_y):
        super().__init__()
        self.image_source = pygame.image.load("static/images/star.png").convert()
        self.image = pygame.transform.scale(self.image_source, (50, 50))
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.center = (center_x, center_y)
        self.scale = 1
        self.scale_delta = 0.01

    def update(self):
        # 图形以中心点为锚点变化（90%-110%）
        self.scale += self.scale_delta
        if self.scale < 0.9 or self.scale > 1.1:
            self.scale_delta = -self.scale_delta
        self.image = pygame.transform.scale(self.image_source, (50 * self.scale, 50 * self.scale))
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
