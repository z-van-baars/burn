import random
import art
import pygame


class Particle(object):
    def __init__(self, x, y, duration, physical=False):
        self.x = x
        self.y = y
        self.duration = duration
        self.physical = physical
        self.x_velocity = 0
        self.y_velocity = 0
        self.remove_flag = False


class PhysParticle(Particle):
    def __init__(self, x, y, duration):
        super().__init__(x, y, duration, True)


class Flame(Particle):
    def __init__(self, x, y):
        super().__init__(x, y, 2)
        self.image = random.choice(art.flame_sprites)

class SmallFlame(Particle):
    def __init__(self, x, y):
        super().__init__(x, y, 2)
        self.image = random.choice(art.small_flame_sprites)


class Smoke(Particle):
    def __init__(self, x, y, duration_boost=0):
        super().__init__(x, y, 120+duration_boost)
        self.image = random.choice(art.smoke_sprites)


class Spark(PhysParticle):
    def __init__(self, x, y, lander_y_velocity, duration_boost=0):
        super().__init__(random.randint(x + 28, x + 32), y + 54, 30 + duration_boost)

        self.image = pygame.Surface([1, 1])
        self.image.fill((255, 200, 0))
        self.x_velocity = random.randrange(-4, 4, 2) / 10
        self.y_velocity = random.randrange(5, 30, 2) / 10

        if lander_y_velocity > 0:
            self.y_velocity += lander_y_velocity


class LunarDust(PhysParticle):
    def __init__(self, x, y, lander_y_velocity, duration_boost=0):
        super().__init__(x, y, 90 + duration_boost)

        size = random.choice([1, 2, 3])
        self.image = pygame.Surface([size, size])
        tone_l = random.randrange(135, 175)
        tone_d = random.randrange(50, 70)
        tone = random.choice([tone_l, tone_d])
        self.image.fill((tone, tone, tone))


class SmallSmoke(Particle):
    def __init__(self, x, y, duration_boost=0):
        super().__init__(x, y, 90+duration_boost)
        self.image = random.choice(art.small_smoke_sprites)