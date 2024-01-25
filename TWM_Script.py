from binance import ThreadedWebsocketManager
import time
import pandas as pd

def stream_data(msg):
    time = pd.to_datetime(msg["E"], unit= "ms")
    price = msg['c']
    print("Time: {}  || Price: {}".format(time, price))

twm = ThreadedWebsocketManager()
twm.start()

twm.start_symbol_miniticker_socket(callback = stream_data, symbol = "BTCUSDT")

while True:
    time.sleep(20)
    twm.stop()
    break