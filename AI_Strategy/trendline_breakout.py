import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from trendline_automation import fit_trendlines_single


def trendline_breakout(close: np.array, lookback: int):
    s_tl = np.zeros(len(close))
    s_tl[:] = np.nan

    r_tl = np.zeros(len(close))
    r_tl[:] = np.nan

    sig = np.zeros(len(close))

    for i in range(lookback, len(close)):
        # NOTE window does NOT include the current candle
        window = close[i - lookback: i]

        s_coefs, r_coefs = fit_trendlines_single(window)

        # Find current value of line, projected forward to current bar
        s_val = s_coefs[1] + lookback * s_coefs[0]
        r_val = r_coefs[1] + lookback * r_coefs[0]

        s_tl[i] = s_val
        r_tl[i] = r_val

        if close[i] > r_val:
            sig[i] = 1.0
        elif close[i] < s_val:
            sig[i] = -1.0
        else:
            sig[i] = sig[i - 1]

    return s_tl, r_tl, sig


if __name__ == '__main__':
    data = pd.read_csv('data.csv')
    data['date'] = pd.to_datetime(data['date'])
    data = data.set_index('date')
    data = data.dropna()

    lookback = 72
    support, resist, signal = trendline_breakout(data['close'].to_numpy(), lookback)
    data['support'] = support
    data['resist'] = resist
    data['signal'] = signal

    plt.style.use('dark_background')
    data['close'].plot(label='Close')
    data['resist'].plot(label='Resistance', color='green')
    data['support'].plot(label='Support', color='red')
    plt.show()

    data['r'] = np.log(data['close']).diff().shift(-1)
    data['strategy'] = data['signal'] * data['r']
    data['trades'] = data['signal'].diff().fillna(0).abs()
    data['strategy'] = data['strategy'] + data['trades']
    data['creturns'] = data['r'].cumsum().apply(np.exp)
    data['cstrategy'] = data['strategy'].cumsum().apply(np.exp)

    strategy_returns = data['strategy']

    # Additional calculations
    cagr = np.exp(strategy_returns.sum()) ** (1 / (len(strategy_returns) / 252)) - 1  # Assuming 252 trading days
    ann_mean = strategy_returns.mean() * 252
    ann_std = strategy_returns.std() * np.sqrt(252)
    sharpe_ratio = cagr / ann_std if ann_std != 0 else np.nan

    print(100 * "=")
    print("Breakout based strategy")
    print(100 * "-")
    print("PERFORMANCE MEASURES:")
    print("\n")
    print("Annualized Mean:             {}".format(ann_mean))
    print("Annualized Std:              {}".format(ann_std))
    print("Sharpe Ratio:                {}".format(sharpe_ratio))

    # Print cumulative results and profit factor
    cumulative_strategy_returns = data['cstrategy'].iloc[-1]
    profit_factor = strategy_returns[strategy_returns > 0].sum() / strategy_returns[strategy_returns < 0].abs().sum()

    print("\n")
    print("Cumulative Strategy Returns: {}".format(cumulative_strategy_returns))
    print("Profit Factor:               {}".format(profit_factor))

    plt.style.use('dark_background')
    data['creturns'].plot(label='Buy and Hold')
    data['cstrategy'].plot(label='Strategy')
    plt.legend()
    plt.show()