# Import the requests library
from urllib import response
import requests


class TAAPI:
    def __init__(self):
        pass

    def get_rsi(secret):
        endpoint = "https://api.taapi.io/rsi"
        parameters = {
            "secret": secret,
            "exchange": "binance",
            "symbol": "BTC/USDT",
            "interval": "15m",
            "backtrack": "1",
            "period": "10",
        }
        response = requests.get(url=endpoint, params=parameters)
        result = response.json()
        # print(result)
        return result['value']

    def get_ema(secret):
        endpoint = "https://api.taapi.io/ema"
        parameters = {
            "secret": secret,
            "exchange": "binance",
            "symbol": "BTC/USDT",
            "interval": "15m",
            "backtrack": "1",
            "period": "50",

        }
        response = requests.get(url=endpoint, params=parameters)
        result = response.json()
        # print(result)
        return result['value']

    def get_atr(secret, up_flag):
        endpoint = "https://api.taapi.io/atr"
        ticker = "BTCDOWN/USDT"
        if up_flag:
            ticker = "BTCUP/USDT"
        parameters = {
            "secret": secret,
            "exchange": "binance",
            "symbol": ticker,
            "interval": "15m",
            "period": "50",

        }
        response = requests.get(url=endpoint, params=parameters)
        result = response.json()
        # print(result)
        return result['value']

    def bulk_request_indicators(secret):
        ret = []
        endpoint = "https://api.taapi.io/bulk"
        parameters = {
            "secret": secret,
            "construct": {
                "exchange": "binance",
                "symbol": "BTC/USDT",
                "interval": "15m",
                "backtracks": "5",
                "indicators": [
                    {
                        "indicator": "rsi",
                        "period": "10",
                    },
                    {
                        "indicator": "ema",
                        "period": "50",
                    }
                ]
            }
        }
        response = requests.post(url=endpoint, json=parameters)
        result = response.json()
        print(result)
        # rsi 10
        ret.append(result['data'][0]['result']['value'])
        # ema 50
        ret.append(result['data'][1]['result']['value'])
        return ret

    def candle_request(secret):
        ret = []
        endpoint = "https://api.taapi.io/candles"
        parameters = {
            "secret": secret,
            "exchange": "binance",
            "symbol": "BTC/USDT",
            "interval": "15m",
            "backtracks": "1",
            "chart": "candles",
        }
        response = requests.get(url=endpoint, params=parameters)
        result = response.json()
        # print(result)
        # backtrack 1 candle close
        ret.append(result[0][12]['close'])
        # backtrack 1 candle low
        ret.append(result[0][12]['low'])
        # backtrack 1 candle high
        ret.append(result[0][12]['high'])
        # backtrack 2 candle close
        ret.append(result[0][11]['close'])
        # current candle close
        ret.append(result[0][13]['close'])
        return ret

    def margin_candle_request(secret, up_flag):
        ret = []
        ticker = "BTCDOWN/USDT"
        if up_flag:
            ticker = "BTCUP/USDT"
        endpoint = "https://api.taapi.io/candles"
        parameters = {
            "secret": secret,
            "exchange": "binance",
            "symbol": ticker,
            "interval": "15m",
            "backtracks": "1",
            "chart": "candles",
        }
        response = requests.get(url=endpoint, params=parameters)
        result = response.json()
        # print(result)
        # backtrack 1 candle close
        ret.append(result[0][12]['close'])
        # backtrack 1 candle low
        ret.append(result[0][12]['low'])
        return ret
