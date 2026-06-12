from binance.exceptions import BinanceAPIException, BinanceOrderException
from bot.logging_config import logger

class OrderManager:
    """Encapsulates structural business logic targeting payload preparation and dispatching."""
    def __init__(self, client_wrapper):
        self.wrapper = client_wrapper

    def execute_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
        """Dispatches validated parameter sets to the exchange execution layer endpoints."""
        symbol = symbol.upper()
        side = side.upper()
        order_type = order_type.upper()
        
        # Build out runtime argument map for the API request package
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity
        }

        if order_type == 'LIMIT':
            params['price'] = str(price)
            params['timeInForce'] = 'GTC'  # Good 'Til Cancelled default constraint execution tracking
        elif order_type == 'STOP_LIMIT':
            params['price'] = str(price)
            params['stopPrice'] = str(stop_price)
            params['timeInForce'] = 'GTC'

        logger.info(f"Dispatching Order Request Payload: {params}")

        try:
            # Issue payload natively through the futures order placement path
            response = self.wrapper.client.futures_create_order(**params)
            logger.info(f"Order processed successfully by Exchange matching engine. OrderID: {response.get('orderId')}")
            logger.debug(f"Complete Exchange Response Frame: {response}")
            return True, response
            
        except BinanceAPIException as api_err:
            logger.error(f"Binance Core Exchange API Failure [{api_err.status_code}]: {api_err.message}")
            return False, {"error": "API_EXCHANGE_REJECTED", "details": api_err.message}
        except BinanceOrderException as order_err:
            logger.error(f"Local Execution Structural Processing Error: {order_err.message}")
            return False, {"error": "ORDER_MALFORMED", "details": order_err.message}
        except Exception as system_err:
            logger.exception(f"Unexpected connection or internal runtime pipeline fault: {str(system_err)}")
            return False, {"error": "SYSTEM_FAULT", "details": str(system_err)}