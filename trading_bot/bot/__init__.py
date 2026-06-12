"""
Trading Bot Module
Exposes core functional structures for client connectivity and order management.
"""

from bot.client import BinanceFuturesClient
from bot.orders import OrderManager
from bot.logging_config import logger

__all__ = ["BinanceFuturesClient", "OrderManager", "logger"]