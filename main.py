import pygame
import config
from game_manager import GameManager
from utils.draw_text import draw_text


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pygame.time.Clock()

ico = pygame.image.load("static/images/maze.png").convert()
pygame.display.set_icon(ico)
pygame.display.set_caption("迷宫汽车")

pygame.mixer.music.load("static/sounds/bgm.wav")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)  # 循环播放

game_manager = GameManager(screen, 1)

running = True
success_time = -1  # 获胜时刻
success_finished = False  # 完全通关
while running:
    # 退出或通关后按任意键结束
    for event in pygame.event.get():
        if event.type == pygame.QUIT or success_finished and event.type == pygame.KEYDOWN:
            running = False

    if success_finished:
        screen.fill("black")
        draw_text(screen, "Win!!!", 200, config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2)
    else:
        # 获胜后2秒切换下一关
        if success_time >= 0:
            if pygame.time.get_ticks() - success_time >= 2000:
                has_next = game_manager.next_level()
                if not has_next:
                    success_finished = True
                    continue
                success_time = -1

        screen.fill("black")
        if game_manager.update():
            success_time = pygame.time.get_ticks()

    pygame.display.flip()

    clock.tick(config.FPS)

pygame.quit()
