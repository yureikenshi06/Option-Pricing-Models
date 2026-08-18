"""
Market data fetcher for stock prices.
"""
from typing import Optional
from models import OptionParameters

try:
    from alpha_vantage.timeseries import TimeSeries

    ALPHA_VANTAGE_AVAILABLE = True
except ImportError:
    ALPHA_VANTAGE_AVAILABLE = False


class DataFetcher:
    """Fetches real-time stock data from Alpha Vantage API."""

    def __init__(self, api_key: str = "Q3TZR7UE53Q68L5K"):
        self.api_key = api_key
        self.ts = TimeSeries(key=api_key, output_format='pandas') if ALPHA_VANTAGE_AVAILABLE else None

    def get_current_price(self, ticker: str) -> Optional[float]:
        """Fetch current stock price."""
        if not self.ts:
            return None

        try:
            data, _ = self.ts.get_intraday(symbol=ticker, outputsize='compact')
            return float(data['4. close'].iloc[0])
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            return None

    def create_option_params(self, ticker: str, strike: float, time_to_expiry: float,
                             risk_free_rate: float = 0.05, volatility: float = 0.2) -> OptionParameters:
        """Create option parameters with fetched or manual price input."""
        current_price = self.get_current_price(ticker)

        if current_price is None:
            current_price = float(input(f"Enter current price for {ticker}: "))

        return OptionParameters(
            S0=current_price,
            K=strike,
            T=time_to_expiry,
            r=risk_free_rate,
            sigma=volatility
        )