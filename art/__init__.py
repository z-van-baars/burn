import pygame

pygame.init()
pygame.display.set_mode([0, 0])
pygame.display.set_caption("Burn v0.1")


key_color = (255, 0, 128)
fuel_gauge_overlay = pygame.image.load("art/ui/fuel_gauge_overlay.png")
fuel_gauge_overlay.set_colorkey(key_color)
fuel_gauge_overlay = fuel_gauge_overlay.convert_alpha()

throttle_gauge_overlay = pygame.image.load("art/ui/throttle_gauge_overlay.png")
throttle_gauge_overlay.set_colorkey(key_color)
throttle_gauge_overlay = throttle_gauge_overlay.convert_alpha()

throttle_pointer = pygame.image.load("art/ui/throttle_pointer.png")
throttle_pointer.set_colorkey(key_color)
throttle_pointer = throttle_pointer.convert_alpha()


lander_sprite = pygame.image.load("art/lander.png").convert_alpha()
lander_sprite.set_colorkey(key_color)
lander_sprite = lander_sprite.convert_alpha()
flame_sprites = []
for i in range(3):
    flame_sprite = pygame.image.load("art/particles/flame_{0}.png".format(i + 1))
    flame_sprite.set_colorkey(key_color)
    flame_sprite = flame_sprite.convert_alpha()
    flame_sprites.append(flame_sprite)

med_flame_sprites = []
for i in range(6):
    med_flame_sprite = pygame.image.load("art/particles/med_flame_{0}.png".format(i + 1))
    med_flame_sprite.set_colorkey(key_color)
    med_flame_sprite = med_flame_sprite.convert_alpha()
    med_flame_sprites.append(med_flame_sprite)

small_flame_sprites = []
for i in range(4):
    small_flame_sprite = pygame.image.load("art/particles/small_flame_{0}.png".format(i + 1))
    small_flame_sprite.set_colorkey(key_color)
    small_flame_sprite = small_flame_sprite.convert_alpha()
    small_flame_sprites.append(small_flame_sprite)


smoke_sprites = []
for i in range(6):
    smoke_sprite = pygame.image.load("art/particles/smoke_{0}.png".format(i + 1))
    smoke_sprite.set_colorkey(key_color)
    smoke_sprite = smoke_sprite.convert_alpha()
    smoke_sprites.append(smoke_sprite)
small_smoke_sprites = smoke_sprites[3:]

explosion_spritesheet = pygame.image.load("art/effects/explosion.png")
explosion_spritesheet.set_colorkey(key_color)
explosion_spritesheet = explosion_spritesheet.convert_alpha()
explosion = []
for i in range(8):
    explosion_frame = pygame.Surface([50, 60])
    explosion_frame.fill((255, 0, 128))
    explosion_frame.blit(explosion_spritesheet, [0, 0], (50 * i, 0, 50, 60))
    explosion_frame.set_colorkey(key_color)
    explosion_frame = explosion_frame.convert_alpha()
    explosion_frame = pygame.transform.scale2x(explosion_frame)
    explosion.append(explosion_frame)