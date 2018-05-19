from abc import *

from ccxt.base.exchange import Exchange as ccxtExchange

from tools.symbol_util import merge_symbol
from trading import AbstractExchange
from trading.exchanges.exchange_data import ExchangeData


class AbstractWebSocketManager(AbstractExchange):

    def __init__(self, config, exchange_type):
        super().__init__(config, exchange_type)
        self.config = config
        self.client = None
        self.exchange_data = ExchangeData()

    @classmethod
    @abstractmethod
    def get_name(cls):
        raise NotImplementedError("get_name not implemented")

    @staticmethod
    @abstractmethod
    def convert_into_ccxt_order(msg):
        raise NotImplementedError("convert_into_ccxt_order not implemented")

    @staticmethod
    @abstractmethod
    def format_price_ticker(price_ticker):
        raise NotImplementedError("format_price_ticker not implemented")

    @abstractmethod
    def get_last_price_ticker(self, symbol):
        raise NotImplementedError("get_last_price_ticker not implemented")

    @abstractmethod
    def start_sockets(self):
        raise NotImplementedError("start_sockets not implemented")

    @abstractmethod
    def stop_sockets(self):
        raise NotImplementedError("stop_sockets not implemented")

    @staticmethod
    @abstractmethod
    def get_websocket_client(config, exchange_type):
        raise NotImplementedError("get_websocket_client not implemented")

    @abstractmethod
    def init_all_currencies_prices_web_socket(self, time_frames, trader_pairs):
        raise NotImplementedError("init_all_currencies_klines_web_socket not implemented")

    @abstractmethod
    def init_web_sockets(self, time_frames, trader_pairs):
        raise NotImplementedError("init_web_sockets not implemented")

    def last_price_ticker_is_initialized(self, symbol):
        return merge_symbol(symbol) in self.exchange_data.symbol_tickers

    def currency_database_is_initialized(self, symbol):
        return self.exchange_data.is_initialized(symbol)

    def portfolio_is_initialized(self):
        return self.exchange_data.portfolio

    def orders_are_initialized(self):
        return self.exchange_data.is_initialized[ExchangeData.ORDERS_KEY]

    def get_symbol_prices(self, symbol, time_frame, limit=None, data_frame=True):
        pass

    def get_portfolio(self):
        return self.exchange_data.portfolio

    def has_order(self, order_id):
        return order_id in self.exchange_data.orders

    def get_order(self, order_id):
        return self.exchange_data.orders[order_id]

    def get_all_orders(self, symbol, since, limit):
        return self.exchange_data.get_all_orders(symbol, since, limit)

    def get_open_orders(self, symbol, since, limit):
        return self.exchange_data.get_open_orders(symbol, since, limit)

    def get_closed_orders(self, symbol, since, limit):
        return self.exchange_data.get_closed_orders(symbol, since, limit)

    def set_orders_are_initialized(self, value):
        self.exchange_data.is_initialized[ExchangeData.ORDERS_KEY] = value

    def init_ccxt_order_from_other_source(self, ccxt_order):
        self.exchange_data.upsert_order(ccxt_order["id"], ccxt_order)

    def _update_order(self, msg):
        ccxt_order = self.convert_into_ccxt_order(msg)
        self.exchange_data.upsert_order(ccxt_order["id"], ccxt_order)

    # ============== ccxt adaptation methods ==============
    @staticmethod
    @abstractmethod
    def parse_order_status(status):
        raise NotImplementedError("parse_order_status not implemented")

    @staticmethod
    def safe_lower_string(dictionary, key, default_value=None):
        value = AbstractWebSocketManager.safe_string(dictionary, key, default_value)
        if value is not None:
            value = value.lower()
        return value

    @staticmethod
    def safe_string(dictionary, key, default_value=None):
        return ccxtExchange.safe_string(dictionary, key, default_value)

    @staticmethod
    def safe_float(dictionary, key, default_value=None):
        return ccxtExchange.safe_float(dictionary, key, default_value)

    @staticmethod
    def safe_value(dictionary, key, default_value=None):
        return ccxtExchange.safe_value(dictionary, key, default_value)

    @staticmethod
    def iso8601(value):
        return ccxtExchange.iso8601(value)

    # ==============      -------------      ==============

