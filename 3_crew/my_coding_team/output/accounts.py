from datetime import datetime

def get_share_price(symbol: str) -> float:
    """
    Returns the current price of a share.
    This is a test implementation that returns fixed prices for AAPL, TSLA, GOOGL.
    
    Args:
        symbol (str): The stock symbol.
        
    Returns:
        float: The current price of the share.
    """
    prices = {
        'AAPL': 150.0,
        'TSLA': 800.0,
        'GOOGL': 2800.0
    }
    return prices.get(symbol, 0.0)

class Account:
    """
    A class that represents a user account in a trading simulation platform.
    
    Attributes:
        user_id (str): Unique identifier for the user/account.
        balance (float): The current cash balance of the account.
        portfolio (dict): A dictionary holding the shares currently owned by the user, mapping symbol -> quantity.
        initial_deposit (float): The initial fund deposited when the account was created.
        transactions (list): A list of transaction records.
    """
    
    def __init__(self, user_id: str, initial_deposit: float) -> None:
        """
        Initializes a new account with an initial deposit.
        
        Args:
            user_id (str): Unique identifier for the user/account.
            initial_deposit (float): Initial deposit amount to open an account.
            
        Raises:
            ValueError: If initial_deposit is less than or equal to zero.
        """
        if initial_deposit <= 0:
            raise ValueError("Initial deposit must be greater than zero.")
        
        self.user_id = user_id
        self.balance = initial_deposit
        self.portfolio = {}
        self.initial_deposit = initial_deposit
        self.transactions = []
        
        # Record the initial deposit transaction
        self._record_transaction('deposit', None, None, initial_deposit)
    
    def deposit_funds(self, amount: float) -> None:
        """
        Deposits funds into the user's account.
        
        Args:
            amount (float): The amount to deposit.
            
        Raises:
            ValueError: If amount is less than or equal to zero.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        
        self.balance += amount
        self._record_transaction('deposit', None, None, amount)
    
    def withdraw_funds(self, amount: float) -> None:
        """
        Withdraws funds from the user's account, ensuring the balance does not go negative.
        
        Args:
            amount (float): The amount to withdraw.
            
        Raises:
            ValueError: If amount is less than or equal to zero, or if withdrawal causes a negative balance.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        
        if amount > self.balance:
            raise ValueError(f"Insufficient funds. Current balance: {self.balance}, Attempted withdrawal: {amount}")
        
        self.balance -= amount
        self._record_transaction('withdraw', None, None, amount)
    
    def buy_shares(self, symbol: str, quantity: int) -> None:
        """
        Records the purchase of shares, ensuring the user can afford the purchase.
        
        Args:
            symbol (str): The stock symbol.
            quantity (int): The number of shares to buy.
            
        Raises:
            ValueError: If the user cannot afford the purchase.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        
        price = get_share_price(symbol)
        if price == 0.0:
            raise ValueError(f"Invalid symbol: {symbol}")
        
        total_cost = price * quantity
        
        if total_cost > self.balance:
            raise ValueError(f"Insufficient funds to buy {quantity} shares of {symbol} at {price} per share. Current balance: {self.balance}")
        
        # Update portfolio
        if symbol in self.portfolio:
            self.portfolio[symbol] += quantity
        else:
            self.portfolio[symbol] = quantity
        
        # Update balance
        self.balance -= total_cost
        
        # Record transaction
        self._record_transaction('buy', symbol, quantity, price)
    
    def sell_shares(self, symbol: str, quantity: int) -> None:
        """
        Records the sale of shares, ensuring the user owns enough shares to sell.
        
        Args:
            symbol (str): The stock symbol.
            quantity (int): The number of shares to sell.
            
        Raises:
            ValueError: If the user does not own enough shares.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        
        if symbol not in self.portfolio or self.portfolio[symbol] < quantity:
            raise ValueError(f"Insufficient shares. Current holdings of {symbol}: {self.portfolio.get(symbol, 0)}, Attempted sale: {quantity}")
        
        price = get_share_price(symbol)
        total_value = price * quantity
        
        # Update portfolio
        self.portfolio[symbol] -= quantity
        if self.portfolio[symbol] == 0:
            del self.portfolio[symbol]
        
        # Update balance
        self.balance += total_value
        
        # Record transaction
        self._record_transaction('sell', symbol, quantity, price)
    
    def calculate_portfolio_value(self) -> float:
        """
        Calculates the total value of the user's portfolio based on current market prices.
        
        Returns:
            float: The total portfolio value.
        """
        total_value = self.balance
        
        for symbol, quantity in self.portfolio.items():
            price = get_share_price(symbol)
            total_value += price * quantity
        
        return total_value
    
    def calculate_profit_loss(self) -> float:
        """
        Calculates the profit or loss from the initial deposit.
        
        Returns:
            float: The calculated profit or loss.
        """
        current_value = self.calculate_portfolio_value()
        return current_value - self.initial_deposit
    
    def get_holdings(self) -> dict:
        """
        Returns the current holdings of the user.
        
        Returns:
            dict: The portfolio mapping symbol -> quantity.
        """
        return self.portfolio.copy()
    
    def get_transactions(self) -> list:
        """
        Returns the list of all transactions made by the user.
        
        Returns:
            list: List of transaction records.
        """
        return self.transactions.copy()
    
    def _record_transaction(self, transaction_type: str, symbol: str, quantity: int, price: float) -> None:
        """
        Records a transaction in the transaction history.
        
        Args:
            transaction_type (str): The type of transaction ('buy', 'sell', 'deposit', 'withdraw').
            symbol (str): The stock symbol (None for deposit/withdraw).
            quantity (int): The number of shares (None for deposit/withdraw).
            price (float): The price per share or the amount for deposit/withdraw.
        """
        transaction = {
            'type': transaction_type,
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'timestamp': datetime.now()
        }
        self.transactions.append(transaction)