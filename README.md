# wpm-applet

This applet shows the number of keys you are actually typing.
It's meant to encourage those with RSI to take it easy.

## Setup

```
$ sudo apt install python2.7 python-gi gir1.2-gtk-3.0 xinput libgtk-3-dev
$ ./applet.py
```

## Sample output

Rates are characters per minute (divide by five for wpm).
Total counts are in parentheses.

```
MAX 246.0/min,   0.0/min @10s (   0),   23.0/min @1m (  23),   31.0/min @5m ( 155),   10.3/min @15m ( 155),    2.6/min @1h ( 155),
MAX 246.0/min,   6.0/min @10s (   1),   24.0/min @1m (  24),   31.2/min @5m ( 156),   10.4/min @15m ( 156),    2.6/min @1h ( 156),
MAX 246.0/min,  36.0/min @10s (   6),   27.0/min @1m (  27),   32.2/min @5m ( 161),   10.7/min @15m ( 161),    2.7/min @1h ( 161),
MAX 246.0/min, 222.0/min @10s (  37),   58.0/min @1m (  58),   38.4/min @5m ( 192),   12.8/min @15m ( 192),    3.2/min @1h ( 192),
MAX 462.0/min, 462.0/min @10s (  77),   98.0/min @1m (  98),   46.4/min @5m ( 232),   15.5/min @15m ( 232),    3.9/min @1h ( 232),
MAX 696.0/min, 696.0/min @10s ( 116),  133.0/min @1m ( 133),   54.2/min @5m ( 271),   18.1/min @15m ( 271),    4.5/min @1h ( 271),
MAX 930.0/min, 930.0/min @10s ( 155),  171.0/min @1m ( 171),   62.2/min @5m ( 311),   20.7/min @15m ( 311),    5.2/min @1h ( 311),
MAX 978.0/min, 978.0/min @10s ( 163),  184.0/min @1m ( 184),   65.0/min @5m ( 325),   21.7/min @15m ( 325),    5.4/min @1h ( 325),
MAX 978.0/min, 774.0/min @10s ( 129),  184.0/min @1m ( 184),   65.0/min @5m ( 325),   21.7/min @15m ( 325),    5.4/min @1h ( 325),
MAX 978.0/min, 546.0/min @10s (  91),  186.0/min @1m ( 186),   65.4/min @5m ( 327),   21.8/min @15m ( 327),    5.5/min @1h ( 327),
MAX 978.0/min, 342.0/min @10s (  57),  192.0/min @1m ( 192),   66.6/min @5m ( 333),   22.2/min @15m ( 333),    5.5/min @1h ( 333),
MAX 978.0/min, 126.0/min @10s (  21),  195.0/min @1m ( 195),   67.2/min @5m ( 336),   22.4/min @15m ( 336),    5.6/min @1h ( 336),
MAX 978.0/min, 252.0/min @10s (  42),  226.0/min @1m ( 226),   73.4/min @5m ( 367),   24.5/min @15m ( 367),    6.1/min @1h ( 367),
MAX 978.0/min, 342.0/min @10s (  57),  241.0/min @1m ( 241),   76.2/min @5m ( 381),   25.5/min @15m ( 382),    6.4/min @1h ( 382),
MAX 978.0/min, 378.0/min @10s (  63),  249.0/min @1m ( 249),   77.8/min @5m ( 389),   26.0/min @15m ( 390),    6.5/min @1h ( 390),
MAX 978.0/min, 366.0/min @10s (  61),  254.0/min @1m ( 254),   78.8/min @5m ( 394),   26.3/min @15m ( 395),    6.6/min @1h ( 395),
MAX 978.0/min, 390.0/min @10s (  65),  263.0/min @1m ( 263),   80.6/min @5m ( 403),   26.9/min @15m ( 404),    6.7/min @1h ( 404),
MAX 978.0/min, 222.0/min @10s (  37),  257.0/min @1m ( 257),   80.6/min @5m ( 403),   26.9/min @15m ( 404),    6.7/min @1h ( 404),
MAX 978.0/min, 108.0/min @10s (  18),  257.0/min @1m ( 257),   80.6/min @5m ( 403),   26.9/min @15m ( 404),    6.7/min @1h ( 404),
MAX 978.0/min,  78.0/min @10s (  13),  256.0/min @1m ( 256),   80.6/min @5m ( 403),   26.9/min @15m ( 404),    6.7/min @1h ( 404),
MAX 978.0/min,  54.0/min @10s (   9),  249.0/min @1m ( 249),   80.6/min @5m ( 403),   26.9/min @15m ( 404),    6.7/min @1h ( 404),
MAX 978.0/min,   0.0/min @10s (   0),  249.0/min @1m ( 249),   80.6/min @5m ( 403),   26.9/min @15m ( 404),    6.7/min @1h ( 404),
```
