from flask import Flask, request
import requests, os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")

def send(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text,
        "disable_web_page_preview": True
    }, timeout=10)
    r.raise_for_status()

@app.get("/")
def home():
    return "OK"

@app.post("/tv")
def tv():
    d = request.get_json(force=True, silent=True) or {}

    t = d.get("type", "")
    symbol = d.get("symbol", "—")
    side = d.get("side", "—")
    entry = d.get("entry", "—")
    sl = d.get("sl", "—")
    tp = d.get("tp", "—")

    if t == "ENTRY":
        rr = d.get("rr", "—")
        logic = d.get("logic", "—")
        msg = (
            f"🟢 {side} {symbol}\n"
            f"Entry: {entry}\n"
            f"SL: {sl}\n"
            f"TP: {tp}\n"
            f"RR: {rr}\n"
            f"{logic}"
        )
        send(msg)

    elif t == "RESULT":
        res = d.get("result", "—")
        emoji = "✅" if res == "TP" else "❌"
        msg = (
            f"{emoji} RESULT {symbol}\n"
            f"{side}\n"
            f"{res} HIT\n"
            f"Entry: {entry}\n"
            f"SL: {sl}\n"
            f"TP: {tp}"
        )
        send(msg)

    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
