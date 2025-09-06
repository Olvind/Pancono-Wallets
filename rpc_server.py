from flask import Flask, request, jsonify
from pancono import blockchain

app = Flask(__name__)

@app.route("/", methods=["POST"])
def rpc():
    data = request.get_json()
    method = data.get("method")
    params = data.get("params", [])
    response = {"jsonrpc": "2.0", "id": data.get("id", 1)}

    try:
        if method == "getbalance":
            response["result"] = blockchain.get_balance(params[0])
        elif method == "send":
            response["result"] = blockchain.send(params[0], params[1], params[2])
        elif method == "createwallet":
            response["result"] = blockchain.create_wallet()
        else:
            response["error"] = "Unknown method"
    except Exception as e:
        response["error"] = str(e)

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8332)
