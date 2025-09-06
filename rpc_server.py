from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pancono.blockchain import Blockchain, Wallet  # import your repo classes

blockchain = Blockchain()

class RPCHandler(BaseHTTPRequestHandler):
    def _send_response(self, result=None, error=None, id=None):
        response = {
            "jsonrpc": "2.0",
            "id": id,
            "result": result,
            "error": error
        }
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        req = json.loads(body)

        method = req.get("method")
        params = req.get("params", [])
        req_id = req.get("id")

        try:
            if method == "getnewaddress":
                wallet = Wallet()
                address = wallet.get_address()
                result = {"address": address, "private_key": wallet.private_key}
            elif method == "getbalance":
                address = params[0]
                result = blockchain.get_balance(address)
            elif method == "sendtoaddress":
                from_addr, to_addr, amount = params
                tx = blockchain.create_transaction(from_addr, to_addr, amount)
                result = tx.to_dict()
            elif method == "generate":
                result = blockchain.mine_block()
            else:
                raise Exception(f"Unknown method: {method}")

            self._send_response(result=result, id=req_id)

        except Exception as e:
            self._send_response(error=str(e), id=req_id)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8332), RPCHandler)
    print("🚀 Pancono RPC Server running at http://127.0.0.1:8332")
    server.serve_forever()
