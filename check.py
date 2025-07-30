import requests
from bs4 import BeautifulSoup
import os
import time

HEADERS = {"User-Agent": "Mozilla/5.0"}

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
print(f"Chat Id found: {CHAT_ID}")

def check_availability(product_url):
    try:
        print(f"Checking: {product_url}")
        r = requests.get(product_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')

        # Customize this condition based on the site's HTML
        if "There is no Product Here" not in soup.text:
            print(f"✅ Product may be available! {product_url}")
            send_telegram(f"🎉 Product may be available!\n{product_url}")
        else:
            print(f"❌ Still out of stock: {product_url}")
    except Exception as e:
        error_msg = f"⚠️ Error checking product:\n{product_url}\n{e}"
        print(error_msg)
        #send_telegram(error_msg)


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}
    r = requests.post(url, data=payload)
    if r.status_code != 200:
        print(f"Failed to send Telegram message: {r.text}")

def main():
     urls_env = os.environ.get("PRODUCT_URLS")
     if not urls_env:
        print("❌ No PRODUCT_URLS env variable found.")
        return

     urls = [url.strip() for url in urls_env.split(",") if url.strip()]
     if not urls:
        print("❌ No valid URLs to check.")
        return

     for url in urls:
        check_availability(url)
        print("Waiting 60 seconds before next check...")
        time.sleep(60)

if __name__ == "__main__":
    main()
