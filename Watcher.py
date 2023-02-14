import os
import signal
import certifi

from decimal import Decimal
from binance.websocket.spot.websocket_client import SpotWebsocketClient

signal.signal(signal.SIGINT, signal.SIG_DFL)


class Watcher:
    """
    Мониторинг криптовалюты через Websocket Protocol.
    Старт функции Watcher().start_watcher("xrpusdt").
    Сообщение в консоли об изменении цены на 1%.
    Для цен используется Decimal.
    """

    """Используем сертификат для SSL"""
    os.environ["SSL_CERT_FILE"] = certifi.where()

    def __init__(self):
        self.init_price: Decimal or None = None  # Цена от которой считаем 1%
        self.ws_client = SpotWebsocketClient()  # Клиент Websocket

    def stream_message_handle(self, msg) -> None:
        """
        Обрабатывает сообщения содержащие "Close price"
        :param msg: {
            "e": "aggTrade",    // Event type
            "E": 1672515782136, // Event time
            "s": "BNBBTC",      // Symbol
            "a": 12345,         // Aggregate trade ID
            "p": "0.001",       // Price
            "q": "100",         // Quantity
            "f": 100,           // First trade ID
            "l": 105,           // Last trade ID
            "T": 1672515782136, // Trade time
            "m": true,          // Is the buyer the market maker?
            "M": true           // Ignore
        }
        """
        if "p" in msg:  # Если сообщение содержит Price
            self.mor_than_1_percent(msg)

    def mor_than_1_percent(self, msg) -> bool:
        """
        Если разница цен больше чем 1:100, то цена изменилась более чем на 1%.
        """
        price = Decimal(msg["p"])

        """Если нет исходной цены, записываем"""
        if not self.init_price:
            self.init_price = price

        if round(self.init_price / 100, 8) <= abs(self.init_price - price):
            """Выполняем действие"""
            self.action(price)
            """Записываем новую цену закрытия от которой будет считать 1%"""
            self.init_price = Decimal(msg["p"])
            return True
        return False

    def action(self, price):
        print(
            f"Цена изменилась минимум на 1% от цены {self.init_price} "
            f"на {abs(self.init_price - price)} \n"
            f"Записываем текущую цену для отслеживания дальнейших "
            f"изменений на 1%"
        )

    def start_watcher(self, name_pair: str):
        """Подключаемся к mini_ticker через Websocket"""
        self.ws_client.start()
        self.ws_client.agg_trade(
            symbol=name_pair, id=1, callback=self.stream_message_handle
        )

    def close_stream(self):
        self.ws_client.close()
