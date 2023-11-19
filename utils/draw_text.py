import pygame


def draw_text(scree, text, size, x, y):
    font = pygame.font.SysFont(pygame.font.get_default_font(), size)
    image = font.render(text, True, "white")
    rect = image.get_rect()
    rect.center = (x, y)
    scree.blit(image, rect)
