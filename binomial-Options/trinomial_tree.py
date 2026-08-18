"""
Trinomial tree model for options pricing.
"""
import numpy as np
from typing import Dict, List, Tuple
from models import OptionParameters, Greeks


class TrinomialTreeModel:
    """Trinomial tree implementation for European and American options."""

    def __init__(self, params: OptionParameters, n_steps: int = 100,
                 option_type: str = 'call', exercise_type: str = 'european',
                 dividend_schedule: List[Tuple[float, float]] = None):

        self.params = params
        self.n_steps = n_steps
        self.option_type = option_type.lower()
        self.exercise_type = exercise_type.lower()
        self.dividend_schedule = dividend_schedule or []

        self.dt = params.T / n_steps
        self.discount_factor = np.exp(-params.r * self.dt)
        self._setup_tree_parameters()

    def _setup_tree_parameters(self):
        """Calculate trinomial tree parameters."""
        p = self.params
        self.dx = p.sigma * np.sqrt(3 * self.dt)
        self.nu = (p.r - p.q - 0.5 * p.sigma ** 2) * self.dt

        self.p_up = 0.5 * ((p.sigma ** 2 * self.dt + self.nu ** 2) / self.dx ** 2 + self.nu / self.dx)
        self.p_down = 0.5 * ((p.sigma ** 2 * self.dt + self.nu ** 2) / self.dx ** 2 - self.nu / self.dx)
        self.p_middle = 1 - self.p_up - self.p_down

        if not all(0 <= p <= 1 for p in [self.p_up, self.p_down, self.p_middle]):
            raise ValueError("Invalid probabilities. Adjust parameters.")

    def _payoff(self, S: float) -> float:
        """Calculate option payoff."""
        if self.option_type == 'call':
            return max(S - self.params.K, 0)
        return max(self.params.K - S, 0)

    def _build_stock_tree(self) -> Dict[int, Dict[int, float]]:
        """Build stock price tree with dividend adjustments."""
        tree = {}
        for i in range(self.n_steps + 1):
            tree[i] = {}
            for j in range(-i, i + 1):
                S = self.params.S0 * np.exp(j * self.dx)

                # Apply discrete dividends
                current_time = i * self.dt
                for div_time, div_amount in self.dividend_schedule:
                    if div_time <= current_time:
                        S -= div_amount * np.exp(-self.params.r * (current_time - div_time))

                tree[i][j] = S
        return tree

    def price_option(self) -> float:
        """Price option using trinomial tree."""
        stock_tree = self._build_stock_tree()
        option_tree = {}

        # Terminal values
        option_tree[self.n_steps] = {
            j: self._payoff(stock_tree[self.n_steps][j])
            for j in range(-self.n_steps, self.n_steps + 1)
            if j in stock_tree[self.n_steps]
        }

        # Backward induction
        for i in range(self.n_steps - 1, -1, -1):
            option_tree[i] = {}
            for j in range(-i, i + 1):
                # Continuation value
                continuation = (
                                       self.p_up * option_tree[i + 1].get(j + 1, 0) +
                                       self.p_middle * option_tree[i + 1].get(j, 0) +
                                       self.p_down * option_tree[i + 1].get(j - 1, 0)
                               ) * self.discount_factor

                # American option early exercise
                if self.exercise_type == 'american':
                    intrinsic = self._payoff(stock_tree[i][j])
                    option_tree[i][j] = max(continuation, intrinsic)
                else:
                    option_tree[i][j] = continuation

        return option_tree[0][0]

    def calculate_greeks(self, bump_size: float = 0.01) -> Greeks:
        """Calculate Greeks using finite differences."""
        base_price = self.price_option()

        # Delta and Gamma
        original_s0 = self.params.S0

        self.params.S0 += bump_size
        self._setup_tree_parameters()
        price_up = self.price_option()

        self.params.S0 = original_s0 - bump_size
        self._setup_tree_parameters()
        price_down = self.price_option()

        self.params.S0 = original_s0
        self._setup_tree_parameters()

        delta = (price_up - price_down) / (2 * bump_size)
        gamma = (price_up - 2 * base_price + price_down) / (bump_size ** 2)

        # Theta
        original_t = self.params.T
        self.params.T -= 1 / 365
        self.dt = self.params.T / self.n_steps
        self._setup_tree_parameters()
        price_theta = self.price_option()

        self.params.T = original_t
        self.dt = self.params.T / self.n_steps
        self._setup_tree_parameters()
        theta = price_theta - base_price

        # Vega
        original_sigma = self.params.sigma
        self.params.sigma += 0.01
        self._setup_tree_parameters()
        price_vega = self.price_option()

        self.params.sigma = original_sigma
        self._setup_tree_parameters()
        vega = price_vega - base_price

        # Rho
        original_r = self.params.r
        self.params.r += 0.01
        self._setup_tree_parameters()
        price_rho = self.price_option()

        self.params.r = original_r
        self._setup_tree_parameters()
        rho = price_rho - base_price

        return Greeks(delta=delta, gamma=gamma, theta=theta, vega=vega, rho=rho)