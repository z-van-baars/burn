import random
import art
import pygame as pg
import particle as prt
from display import display_update


class GameState(object):
    def __init__(self, screen_dimensions):
        self.screen_width = screen_dimensions[0]
        self.screen_height = screen_dimensions[1]
        self.screen = pg.display.set_mode(
            [screen_dimensions[0],
             screen_dimensions[1]])
        self.clock = pg.time.Clock()

        self.gravity = 0.03

        self.ground = Ground(screen_dimensions)
        self.lander = Lander(screen_dimensions[0])
        self.lander_shadow = LanderShadow(screen_dimensions[1])

        self.static_objects = []
        self.physical_objects = []
        self.particles = []


class Lander(object):
    def __init__(self, screen_width):
        self.x = int(screen_width / 3)
        self.y = 30
        self.y_velocity = 0
        self.x_velocity = 1
        self.image = art.lander_sprite
        self.fuel = 1000
        self.thrusting = False
        self.crashed = False
        self.explodes = False
        self.landed = False

    def thrust(self):
        self.fuel -= 1
        return -0.06


class LanderShadow(object):
    def __init__(self, screen_height):
        self.x = -100
        self.y = screen_height - 90
        self.image = pg.Surface([60, 20])
        self.image.fill((255, 0, 128))
        self.image.set_colorkey((255, 0, 128))
        self.image = self.image.convert_alpha()
        pg.draw.ellipse(self.image, (115, 115, 115, 50), [0, 0, 60, 20])

        # self.image.set_alpha(10)
        # self.image = self.image.convert_alpha()

    def get_xposition(self, screen_height, lander_x, lander_y):
        self.x = lander_x - (screen_height - 130 - lander_y) * 0.5

    def redraw_image(self, screen_height, lander_x, lander_y):
        alpha_value = max(10, 255 - (screen_height - 130 - lander_y) * 0.3)
        for i in range(3):
            pg.draw.ellipse(self.image, (25, 25, 25, min(255, max(0, (alpha_value - 225) + i * 75))),
                [0 + i * 3,
                 0 + i * 3,
                 60 - i * 6,
                 20 - i * 6])


class Boulder(object):
    def __init__(self):
        self.width = 30
        self.height = 30
        self.x = 0
        self.y = random.randint(600 - 230, 600 - 30)
        self.image = pg.Surface([self.width, self.height])
        self.image.fill((100, 100, 100))


class Ground(object):
    def __init__(self, screen_dimensions):
        self.width = screen_dimensions[0]
        self.height = 200
        self.image = pg.Surface([self.width, self.height])
        self.image.fill((100, 100, 100))


def mousedown_handler(state, event):
    pass


def mouseup_handler(state, event):
    pass


def keydown_handler(state, event):
    if event.key == pg.K_z:
        if state.lander.fuel > 0:
            print("Thrusting!")
            state.lander.thrusting = True
        else:
            state.lander.thrusting = False
            print("Out of fuel!!")

    elif event.key == pg.K_SPACE:
        return True



def keyup_handler(state, event):
    if event.key == pg.K_z:
        print("Thrust Stopped")
        state.lander.thrusting = False


def event_handler(state):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.display.quit()
            pg.quit()
        if event.type == pg.KEYDOWN:
            return keydown_handler(state, event)

        if event.type == pg.KEYUP:
            keyup_handler(state, event)

        if event.type == pg.MOUSEBUTTONDOWN:
            mousedown_handler(state, event)

        if event.type == pg.MOUSEBUTTONUP:
            mouseup_handler(state, event)


def physics_update(screen_height, lander, gravity, active_particles):
    thrust = 0
    if lander.thrusting == True:
        thrust = lander.thrust()
    lander.y_velocity = round(min(4, lander.y_velocity + thrust + gravity), 2)
    lander.y += lander.y_velocity
    lander.y = round(lander.y, 2)
    if lander.y >= screen_height - 130:
        lander.y = screen_height - 130
        if lander.y_velocity >= 2.0:
            lander.crashed = True
            if lander.y_velocity > 3.5:
                lander.explodes = True
        else:
            lander.landed = True
        lander.y_velocity = 0
        lander.x_velocity = 0
    for particle in active_particles:
        if particle.physical == True:
            particle.y_velocity = round(min(4, particle.y_velocity + gravity), 2)
        particle.x_velocity *= 0.995
        particle.x_velocity = round(particle.x_velocity, 2)

        particle.x += particle.x_velocity
        particle.y += particle.y_velocity

    state.lander_shadow.get_xposition(screen_height, lander.x, lander.y)


def update(state, lander):

    # Conditional Events Based On Lander Height
    adj_alt = state.screen_height - 130 - lander.y
    if lander.thrusting == True:
        new_flame_particle = prt.SmallFlame(
            lander.x + 20,
            lander.y + 48)
        new_flame_particle.y_velocity += lander.y_velocity
        state.particles.append(new_flame_particle)
        if random.randint(1, 100) > 50:
            new_spark_particle = prt.Spark(
                lander.x,
                lander.y,
                lander.y_velocity,
                random.randrange(-10, 10))
            state.particles.append(new_spark_particle)

        if adj_alt <= 90:
            if random.randint(1, 100) > 70:
                smkp = prt.Smoke(lander.x + 15, state.screen_height - 90, random.randrange(-40, 0))
                smkp.x_velocity = random.choice([-3, 3])
                smkp.x += 10 * smkp.x_velocity
                smkp.y += random.randrange(-5, 5)
                state.particles.append(smkp)
        if adj_alt <= 60:
            if random.randint(1, 100) > 80:
                ld = prt.LunarDust(lander.x + 30, state.screen_height - 75, random.randrange(-30, 30))
                ld.x_velocity = random.choice([-4, -3, 3, 4])
                ld.x += 3 * ld.x_velocity
                ld.y += random.randrange(-3, 3)
                ld.y_velocity = random.randrange(-30, -10, 1) / 10
                state.particles.append(ld)
    if lander.explodes == True:
        lander.explodes = False
        for i in range(25):
            sp = prt.Spark(lander.x, lander.y - 40, lander.y_velocity, random.randrange(-10, 20))
            sp.y_velocity += random.randrange(-30, -20, 1) / 5
            sp.x_velocity *= random.randrange(10, 30, 1) / 10
            state.particles.append(sp)
        for j in range(3):
            smkpr = prt.Smoke(lander.x + 15, lander.y + 40)
            smkpr.y_velocity = -random.randrange(0, 2, 1) / 10
            smkpr.x_velocity = random.randrange(2, 10, 1) / 10
            smkpr.x += smkpr.x_velocity * 5
            state.particles.append(smkpr)
            smkpl = prt.Smoke(lander.x + 15, lander.y + 40)
            smkpl.y_velocity = -random.randrange(0, 2, 1) / 10
            smkpl.x_velocity = -random.randrange(2, 10, 1) / 10
            smkpl.x += smkpl.x_velocity * 5
            state.particles.append(smkpl)

    # Process particles and duration
    for particle in state.particles:
        particle.duration -= 1
        if particle.duration == 0:
            particle.remove_flag = True

    # Check Particles for deletion
    active_particles = []
    for particle in state.particles:
        if particle.remove_flag == True:
            continue
        active_particles.append(particle)
    state.particles = []
    state.particles = active_particles

width, height = 800, 600
state = GameState([width, height])

while True:
    start = event_handler(state)
    if start is True:
        break
    display_update(state.screen, state.clock, state)
    state.clock.tick(60)

while True:
    event_handler(state)
    update(state, state.lander)
    physics_update(state.screen_height, state.lander, state.gravity, state.particles)
    display_update(state.screen, state.clock, state)
    state.clock.tick(60)