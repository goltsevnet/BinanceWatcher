import pytest
from decimal import Decimal

from Watcher import Watcher

watcher = Watcher()


def generate_msg(price: str):
    return {
        "e": "aggTrade",
        "E": 1672515782136,
        "s": "SomeSymbol",  # Любая строка, проверки на нее сейчас нет
        "a": 12345,
        "p": price,
        "q": "100",
        "f": 100,
        "l": 105,
        "T": 1672515782136,
        "m": True,
        "M": True,
    }


"""
Тривиальная проверка функции на реагирование изменения цены
"""


def test_logic():
    """Первая цена всегда False"""
    assert watcher.mor_than_1_percent(generate_msg("0.1")) is False

    """Цена упала менее чем на 1%"""
    assert watcher.mor_than_1_percent(generate_msg("0.0991")) is False

    """Цена выросла ровно на 1%"""
    assert watcher.mor_than_1_percent(generate_msg("0.101")) is True

    """Цена упала ровно на 1%"""
    assert watcher.mor_than_1_percent(generate_msg("0.099")) is True
