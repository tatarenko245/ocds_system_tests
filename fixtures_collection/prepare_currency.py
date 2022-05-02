import random
import pytest

from data_collection.data_constant import currency_tuple


@pytest.fixture
def prepare_currency():
    currency = f"{random.choice(currency_tuple)}"
    return currency
