
import pandas as pd
import numpy as np
import pytest
import yfinance as yf

from project.labeling import apply_labels
from project.common_helpers import get_returns

# Assume we have a sample input of prices
prices = pd.Series([10, 12, 15, 11, 13, 16, 12, 14, 17, 15])
@pytest.fixture
def mock_data():
    # return pd.read_csv("pld.csv")
    # define the ticker symbol
    tickerSymbol = 'GOOGL'

    # get data on this ticker
    tickerData = yf.Ticker(tickerSymbol)

    # get the historical prices for this ticker
    # tickerDf = tickerData.history(interval='2m', start='2023-6-20', end='2023-6-23')
    tickerDf = tickerData.history(interval='1d', period='10y')

    # see your data
    return tickerDf

def test_get_returns(mock_data):
    # Call the get_vol function with sample input
    result = get_returns(mock_data['Close'])
    prices = mock_data['Close']
    # Compute the expected output manually
    returns = prices / prices.shift(1) - 1

    # Compare the expected output with the actual result
    pd.testing.assert_series_equal(result, returns)


def test_labels(mock_data):
    # Call the get_vol function with sample input
    mock_data["returns"] = get_returns(mock_data['Close'])
    result = apply_labels(mock_data)

    prices = mock_data['Close']
    # Compute the expected output manually
    returns = prices / prices.shift(1) - 1

    # Compare the expected output with the actual result
    pd.testing.assert_series_equal(result, returns)