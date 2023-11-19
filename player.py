import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y, forward_angle):
        super().__init__()
        self.width = 100
        self.height = 50
        self.forward_angle = forward_angle
        self.image_source = pygame.image.load("static/images/car.png").convert()
        self.image = pygame.transform.scale(self.image_source, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, -self.forward_angle)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.center = (center_x, center_y)
        # 帧时间
        self.last_time = pygame.time.get_ticks()
        self.delta_time = 0
        # 移动相关
        self.move_velocity = 0
        self.move_velocity_limit = 220
        self.move_acc = 600
        self.friction = 0.98
        # 转动相关
        self.rotate_velocity = 0
        self.rotate_velocity_limit = 120
        # 音效
        self.crash_sound = pygame.mixer.Sound("static/sounds/crash.mp3")
        self.crash_sound.set_volume(0.1)
        self.move_sound = pygame.mixer.Sound("static/sounds/move.mp3")
        self.move_sound.set_volume(0.5)
        self.move_sound_channel = pygame.mixer.Channel(7)  # 7号声道

    def update_delta_time(self):
        cur_time = pygame.time.get_ticks()
        self.delta_time = (cur_time - self.last_time) / 1000
        self.last_time = cur_time

    def input(self):
        self.update_delta_time()
        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_w]:
            self.move_velocity += self.move_acc * self.delta_time
            self.move_velocity = min(self.move_velocity, self.move_velocity_limit)
            if not self.move_sound_channel.get_busy():
                self.move_sound_channel.play(self.move_sound)
        elif key_pressed[pygame.K_s]:
            self.move_velocity -= self.move_acc * self.delta_time
            self.move_velocity = max(self.move_velocity, -self.move_velocity_limit)
            if not self.move_sound_channel.get_busy():
                self.move_sound_channel.play(self.move_sound)
        else:
            self.move_velocity = int(self.move_velocity * self.friction)
            if self.move_sound_channel.get_busy():
                self.move_sound_channel.stop()

        single = 1  # 前进或后退（转动方向不同）
        if self.move_velocity < 0:
            single = -1
        if key_pressed[pygame.K_d]:
            self.rotate_velocity = self.rotate_velocity_limit * single
        elif key_pressed[pygame.K_a]:
            self.rotate_velocity = -self.rotate_velocity_limit * single
        else:
            self.rotate_velocity = 0

    def rotate(self, direction):
        self.forward_angle += self.rotate_velocity * self.delta_time * direction
        self.image = pygame.transform.scale(self.image_source, (self.width, self.height))  # 多次修改图像会造成误差累计
        self.image = pygame.transform.rotate(self.image, -self.forward_angle)
        self.image.set_colorkey("black")
        # 围绕汽车中心转动
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def move(self, direction=1):
        if self.move_velocity:
            if direction == 1 and abs(self.move_velocity) > 50:
                self.rotate(direction)
            vx = self.move_velocity * math.cos(math.pi * self.forward_angle / 180) * direction
            vy = self.move_velocity * math.sin(math.pi * self.forward_angle / 180) * direction
            self.rect.x += vx * self.delta_time
            self.rect.y += vy * self.delta_time
            # 退回与前进对称
            if direction == -1 and abs(self.move_velocity) > 50:
                self.rotate(direction)

    # 撞墙
    def crash(self):
        self.crash_sound.play()
        self.move(-1)  # 退回
        # 小速度碰撞也会反弹退回
        if self.move_velocity >= 0:
            self.move_velocity = min(-self.move_velocity, -100)
        else:
            self.move_velocity = max(-self.move_velocity, 100)

    def update(self):
        self.input()
        self.move()
