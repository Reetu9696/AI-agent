import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv
from bot.logging_config import logger

class BinanceFuturesClient:
    """Manages connection, authentication, and state lifecycle with the Binance Testnet."""
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")
        self.client = None
        
        if not self.api_key or not self.api_secret:
            logger.critical("API credentials missing from local execution environment (.env file).")
            raise RuntimeError("Credentials missing. Please verify configuration inside your local .env file.")

    # def connect(self):
    #     """Initializes the underlying client authenticated targeting the USDT-M Testnet endpoints."""
    #     try:
    #         logger.debug("Initializing Binance Testnet Futures Client connection wrapper...")
    #         self.client = Client(
    #             api_key=self.api_key,
    #             api_secret=self.api_secret,
    #             testnet=True  # Points automatically to https://testnet.binancefuture.com
    #         )
    #         # Verify connectivity to endpoints implicitly
    #         self.client.futures_ping()
    #         logger.info("Connected successfully to Binance Futures Testnet infrastructure.")
    #     except Exception as e:
    #         logger.exception(f"Connection setup failed to finalize: {str(e)}")
    #         raise ConnectionError(f"Network handshake or authentication verification dropped: {e}")
    def connect(self):
        """Initializes the underlying client authenticated targeting the USDT-M Testnet endpoints."""
        try:
            logger.debug("Initializing Binance Testnet Futures Client connection wrapper...")
            
            # Initialize with credentials
            self.client = Client(
                api_key=self.api_key,
                api_secret=self.api_secret
            )
            
            # Explicitly force the framework to route requests through the Futures Testnet API layers
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
            
            # Verify connectivity to endpoints implicitly
            self.client.futures_ping()
            logger.info("Connected successfully to Binance Futures Testnet infrastructure.")
        except Exception as e:
            logger.exception(f"Connection setup failed to finalize: {str(e)}")
            raise ConnectionError(f"Network handshake or authentication verification dropped: {e}")