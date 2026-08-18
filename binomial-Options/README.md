# TrinoPrice---Trinomial-Options-Pricing-Engine

A professional options pricing system using trinomial tree models with implied volatility surface construction.

## Features

- **Trinomial Tree Model**: European and American options pricing
- **Greeks Calculation**: Delta, Gamma, Theta, Vega, Rho
- **Dividend Support**: Continuous and discrete dividends
- **Implied Volatility Surface**: Market data calibration and interpolation
- **Real-time Data**: Alpha Vantage API integration

## Project Structure

```
options-pricing/
├── models.py              # Data models and structures
├── data_fetcher.py        # Market data fetching
├── trinomial_tree.py      # Core pricing engine
├── volatility_surface.py  # IV surface construction
├── main.py               # Main application
├── requirements.txt      # Dependencies
└── README.md            # Documentation
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from models import OptionParameters
from trinomial_tree import TrinomialTreeModel

# Create option parameters
params = OptionParameters(S0=100, K=105, T=0.25, r=0.05, sigma=0.2)

# Price European option
model = TrinomialTreeModel(params, option_type='call', exercise_type='european')
price = model.price_option()
greeks = model.calculate_greeks()

print(f"Option Price: ${price:.4f}")
print(f"Delta: {greeks.delta:.4f}")
```

### Command Line Interface

```bash
python main.py
```

### Implied Volatility Surface

```python
from volatility_surface import ImpliedVolatilitySurface

# Create surface
iv_surface = ImpliedVolatilitySurface(S0=100, r=0.05)

# Add market data
iv_surface.add_market_data(K=105, T=0.25, market_price=2.5)

# Build surface
surface = iv_surface.build_surface()

# Get interpolated IV
iv = iv_surface.get_iv(K=102, T=0.3)
```

## API Reference

### OptionParameters
- `S0`: Current stock price
- `K`: Strike price  
- `T`: Time to expiry (years)
- `r`: Risk-free rate
- `sigma`: Volatility
- `q`: Dividend yield

### TrinomialTreeModel
- `price_option()`: Calculate option price
- `calculate_greeks()`: Calculate option Greeks

### ImpliedVolatilitySurface
- `add_market_data()`: Add market option data
- `build_surface()`: Construct IV surface
- `get_iv()`: Get implied volatility

## Examples

The system includes comprehensive examples demonstrating:
- European vs American option pricing
- Dividend impact analysis
- Greeks calculation
- Implied volatility surface construction

## Requirements

- Python 3.7+
- NumPy, Pandas, SciPy, Matplotlib
- Alpha Vantage API key (optional)
