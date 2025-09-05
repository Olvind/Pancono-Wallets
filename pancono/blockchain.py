import uuid
import random

wallets = {}  # {address: {"balance": float, "private_key": str}}

def create_wallet():
    address = "PANCA" + str(uuid.uuid4())[:8]
    private_key = str(uuid.uuid4()).replace("-", "")
    wallets[address] = {"balance": 0.0, "private_key": private_key}
    return {"address": address, "private_key": private_key}

def get_balance(address):
    return wallets.get(address, {}).get("balance", 0.0)

def send(sender, recipient, amount):
    if sender not in wallets or recipient not in wallets:
        raise Exception("Invalid address")

    if wallets[sender]["balance"] < amount:
        raise Exception("Insufficient funds")

    wallets[sender]["balance"] -= amount
    wallets[recipient]["balance"] += amount
    return {"from": sender, "to": recipient, "amount": amount}
