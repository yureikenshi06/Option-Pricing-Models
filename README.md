# Option-Pricing-Models

# Black-Scholes Options 

A Python application for visualizing implied volatility and option price surfaces using the Black-Scholes model.

## Features

- **Real-time Data Fetching**: Retrieves live stock prices and option chain data from Yahoo Finance
- **Implied Volatility Calculation**: Computes implied volatility using Newton-Raphson method
- **3D Surface Visualization**: Interactive 3D plots for volatility and price surfaces
- **Flexible Analysis**: Option to plot by strike price or moneyness
- **Professional Architecture**: Clean, modular codebase with separation of concerns

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup
1. Clone or download the repository
2. Navigate to the project directory
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start
```bash
python main.py
```

### Interactive Prompts
The application will prompt you for:
- **Stock Ticker**: Enter symbol (e.g., AAPL, MSFT, GOOGL)
- **Risk-free Rate**: Enter as decimal (e.g., 0.05 for 5%)
- **Dividend Yield**: Enter as decimal (e.g., 0.02 for 2%)
- **Plot Type**: Choose between "Strike Price" or "Moneyness"

### Example Session
```
Enter stock ticker (e.g. AAPL): AAPL
Enter risk-free rate (e.g. 0.05): 0.05
Enter dividend yield (e.g. 0.00): 0.015
Plot by [Strike Price / Moneyness] (default = Strike Price): moneyness
```

## Project Structure

```
├── main.py              # Main application entry point
├── models.py            # BlackScholes data model
├── data_fetcher.py      # Yahoo Finance data retrieval
├── option_calculator.py # Option pricing calculations
├── surface_plotter.py   # 3D visualization utilities
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Module Overview

### `models.py`
- `BlackScholes`: Core option pricing model with call/put price calculations

### `data_fetcher.py`
- `DataFetcher`: Handles live market data retrieval and filtering

### `option_calculator.py`
- `OptionCalculator`: Implied volatility calculations and surface generation

### `surface_plotter.py`
- `SurfacePlotter`: Interactive 3D plotting with Plotly

### `main.py`
- User interface and application orchestration

## Output

The application generates three interactive 3D surface plots:
1. **Implied Volatility Surface**: Shows how IV varies with time and strike/moneyness
2. **Call Price Surface**: Theoretical call option prices using Black-Scholes




# Binomial-Options-Pricing-Engine

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

3. **Put Price Surface**: Theoretical put option prices using Black-Scholes





