import threading
import os
import bot
import rpc_server

# === 1. Setup RPC host & port ===
RPC_HOST = os.environ.get("RPC_HOST", "0.0.0.0")
RPC_PORT = int(os.environ.get("PORT", 8332))

if hasattr(rpc_server, "HOST"):
    rpc_server.HOST = RPC_HOST
if hasattr(rpc_server, "PORT"):
    rpc_server.PORT = RPC_PORT

# === 2. Start RPC server in a separate thread ===
def run_rpc():
    if hasattr(rpc_server, "run_rpc"):
        rpc_server.run_rpc(host=RPC_HOST, port=RPC_PORT)
    else:
        rpc_server.main()

rpc_thread = threading.Thread(target=run_rpc)
rpc_thread.start()

# === 3. Start Telegram bot ===
if hasattr(bot, "main"):
    bot.main()
else:
    exec(open("bot.py").read())
