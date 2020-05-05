import art


class Effect(object):
    def __init__(self, x, y, animation, looping=False, frame_duration=1):
        self.active = True
        self.x = x
        self.y = y
        # start the animation over if we reach the end of the sequence
        self.looping = looping
        # animation is a list of image files
        self.animation = animation
        self.frame = 0
        self.active_frame = animation[self.frame]
        self.frame_duration = frame_duration
        self.frame_count = 0

    def play(self):
        self.frame_count += 1
        if self.frame_count > self.frame_duration:
            self.frame_count = 0
            self.frame += 1

            if self.frame >= len(self.animation):
                if self.looping:
                    self.frame = 0
                else:
                    self.active = False
                    return
            self.active_frame = self.animation[self.frame]

    def loop_condition(self):
        pass


class Explosion(Effect):
    def __init__(self, x, y):
        super().__init__(x, y, art.explosion, False, 2)
