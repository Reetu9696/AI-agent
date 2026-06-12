import argparse
import sys
from bot.client import BinanceFuturesClient
from bot.validators import validate_inputs
from bot.orders import OrderManager
from bot.logging_config import logger

def display_summary(symbol, side, order_type, quantity, price, stop_price):
    """Prints a clear summary of the order configuration on the terminal."""
    print("\n" + "="*50)
    print("               ORDER REQUEST SUMMARY            ")
    print("="*50)
    print(f" Asset Symbol   : {symbol.upper()}")
    print(f" Execution Side : {side.upper()}")
    print(f" Position Type  : {order_type.upper()}")
    print(f" Size/Quantity  : {quantity}")
    if price: print(f" Target Price   : {price}")
    if stop_price: print(f" Trigger Price  : {stop_price}")
    print("="*50)

def main():
    parser = argparse.ArgumentParser(
        description="Production-grade CLI Execution Wrapper for Binance Futures Testnet Trading Engine."
    )
    parser.add_argument("--symbol", type=str, required=True, help="Target asset pair ticker (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, required=True, choices=["BUY", "SELL"], help="Direction execution parameter")
    parser.add_argument("--type", type=str, required=True, choices=["MARKET", "LIMIT", "STOP_LIMIT"], help="Order execution type constraint")
    parser.add_argument("--quantity", type=float, required=True, help="Position order size unit tracking")
    parser.add_argument("--price", type=float, default=None, help="Trigger benchmark target price matching limit structures")
    parser.add_argument("--stopprice", type=float, default=None, help="Trigger breakpoint bound targeting Stop-Limit executions [Bonus feature]")

    args = parser.parse_args()

    # Validate inputs against system invariants
    validate_inputs(args.symbol, args.side, args.type, args.quantity, args.price)
    
    # Assert additional conditions for the bonus Stop-Limit order type
    if args.type.upper() == 'STOP_LIMIT' and not args.stopprice:
        print("\n[!] Input Error: --stopprice argument missing, required for STOP_LIMIT orders.")
        sys.exit(1)

    display_summary(args.symbol, args.side, args.type, args.quantity, args.price, args.stopprice)

    # Initialize connection client
    bot_client = BinanceFuturesClient()
    try:
        bot_client.connect()
    except Exception as network_err:
        print(f"\n[!] Connection Setup Error: {network_err}")
        sys.exit(1)

    # Process and execute order tracking logic
    manager = OrderManager(bot_client)
    print("\n[*] Sending payload data tracking framework to exchange...")
    success, response = manager.execute_order(
        symbol=args.symbol,
        side=args.side,
        order_type=args.type,
        quantity=args.quantity,
        price=args.price,
        stop_price=args.stopprice
    )

    print("\n" + "="*50)
    print("               EXCHANGE RESPONSE DETAILS        ")
    print("="*50)
    if success:
        print(f" Status Check   : SUCCESS ✅")
        print(f" System OrderID : {response.get('orderId')}")
        print(f" Engine Status  : {response.get('status')}")
        print(f" Cumulative Qty : {response.get('executedQty')}")
        print(f" Execution Price: {response.get('avgPrice') or response.get('price') or 'Market-Driven Price'}")
    else:
        print(f" Status Check   : FAILED ❌")
        print(f" Error Class    : {response.get('error')}")
        print(f" Context Details: {response.get('details')}")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()