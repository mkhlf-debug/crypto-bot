import os
import requests

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

TARGET_SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "DOGEUSDT"]


def get_crypto_prices_text():
    message = "اخبارك يا درش دي اسعار العملات الحالي 📈:\n"
    for symbol in TARGET_SYMBOLS:
        url = "https://data-api.binance.vision/api/v3/ticker/price"
        try:
            response = requests.get(url, params={"symbol": symbol}, timeout=15).json()
            if "price" in response:
                price = round(float(response["price"]), 4)
                clean_name = symbol.replace("USDT", "")
                message += f"- {clean_name}: {price} $\n"
            else:
                print(f"رد غير متوقع لـ {symbol}: {response}")
        except Exception as e:
            print(f"خطأ في السعر {symbol}: {e}")
    return message


def send_to_telegram(text):
    r = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text},
        timeout=15,
    )
    r.raise_for_status()
    print("تم الإرسال بنجاح")


if __name__ == "__main__":
    send_to_telegram(get_crypto_prices_text())