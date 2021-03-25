import unittest
import os
from datetime import datetime
from decimal import Decimal

from huokanpayout.payoutsearch import search_payouts

PATH = os.path.dirname(os.path.realpath(__file__))


class PayoutSearchTest(unittest.TestCase):
    def test_search_no_params(self):
        results = list(search_payouts(os.path.join(PATH, "_retail_")))

        self.assertCountEqual(
            results,
            [
                {
                    "name": "Player1",
                    "timestamp": datetime.fromtimestamp(0),
                    "gold": Decimal(1),
                },
                {
                    "name": "Player2",
                    "timestamp": datetime.fromtimestamp(0),
                    "gold": Decimal(2),
                },
                {
                    "name": "Player3",
                    "timestamp": datetime.fromtimestamp(0),
                    "gold": Decimal(3),
                },
                {
                    "name": "Player1",
                    "timestamp": datetime.fromtimestamp(1),
                    "gold": Decimal(1),
                },
                {
                    "name": "Player5",
                    "timestamp": datetime.fromtimestamp(1),
                    "gold": Decimal(5),
                },
                {
                    "name": "Player1",
                    "timestamp": datetime.fromtimestamp(2),
                    "gold": Decimal(1),
                },
                {
                    "name": "Player6",
                    "timestamp": datetime.fromtimestamp(2),
                    "gold": Decimal(6),
                },
                {
                    "name": "Player1",
                    "timestamp": datetime.fromtimestamp(3),
                    "gold": Decimal(1),
                },
                {
                    "name": "Someone",
                    "timestamp": datetime.fromtimestamp(3),
                    "gold": Decimal(1),
                },
            ],
        )
