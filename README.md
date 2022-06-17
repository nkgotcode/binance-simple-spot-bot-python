# Binance Public API Connector Python

[![PyPI version](https://img.shields.io/pypi/v/binance-connector)](https://pypi.python.org/pypi/binance-connector)
[![Python version](https://img.shields.io/pypi/pyversions/binance-connector)](https://www.python.org/downloads/)
[![Documentation](https://img.shields.io/badge/docs-latest-blue)](https://binance-connector.readthedocs.io/en/stable/)
[![Code Style](https://img.shields.io/badge/code_style-black-black)](https://black.readthedocs.io/en/stable/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is a lightweight library that works as a connector to [Binance public API](https://github.com/binance/binance-spot-api-docs)

- Supported APIs:
  - `/api/*`
  - `/sapi/*`
  - Spot Websocket Market Stream
  - Spot User Data Stream
- Inclusion of test cases and examples
- Customizable base URL, request timeout and HTTP proxy
- Response metadata can be displayed

Spot Bot is located inside the binance folder. It utilizes Binance Spot API to create market buy orders and OCO orders according to EMA, RSI, and ATR indicators from taapi API. Currently support analyzing BTC/USDT ticker, and then buying BTCUP or BTCDOWN according to the technical analysis.

## Installation

```bash
pip install binance-connector
```

## Documentation

[https://binance-connector.readthedocs.io](https://binance-connector.readthedocs.io)

### Heartbeat

Once connected, the websocket server sends a ping frame every 3 minutes and requires a response pong frame back within
a 10 minutes period. This package handles the pong responses automatically.

### Testnet

```python
from binance.websocket.spot.websocket_client import SpotWebsocketClient as WebsocketClient

ws_client = WebsocketClient(stream_url='wss://testnet.binance.vision')
```

## Test Case

```python
# In case packages are not installed yet
pip install -r requirements/requirements-test.txt

pytest
```

## Limitation

Futures and Vanilla Options APIs are not supported:

- `/fapi/*`
- `/dapi/*`
- `/vapi/*`
- Associated Websocket Market and User Data Streams

## Contributing

Contributions are welcome.<br/>
If you've found a bug within this project, please open an issue to discuss what you would like to change.<br/>
If it's an issue with the API, please open a topic at [Binance Developer Community](https://dev.binance.vision)
