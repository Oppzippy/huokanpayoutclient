import os
import glob
import csv
from datetime import datetime
from decimal import Decimal
from typing import Iterable, List, Dict
from slpp import slpp


ONE_GOLD = Decimal(1_00_00)


def search_payouts(
    wow_path: str,
    recipient_name: str = None,
    sender_name: str = None,
    sender_realm: str = None,
) -> Iterable[dict]:
    filtered_payments = get_and_parse_history(wow_path)
    if recipient_name is not None:
        filtered_payments = filter_by_key_case_insensitive(
            filtered_payments, "recipientName", recipient_name
        )
    if sender_name is not None:
        filtered_payments = filter_by_key_case_insensitive(
            filtered_payments, "senderName", sender_name
        )
    if sender_realm is not None:
        filtered_payments = filter_by_key_case_insensitive(
            filtered_payments, "senderRealm", sender_realm
        )
    return filtered_payments


def filter_by_key_case_insensitive(
    iterable_to_filter: Iterable[dict], key, search: str
) -> Iterable[dict]:
    search = search.lower()
    return filter(
        lambda item: item.get(key, "").lower().startswith(search), iterable_to_filter
    )


def get_and_parse_history(wow_path: str) -> List[dict]:
    history = get_history(wow_path)
    return parse_history(history)


def parse_history(history: List[dict]) -> List[dict]:
    completed_payments = []
    for payment_batch in history:
        input_payments = read_payments_csv(payment_batch["input"])
        output_payments = read_payments_csv(payment_batch.get("output", ""))
        payments = get_completed_payments(input_payments, output_payments)
        unit = Decimal(payment_batch.get("unit", ONE_GOLD))
        sender = {}
        if "sender" in payment_batch:
            sender["senderName"] = payment_batch["sender"]["name"]
            sender["senderRealm"] = payment_batch["sender"]["realm"]
        transformed_payments = [
            {
                "recipientName": name,
                "gold": round(money / unit * ONE_GOLD, 4),  # Convert to gold
                "timestamp": datetime.fromtimestamp(int(payment_batch["timestamp"])),
                **sender,
            }
            for name, money in payments.items()
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
    input_payments: Dict[str, Decimal], output_payments: Dict[str, Decimal]
) -> Dict[str, Decimal]:
    diff = input_payments.copy()
    for name, gold in output_payments.items():
        diff[name] = diff.get(name, Decimal(0)) - gold
        if diff[name] == Decimal(0):
            del diff[name]
    return diff


def get_history(wow_path: str) -> list:
    savedvariables_files = find_files(wow_path)
    if len(savedvariables_files) == 0:
        raise InvalidWoWDirectoryException(wow_path)
    savedvariables = read_files(savedvariables_files)
    history = []
    for savedvariable in savedvariables:
        if "profiles" in savedvariable:
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
    return filter(lambda sv: sv is not None, map(lambda f: read_file(f), files))


def read_file(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        text = "\n".join(lines)
        text = text.replace("HuokanPayoutDB = {", "{", 1)
        table = slpp.decode(text)
        return table


class InvalidWoWDirectoryException(Exception):
    pass
