import logging


class PipePair(object):
    def __init__(self, x, width, height_up, height_down) -> None:
        self.x = x
        self.width = width
        self.height_up = height_up
        self.height_down = height_down
        self.speed = -1.2

        logging.info(f'Pipe created: ({self.width, self.x, self.height_up, self.height_down})')

    def move(self):
        self.x += self.speed
