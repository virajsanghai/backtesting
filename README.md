# backtesting

Note: This is a research project will all the detailed analysis available in the
end_to_end_proj.ipynb. To make this production ready, we would ideally add unit tests, 
type hints, logging and docstrings. 

## Aim 
The aim of this project is to apply a ML model to a trading strategy and calculate
the deflated sharpe ratio for that trading strategy

## Method
We construct a toy investment strategy from 11 of the largest stocks from 11 of the 
the different sectors in the S&P500. We calculate the sharpe ratio of that on the 
out of sample data. We also calculate a distribution of sharpe ratios on a 
monte carlo simulation of out of sample prices, generated from the true out-of 
sample prices. We use this to calculate the mean sharpe ratio, variance of 
sharpe ratios and the deflated sharpe ratio. We compare the toy investment 
strategy to a baseline. In this case, we take our baseline as a simple but 
and hold strategy. We use the Hierarcical Risk Parity method to construct the 
optimal portfolio from our stocks at the beginning of the buy and hold strategy. 
We also use this method of portfolio optimisation for rebalancing in the toy 
investment strategy.

List of TOP 11 stocks in SP500 for each sector

- AAPL - Technology
- AMZN - Consumer discretionary
- GOOGL - Communication Services
- Berkshire Hathway (BRK.B) BRK-B  - Financials
- United Health Group (UNH) - healthcare
- Exxon (XOM) - Energy
- Walmart (WMT) - Consumer Staples
- Linde Plc (LIN) - Materials
- UPS - Industrials
- Nextera energy (NEE) - Utilities
- Prologis Inc (PLD) - Real Estate 

## Results

For the buy and hold strategy we get a mean SR of 0.8 and variance of SR of 0.9. 
The deflated SR is about 5.4%. For the toy investment strategy, we get a mean SR of
0.78 and variance of SR of 0.92. The deflated SR is even lower at about 5%. This means 
that both strategies only have a 5% chance of giving positive excess returns. Note: we 
take the risk free rate as 2%.