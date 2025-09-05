import os
import requests
import threading
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv
import claim_manager

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RPC_URL = f"http://{os.getenv('RPC_HOST')}:{os.getenv('RPC_PORT')}"

# JSON-RPC helper
def rpc_call(method, params=[]):
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    r = requests.post(RPC_URL, json=payload)
    return r.json().get("result")

# Commands
def start(update: Update, context: CallbackContext):
    update.message.reply_text("🚀 Welcome to Pancono Wallet Bot!\nUse /createwallet to get started.")

def createwallet(update: Update, context: CallbackContext):
    wallet = rpc_call("createwallet")
    update.message.reply_text(f"✅ Wallet created!\nAddress: {wallet['address']}\nPrivate Key: {wallet['private_key']}")

def balance(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Usage: /balance <address>")
        return
    bal = rpc_call("getbalance", [context.args[0]])
    update.message.reply_text(f"💰 Balance: {bal} PANCA")

def send(update: Update, context: CallbackContext):
    if len(context.args) != 3:
        update.message.reply_text("Usage: /send <from_address> <to_address> <amount>")
        return
    try:
        tx = rpc_call("send", [context.args[0], context.args[1], float(context.args[2])])
        update.message.reply_text(f"✅ Sent {tx['amount']} PANCA from {tx['from']} → {tx['to']}")
    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")

def startclaim(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Usage: /startclaim <address>")
        return
    msg = claim_manager.start_claim(update.effective_user.id, context.args[0])
    update.message.reply_text(msg)

# Background thread for auto-claim
def run_claim_checker():
    while True:
        claim_manager.check_claims()
        time.sleep(3600)  # check hourly

if __name__ == "__main__":
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("createwallet", createwallet))
    dp.add_handler(CommandHandler("balance", balance))
    dp.add_handler(CommandHandler("send", send))
    dp.add_handler(CommandHandler("startclaim", startclaim))

    threading.Thread(target=run_claim_checker, daemon=True).start()

    updater.start_polling()
    updater.idle()
