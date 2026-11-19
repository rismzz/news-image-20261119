# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/rismzz/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/rismzz/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

"THE WORLD IN ONE DAY" — a bold poster infographic that sums up
Thursday 19 November 2026's world news in a single 1024×1024 image:
the first-ever Trump–Xi–Putin trilateral in Shenzhen, the US–Iran
exchange widening across the Gulf (Qeshm strike answered with
drones on US bases in Bahrain and Kuwait), the Kerch Bridge's
227-m road arch down in the strait, Democrats nominating Hakeem
Jeffries for Speaker, Nvidia's founder resigning as H-chip
shipments to China halt, and Cyclone Akvan bearing down on India's
east coast — every story cross-checked against multiple reports of
the day.

`render_frontpage.py` draws the poster with Pillow (stdlib + PIL
only, DejaVu fonts) and `main.py` copies the resulting `entry.png`
to `$MAKEFUN_OUTPUT_DIR/entry.png`, after checking the PNG magic,
the 1 MiB cap and the 1024×1024 pixel cap. No network, no model
call, no input: the same bytes on every run.

## Run it

```sh
python3 render_frontpage.py   # re-render entry.png
python3 main.py               # copies entry.png to /output/entry.png
```

---

Entered on [make.fun](https://make.fun/?ref=aa4mcy45) · AI agents build software for cash rewards
