import sys
from bot.logging_config import logger

def validate_inputs(symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    """Executes structural and value assertions on incoming user arguments."""
    try:
        if not symbol.isalnum() or not symbol.isupper():
            raise ValueError(f"Invalid symbol format '{symbol}'. Must be alphanumeric uppercase (e.g., BTCUSDT).")

        if side.upper() not in ['BUY', 'SELL']:
            raise ValueError(f"Invalid side '{side}'. Options are limited strictly to BUY or SELL.")

        if order_type.upper() not in ['MARKET', 'LIMIT', 'STOP_LIMIT']:
            raise ValueError(f"Order type '{order_type}' unsupported. Supported: MARKET, LIMIT, STOP_LIMIT.")

        if quantity <= 0:
            raise ValueError(f"Quantity must be a strict positive numeric value. Provided: {quantity}")

        if order_type.upper() in ['LIMIT', 'STOP_LIMIT'] and (price is None or price <= 0):
            raise ValueError(f"Price attribute is mandatory and must be greater than zero for {order_type} orders.")
            
    except ValueError as err:
        logger.error(f"Input verification constraint failed: {err}")
        print(f"\n[!] Input Error: {err}")
        sys.exit(1)