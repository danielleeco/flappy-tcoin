from datetime import datetime
import logging

from tinkoff.invest import Client, CandleInterval, Quotation

from flappy.config import Config


def quot2float(x: Quotation):
    return x.units + float('.' + str(x.nano))


def pre_defined_data():
    return [
        (123.33, 126.0), (123.21, 124.5), (123.3, 124.59), (123.8, 124.7),
        (124.3, 125.4), (125.13, 126.6), (125.57, 126.86), (125.3, 126.7),
        (124.63, 125.5), (125.0, 125.72), (124.3, 125.14), (124.39, 125.3),
        (124.5, 125.3), (125.6, 126.0), (125.3, 125.63), (125.15, 125.48),
        (125.8, 125.8), (125.32, 125.8), (125.1, 125.7), (124.15, 125.41),
        (124.18, 125.8), (124.8, 126.49), (125.1, 125.72), (124.88, 125.27),
        (124.8, 125.5), (125.1, 125.47), (125.13, 125.75), (125.1, 125.8),
        (125.1, 125.6), (125.15, 125.91), (125.5, 125.86), (125.33, 125.72),
        (125.38, 125.79), (125.5, 125.77), (125.32, 125.62), (125.6, 125.6),
    ]


def get_candles(
    ticker: str = None,
    figi: str = 'BBG004730N88',
    _from: datetime = None,
    _to: datetime = None,
    config: Config = None
):
    if config is None:
        config = Config()
    if config.TOKEN == 'REPLACE_ME':
        logging.warning('The token is not defined. Check `config.env`. Predefined data loaded.')
        return pre_defined_data()

    logging.info(f'fetch candles... {figi, _from, _to}')
    candles = []
    with Client(config.TOKEN) as client:
        for candle in client.get_all_candles(
            figi=figi,
            from_=_from,
            to=_to,
            interval=CandleInterval.CANDLE_INTERVAL_15_MIN
        ):
            # fix tinkoff-invest feature/bug
            a, b = quot2float(candle.low), quot2float(candle.high)
            a, b = min(a, b), max(a, b)
            candles.append(
                (
                    a,
                    b,
                )
            )
    logging.info(f'Candles: {candles}')
    return candles
