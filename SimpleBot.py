from binance import ThreadedWebsocketManager
from binance.client import Client
import pandas as pd

api_key = "VxuqPa3p6RrAN8wBxSP7BFcFr1xyA6Wc9FrWdOu6lFMANIlr5UhekZdep67NBgNJ"
secret_key = "EgB2E9eq55Kkjp6SJTpU4GK0Yp0SMqNyLdoHyC9cdbakF6BFTGonfloDADbGJYVb"

client = Client(api_key = api_key, api_secret = secret_key, tld="com", testnet=True)

twm = ThreadedWebsocketManager()
twm.start()

def simple_bot(msg):

    time = pd.to_datetime(msg["E"], unit="ms")
    price = float(msg["c"])

    print("Time: {} | Price: {}".format(time, price))

    if int(price) % 10 == 0:
        order = client.create_order(symbol="BTCUSDT", side="SELL", type="MARKET", quantity=0.1)
        print("\n" + 50 * "-")
        print("Buy {} BTC for {} USDT".format(order["executedQty"], order["cummulativeQuoteQty"]))
        print(50 * "-" + "\n")

        twm.stop() # stop defined inside callback

twm.start_symbol_miniticker_socket(callback = simple_bot, symbol = "BTCUSDT")
twm.join() # required if stop is defined in callback function