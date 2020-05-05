import art
import pygame as pg


class Colors(object):
    white = (255, 255, 255)
    black = (0, 0, 0)
    background_black = (20, 20, 20)
    red = (225, 10, 10)
    yellow = (225, 200, 10)

    def __init__(self):
        pass


colors = Colors()


class Fonts(object):
    arial = pg.font.Sysfont(
        'Arial',
        24,
        False,
        False)
    calibri = pg.font.Sysfont(
        'Calibri',
        24,
        False,
        False)
    banschrift = pg.font.Sysfont(
        'Banschrift Light Semicondensed',
        24,
        False,
        False)

    def __init__(self):
        pass


fonts = Fonts()


class Banner(object):
    def __init__(self, screen_dimensions, x, y, message, font=fonts.helvetica, color=colors.white):
        self.x = x
        self.y = y
        self.font = font
        self.message = message
        self.color = color
        self.image = pygame.Surface([0, 0])

    def render_image(self)
        self.image = self.font.render(self.message, True, self.color)


class Decals(object):
    def __init__(self):
        altitude_stamp = large_font.render(, True, (255, 255, 255))
        self.altitude_stamp = Banner(
            screen_dimensions,
            4,
            10,
            "Altitude: {0}".format(
                round(state.screen_height - 130 - state.lander.y), 3),
            fonts.banschrift)
        self.velocity_banner = Banner(
            screen_dimensions,
            "Velocity: {0}".format(-state.lander.y_velocity),
            4,
            30,
            fonts.banschrift)
        self.fuel_banner = Banner(
            screen_dimensions,
            "Fuel: [ {0} / 500 ]".format(state.lander.fuel),
            4,
            50,
            fonts.banschrift)

        self.active_messages = []

    def get_all_decals(self):
        return self.active_messages + [
            self.altitude_stamp,
            self.fuel_stamp]


def display_update(screen, clock, state):
    screen.fill((20, 20, 20))

    # Draw the ground / background
    screen.blit(
        state.ground.image,
        [0, state.screen_height - state.ground.height])
    # Draw Props
    for prop in state.props:
        screen.blit(prop.image, [prop.x, prop.y])
    # Redraw the lander shadow with alt. based opacity
    state.lander_shadow.redraw_image(
        state.screen_height,
        state.lander.x,
        state.lander.y)
    # Draw the shadow to the screen
    screen.blit(
        state.lander_shadow.image,
        [state.lander_shadow.x,
         state.lander_shadow.y])
    # Draw the Lander
    screen.blit(
        state.lander.image,
        [state.lander.x,
         state.lander.y])
    # Draw the Effects + Animations
    for active_effect in state.effects:
        screen.blit(
            active_effect.active_frame,
            [active_effect.x, active_effect.y])
    # Draw particles
    for particle in state.particles:
        screen.blit(particle.image, [particle.x, particle.y])

    # Decals and UI
    if 3.5 >= state.lander.y_velocity > 2:
        decals.velocity_banner.color = colors.yellow
    elif state.lander.y_velocity > 3.5:
        decals.velocity_banner.color = colors.red
    f_color = colors.white
    if 25 < state.lander.fuel <= 50:
        decals.fuel_banner.color = colors.yellow
    elif state.lander.fuel <= 25:
        decals.fuel_banner.color = colors.red

    fuel_bar = pg.Surface([
        40,
        max(1, int(200 * (state.lander.fuel / 100)))])
    if state.lander.fuel > 0:
        fuel_bar.fill((225, 10, 10))

    screen.blit(
        fuel_bar
        [state.screen_width - 50,
         110 + (200 - fuel_bar.get_height())])
    screen.blit(art.fuel_gauge_overlay, [state.screen_width - 55, 100])

    # screen.blit(art.throttle_gauge_overlay, [state.screen_width - 55, 300])
    if state.lander.landed is True:
        landed_message =
        landed_message = Banner(
            screen_dimensions,
            int(screen.get_width() * 0.5 - m_width * 0.5),
            int(screen.get_height() * 0.3),
            "You landed with [ {0} / 500 ] fuel remaining!".format(state.lander.fuel),
            fonts.banschrift)
        decals.active_messages.append()
        landed_stamp = large_font.render(, True, (255, 255, 255))
        m_width = landed_stamp.get_width()
        screen.blit(landed_stamp, [int(screen.get_width() * 0.5 - m_width * 0.5), int(screen.get_height() * 0.3)])
    if state.lander.crashed == True:
        crashed_stamp = large_font.render(
            "You have crashed!", True, (245, 10, 10))
        m_width = crashed_stamp.get_width()
        screen.blit(crashed_stamp, [int(screen.get_width() * 0.5 - m_width * 0.5), int(screen.get_height() * 0.4)])

    pg.display.flip()
    clock.tick(60)

