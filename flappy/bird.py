import logging


class Bird(object):
    """Just a flappy bird itself.
    """
    BASE_RADIUS = 24

    def __init__(self, x, y) -> None:
        self.x: float = x
        self.y: float = y
        self.radius = self.BASE_RADIUS
        self.is_dead = False

        self.vy: float = 0
        self.wing_strength: float = -1.12
        logging.info(f'Bird created: ({self.x, self.y, self.vy})')

    def up(self, gravity=0):
        self.y += self.vy
        self.vy += gravity

    def wave_up(self):
        self.vy += self.wing_strength
        logging.info('wave up...')

    def die(self, top=0, bottom=200):
        if self.y < top:
            self.is_dead = True
        if self.y > bottom:
            self.is_dead = True
        # logging.info('Bird is dead? ' + str(self.is_dead))
        return self.is_dead
