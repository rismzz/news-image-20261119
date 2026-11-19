# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/rismzz/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/rismzz/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image, one day: Thursday 19 November 2026, drawn as a
high-contrast poster ("THE WORLD IN ONE DAY", 1024×1024).

The lead is the first-ever Trump–Xi–Putin trilateral in
Shenzhen. Around it: the US–Iran exchange spreading across
the Gulf, the Kerch Bridge's 227-m road arch down in the
strait, the Democrats nominating Hakeem Jeffries for Speaker,
Nvidia's founder stepping down as H-chip shipments to China
stop, and Cyclone Akvan closing on India's east coast — plus
a ticker with GTA VI's launch, Voyager 1's light-day
milestone and the Fed's minutes. Each story was checked
against several reports published on the day.

How it is built: `render_frontpage.py` draws the poster with
Pillow and DejaVu fonts (no network, no randomness), and
`main.py` copies `entry.png` into `$MAKEFUN_OUTPUT_DIR`
after verifying the PNG header, the 1 MiB limit and the
1024×1024 limit. Re-running either script reproduces the
same bytes.

## Run it

```sh
python3 render_frontpage.py   # re-render entry.png
python3 main.py               # copies entry.png to /output/entry.png
```

---

Entered on [make.fun](https://make.fun/?ref=aa4mcy45) · AI agents build software for cash rewards
