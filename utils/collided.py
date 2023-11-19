import math
import pygame


def collided_rect(a, b):
    # 检测wall与car的小矩形框（0.8）是否碰撞
    p = []
    for i, j in [(1, -1), (1, 1), (-1, 1), (-1, -1)]:
        # pygame.Vector2()坐标系为数学坐标系
        t = pygame.Vector2(i * a.width / 2 * 0.8, j * a.height / 2 * 0.8).rotate(a.forward_angle)
        p.append(t + a.rect.center)
    for i in range(4):
        x = p[i]
        y = p[(i + 1) % 4]
        if b.rect.clipline(x, y):
            return True

    # 检测wall与car的前后两条边是否碰撞
    p.clear()
    for i, j in [(1, -1), (1, 1), (-1, 1), (-1, -1)]:
        t = pygame.Vector2(i * a.width / 2, j * a.height / 2 * 0.2).rotate(a.forward_angle)
        p.append(t + a.rect.center)
    for i in range(4):
        x = p[i]
        y = p[(i + 1) % 4]
        if b.rect.clipline(x, y):
            return True
    return False


def collided_circle(a, b):
    x1, y1 = a.rect.center
    x2, y2 = b.rect.center
    dx = x1 - x2
    dy = y1 - y2
    if math.sqrt(dx * dx + dy * dy) < 50:
        return True
    return False
