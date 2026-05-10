from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)

TICKERS = ["RKLB", "BWXT", "RTX", "AXON", "LMT", "GEV"]

@app.route("/prices")
def get_prices():
    result = {}
    for ticker in TICKERS:
        try:
            stock = yf.Ticker(ticker)
            info = stock.fast_info
            price = round(info.last_price, 2)
            prev  = round(info.previous_close, 2)
            change = round(price - prev, 2)
            changeP = round(((price - prev) / prev) * 100, 2)
            result[ticker] = {
                "price": price,
                "change": change,
                "changeP": changeP,
                "high52": round(info.year_high, 2),
                "low52": round(info.year_low, 2),
            }
        except Exception as e:
            result[ticker] = {"error": str(e)}
    return jsonify(result)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
