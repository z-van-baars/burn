import random
import art
import pygame as pg
import particle as prt
import effect as eft
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

        self.props = []
        self.physical_objects = []
        self.particles = []
        self.effects = []


class Lander(object):
    def __init__(self, screen_width):
        self.x = int(screen_width / 3)
        self.y = 30
        self.y_velocity = 0
        self.x_velocity = -1
        self.image = art.lander_sprite
        self.fuel = 100
        self.thrusting = False
        self.crashed = False
        self.explodes = False
        self.landed = False

    def thrust(self):
        self.fuel -= 1
        return -0.06

    def clear_image(self):
        self.image = pg.Surface([60, 50])
        self.image.fill((255, 0, 128))
        self.image.set_colorkey((255, 0, 128))
        self.image = self.image.convert_alpha()


class LanderShadow(object):
    def __init__(self, screen_height):
        self.x = -100
        self.y = screen_height - 90
        self.image = pg.Surface([60, 20])
        self.image.fill((255, 0, 128))
        self.image.set_colorkey((255, 0, 128))
        self.image = self.image.convert_alpha()
        pg.draw.ellipse(self.image, (115, 115, 115, 50), [0, 0, 60, 20])

    def get_xposition(self, screen_height, lander_x, lander_y):
        self.x = lander_x - (screen_height - 130 - lander_y) * 0.5

    def redraw_image(self, screen_height, lander_x, lander_y):
        alpha_value = max(10, 255 - (screen_height - 130 - lander_y) * 0.3)
        for i in range(3):
            refined_alpha = min(
                255,
                max(
                    0,
                    (alpha_value - 225) + i * 75))
            pg.draw.ellipse(
                self.image,
                (25, 25, 25, refined_alpha),
                [0 + i * 3,
                 0 + i * 3,
                 60 - i * 6,
                 20 - i * 6])


class Boulder(object):
    def __init__(self, x):
        self.width = 20
        self.height = 30
        self.x = x
        self.y = random.randint(600 - 230, 600 - 30)
        self.image = pg.Surface([self.width, self.height])
        self.image.fill((70, 70, 70))


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
            state.lander.thrusting = True
        else:
            state.lander.thrusting = False

    elif event.key == pg.K_SPACE:
        if state.lander.crashed or state.lander.landed:
            reset_new_game(state)
            return
        return True


def keyup_handler(state, event):
    if event.key == pg.K_z:
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


def physics_update(screen_height, lander, gravity, active_props, active_particles):
    thrust = 0
    if lander.thrusting is True:
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

    # particle physics and position math
    for particle in active_particles:
        if particle.physical is True:
            # 4 is terminal particle velocity for physical particles
            # chop the float down to keep the numbers reasonable
            particle.y_velocity = round(
                min(4, particle.y_velocity + gravity), 2)

        # chop the float after multiplication | keep the numbers compact
        particle.x_velocity *= 0.995
        particle.x_velocity = round(particle.x_velocity, 2)

        particle.x += particle.x_velocity
        particle.y += particle.y_velocity

    # move scene items to make it appear as if the lander is travelling
    for prop in active_props:
        prop.x += lander.x_velocity

    state.lander_shadow.get_xposition(screen_height, lander.x, lander.y)


def update(state, lander):
    # Spawn Boulders
    if random.randint(1, 100) > 99:
        new_boulder = Boulder(state.screen_width)
        state.props.append(new_boulder)

    # Conditional Events Based On Lander Height
    adj_alt = state.screen_height - 130 - lander.y
    if lander.fuel == 0:
        lander.thrusting = False
    if lander.thrusting is True:
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
                smkp = prt.Smoke(
                    lander.x + 15,
                    state.screen_height - 90,
                    random.randrange(-40, 0))
                smkp.x_velocity = random.choice([-3, 3])
                smkp.x += 10 * smkp.x_velocity
                smkp.y += random.randrange(-5, 5)
                state.particles.append(smkp)
        if adj_alt <= 60:
            if random.randint(1, 100) > 80:
                ld = prt.LunarDust(
                    lander.x + 30,
                    state.screen_height - 75,
                    random.randrange(-30, 30))
                ld.x_velocity = random.choice([-4, -3, 3, 4])
                ld.x += 3 * ld.x_velocity
                ld.y += random.randrange(-3, 3)
                ld.y_velocity = random.randrange(-30, -10, 1) / 10
                state.particles.append(ld)
    if lander.explodes is True:
        lander.explodes = False
        lander.clear_image()
        new_expl = eft.Explosion(lander.x - 20, lander.y - 35)
        state.effects.append(new_expl)
        for i in range(25):
            sp = prt.Spark(
                lander.x,
                lander.y - 40,
                lander.y_velocity,
                random.randrange(-10, 20))
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

    # Process effects
    active_effects = []
    for active_effect in state.effects:
        active_effect.play()
        if active_effect.active:
            active_effects.append(active_effect)
    state.effects = active_effects

    # Process particles and duration
    for particle in state.particles:
        particle.duration -= 1
        if particle.duration == 0:
            particle.remove_flag = True

    # Check Particles for deletion
    active_particles = []
    for particle in state.particles:
        if particle.remove_flag is True:
            continue
        active_particles.append(particle)
    state.particles = []
    state.particles = active_particles


def reset_new_game(state):
    state.__init__((state.screen_width, state.screen_height))


state = GameState((800, 600))

while True:
    start = event_handler(state)
    if start is True:
        break
    display_update(state.screen, state.clock, state)
    state.clock.tick(60)

while True:
    event_handler(state)
    update(state, state.lander)
    physics_update(
        state.screen_height,
        state.lander,
        state.gravity,
        state.props,
        state.particles)
    display_update(state.screen, state.clock, state)
    state.clock.tick(60)
