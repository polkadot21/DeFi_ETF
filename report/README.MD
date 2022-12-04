# DeFi ETF

This is a vanilla DeFi ETF implemented as a cap-weighted index of the top market cap assets
on the Ethereum blockchain. 
This index reveals a simple yet diversified exposure to the field of DeFi.


## Assets

The Ethereum blockchain is currently hosting more than [600 DeFi-protocols](https://defillama.com/chains) 
with over than $24b in TVL which serves for stability and opportunity to gain 
profits.

a) The first portfolio considered in this PoC consisted of the top-12 market-cap DeFi applications
on the Ethereum blockchain. However, the wrapped/liquid and stable coins were excluded.
The market cap cut was done on December 3, 2022. 
The tokens are weighted based on their market capitalization. 
For sake of simplicity, the total market capitalization of the chosen assets was computed on the daily basis.
Then, the weight of each asset was acquired as a ratio of the market capitalization of a particular token over the total market capitalization on that day.
In the end, the "etf price" was calculates as the sum of the price of each token multiplied by the corresponding weight.
The rebalancement of the weights was done daily.


**Spoiler**: this set of assets proved non-profitable for any strategy
described in the further sections. Thus, the next set of assets was considered in this case.

b) Another set of assets mimics the renown [DeFi Pulse Index](https://indexcoop.com/defi-pulse-index-dpi#:~:text=The%20DeFi%20Pulse%20Index%20is,of%20each%20token's%20circulating%20supply.).
To appear in this index, the token must satisfy the following criteria:

- exist on the Ethereum blockchain;
- must be in the top-10 according to the market-cap;
- is NOT a wrapped token or/and NOT a derivative or/and NOT a stablecoin.

The market cap cut was done on September, 8, 2020.
This set was used to backtest the strategies. All the results in the next sections reveal the metrics on this set!

## Strategies

To compare and evaluate different investment strategies, [the Python Backtester](https://kernc.github.io/backtesting.py/) is used.
While "buy and hold" was taken as a benchmark, two investment strategies were compared in this experiment:

a) [moving-average crossover](https://en.wikipedia.org/wiki/Moving_average_crossover).

b) forecasting with the k-NN algorithm

In this strategy, we trained a simple k-NN classifier on the first 75 days and tried to forecast the price movement
in the next 48 hours. 

Backtesting was done on the previous 365 days. Surprisingly, the MA crossover strategy showed almost 500% annual returns 
with the Sharpe ratio equal to 0.68. In contrast to that, the strategy utilizing the k-NN classifier performed poorly 
and wasn't profitable (-23% annual return).

## Discussion

As we have seen above, the value of the index has dropped drastically over the past 365 days. Nevertheless,
such a simple strategy as SMA crossover yielded almost 500% annually. On the other hand, a k-NN model failed to 
generalize after having been trained on 75 days. There exist different reasons for that:

1) the model couldn't adjust to a shift in the distribution. Obviously, the sample size was too small;

2) k-NN is a practical yet simple algorithm which can't capture complex behavior. More sophisticated
algorithms are needed (LSTM, Transformer);

3) the feature set was not sufficient to map the dependent variable. Consider adding sentiment and other technical markers.

4) Also, there might be even more dependent variables, say, price, volume, etc. And the decision can be made based on their combination.
