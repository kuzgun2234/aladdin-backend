from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

TICKERS = ["RKLB", "BWXT", "RTX", "AXON", "LMT", "GEV"]
API_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "B79Y1937UOCMMZMS")

@app.route("/prices")
def get_prices():
    result = {}
    for ticker in TICKERS:
        try:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}"
            r = requests.get(url, timeout=10)
            data = r.json()
            quote = data.get("Global Quote", {})

            if not quote or not quote.get("05. price"):
                result[ticker] = {"error": "no data"}
                continue

            price   = round(float(quote["05. price"]), 2)
            change  = round(float(quote["09. change"]), 2)
            changeP = round(float(quote["10. change percent"].replace("%", "")), 2)
            high52  = round(float(quote.get("03. high", price)), 2)
            low52   = round(float(quote.get("04. low", price)), 2)

            result[ticker] = {
                "price":   price,
                "change":  change,
                "changeP": changeP,
                "high52":  high52,
                "low52":   low52,
            }
        except Exception as e:
            result[ticker] = {"error": str(e)}

    return jsonify(result)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
