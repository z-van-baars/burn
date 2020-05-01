import art
import pygame as pg


def display_update(screen, clock, state):
    large_font = pg.font.SysFont('Banschrift Light Semicondensed', 24, False, False)
    screen.fill((20, 20, 20))

    screen.blit(state.ground.image, [0, state.screen_height - state.ground.height])
    state.lander_shadow.redraw_image(state.screen_height, state.lander.x, state.lander.y)
    screen.blit(state.lander_shadow.image, [state.lander_shadow.x, state.lander_shadow.y])
    screen.blit(state.lander.image, [state.lander.x, state.lander.y])
    for particle in state.particles:
        screen.blit(particle.image, [particle.x, particle.y])
    # Decals and UI
    altitude_stamp = large_font.render("Altitude: {0}".format(round(state.screen_height - 130 - state.lander.y), 3), True, (255, 255, 255))
    v_color = (255, 255, 255)
    if 3.5 >= state.lander.y_velocity > 2:
        v_color = (255, 200, 10)
    elif state.lander.y_velocity > 3.5:
        v_color = (225, 10, 10)
    f_color = (255, 255, 255)
    if 25 < state.lander.fuel <= 50:
        f_color = (255, 200, 10)
    elif state.lander.fuel <= 25:
        f_color = (225, 10, 10)
    velocity_stamp = large_font.render(
        "Velocity: {0}".format(-state.lander.y_velocity),
        True,
        v_color)
    fuel_stamp = large_font.render(
        "Fuel: [ {0} / 500 ]".format(state.lander.fuel),
        True,
        f_color)

    fuel_bar = pg.Surface([40, max(1, int(200 * (state.lander.fuel / 100)))])
    if state.lander.fuel > 0:
        fuel_bar.fill((225, 10, 10))

    screen.blit(fuel_bar, [state.screen_width - 50, 110 + (200 - fuel_bar.get_height())])
    screen.blit(art.fuel_gauge_overlay, [state.screen_width - 55, 100])

    # screen.blit(art.throttle_gauge_overlay, [state.screen_width - 55, 300])

    screen.blit(altitude_stamp, [4, 10])
    screen.blit(velocity_stamp, [4, 30])
    screen.blit(fuel_stamp, [4, 50])
    if state.lander.landed == True:
        landed_stamp = large_font.render("You landed with [ {0} / 500 ] fuel remaining!".format(state.lander.fuel), True, (255, 255, 255))
        m_width = landed_stamp.get_width()
        screen.blit(landed_stamp, [int(screen.get_width() * 0.5 - m_width * 0.5), int(screen.get_height() * 0.3)])
    if state.lander.crashed == True:
        crashed_stamp = large_font.render(
            "You have crashed!", True, (245, 10, 10))
        m_width = crashed_stamp.get_width()
        screen.blit(crashed_stamp, [int(screen.get_width() * 0.5 - m_width * 0.5), int(screen.get_height() * 0.3)])

    pg.display.flip()
    clock.tick(60)

