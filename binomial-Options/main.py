
import numpy as np
from models import OptionParameters
from data_fetcher import DataFetcher
from trinomial_tree import TrinomialTreeModel



class OptionsPricingSystem:
    """Main options pricing system."""

    def __init__(self):
        self.data_fetcher = DataFetcher()

    def get_user_input(self) -> tuple:
        """Get user input for option parameters."""
        print("Options Pricing System")
        print("=" * 30)

        ticker = input("Enter ticker (or press Enter for manual): ").strip()

        if ticker:
            current_price = self.data_fetcher.get_current_price(ticker)
            if current_price:
                print(f"Current price for {ticker}: ${current_price:.2f}")
            else:
                current_price = float(input("Enter current price: "))
        else:
            current_price = float(input("Enter current price: "))

        strike = float(input("Enter strike price: "))
        maturity = float(input("Enter time to expiry (years): "))
        volatility = float(input("Enter volatility (e.g., 0.2 for 20%): "))
        risk_free_rate = float(input("Enter risk-free rate (e.g., 0.05 for 5%): "))

        return current_price, strike, maturity, volatility, risk_free_rate

    def price_options(self, params: OptionParameters) -> dict:
        """Price European and American options."""
        results = {}

        # European option
        eur_model = TrinomialTreeModel(params, option_type='call', exercise_type='european')
        results['european'] = {
            'price': eur_model.price_option(),
            'greeks': eur_model.calculate_greeks()
        }

        # American option
        am_model = TrinomialTreeModel(params, option_type='call', exercise_type='american')
        results['american'] = {
            'price': am_model.price_option(),
            'greeks': am_model.calculate_greeks()
        }

        results['early_exercise_premium'] = results['american']['price'] - results['european']['price']

        return results

    def analyze_dividends(self, params: OptionParameters) -> dict:
        """Analyze dividend impact on option prices."""
        base_model = TrinomialTreeModel(params, option_type='call', exercise_type='american')
        base_price = base_model.price_option()

        # With continuous dividend
        params.q = 0.03
        div_model = TrinomialTreeModel(params, option_type='call', exercise_type='american')
        div_price = div_model.price_option()

        # With discrete dividends
        params.q = 0.0
        discrete_model = TrinomialTreeModel(
            params, option_type='call', exercise_type='american',
            dividend_schedule=[(0.1, 2.0), (0.2, 2.0)]
        )
        discrete_price = discrete_model.price_option()

        return {
            'no_dividends': base_price,
            'continuous_dividend': div_price,
            'discrete_dividends': discrete_price
        }


    def run(self):
        """Run the main application."""
        try:
            # Get user input
            S0, K, T, sigma, r = self.get_user_input()
            params = OptionParameters(S0, K, T, r, sigma)

            # Price options
            print("\n1. Option Pricing Results")
            print("-" * 25)
            results = self.price_options(params)

            print(f"European Call: ${results['european']['price']:.4f}")
            print(f"American Call: ${results['american']['price']:.4f}")
            print(f"Early Exercise Premium: ${results['early_exercise_premium']:.4f}")

            # Greeks
            print(f"\nGreeks (European):")
            greeks = results['european']['greeks']
            print(f"  Delta: {greeks.delta:.4f}")
            print(f"  Gamma: {greeks.gamma:.4f}")
            print(f"  Theta: {greeks.theta:.4f}")
            print(f"  Vega: {greeks.vega:.4f}")
            print(f"  Rho: {greeks.rho:.4f}")

            # Dividend analysis
            print("\n2. Dividend Impact Analysis")
            print("-" * 25)
            div_results = self.analyze_dividends(params)

            for key, value in div_results.items():
                print(f"{key.replace('_', ' ').title()}: ${value:.4f}")

        except Exception as e:
            print(f"Error: {e}")


def main():
    """Entry point."""
    app = OptionsPricingSystem()
    app.run()


if __name__ == "__main__":
    main()