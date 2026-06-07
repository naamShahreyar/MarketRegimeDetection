# Market Regime Detection and Dynamic Portfolio Allocation

A regime-based risk overlay that uses a Hidden Markov Model (HMM) to detect latent market states and dynamically reduce SPY exposure during crisis regimes, cutting drawdown at the cost of some upside in strong bull markets.

---

## Overview

Financial markets alternate between distinct regimes — periods of calm, trending growth and periods of elevated stress, high volatility, and drawdowns. This project models those regimes in an unsupervised fashion using a Gaussian HMM trained on a multi-asset feature set, then uses the resulting regime probabilities to scale portfolio exposure continuously rather than switching between binary states.

The primary goal is **drawdown reduction**, not return maximisation. The strategy trades some upside in strong bull markets for materially lower peak-to-trough losses — the kind of risk overlay used in practice to make a portfolio more survivable across full market cycles.

The strategy is benchmarked against a passive SPY buy-and-hold from 2005 to the present, with 5 bps per unit of turnover deducted to account for transaction costs.

---

## Project Structure

```
MarketRegimeDetection/
├── data/
│   ├── raw/
│   │   └── market_prices.csv       # Downloaded OHLC close prices
│   └── processed/
│       └── features.csv            # Engineered feature matrix
├── notebooks/
│   ├── 01_data_collection.ipynb    # Download and clean market data
│   ├── 02_feature_engineering.ipynb# Construct the feature set
│   └── 03_hmm_modelling.ipynb      # Model training, regime analysis, backtest
├── requirements.txt
└── README.md
```

---

## Data

Daily close prices are downloaded via `yfinance` from 2005-01-01 to the present for four assets:

| Ticker | Asset              |
|--------|--------------------|
| SPY    | S&P 500 ETF        |
| TLT    | 20+ Year Treasury  |
| GLD    | Gold ETF           |
| ^VIX   | CBOE Volatility Index |

Missing values (one trading day per asset) are forward-filled.

---

## Feature Engineering

Nine features are constructed from the raw price series:

| Feature           | Description                                      |
|-------------------|--------------------------------------------------|
| `SPY_vol_20`      | 20-day annualized rolling volatility of SPY      |
| `SPY_price_ma50`  | SPY price divided by its 50-day moving average   |
| `SPY_price_ma200` | SPY price divided by its 200-day moving average  |
| `SPY_drawdown`    | SPY drawdown from rolling peak                   |
| `VIX_level`       | Raw VIX close                                    |
| `TLT_ret_20`      | 20-day return of TLT (flight-to-safety signal)   |
| `GLD_ret_20`      | 20-day return of GLD (safe-haven signal)         |
| `SPY_ret_5`       | 5-day return of SPY                              |
| `SPY_ret_20`      | 20-day return of SPY                             |

All features are standardized with `StandardScaler` fit on the training set only.

---

## Methodology

### Train / Test Split

The feature matrix (starting 2005-10-17 after the longest rolling window fills) is split chronologically: 70% training, 30% test.

### Choosing the Number of Regimes

Two methods were used to select `K`:

- **Elbow method** on KMeans inertia: K=4 was visually plausible.
- **Silhouette score**: K=2 scored highest.
- **PCA cluster visualization**: K=3 and K=4 produced heavily overlapping clusters; K=2 gave clear separation.

K=2 was selected.

### Hidden Markov Model

A `GaussianHMM` with full covariance matrices is fit on the standardized training data:

```python
from hmmlearn.hmm import GaussianHMM

model = GaussianHMM(
    n_components=2,
    covariance_type="full",
    n_iter=1000,
    random_state=42
)
model.fit(X_train)
```

### Regime Interpretation

Mean feature values by regime on the training set:

| Regime | SPY 20d Return | SPY Volatility | VIX Level | SPY Drawdown | Label        |
|--------|---------------|----------------|-----------|--------------|--------------|
| 0      | -0.25%        | 22.6%          | 25.6      | -17.7%       | Crisis / Risk-off |
| 1      | +1.40%        | 10.3%          | 14.0      | -1.2%        | Bull / Risk-on    |

### Regime Validation on Historical Events

| Period           | % Time in Regime 0 (Crisis) |
|------------------|-----------------------------|
| 2008 Crisis      | 100%                        |
| COVID Crash      | 83%                         |
| 2022 Inflation   | 94%                         |

---

## Strategy Logic

Position size scales continuously from 0.5x (full risk-off) to 1.5x (full risk-on) based on the regime probability:

```python
position = 0.5 + p_risk_on * 1.0
```

The 0.5x floor keeps the strategy partially invested during crisis regimes, capturing recovery rallies rather than going fully flat. The 1.5x ceiling adds modest upside during bull regimes without excessive leverage.

Regime probabilities are computed on the test set only using a rolling 20-day context window, with `predict_proba` called one day at a time — no future test observations are used:

```python
for i in range(len(X_test)):
    start = max(0, i - context_window + 1)
    prob = model.predict_proba(X_test.iloc[start:i+1].values)
    p_risk_on[i] = prob[-1, risk_on_idx]
```

Daily strategy return with transaction costs:

```python
strategy_return = position.shift(1) * SPY_ret - (0.0005 * position.diff().abs())
```

---

## Backtest Results

All results are computed on the **test set only (30% of data, unseen during training)**. The model is trained on the 70% training split and frozen — no test data is used during fitting or probability estimation.

| Metric        | Buy and Hold | Regime Strategy |
|---------------|-------------|-----------------|
| Sharpe Ratio  | 1.11        | 0.94            |
| Sortino Ratio | 1.09        | 0.87            |
| Max Drawdown  | -24%        | -20%            |
| Total Return  | 2.07x       | 1.09x           |

The strategy underperforms on raw returns during the test period, which covers a strong bull market where the 0.5x floor during risk-off regimes limits upside. However, it reduces maximum drawdown by 17% (-20% vs -24%) with no look-ahead bias in the probability estimates.

This is a risk overlay, not an alpha generator — the intended use case is drawdown reduction across full market cycles.

---

## Installation

```bash
git clone https://github.com/naamShahreyar/MarketRegimeDetection.git
cd MarketRegimeDetection
pip install -r requirements.txt
```

Run the notebooks in order:

1. `notebooks/01_data_collection.ipynb`
2. `notebooks/02_feature_engineering.ipynb`
3. `notebooks/03_hmm_modelling.ipynb`

---

## Requirements

```
pandas
numpy
yfinance
matplotlib
scikit-learn
hmmlearn
seaborn
```
