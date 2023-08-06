League.py
-

[![Documentation Status](https://readthedocs.org/projects/leaguepy/badge/?version=latest)](http://leaguepy.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/league.py.svg)](https://pypi.python.org/pypi/league.py/)
[![PyPI](https://img.shields.io/pypi/pyversions/league.py.svg)](https://pypi.python.org/pypi/league.py/)

### An Asyncio league of legends API wrapper made for python 3.4.2+


Built for Riot's new **V3** endpoints.

# Requirements

- Python 3.4.2+
- `aiohttp` library


# Installation
```
python3 -m pip install -U git+https://github.com/datmellow/League.py
```


# Example

```python
import league
import asyncio

# Python 3.4
@asyncio.coroutine
def test_method():
    client = league.Client(api_key="Token")
    yield from client.cache_setup() # Optional
    summoner = yield from client.get_summoner(summoner_name="RiotPhreak")
    print(summoner)

# Python 3.5+
async def test_method():
    client = league.Client(api_key="Token")
    await client.cache_setup() # Optional
    summoner = await client.get_summoner(summoner_name="RiotPhreak")
    print(summoner)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_method())
```
