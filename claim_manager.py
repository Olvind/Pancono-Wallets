import time
from pancono import blockchain

claims = {}  # {user_id: {"last_claim": timestamp, "claimed_hours": int}}

def start_claim(user_id, address):
    claims[user_id] = {"last_claim": time.time(), "claimed_hours": 0, "address": address}
    return "Auto-claim started for 24 hours."

def check_claims():
    now = time.time()
    for user_id, data in list(claims.items()):
        elapsed_hours = int((now - data["last_claim"]) / 3600)
        if elapsed_hours > data["claimed_hours"] and data["claimed_hours"] < 24:
            blockchain.wallets[data["address"]]["balance"] += 0.005
            claims[user_id]["claimed_hours"] += 1
        if claims[user_id]["claimed_hours"] >= 24:
            del claims[user_id]
