import gradio as gr
from accounts import Account, get_share_price
from datetime import datetime

# Initialize a singleton account instance for the demo
account = None

def initialize_account(user_id, initial_deposit):
    """Initialize a new account with the given user ID and initial deposit."""
    global account
    try:
        initial_deposit = float(initial_deposit)
        account = Account(user_id, initial_deposit)
        return f"Account initialized for {user_id} with ${initial_deposit:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def deposit(amount):
    """Deposit funds into the account."""
    global account
    if account is None:
        return "Error: No account initialized. Please create an account first."
    
    try:
        amount = float(amount)
        account.deposit_funds(amount)
        return f"Successfully deposited ${amount:.2f}. New balance: ${account.balance:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def withdraw(amount):
    """Withdraw funds from the account."""
    global account
    if account is None:
        return "Error: No account initialized. Please create an account first."
    
    try:
        amount = float(amount)
        account.withdraw_funds(amount)
        return f"Successfully withdrew ${amount:.2f}. New balance: ${account.balance:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def buy_shares(symbol, quantity):
    """Buy shares of a stock."""
    global account
    if account is None:
        return "Error: No account initialized. Please create an account first."
    
    try:
        quantity = int(quantity)
        account.buy_shares(symbol, quantity)
        return f"Successfully bought {quantity} shares of {symbol} at ${get_share_price(symbol):.2f} per share. New balance: ${account.balance:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def sell_shares(symbol, quantity):
    """Sell shares of a stock."""
    global account
    if account is None:
        return "Error: No account initialized. Please create an account first."
    
    try:
        quantity = int(quantity)
        account.sell_shares(symbol, quantity)
        return f"Successfully sold {quantity} shares of {symbol} at ${get_share_price(symbol):.2f} per share. New balance: ${account.balance:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def check_price(symbol):
    """Check the current price of a stock."""
    price = get_share_price(symbol)
    if price == 0.0:
        return f"Error: Invalid symbol '{symbol}'"
    return f"Current price of {symbol}: ${price:.2f}"

def get_account_summary():
    """Get a summary of the account."""
    global account
    if account is None:
        return "Error: No account initialized. Please create an account first."
    
    holdings = account.get_holdings()
    portfolio_value = account.calculate_portfolio_value()
    profit_loss = account.calculate_profit_loss()
    
    summary = f"Account ID: {account.user_id}\n"
    summary += f"Cash Balance: ${account.balance:.2f}\n"
    summary += f"Portfolio Value: ${portfolio_value:.2f}\n"
    summary += f"Profit/Loss: ${profit_loss:.2f}\n\n"
    
    if holdings:
        summary += "Current Holdings:\n"
        for symbol, quantity in holdings.items():
            price = get_share_price(symbol)
            value = price * quantity
            summary += f"- {symbol}: {quantity} shares, Price: ${price:.2f}, Value: ${value:.2f}\n"
    else:
        summary += "No shares currently held.\n"
    
    return summary

def get_transactions_history():
    """Get the transaction history of the account."""
    global account
    if account is None:
        return "Error: No account initialized. Please create an account first."
    
    transactions = account.get_transactions()
    if not transactions:
        return "No transactions recorded."
    
    history = "Transaction History:\n"
    for i, transaction in enumerate(transactions, 1):
        time_str = transaction['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        
        if transaction['type'] == 'deposit':
            history += f"{i}. [{time_str}] Deposited ${transaction['price']:.2f}\n"
        elif transaction['type'] == 'withdraw':
            history += f"{i}. [{time_str}] Withdrew ${transaction['price']:.2f}\n"
        elif transaction['type'] == 'buy':
            total = transaction['price'] * transaction['quantity']
            history += f"{i}. [{time_str}] Bought {transaction['quantity']} shares of {transaction['symbol']} at ${transaction['price']:.2f} (Total: ${total:.2f})\n"
        elif transaction['type'] == 'sell':
            total = transaction['price'] * transaction['quantity']
            history += f"{i}. [{time_str}] Sold {transaction['quantity']} shares of {transaction['symbol']} at ${transaction['price']:.2f} (Total: ${total:.2f})\n"
    
    return history

# Define the Gradio interface
with gr.Blocks(title="Trading Simulation Platform") as demo:
    gr.Markdown("# Trading Simulation Platform")
    
    with gr.Tab("Account Management"):
        with gr.Group():
            gr.Markdown("### Initialize Account")
            with gr.Row():
                user_id_input = gr.Textbox(label="User ID", placeholder="Enter your user ID")
                initial_deposit_input = gr.Textbox(label="Initial Deposit", placeholder="Enter initial deposit amount")
            initialize_btn = gr.Button("Initialize Account")
            initialize_output = gr.Textbox(label="Result")
            
            initialize_btn.click(
                initialize_account,
                inputs=[user_id_input, initial_deposit_input],
                outputs=initialize_output
            )
        
        with gr.Group():
            gr.Markdown("### Deposit Funds")
            deposit_input = gr.Textbox(label="Amount", placeholder="Enter deposit amount")
            deposit_btn = gr.Button("Deposit")
            deposit_output = gr.Textbox(label="Result")
            
            deposit_btn.click(
                deposit,
                inputs=[deposit_input],
                outputs=deposit_output
            )
        
        with gr.Group():
            gr.Markdown("### Withdraw Funds")
            withdraw_input = gr.Textbox(label="Amount", placeholder="Enter withdrawal amount")
            withdraw_btn = gr.Button("Withdraw")
            withdraw_output = gr.Textbox(label="Result")
            
            withdraw_btn.click(
                withdraw,
                inputs=[withdraw_input],
                outputs=withdraw_output
            )
    
    with gr.Tab("Trading"):
        with gr.Group():
            gr.Markdown("### Check Stock Price")
            price_symbol_input = gr.Textbox(label="Symbol", placeholder="Enter stock symbol (e.g., AAPL, TSLA, GOOGL)")
            check_price_btn = gr.Button("Check Price")
            price_output = gr.Textbox(label="Price Information")
            
            check_price_btn.click(
                check_price,
                inputs=[price_symbol_input],
                outputs=price_output
            )
        
        with gr.Group():
            gr.Markdown("### Buy Shares")
            with gr.Row():
                buy_symbol_input = gr.Textbox(label="Symbol", placeholder="Enter stock symbol")
                buy_quantity_input = gr.Textbox(label="Quantity", placeholder="Enter number of shares")
            buy_btn = gr.Button("Buy Shares")
            buy_output = gr.Textbox(label="Result")
            
            buy_btn.click(
                buy_shares,
                inputs=[buy_symbol_input, buy_quantity_input],
                outputs=buy_output
            )
        
        with gr.Group():
            gr.Markdown("### Sell Shares")
            with gr.Row():
                sell_symbol_input = gr.Textbox(label="Symbol", placeholder="Enter stock symbol")
                sell_quantity_input = gr.Textbox(label="Quantity", placeholder="Enter number of shares")
            sell_btn = gr.Button("Sell Shares")
            sell_output = gr.Textbox(label="Result")
            
            sell_btn.click(
                sell_shares,
                inputs=[sell_symbol_input, sell_quantity_input],
                outputs=sell_output
            )
    
    with gr.Tab("Account Summary"):
        summary_btn = gr.Button("Get Account Summary")
        summary_output = gr.Textbox(label="Account Summary", lines=10)
        
        summary_btn.click(
            get_account_summary,
            inputs=[],
            outputs=summary_output
        )
    
    with gr.Tab("Transaction History"):
        history_btn = gr.Button("Get Transaction History")
        history_output = gr.Textbox(label="Transaction History", lines=15)
        
        history_btn.click(
            get_transactions_history,
            inputs=[],
            outputs=history_output
        )

if __name__ == "__main__":
    demo.launch()