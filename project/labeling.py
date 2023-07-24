import numpy as np
import pandas as pd

def apply_labels(data_ohlc: pd.DataFrame):
    data_ohlc = data_ohlc.assign(threshold=get_vol_returns(data_ohlc['returns'])).dropna()
    data_ohlc = data_ohlc.assign(t1=get_horizons(data_ohlc)).dropna()
    events = data_ohlc[['t1', 'threshold']]
    events = events.assign(side=pd.Series(1., events.index))  # long only
    touches = get_touches(data_ohlc['Close'], events, [1, 1])
    touches = get_labels(touches)
    data_ohlc = data_ohlc.assign(label=touches['label'])
    return data_ohlc

def get_vol_returns(returns, span=100):
  # 2. estimate rolling standard deviation
  vols = returns.ewm(span=span).std()
  return vols

def get_horizons(prices, delta=pd.Timedelta(days=5)):
    t1 = prices.index.searchsorted(prices.index + delta)
    t1 = t1[t1 < prices.shape[0]]
    t1 = prices.index[t1]
    t1 = pd.Series(t1, index=prices.index[:t1.shape[0]])
    return t1
def get_touches(prices, events, factors=[1, 1]):
  '''
  events: pd dataframe with columns
    t1: timestamp of the next horizon
    threshold: unit height of top and bottom barriers
    side: the side of each bet
  factors: multipliers of the threshold to set the height of
           top/bottom barriers
  '''
  out = events[['t1']].copy(deep=True)
  if factors[0] > 0: thresh_uppr = factors[0] * events['threshold']
  else: thresh_uppr = pd.Series(index=events.index) # no uppr thresh
  if factors[1] > 0: thresh_lwr = -factors[1] * events['threshold']
  else: thresh_lwr = pd.Series(index=events.index)  # no lwr thresh
  for loc, t1 in events['t1'].items():
    df0=prices[loc:t1]                              # path prices
    df0=(df0 / prices[loc] - 1) * events.side[loc]  # path returns
    out.loc[loc, 'stop_loss'] = \
      df0[df0 < thresh_lwr[loc]].index.min()  # earliest stop loss
    out.loc[loc, 'take_profit'] = \
      df0[df0 > thresh_uppr[loc]].index.min() # earliest take profit
  return out

def get_labels(touches):
  out = touches.copy(deep=True)
  final = out.apply(add_labels_method_1, axis=1)
  return final

def add_labels_method_1(row):
    if pd.isnull(row['stop_loss']) and pd.isnull(row['take_profit']):
        row['label'] = 0
    elif pd.isnull(row['stop_loss']):
        row['label'] = 1
    elif pd.isnull(row['take_profit']):
        row['label'] = -1
    elif row['stop_loss'] < row['take_profit']:
        row['label'] = -1
    elif row['stop_loss'] > row['take_profit']:
        row['label'] = 1
    else:
        row['label'] = 0
    return row

def add_labels(row, epoch):
    if row['stop_loss'] < row['take_profit'] and row['stop_loss'] != epoch:
        row['label'] = -1
    elif row['stop_loss'] > row['take_profit'] and row['take_profit'] != epoch:
        row['label'] = 1
    else:
        row['label'] = 0