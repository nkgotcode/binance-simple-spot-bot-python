#!/usr/bin/env python
import logging
import time
import taapi
import intro_screen
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
from binance.error import ClientError

# config_logging(logging, logging.DEBUG)
logging.basicConfig(filename="console.txt", level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    filemode='a')
# logging = logging.getLogging()
# logging.setLevel(logging.DEBUG)

# get user Binance API key and secret
key, secret = intro_screen.Intro.get_binance_api()
# get TAAPI secret
taapi_secret = intro_screen.Intro.get_taapi_api()
# log in Spot account according to API key and secret
spot_client = Client(key, secret)

rsi_10 = None
ema_50 = None
atr_50 = None
prev1_close = None
prev1_low = None
prev1_high = None
prev2_close = None
count = 0
ticket = None

while True:
    # indicators_arr = taapi.TAAPI.bulk_request_indicators(taapi_secret)
    rsi_10 = taapi.TAAPI.get_rsi(taapi_secret)
    ema_50 = taapi.TAAPI.get_ema(taapi_secret)
    previous_candle = taapi.TAAPI.candle_request(taapi_secret)
    prev1_close = previous_candle[0]
    prev1_low = previous_candle[1]
    prev1_high = previous_candle[2]
    prev2_close = previous_candle[3]
    # current_close = spot_client.klines("BTCUSDT", "15m", limit=3)[2][4]
    print("RSI 10: " + str(rsi_10))
    logging.info("RSI 10: %s", str(rsi_10))
    print("EMA 50: " + str(ema_50))
    logging.info("EMA 50: %s", str(ema_50))
    # print(type(previous_candle[4]))
    # print("ATR 50 BTCDOWN: " + "{:.6f}".format(atr_50))
    print("Backtrack 1 candle close: " + str(prev1_close))
    logging.info("Backtrack 1 candle close: %s", str(prev1_close))
    print("Backtrack 1 candle low: " + str(prev1_low))
    logging.info("Backtrack 1 candle low: %s", str(prev1_low))
    print("Backtrack 1 candle high: " + str(prev1_high))
    logging.info("Backtrack 1 candle high: %s", str(prev1_high))
    print("Backtrack 2 candle close: " + str(prev2_close))
    logging.info("Backtrack 2 candle close: %s", str(prev2_close))
    print("Current candle price is: " + str(previous_candle[4]))
    logging.info("Current candle price is: %s", str(previous_candle[4]))
    # print("SL price should be: " + str(sl))
    # print("Current candle close: " + str(current_close))

    # FOR BTCUP
    if prev2_close < ema_50 and prev1_close > ema_50:
        while True:
            print("waiting for the next candle to buy BTCUP")
            logging.info("waiting for the next candle to buy BTCUP")
            # wait to print next candle
            time.sleep(900 - time.time() % 900)
            # get next candle information
            previous_candle = taapi.TAAPI.candle_request(taapi_secret)
            # get current candle price
            current_price = previous_candle[4]
            rsi_10 = taapi.TAAPI.get_rsi(taapi_secret)
            ema_50 = taapi.TAAPI.get_ema(taapi_secret)
            atr_50 = taapi.TAAPI.get_atr(taapi_secret, True)
            print("validating additional conditions to buy BTCUP")
            logging.info("validating additional conditions to buy BTCUP")
            print("RSI 10: " + str(rsi_10))
            logging.info("RSI 10: %s", str(rsi_10))
            print("EMA 50: " + str(ema_50))
            logging.info("EMA 50: %s", str(ema_50))
            print("ATR 50: " + str(atr_50))
            logging.info("ATR 50: %s", str(atr_50))

            if current_price < ema_50:
                print("invalidating.. not buying BTCUP")
                logging.info("invalidating.. not buying BTCUP")
                break

            elif current_price > ema_50 and rsi_10 > 70:
                print("buying BTCUP")
                logging.info("buying BTCUP")
                available_usdt_balances = next((x for x in spot_client.coin_info() if x["coin"] == "USDT"))['free']
                print("Current USDT Balances: " + available_usdt_balances)
                logging.info("Current USDT Balances: %s", str(available_usdt_balances))
                usdt_balances = float(available_usdt_balances)
                usdt_balances = int(usdt_balances)
                entry_price = None
                ori_quantity = None
                commissions = 0
                params = {
                    "symbol": "BTCUPUSDT",
                    "side": "BUY",
                    "type": "MARKET",
                    "quoteOrderQty": str(usdt_balances * 60 / 100),
                    "newClientOrderId": str(count)
                }

                try:
                    response = spot_client.new_order(**params)
                    logging.info(response)
                    print("Created new buy order!!!!!")
                    logging.info("Created new buy order!!!!!")
                    entry_price = float(response["fills"][0]["price"])
                    ori_quantity = float(response["fills"][0]["origQty"])
                    for i in response['fills']:
                        commissions += float(i["commission"])
                except ClientError as error:
                    logging.error(
                        "Found error. status: {}, error code: {}, error message: {}".format(
                            error.status_code, error.error_code, error.error_message
                        )
                    )

                previous_margin_candle = taapi.TAAPI.margin_candle_request(taapi_secret, True)
                prev1_margin_close = previous_margin_candle[0]
                prev1_margin_low = previous_margin_candle[1]
                sl_margin = prev1_margin_low - atr_50
                print("Backtrack 1 margin candle close: " + str(prev1_margin_close))
                logging.info("Backtrack 1 margin candle close: %s", str(prev1_margin_close))
                print("Backtrack 1 margin candle low: " + str(prev1_margin_low))
                logging.info("Backtrack 1 margin candle low: %s", str(prev1_margin_low))
                print("SL price should be: " + str(sl_margin))
                logging.info("SL price should be: %s", str(sl_margin))

                params = {
                    "symbol": "BTCUPUSDT",
                    "side": "SELL",
                    "quantity": "{:.2f}".format(ori_quantity - commissions),
                    "price": "{:.2f}".format(((prev1_margin_close - prev1_margin_low + atr_50) * 1.4) + prev1_margin_close),
                    "stopPrice": "{:.2f}".format(sl_margin),
                    "stopLimitPrice": "{:.2f}".format(sl_margin - atr_50),
                    "stopLimitTimeInForce": "GTC",
                }

                try:
                    response = spot_client.new_oco_order(**params)
                    logging.info(response)
                    print("Created OCO order!!!!!")
                    logging.info("Created OCO order!!!!!")
                except ClientError as error:
                    logging.error(
                        "Found error. status: {}, error code: {}, error message: {}".format(
                            error.status_code, error.error_code, error.error_message
                        )
                    )
                break

    # FOR BTCDOWN
    if prev2_close > ema_50 and prev1_close < ema_50:
        while True:
            print("waiting for the next candle to buy BTCDOWN")
            logging.info("waiting for the next candle to buy BTCDOWN")
            # wait to print next candle
            time.sleep(900 - time.time() % 900)
            # get next candle information
            previous_candle = taapi.TAAPI.candle_request(taapi_secret)
            # get current candle price
            current_price = previous_candle[4]
            rsi_10 = taapi.TAAPI.get_rsi(taapi_secret)
            ema_50 = taapi.TAAPI.get_ema(taapi_secret)
            atr_50 = taapi.TAAPI.get_atr(taapi_secret, False)
            print("validating additional conditions to buy BTCDOWN")
            logging.info("validating additional conditions to buy BTCDOWN")
            print("RSI 10: " + str(rsi_10))
            logging.info("RSI 10: %s", str(rsi_10))
            print("EMA 50: " + str(ema_50))
            logging.info("EMA 50: %s", str(ema_50))
            print("ATR 50: " + str(atr_50))
            logging.info("ATR 50: %s", str(atr_50))

            if current_price > ema_50:
                print("invalidating.. not buying BTCDOWN")
                logging.info("invalidating.. not buying BTCDOWN")
                break

            elif current_price < ema_50 and rsi_10 < 30:
                print("buying BTCDOWN")
                logging.info("buying BTCDOWN")
                available_usdt_balances = next((x for x in spot_client.coin_info() if x["coin"] == "USDT"))['free']
                print("Current USDT Balances: " + available_usdt_balances)
                logging.info("Current USDT Balances: %s", str(available_usdt_balances))
                usdt_balances = float(available_usdt_balances)
                usdt_balances = int(usdt_balances)
                entry_price = None
                ori_quantity = None
                commissions = 0
                params = {
                    "symbol": "BTCDOWNUSDT",
                    "side": "BUY",
                    "type": "MARKET",
                    "quoteOrderQty": str(usdt_balances * 60 / 100),
                    "newClientOrderId": str(count)
                }

                try:
                    response = spot_client.new_order(**params)
                    logging.info(response)
                    print("Created new buy order!!!!!")
                    logging.info("Created new buy order!!!!!")
                    entry_price = float(response["fills"][0]["price"])
                    ori_quantity = float(response["fills"][0]["origQty"])
                    for i in response['fills']:
                        commissions += float(i["commission"])
                except ClientError as error:
                    logging.error(
                        "Found error. status: {}, error code: {}, error message: {}".format(
                            error.status_code, error.error_code, error.error_message
                        )
                    )

                previous_margin_candle = taapi.TAAPI.margin_candle_request(taapi_secret, False)
                prev1_margin_close = previous_margin_candle[0]
                prev1_margin_low = previous_margin_candle[1]
                sl_margin = prev1_margin_low - atr_50
                print("Backtrack 1 margin candle close: " + str(prev1_margin_close))
                logging.info("Backtrack 1 margin candle close: %s", str(prev1_margin_close))
                print("Backtrack 1 margin candle low: " + str(prev1_margin_low))
                logging.info("Backtrack 1 margin candle low: %s", str(prev1_margin_low))
                print("SL price should be: " + str(sl_margin))
                logging.info("SL price should be: %s", str(sl_margin))

                params = {
                    "symbol": "BTCDOWNUSDT",
                    "side": "SELL",
                    "quantity": "{:.4f}".format(ori_quantity - commissions),
                    "price": "{:.4f}".format(((prev1_margin_close - prev1_margin_low + atr_50) * 1.4) + prev1_margin_close),
                    "stopPrice": "{:.4f}".format(sl_margin),
                    "stopLimitPrice": "{:.4f}".format(sl_margin - atr_50),
                    "stopLimitTimeInForce": "GTC",
                }

                try:
                    response = spot_client.new_oco_order(**params)
                    logging.info(response)
                    print("Created OCO order!!!!!")
                    logging.info("Created OCO order!!!!!")
                except ClientError as error:
                    logging.error(
                        "Found error. status: {}, error code: {}, error message: {}".format(
                            error.status_code, error.error_code, error.error_message
                        )
                    )
                break
    time.sleep(900 - time.time() % 900)
