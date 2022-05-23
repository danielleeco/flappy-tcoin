import logging
import datetime
import operator
from typing import List

import pygame


from .bird import Bird
from .pipes import PipePair
from .tinkvest import get_candles

FPS = 60
WIN_WIDTH = 640
WIN_HEIGHT = 480


def load_image(filepath):
    image = pygame.image.load(filepath)
    image.convert()
    return image


class GBird(pygame.sprite.Sprite, Bird):
    def __init__(self, x, y) -> None:
        super(GBird, self).__init__()
        Bird.__init__(self, x, y)
        self._bird_image = load_image('./data/tcoin48.png')
        self._mask_bird_image = pygame.mask.from_surface(self._bird_image)

    @property
    def image(self):
        return self._bird_image

    @property
    def mask(self):
        return self._mask_bird_image

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)

    def collides_with(self, pipe):
        return pygame.sprite.collide_mask(self, pipe)

    def die(self, top=0, bottom=200, pipe=None):
        Bird.die(self, top, bottom)
        if pipe is None:
            return self.is_dead
        if self.collides_with(pipe):
            self.is_dead = True
        return self.is_dead


class GPipePair(pygame.sprite.Sprite, PipePair):
    def __init__(self, x, width, height_up, height_down, hd) -> None:
        super(GPipePair, self).__init__()
        PipePair.__init__(self, x, width, height_up, height_down)
        self.hd = hd
        self.image = pygame.Surface((self.width, WIN_HEIGHT), pygame.SRCALPHA)
        self.image.convert()
        self.image.fill((0, 0, 0, 0))
        pipe_color = (54, 216, 142)
        pipe_border_color = (0, 115, 62)
        self.image.fill(pipe_border_color, pygame.Rect(0, 0, width, self.height_up * hd - Bird.BASE_RADIUS * 1.5))
        self.image.fill(pipe_color, pygame.Rect(5, 0, -10 + width, -5 + self.height_up * hd - Bird.BASE_RADIUS * 1.5))

        self.image.fill(pipe_border_color, pygame.Rect(0,
                                                       WIN_HEIGHT - (height_down * hd - Bird.BASE_RADIUS * 1.5),
                                                       self.width,
                                                       height_down * hd - Bird.BASE_RADIUS * 1.5))
        self.image.fill(pipe_color, pygame.Rect(5,
                                                5 + WIN_HEIGHT - (height_down * hd - Bird.BASE_RADIUS * 1.5),
                                                -10 + self.width,
                                                height_down * hd - Bird.BASE_RADIUS * 1.5))
        self._mask_pipe_image = pygame.mask.from_surface(self.image)

    @property
    def mask(self):
        return self._mask_pipe_image

    @property
    def rect(self):
        return pygame.Rect(self.x, 0, self.width, WIN_HEIGHT)


def create_pipes(*args, config=None, **kwargs):
    logging.info(f'create_pipes kwargs: {kwargs}')
    candles = get_candles(
        figi=kwargs.get('figi', 'BBG004730N88'),
        _from=kwargs.get('_from', datetime.datetime(2022, 5, 19)),
        _to=kwargs.get('_to', datetime.datetime(2022, 5, 20)),
    )
    if len(candles) == 0:
        logging.error('There are no candles for this period. Try another')
        exit(404)
    min_low = min(candles, key=operator.itemgetter(0))[0]
    max_high = max(candles, key=operator.itemgetter(1))[1]
    logging.info(f'min_low: {min_low}')
    logging.info(f'max_high: {max_high}')
    max_delta = max_high - min_low
    hd = WIN_HEIGHT / max_delta

    pipes: List[GPipePair] = []

    start_pipe_pos_x = 256 + 128
    pipe_width = 64
    default_pipe_distance = 128 + pipe_width
    for i, candle in enumerate(candles):
        pipes.append(
            GPipePair(
                start_pipe_pos_x + i * default_pipe_distance,
                width=pipe_width,
                height_up=max_high-candle[1],
                height_down=candle[0]-min_low,
                hd=hd
            )
        )
    return pipes


def run_game(*args, **kwargs):
    logging.info('starting...')
    logging.info(f'run_game kwargs: {kwargs}')
    pygame.init()

    display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Flappy tinkbird')
    image_background = load_image('./data/back.png')

    clock = pygame.time.Clock()
    score_font = pygame.font.SysFont(None, 32, bold=True)

    start_clock = datetime.datetime.now()
    last_clock = start_clock
    score = 0

    bird = GBird(42, 42)
    pipes = create_pipes(*args, **kwargs)

    gravity = 0.02
    running = True
    the_end_of_pipes = False
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
               event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                break
            elif event.type == pygame.KEYDOWN and (event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w)):
                bird.wave_up()

        display_surface.blit(image_background, (0, 0))

        bird.up(gravity)
        bird.die(0, WIN_HEIGHT)
        display_surface.blit(bird.image, bird.rect)
        for pipe in pipes:
            if not bird.is_dead:
                pipe.move()
                bird.die(0, WIN_HEIGHT, pipe)
            display_surface.blit(pipe.image, pipe.rect)

        if not bird.is_dead and not the_end_of_pipes:
            last_clock = datetime.datetime.now()

        if pipes[-1].x + pipes[-1].width < bird.x:
            the_end_of_pipes = True

        if bird.is_dead or the_end_of_pipes:
            score = last_clock - start_clock
            game_over_background = load_image('./data/game_over.png')
            gravity = 0
            bird.vy = 0
            display_surface.blit(game_over_background, (10, 30))
            score_surface = score_font.render('Score: ' + str(int(score.total_seconds())), True, (255, 255, 255))
            display_surface.blit(score_surface, (250, 320))

        pygame.display.flip()
        pygame.display.update()
