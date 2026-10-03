from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

# =========================================================
# MODIFICA SOLO LE DUE RIGHE QUI SOTTO CON I TUOI DATI:
# =========================================================

TOKEN = "8526126293:AAF-xjsshnhP3riuQ3_9cfCNL4uBWc9JqAU"
# Esempio di come dovrà diventare:
# TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"

CHAT_ID = 5869107307
# Esempio di come dovrà diventare:
# CHAT_ID = 987654321

# =========================================================

COMUNI = {
    "monta": {
        "nome": "Montà (CN)",
        "lat": 44.78,
        "lon": 7.82,
    },
    "realmente": {
        "nome": "Realmonte (AG)",
        "lat": 37.30,
        "lon": 13.52,
    },
}

def prendi_meteo(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
    }
    risposta = requests.get(url, params=params)
    risposta.raise_for_status()
    return risposta.json()

def codice_condizioni(codice):
    if codice == 0:
        return "Cielo sereno"
    elif 1 <= codice <= 3:
        return "Parzialmente nuvoloso"
    elif 45 <= codice <= 48:
        return "Nebbia"
    elif 51 <= codice <= 67:
        return "Pioggia"
    elif 71 <= codice <= 77:
        return "Neve"
    elif 80 <= codice <= 82:
        return "Piogge locali"
    elif 95 <= codice <= 99:
        return "Temporale"
    else:
        return "Condizioni variabili"

async def meteo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        testo = (
            "Comandi disponibili:\n"
            "/meteo monta\n"
            "/meteo realmonte\n"
            "/meteo entrambi"
        )
        await update.message.reply_text(testo)
        return

    chiave = context.args[0].lower()

    chiavi_da_usare = []
    if chiave == "monta":
        chiavi_da_usare = ["monta"]
    elif chiave in ["realmente", "realmonte"]:
        chiavi_da_usare = ["realmente"]
    elif chiave == "entrambi":
        chiavi_da_usare = ["monta", "realmente"]
    else:
        await update.message.reply_text(
            "Comune non riconosciuto.\n"
            "Usa: monta, realmonte o entrambi."
        )
        return

    testi = []
    for k in chiavi_da_usare:
        comune = COMUNI[k]
        dati = prendi_meteo(comune["lat"], comune["lon"])
        meteo = dati["current_weather"]
        temp = meteo["temperature"]
        vento = meteo["windspeed"]
        codice = meteo["weathercode"]
        condizioni = codice_condizioni(codice)

        testo = (
            f"Meteo per {comune['nome']}\n"
            f"Temperatura: {temp} °C\n"
            f"Vento: {vento} km/h\n"
            f"Condizioni: {condizioni}"
        )
        testi.append(testo)

    for t in testi:
        await update.message.reply_text(t)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    testo = (
        "Ciao! Sono il tuo bot meteo per Montà e Realmonte.\n\n"
        "Comandi:\n"
        "/meteo monta\n"
        "/meteo realmonte\n"
        "/meteo entrambi\n\n"
        "Scrivi uno di questi comandi nella chat con me."
    )
    await update.message.reply_text(testo)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("meteo", meteo))
    print("Bot in esecuzione... (non chiudere questa finestra)")
    app.run_polling()

if __name__ == "__main__":
    main()