"""
Data models for options pricing system.
"""
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class OptionParameters:
    """Option parameters container."""
    S0: float  # Current stock price
    K: float   # Strike price
    T: float   # Time to expiry
    r: float   # Risk-free rate
    sigma: float  # Volatility
    q: float = 0.0  # Dividend yield


@dataclass
class MarketData:
    """Market option data for calibration."""
    K: float
    T: float
    market_price: float
    option_type: str = 'call'
    exercise_type: str = 'european'


@dataclass
class Greeks:
    """Option Greeks container."""
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float


@dataclass
class VolatilitySurface:
    """Implied volatility surface data."""
    strikes: List[float]
    maturities: List[float]
    iv_matrix: List[List[float]]
    raw_data: List[MarketData]