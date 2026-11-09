import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde as kde

# Download data
prices = yf.Ticker("XLE").history(
    start="2023-12-01",
    end="2024-01-01"
)["Close"].dropna()

rets = np.log(prices).diff().dropna()

batchLength = 5
splits = [
    rets.iloc[i:i + batchLength]
    for i in range(len(rets) - batchLength + 1)
]


def bootstrap(ret_splits, n_draws=3000, seed=42):
    rng = np.random.default_rng(seed)

    densities = []
    meanVar = []
    intervals = []
    observed = []

    for i, ret_arr in enumerate(ret_splits):

        # Add the newest 20-day batch
        observed.extend(np.asarray(ret_arr, dtype=float))
        x = np.asarray(observed)

        n = len(x)

        # Bayesian bootstrap posterior weights
        weights = rng.dirichlet(
            np.ones(n),
            size=n_draws
        )

        # Joint posterior draws for mean and variance
        means = weights @ x

        variances = (
            weights @ (x ** 2) - means ** 2
        )
        variances = np.maximum(variances, 0)

        # Posterior expected mean and variance
        mean = means.mean()
        variance = variances.mean()

        meanVar.append((mean, variance))

        # 95% credible intervals
        mean_ci = np.quantile(means, [0.025, 0.975])
        var_ci = np.quantile(variances, [0.025, 0.975])

        intervals.append((mean_ci, var_ci))

        # Continuous posterior density of the mean
        density = kde(means)
        densities.append(density)

        # Visualize posterior mean distribution
        x_grid = np.linspace(
            means.min() - 0.002,
            means.max() + 0.002,
            300
        )

        plt.plot(
            x_grid,
            density(x_grid),
            label=f"Batch {i + 1}"
        )

    plt.xlabel("Daily Expected Log Return")
    plt.ylabel("Posterior Density")
    plt.title("Sequential Bayesian Bootstrap Estimates")
    plt.legend()
    plt.show()

    return densities, meanVar, intervals


densities, meanVar, intervals = bootstrap(splits)

for i, ((mean, variance), (mean_ci, var_ci)) in enumerate(
    zip(meanVar, intervals)
):
    print(f"\nBatch {i + 1}")
    print(f"Mean:     {mean:.6f}")
    print(f"Variance: {variance:.8f}")
    print(f"Mean 95% CI: {mean_ci}")
    print(f"Var 95% CI:  {var_ci}")

