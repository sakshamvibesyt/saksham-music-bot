import os
import asyncio
import threading
from urllib.parse import quote_plus

from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes


# =========================
# BOT TOKEN
# =========================

BOT_TOKEN = os.environ["BOT_TOKEN"]


# =========================
# FLASK WEB SERVER
# Render Web Service ke liye
# =========================

web_app = Flask(__name__)


@web_app.route("/")
def home():
    return "🎵 SAKSHAM MUSIC BOT IS RUNNING! 🤖"


@web_app.route("/health")
def health():
    return "OK"


def run_web_server():
    port = int(os.environ.get("PORT", 10000))

    web_app.run(
        host="0.0.0.0",
        port=port,
        use_reloader=False
    )


# =========================
# /start
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "🎵 SEARCH SONG",
                callback_data="search_info"
            )
        ],
        [
            InlineKeyboardButton(
                "▶️ YOUTUBE",
                url="https://www.youtube.com/"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "╔══════════════════════╗\n"
        "     🎵 SAKSHAM MUSIC BOT 🎵\n"
        "╚══════════════════════╝\n\n"
        "✨ Welcome to Saksham Music Bot!\n\n"
        "🎧 Song search karne ke liye:\n\n"
        "▶️ /play <song name>\n\n"
        "Example:\n"
        "/play Arijit Singh\n\n"
        "🔥 Fast • Simple • Music\n"
        "🎶 Enjoy your music!",
        reply_markup=reply_markup
    )


# =========================
# /play
# =========================

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:

        await update.message.reply_text(
            "❌ Song name missing!\n\n"
            "Example:\n"
            "/play Tum Hi Ho"
        )

        return

    song_name = " ".join(context.args)

    search_query = quote_plus(song_name)

    youtube_url = (
        "https://www.youtube.com/results?search_query="
        + search_query
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "▶️ SEARCH ON YOUTUBE",
                url=youtube_url
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"🎵 Song: {song_name}\n\n"
        "🔎 YouTube search ready!\n"
        "👇 Button dabakar song dekho:",
        reply_markup=reply_markup
    )


# =========================
# /help
# =========================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🎵 SAKSHAM MUSIC BOT\n\n"
        "📌 Commands:\n\n"
        "/start - Start bot\n"
        "/play <song> - Search song\n"
        "/help - Help\n\n"
        "Example:\n"
        "/play Kesariya"
    )


# =========================
# TELEGRAM BOT
# =========================

async def run_bot():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("play", play)
    )

    app.add_handler(
        CommandHandler("help", help_command)
    )

    print("🎵 SAKSHAM MUSIC BOT IS RUNNING...")

    await app.initialize()

    await app.start()

    await app.updater.start_polling()

    try:
        while True:
            await asyncio.sleep(3600)

    finally:

        await app.updater.stop()
        await app.stop()
        await app.shutdown()


# =========================
# MAIN
# =========================

def main():

    # Start Render web server
    web_thread = threading.Thread(
        target=run_web_server,
        daemon=True
    )

    web_thread.start()

    # Start Telegram bot
    asyncio.run(run_bot())


if __name__ == "__main__":
    main()
