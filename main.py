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
            hist = stock.history(period="2d")
            if len(hist) >= 2:
                price  = round(float(hist["Close"].iloc[-1]), 2)
                prev   = round(float(hist["Close"].iloc[-2]), 2)
                change = round(price - prev, 2)
                changeP = round(((price - prev) / prev) * 100, 2)
                high52 = round(float(hist["High"].max()), 2)
                low52  = round(float(hist["Low"].min()), 2)
            elif len(hist) == 1:
                price   = round(float(hist["Close"].iloc[-1]), 2)
                change  = 0.0
                changeP = 0.0
                high52  = price
                low52   = price
            else:
                result[ticker] = {"error": "no data"}
                continue
 
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
