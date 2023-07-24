import matplotlib.pyplot as plt
import pandas as pd


def get_returns(prices):
  # 1. compute returns of the form p[t]/p[t-1] - 1
  price_returns = prices/ prices.shift(1) - 1
  return price_returns.rename("returns")


def plot_series(series_data: pd.Series, xlabel: str, ylabel: str):
    plt.plot(series_data)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()