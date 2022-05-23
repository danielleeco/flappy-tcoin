from distutils.command import config
import os
from dotenv import load_dotenv

load_dotenv('./config.env')


class Config(object):
    def __init__(self) -> None:
        # tinkoff part of config
        self.TOKEN: str = os.getenv('TINKOFF_TOKEN')
        self.IS_SANDBOX: bool = True if os.getenv('IS_TINKOFF_SANDBOX', 'False').lower() == 'true' else False

        self.BIRD_SPEED: float = float(os.getenv('BIRD_SPEED', 1.2))
        self.WING_STRENGTH: float = float(os.getenv('WING_STRENGTH', 1.12))
        self.PIPE_WIDTH: int = 64
        self.PIPE_DISTANCE: int = 128 + 64


config = Config()  # noqa: F811
