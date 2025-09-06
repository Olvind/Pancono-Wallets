import requests
from telegram.ext import Updater, CommandHandler

RPC_URL = "http://127.0.0.1:8332"
API_KEY = "supersecret123"  # must match rpc_server.py

def rpc_call(method, params=[]):
    headers = {"X-API-KEY": API_KEY}
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    response = requests.post(RPC_URL, json=payload, headers=headers).json()
    if "error" in response and response["error"]:
        return f"❌ Error: {response['error']}"
    return response["result"]

def start(update, context):
    update.message.reply_text("🚀 Welcome to Pancono Wallet Bot!\n\nCommands:\n/createwallet\n/balance <address>\n/send <from> <to> <amount>\n/mine")

def create_wallet(update, context):
    result = rpc_call("getnewaddress")
    update.message.reply_text(f"🆕 Wallet created:\nAddress: {result['address']}\nPrivate Key: {result['private_key']}")

def balance(update, context):
    if len(context.args) == 0:
        update.message.reply_text("Usage: /balance <address>")
        return
    result = rpc_call("getbalance", [context.args[0]])
    update.message.reply_text(f"💰 Balance: {result} PANCA")

def send(update, context):
    if len(context.args) != 3:
        update.message.reply_text("Usage: /send <from_addr> <to_addr> <amount>")
        return
    from_addr, to_addr, amount = context.args
    result = rpc_call("sendtoaddress", [from_addr, to_addr, float(amount)])
    update.message.reply_text(f"✅ Transaction sent:\n{result}")

def mine(update, context):
    result = rpc_call("generate")
    update.message.reply_text(f"⛏️ New block mined: {result}")

def main():
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("createwallet", create_wallet))
    dp.add_handler(CommandHandler("balance", balance))
    dp.add_handler(CommandHandler("send", send))
    dp.add_handler(CommandHandler("mine", mine))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
