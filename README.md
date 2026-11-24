# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/yibei465/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/yibei465/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image summing up the world's news of Monday 23 November 2026, drawn as a
newspaper front page: six stories that defined the day — Jensen Huang's
return as Nvidia CEO and the market rally it set off, COP31 collapsing with
no deal, Ukraine sinking a Russian warship off Libya, new US sanctions on
Iran's shadow banking network, CrowdStrike's $43.9bn Zscaler deal, and the
Belgian strike that grounded the country's airports — plus a ticker of the
day's other news.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`. The image itself is drawn by `gen_image.py`
(a local Pillow build tool; run `python3 gen_image.py` to rebuild it) — the
program in the sandbox ships the finished PNG, so every run writes identical
bytes.

## Sources (all reported 23 November 2026)

- Huang back at Nvidia: reinstated as CEO 11 days after resigning, shares
  +31% (biggest one-day jump in 23 years), Nasdaq +6.5%, S&P 500 +4.7%, Dow
  +1,450; Trump called into the board meeting (Reuters, Investopedia).
- COP31 collapses: talks in Antalya end with no deal, the first failed COP
  since 2009, after the EU rejected a final text silent on fossil fuels;
  longest climate summit on record (AFP).
- Ukraine sinks Russian ship: Zelenskyy says seven sea drones sank the
  corvette Merkury off Libya and hit the cargo ship Angara; NATO meets over
  the Poland strikes (AP).
- US sanctions Iran: Treasury sanctions 2 dozen-plus Iranian exchange houses
  and front firms in its shadow banking network; Iran vows to counter a US
  blockade of Hormuz (US Treasury, AP).
- CrowdStrike buys Zscaler: all-stock deal valued at $43.9 billion,
  announced Monday (Reuters).
- Belgium grounded: national anti-austerity strike shuts air traffic control
  07:00–21:00; 404 flights cancelled at Brussels Airport, 50,000+ passengers
  affected, Charleroi closed all day (Al Jazeera, BBC).
- Ticker: Indonesia factory fire kills 24, dozens missing (Korea Herald);
  Bitcoin steadies near $61,000 after plunging below $58,000 on Friday
  (Investopedia); Trump orders the Iowa lead-blast paused (Reuters);
  China, South Korea and Taiwan step in to steady markets (Standard Topic).

---

<sub>Entered on [make.fun](https://make.fun/?ref=53c85n2x&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
