# DeFi ETF

This is a vanilla DeFi ETF implemented as a cap-weighted index of the top market cap assets
on the Ethereum blockchain. 
This index reveals a simple yet diversified exposure to the field of DeFi.

## Disclaimer

A person who gives financial advice is called a financial advisor and takes money for his duties. I share this project for free and thus have nothing to do with any type of financial advice. Remember that this project serves for educations purposes only!


## Tokens included (Updated!)

The Ethereum blockchain is currently hosting more than [600 DeFi-protocols](https://defillama.com/chains) 
with over than $24b in TVL which serves for stability and opportunity to gain 
profits.

The first portfolio considered in this PoC consisted of the top-12 market-cap DeFi applications
on the Ethereum blockchain. However, the wrapped/liquid and stable coins were excluded.
The market cap cut was done on December 3, 2022. Indeed, this portfolio is taken
into consideration when you run the following command:

`bash run.sh default
`

Another set of assets mimics the renown [DeFi Pulse Index](https://indexcoop.com/defi-pulse-index-dpi#:~:text=The%20DeFi%20Pulse%20Index%20is,of%20each%20token's%20circulating%20supply.)..
To appear in this index, the token must satisfy the following criteria:

- exist on the Ethereum blockchain;
- must be in the top-10 according to the market-cap;
- is NOT a wrapped token or/and NOT a derivative or/and NOT a stablecoin.

The market cap cut was done on September, 8, 2020.

![img.png](img/img.png)

In the future, you will be able to pass your custom set of tokens.
Feel free to open an issue and a PR with the implementation.

## Token's Composition

The tokens are weighted based on their market capitalization. 
For sake of simplicity, the total market capitalization of the chosen assets was computed on the daily basis.
Then, the weight of each asset was acquired as a ratio of the market capitalization of a particular token over the total market capitalization on that day.
In the end, the "etf price" was calculates as the sum of the price of each token multiplied by the corresponding weight.
The rebalancement of the weights was done daily.

## Trading Strategy

To compare and evaluate different investment strategies, [the Python Backtester](https://kernc.github.io/backtesting.py/) is used.
While "buy and hold" was taken as a benchmark, two investment strategies were compared in this experiment:

a) [moving-average crossover](https://en.wikipedia.org/wiki/Moving_average_crossover).

![SMA_crossover.png](img/smacrossover.png)

b) forecasting with the k-NN algorithm

![forecasting.png](img/forecasting.png)


In this strategy, we trained a simple k-NN classifier on the first 75 days and tried to forecast the price movement
in the next 48 hours. 

Backtesting was done on the previous 365 days. Surprisingly, the MA crossover strategy showed almost 500% annual returns 
with the Sharpe ratio equal to 0.68. In contrast to that, the strategy utilizing the k-NN classifier performed poorly 
and wasn't profitable (-23% annual return). The reasons for that will be discussed later.
In the meantime, a vanilla "buy & hold" would achieve -89% over the same period. It means that
the both strategies were able to outperform "buy and hold" by 586% and 66% respectively.


P.S. Due to [a known bug](https://github.com/kernc/backtesting.py/issues/803) in Bokeh the plotting doesn't work in PyCharm.
Hence, there are .ipynb files to reproduce the plots.

## Discussion

As we have seen above, the value of the index has dropped drastically over the past 365 days. Nevertheless,
such a simple strategy as SMA crossover yielded almost 500% annually. On the other hand, a k-NN model failed to 
generalize after having been trained on 75 days. There exist different reasons for that:

1) the model couldn't adjust to a shift in the distribution. Obviously, the sample size was too small while 
the inference data were too big;

2) k-NN is a practical yet simple algorithm which can't capture complex behavior. More sophisticated
algorithms are needed (LSTM, Transformer);

3) the feature set was not sufficient to map the dependent variable. Consider adding sentiment and other technical markers.

4) Also, there might be even more dependent variables, say, price, volume, etc. And the decision can be made based on their combination.

## How to run?

1) Docker

You can download the image from DockerHub and run it locally:

```bash
docker pull evsa/defi
docker run defi
```
2) Conda

You can download the project and create a new conda env to run it locally:

```bash
mkdir defi && cd ./defi
git clone https://github.com/polkadot21/DeFi_ETF.git
conda create -yn defi python=3.10
conda activate defi
pip3 install -r requirements.txt
bash run.sh DeFiPulse smacrossover
```


## ToDo

- implement unit tests for the remaining utils;
- implement the network and exchange fees when rebalancing;
- implement the input of arbitrary assets.

## How to contribute?

Pull requests are welcome!
Please consider openning an issue first and include proper testing into your PR.

## License

[MIT](https://choosealicense.com/licenses/mit/)