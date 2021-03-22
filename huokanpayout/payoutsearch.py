import os
import glob
import csv
from datetime import datetime
from decimal import Decimal
from typing import Iterable, List
from slpp import slpp


def search_payouts(wow_path: str, name: str = None) -> Iterable[dict]:
    filtered_payments = get_and_parse_history(wow_path)
    if name is not None:
        name = name.lower()
        filtered_payments = filter(
            lambda payment: payment["name"].lower().startswith(name), filtered_payments
        )
    return filtered_payments


def get_and_parse_history(wow_path: str) -> List[dict]:
    history = get_history(wow_path)
    return parse_history(history)


def parse_history(history: list) -> List[dict]:
    completed_payments = []
    for payment_batch in history:
        input_payments = read_payments_csv(payment_batch["input"])
        output_payments = read_payments_csv(payment_batch.get("output", ""))
        payments = get_completed_payments(input_payments, output_payments)
        transformed_payments = [
            {
                "name": name,
                "gold": gold,
                "timestamp": datetime.fromtimestamp(int(payment_batch["timestamp"])),
            }
            for name, gold in payments.items()
        ]
        completed_payments.extend(transformed_payments)
    return completed_payments


def read_payments_csv(history: str) -> dict:
    payments = {}
    for row in csv.DictReader(history.split("\\n"), fieldnames=["name", "gold"]):
        payments[row["name"]] = Decimal(payments.get(row["name"], 0)) + Decimal(
            row["gold"]
        )
    return payments


def get_completed_payments(
    input_payments: dict[str, Decimal], output_payments: dict[str, Decimal]
) -> dict[str, Decimal]:
    diff = input_payments.copy()
    for name, gold in output_payments.items():
        diff["name"] = diff.get(name, Decimal(0)) - gold
        if diff["name"] == Decimal(0):
            del diff["name"]
    return diff


def get_history(wow_path: str) -> list:
    savedvariables_files = find_files(wow_path)
    if len(savedvariables_files) == 0:
        raise InvalidWoWDirectoryException(wow_path)
    savedvariables = read_files(savedvariables_files)
    history = []
    for savedvariable in savedvariables:
        profiles = savedvariable["profiles"]
        for profile in profiles.values():
            history.extend(profile["history"])
    return history


def find_files(wow_path: str) -> List[str]:
    account_path = os.path.join(
        wow_path, "WTF", "Account", "*", "SavedVariables", "HuokanPayout.lua"
    )
    return glob.glob(account_path)


def read_files(files: Iterable) -> Iterable:
    return map(lambda f: read_file(f), files)


def read_file(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        text = "\n".join(lines)
        text = text.replace("HuokanPayoutDB = {", "{", 1)
        table = slpp.decode(text)
        return table


class InvalidWoWDirectoryException(Exception):
    pass
