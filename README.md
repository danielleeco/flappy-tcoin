# flappy tinkbird

Just some mini game for tinkoff contest.

Flappy coin flying beetween historic stocks candles

![image](https://user-images.githubusercontent.com/27200843/169881953-da0cbfaa-4507-477c-8152-4085acb488df.png)

<details>
    <summary>Gameplay</summary>

![tcoin](https://user-images.githubusercontent.com/27200843/169881636-a2a4e8c9-9bef-4c8b-8ddd-c68017c8883a.gif)
</details>

## Installation

```bash
pip install -r requirements.txt
```

## Run

Place your tinkoff token to `config.env` file, instead of `REPLACE_ME`

```bash
python tflappy.py
python tflappy.py --figi BBG0013HGFT4
python tflappy.py --figi BBG000B9XRY4 --date 2021-01-21
python tflappy.py --figi BBG000N9MNX3 --date 2021-02-22
```


### Some interesting figi's
- `BBG0013HGFT4` - Доллар США
- `BBG000N9MNX3` - `TSLA`/Tesla Motors
- `BBG000B9XRY4` - `AAPL`/Apple
