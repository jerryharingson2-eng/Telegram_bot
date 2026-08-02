from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from datetime import datetime

# توکن بات
BOT_TOKEN = "8694609241:AAGRAd6F5P0SYFKZBgYKRvQWpCz-pHh_gBg"

# کلید آب‌وهوا
WEATHER_API_KEY = "c990b65cc31c1b175e609f9f9484cae9"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "سلام 👋\n"
        "دستورها:\n"
        "/weather شهر\n"
        "/dollar\n"
        "/btc\n"
        "/time"
    )
    await update.message.reply_text(text)


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("نام شهر را بنویس. مثال: /weather Berlin")
        return

    city = " ".join(context.args)

    url = (
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=fa"
    )

    r = requests.get(url).json()

    if r.get("cod") != 200:
        await update.message.reply_text("شهر پیدا نشد ❌")
        return

    temp = r["main"]["temp"]
    desc = r["weather"][0]["description"]

    msg = f"🌤 آب‌وهوای {city}\n🌡 دما: {temp}°C\n📝 وضعیت: {desc}"
    await update.message.reply_text(msg)


async def dollar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # نرخ تقریبی دلار از API رایگان فرانکفورتر
    r = requests.get("https://api.frankfurter.app/latest?from=USD&to=EUR").json()
    rate = r["rates"]["EUR"]

    await update.message.reply_text(
        f"💵 1 دلار آمریکا = {rate} یورو\n(نرخ جهانی تقریبی)"
    )


async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    r = requests.get(
        "https://api.coindesk.com/v1/bpi/currentprice/USD.json"
    ).json()

    price = r["bpi"]["USD"]["rate"]

    await update.message.reply_text(f"₿ قیمت بیت‌کوین: ${price}")


async def time_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"⏰ زمان سیستم: {now}")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("weather", weather))
app.add_handler(CommandHandler("dollar", dollar))
app.add_handler(CommandHandler("btc", btc))
app.add_handler(CommandHandler("time", time_cmd))

print("Bot is running...")

app.run_polling()