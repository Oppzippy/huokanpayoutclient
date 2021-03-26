import unittest
import os
from datetime import datetime
from decimal import Decimal

from huokanpayoutclient.huokanpayout.payoutsearch import search_payouts

PATH = os.path.dirname(os.path.realpath(__file__))


class PayoutSearchTest(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        # pylint: disable=invalid-name
        self.maxDiff = None

    def test_search_no_params(self):
        results = list(search_payouts(os.path.join(PATH, "_retail_")))

        self.assertCountEqual(
            results,
            [
                {
                    "recipientName": "Player1",
                    "timestamp": datetime.fromtimestamp(0),
                    "gold": Decimal(1),
                },
                {
                    "recipientName": "Player2",
                    "timestamp": datetime.fromtimestamp(0),
                    "gold": Decimal(2),
                },
                {
                    "recipientName": "Player3",
                    "timestamp": datetime.fromtimestamp(0),
                    "gold": Decimal(3),
                },
                {
                    "recipientName": "Player1",
                    "timestamp": datetime.fromtimestamp(1),
                    "gold": Decimal(1),
                },
                {
                    "recipientName": "Player5",
                    "timestamp": datetime.fromtimestamp(1),
                    "gold": Decimal(5),
                },
                {
                    "recipientName": "Player1",
                    "timestamp": datetime.fromtimestamp(2),
                    "gold": Decimal(1),
                },
                {
                    "recipientName": "Player6",
                    "timestamp": datetime.fromtimestamp(2),
                    "gold": Decimal(6),
                },
                {
                    "recipientName": "Player1",
                    "timestamp": datetime.fromtimestamp(3),
                    "gold": Decimal(1),
                    "senderName": "Sender",
                    "senderRealm": "Realm",
                },
                {
                    "recipientName": "Someone",
                    "timestamp": datetime.fromtimestamp(3),
                    "gold": Decimal(1),
                    "senderName": "Sender",
                    "senderRealm": "Realm",
                },
            ],
        )
