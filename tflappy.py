import logging
from datetime import date, timedelta

import click

from flappy.pygame_adapter import run_game


@click.command()
@click.option("--figi", type=str, default='BBG004730N88')
@click.option('--date', type=click.DateTime(formats=["%Y-%m-%d"]),
              default=str(date.today()))
# @click.option('--date-end', type=click.DateTime(formats=["%Y-%m-%d"]),
#               default=str(date.today() + timedelta(1)))
def main(figi, date):
    date_start = date
    date_end = date_start + timedelta(1)
    run_game(figi=figi, _from=date_start, _to=date_end)


if __name__ == '__main__':
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s [%(module)s.%(funcName)s:%(lineno)d] %(message)s"
    )
    # logging.getLogger().setLevel(logging.INFO)
    logging.getLogger().setLevel(logging.WARNING)
    logging.info('Flappy bird running...')
    main()
