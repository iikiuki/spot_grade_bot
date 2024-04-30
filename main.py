import ccxt
import time
import dontshareconfig

# Set up exchange with your API keys
exchange = ccxt.phemex({
    'apiKey': dontshareconfig.id,
    'secret': dontshareconfig.secret,
})

# Define trading parameters
symbol = 'BTC/USDT'  # The trading pair
grid_levels = 6  # Total grid levels (3 below and 3 above the current price)
grid_spacing =exchange.fetch_ticker(symbol)['last']*0.02 # Spacing between grid levels in USDT
trade_amount = 1.1/exchange.fetch_ticker(symbol)['last']  # Amount to trade at each level in BTC
refresh_interval = 2  # How often to re-check the grid (in seconds)

def create_grid_orders(current_price):
    orders = []
    
    # Create buy orders below the current price
    for i in range(1, (grid_levels // 2) + 1):
        price = current_price - (i * grid_spacing)
        orders.append({'side': 'buy', 'price': price})

    # Create sell orders above the current price
    for i in range(1, (grid_levels // 2) + 1):
        price = current_price + (i * grid_spacing)
        orders.append({'side': 'sell', 'price': price})

    return orders

def place_grid_orders(orders):
    for order in orders:
        if order['side'] == 'buy':
            try:
                exchange.create_limit_buy_order(symbol, trade_amount, order['price'])
                print("placed buy order \"done\"")
            except:
                print( "Error placing buy order" )
        else:
            try:
                exchange.create_limit_sell_order(symbol, trade_amount, order['price'])
                print("placed sell order \"done\"")
            except:
                print( "Error placing sell order" )
# Main loop to monitor and adjust grid orders
while True:
    # Get the current price
    current_price = exchange.fetch_ticker(symbol)['last']
    print(current_price)
    
    # Create grid orders based on current price
    grid_orders = create_grid_orders(current_price)
    
    # Place grid orders
    place_grid_orders(grid_orders)
    
    # Wait for the specified interval before checking again
    time.sleep(refresh_interval)
