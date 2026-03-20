import requests

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

def send_telegram_message(message_text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    parameters = {
        "chat_id": CHAT_ID,
        "text": message_text,
        "parse_mode": "HTML"
    }

    requests.post(url, data=parameters)
    print("The message has been successfully sent to Telegram! Check your phone.")


def fortnite_shop():
    print("The bot is running, data is being extracted...")
    url = "https://fortnite-api.com/v2/shop?language=tr"
    cevap = requests.get(url)
    data = cevap.json()

    if cevap.status_code == 200:
        girdiler = data['data'].get('entries', [])

        categories = {
            "📦 PAKETLER": [],
            "👕 KARAKTERLER": [],
            "⛏️ KAZMALAR VE DANSLAR": []
        }

        for esya in girdiler:
            fiyat = esya.get('finalPrice', 0)

            if esya.get('bundle'):
                isim = esya['bundle'].get('name', 'İsimsiz Paket')
                categories["📦 PAKETLER"].append(f"• {isim} | {fiyat} V-Bucks")

            elif esya.get('brItems'):
                br_esya = esya['brItems'][0]
                isim = br_esya.get('name', 'İsimsiz Eşya')
                tur = br_esya.get('type', {}).get('backendValue', 'bilinmeyen').lower()

                if 'athenacharacter' in tur:
                    categories["👕 KARAKTERLER"].append(f"• {isim} | {fiyat} V-Bucks")
                elif 'athenapickaxe' in tur or 'athenadance' in tur:
                    categories["⛏️ KAZMALAR VE DANSLAR"].append(f"• {isim} | {fiyat} V-Bucks")

        final_mesaj = "<b>🛒 GÜNCEL FORTNITE MAĞAZASI</b>\n\n"

        for kategori_adi, esya_listesi in categories.items():
            if len(esya_listesi) > 0:
                final_mesaj += f"<b>=== {kategori_adi} ===</b>\n"

                for esya in esya_listesi[:10]:
                    final_mesaj += f"{esya}\n"

                if len(esya_listesi) > 10:
                    final_mesaj += f"<i>...ve {len(esya_listesi) - 10} eşya daha</i>\n"

                final_mesaj += "\n"

        send_telegram_message(final_mesaj)

    else:
        print(f"Error! Server Code: {cevap.status_code}")


fortnite_shop()