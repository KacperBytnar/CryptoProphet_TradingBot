from binance import ThreadedWebsocketManager
import time
import pandas as pd

def stream_candles(msg):
    # extract required candle items
    event_time = pd.to_datetime(msg["E"], unit="ms")
    start_time = pd.to_datetime(msg["k"]["t"], unit="ms")
    first = float(msg["k"]["o"])
    high = float(msg["k"]["h"])
    low = float(msg["k"]["l"])
    close = float(msg["k"]["c"])
    volume = float(msg["k"]["v"])
    complete = msg["k"]["x"]

    # print out
    print("Time: {} | Price: {}".format(event_time, close))

    # feed df (add a new bar / update)
    df.loc[start_time] = [first, high, low, close, volume, complete]

twm = ThreadedWebsocketManager()
twm.start()

twm.start_symbol_miniticker_socket(callback = stream_candles, symbol = "BTCUSDT", interval = "1m")

while True:
    time.sleep(20)
    twm.stop()
    break

