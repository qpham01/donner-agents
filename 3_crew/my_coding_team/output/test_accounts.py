import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from accounts import Account, get_share_price

class TestGetSharePrice(unittest.TestCase):
    def test_get_share_price_for_valid_symbols(self):
        # Test that get_share_price returns correct prices for valid symbols
        self.assertEqual(get_share_price("AAPL"), 150.0)
        self.assertEqual(get_share_price("TSLA"), 800.0)
        self.assertEqual(get_share_price("GOOGL"), 2800.0)
    
    def test_get_share_price_for_invalid_symbol(self):
        # Test that get_share_price returns 0.0 for invalid symbols
        self.assertEqual(get_share_price("INVALID"), 0.0)
        self.assertEqual(get_share_price(""), 0.0)

class TestAccount(unittest.TestCase):
    def setUp(self):
        # Set up a fresh account before each test
        self.account = Account("user123", 1000.0)
    
    def test_init_with_valid_deposit(self):
        # Test account initialization with valid deposit
        account = Account("user123", 1000.0)
        self.assertEqual(account.user_id, "user123")
        self.assertEqual(account.balance, 1000.0)
        self.assertEqual(account.portfolio, {})
        self.assertEqual(account.initial_deposit, 1000.0)
        self.assertEqual(len(account.transactions), 1)
        self.assertEqual(account.transactions[0]["type"], "deposit")
        self.assertEqual(account.transactions[0]["price"], 1000.0)
        self.assertIsNone(account.transactions[0]["symbol"])
        self.assertIsNone(account.transactions[0]["quantity"])
        self.assertIsInstance(account.transactions[0]["timestamp"], datetime)
    
    def test_init_with_invalid_deposit(self):
        # Test account initialization with invalid deposit amount
        with self.assertRaises(ValueError):
            Account("user123", 0.0)
        with self.assertRaises(ValueError):
            Account("user123", -100.0)

    def test_deposit_funds_valid_amount(self):
        # Test depositing valid amount of funds
        self.account.deposit_funds(500.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1]["type"], "deposit")
        self.assertEqual(self.account.transactions[1]["price"], 500.0)
    
    def test_deposit_funds_invalid_amount(self):
        # Test depositing invalid amounts raises ValueError
        with self.assertRaises(ValueError):
            self.account.deposit_funds(0.0)
        with self.assertRaises(ValueError):
            self.account.deposit_funds(-100.0)
    
    def test_withdraw_funds_valid_amount(self):
        # Test withdrawing valid amount of funds
        self.account.withdraw_funds(500.0)
        self.assertEqual(self.account.balance, 500.0)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1]["type"], "withdraw")
        self.assertEqual(self.account.transactions[1]["price"], 500.0)
    
    def test_withdraw_funds_invalid_amount(self):
        # Test withdrawing invalid amounts raises ValueError
        with self.assertRaises(ValueError):
            self.account.withdraw_funds(0.0)
        with self.assertRaises(ValueError):
            self.account.withdraw_funds(-100.0)
        with self.assertRaises(ValueError):
            self.account.withdraw_funds(2000.0)  # More than balance
    
    def test_buy_shares_valid_purchase(self):
        # Test buying shares with valid parameters
        self.account.buy_shares("AAPL", 5)
        self.assertEqual(self.account.balance, 250.0)  # 1000 - (5 * 150)
        self.assertEqual(self.account.portfolio, {"AAPL": 5})
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1]["type"], "buy")
        self.assertEqual(self.account.transactions[1]["symbol"], "AAPL")
        self.assertEqual(self.account.transactions[1]["quantity"], 5)
        self.assertEqual(self.account.transactions[1]["price"], 150.0)
    
    def test_buy_additional_shares(self):
        # Test buying additional shares of the same symbol
        # First purchase
        self.account.buy_shares("AAPL", 2)
        # Second purchase of same stock
        self.account.buy_shares("AAPL", 3)
        self.assertEqual(self.account.portfolio, {"AAPL": 5})
        self.assertEqual(self.account.balance, 250.0)  # 1000 - 2*150 - 3*150
    
    def test_buy_shares_invalid_purchase(self):
        # Test buying shares with invalid parameters raises ValueError
        # Invalid quantity
        with self.assertRaises(ValueError):
            self.account.buy_shares("AAPL", 0)
        with self.assertRaises(ValueError):
            self.account.buy_shares("AAPL", -5)
        
        # Invalid symbol
        with self.assertRaises(ValueError):
            self.account.buy_shares("INVALID", 5)
        
        # Insufficient funds
        with self.assertRaises(ValueError):
            self.account.buy_shares("TSLA", 2)  # 2 * 800 > 1000
    
    def test_sell_shares_valid_sale(self):
        # Test selling shares with valid parameters
        # First buy shares
        self.account.buy_shares("AAPL", 5)
        initial_balance = self.account.balance
        
        # Then sell some
        self.account.sell_shares("AAPL", 2)
        self.assertEqual(self.account.portfolio, {"AAPL": 3})
        self.assertEqual(self.account.balance, initial_balance + (2 * 150.0))
        self.assertEqual(self.account.transactions[-1]["type"], "sell")
        
        # Sell remaining shares
        self.account.sell_shares("AAPL", 3)
        self.assertEqual(self.account.portfolio, {})
    
    def test_sell_shares_invalid_sale(self):
        # Test selling shares with invalid parameters raises ValueError
        # No shares owned
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", 1)
        
        # Buy some shares first
        self.account.buy_shares("AAPL", 2)
        
        # Invalid quantity
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", 0)
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", -1)
        
        # More than owned
        with self.assertRaises(ValueError):
            self.account.sell_shares("AAPL", 3)
        
        # Symbol not in portfolio
        with self.assertRaises(ValueError):
            self.account.sell_shares("TSLA", 1)
    
    def test_calculate_portfolio_value(self):
        # Test calculating the total portfolio value
        # Empty portfolio
        self.assertEqual(self.account.calculate_portfolio_value(), 1000.0)  # Just the balance
        
        # Add some shares
        self.account.buy_shares("AAPL", 2)  # 2 * 150 = 300
        expected_value = self.account.balance + (2 * 150.0)
        self.assertEqual(self.account.calculate_portfolio_value(), expected_value)
    
    def test_multiple_stock_portfolio_value(self):
        # Test portfolio value calculation with multiple stocks
        # Buy different stocks
        self.account.buy_shares("AAPL", 1)  # 150
        self.account.buy_shares("TSLA", 1)  # 800
        
        expected_value = self.account.balance + 150.0 + 800.0
        self.assertEqual(self.account.calculate_portfolio_value(), expected_value)
    
    def test_calculate_profit_loss(self):
        # Test calculating profit or loss from initial deposit
        # Initial state - no profit/loss
        self.assertEqual(self.account.calculate_profit_loss(), 0.0)
        
        # After buying shares that don't change in value, should still be 0
        self.account.buy_shares("AAPL", 2)
        self.assertEqual(self.account.calculate_profit_loss(), 0.0)
        
        # After depositing more funds (not counted as profit)
        initial_value = self.account.calculate_portfolio_value()
        self.account.deposit_funds(500.0)
        self.assertEqual(self.account.calculate_profit_loss(), initial_value + 500.0 - self.account.initial_deposit)
        
        # After withdrawing funds
        self.account.withdraw_funds(200.0)
        current_value = self.account.calculate_portfolio_value()
        self.assertEqual(self.account.calculate_profit_loss(), current_value - self.account.initial_deposit)
    
    def test_get_holdings(self):
        # Test getting current holdings
        # Empty portfolio
        self.assertEqual(self.account.get_holdings(), {})
        
        # Add some shares
        self.account.buy_shares("AAPL", 2)
        self.assertEqual(self.account.get_holdings(), {"AAPL": 2})
        
        # Verify it's a copy
        holdings = self.account.get_holdings()
        holdings["AAPL"] = 10
        self.assertEqual(self.account.portfolio["AAPL"], 2)  # Original unchanged
    
    def test_get_transactions(self):
        # Test getting transaction history
        # Initial deposit transaction
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]["type"], "deposit")
        
        # Add a transaction
        self.account.buy_shares("AAPL", 1)
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 2)
        
        # Verify it's a copy
        transactions.append("fake")
        self.assertEqual(len(self.account.transactions), 2)  # Original unchanged
    
    @patch("accounts.datetime")
    def test_record_transaction_timestamp(self, mock_datetime):
        # Test that transactions record the correct timestamp
        # Set up mock datetime
        mock_now = datetime(2023, 1, 1, 12, 0)
        mock_datetime.now.return_value = mock_now
        
        # Perform a transaction
        self.account.deposit_funds(100.0)
        
        # Check the timestamp in the transaction
        self.assertEqual(self.account.transactions[-1]["timestamp"], mock_now)

    def test_complex_scenario(self):
        # Test a complex scenario with multiple operations
        # Initial state
        self.assertEqual(self.account.balance, 1000.0)
        
        # Buy some shares
        self.account.buy_shares("AAPL", 2)  # 300
        self.assertEqual(self.account.balance, 700.0)
        
        # Deposit more funds
        self.account.deposit_funds(500.0)
        self.assertEqual(self.account.balance, 1200.0)
        
        # Buy shares with available funds
        self.account.buy_shares("TSLA", 1)  # 800
        self.assertEqual(self.account.balance, 400.0)
        
        # Calculate portfolio value
        portfolio_value = self.account.calculate_portfolio_value()
        expected_value = 400.0 + (2 * 150.0) + (1 * 800.0)
        self.assertEqual(portfolio_value, expected_value)
        
        # Sell some shares
        self.account.sell_shares("AAPL", 1)
        self.assertEqual(self.account.balance, 550.0)  # 400 + 150
        self.assertEqual(self.account.portfolio, {"AAPL": 1, "TSLA": 1})

if __name__ == "__main__":
    unittest.main()