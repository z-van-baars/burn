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
    arial = pg.font.SysFont(
        'Arial',
        24,
        False,
        False)
    calibri = pg.font.SysFont(
        'Calibri',
        24,
        False,
        False)
    banschrift = pg.font.SysFont(
        'Banschrift Light Semicondensed',
        24,
        False,
        False)

    def __init__(self):
        pass


fonts = Fonts()


class Banner(object):
    def __init__(self, message, font=fonts.arial, color=colors.white):
        self.x = 0
        self.y = 0
        self.font = font
        self.message = message
        self.color = color
        self.render_image()

    def render_image(self):
        self.image = self.font.render(self.message, True, self.color)


class Decals(object):
    def __init__(self):
        self.altitude = Banner(
            "Altitude: {0}".format(0),
            fonts.banschrift)
        self.altitude.x = 4
        self.altitude.y = 10
        self.velocity = Banner(
            "Velocity: {0}".format(0),
            fonts.banschrift)
        self.velocity.x = 4
        self.velocity.y = 30
        self.fuel = Banner(
            "Fuel: [ {0} / 500 ]".format(0),
            fonts.banschrift)
        self.fuel.x = 4
        self.fuel.y = 50
        self.active_messages = []

    def get_all_decals(self):
        return self.active_messages + [
            self.altitude,
            self.velocity,
            self.fuel]

    def render_core_decals(self, screen_height, lander):
        self.altitude.message = (
            "Altitude: {0}".format(
                round(screen_height - 130 - lander.y), 3))
        self.velocity.message = (
            "Velocity: {0}".format(-lander.y_velocity))
        self.fuel.message = (
            "Fuel: [ {0} / 500 ]".format(lander.fuel))
        for each in [self.velocity, self.altitude, self.fuel]:
            each.render_image()


def display_update(screen, clock, state, decals):
    screen.fill(colors.background_black)

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
    decals.render_core_decals(state.screen_height, state.lander)
    if 3.5 >= state.lander.y_velocity > 2:
        decals.velocity.color = colors.yellow
    elif state.lander.y_velocity > 3.5:
        decals.velocity.color = colors.red
    if 25 < state.lander.fuel <= 50:
        decals.fuel.color = colors.yellow
    elif state.lander.fuel <= 25:
        decals.fuel.color = colors.red

    for each_decal in decals.get_all_decals():
        screen.blit(
            each_decal.image,
            [each_decal.x,
             each_decal.y])

    fuel_bar = pg.Surface([
        40,
        max(1, int(200 * (state.lander.fuel / 100)))])
    if state.lander.fuel > 0:
        fuel_bar.fill(colors.red)

    screen.blit(
        fuel_bar,
        [state.screen_width - 50,
         110 + (200 - fuel_bar.get_height())])
    screen.blit(art.fuel_gauge_overlay, [state.screen_width - 55, 100])

    # screen.blit(art.throttle_gauge_overlay, [state.screen_width - 55, 300])
    if state.lander.landed is True:
        landed_message = (
            "You landed with [ {0} / 500 ] fuel remaining!".format(
                state.lander.fuel))
        landed_banner = Banner(
            landed_message,
            fonts.banschrift)
        landed_banner.render_image()
        m_width = landed_banner.image.get_width()
        landed_banner.x = int(screen.get_width() * 0.5 - m_width * 0.5)
        landed_banner.y = int(screen.get_height() * 0.3)
        decals.active_messages.append(landed_banner)

    if state.lander.crashed is True:
        crashed_message = ("You have crashed!")
        crashed_banner = Banner(
            crashed_message, fonts.banschrift, colors.red)
        crashed_banner.render_image()
        m_width = crashed_banner.image.get_width()
        crashed_banner.x = int(screen.get_width() * 0.5 - m_width * 0.5)
        crashed_banner.y = int(screen.get_height() * 0.4)
        decals.active_messages.append(crashed_banner)
    pg.display.flip()
    clock.tick(60)

