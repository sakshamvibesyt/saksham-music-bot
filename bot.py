import os
import threading

from flask import Flask
from pyrogram import Client, filters


# =========================
# ENVIRONMENT VARIABLES
# =========================

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]


# =========================
# FLASK SERVER FOR RENDER
# =========================

web_app = Flask(__name__)


@web_app.route("/")
def home():
    return "Saksham Music Bot is running!"


def run_web():
    port = int(os.environ.get("PORT", 10000))

    web_app.run(
        host="0.0.0.0",
        port=port
    )


# =========================
# TELEGRAM BOT
# =========================

bot = Client(
    "saksham_music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# =========================
# START COMMAND
# =========================

@bot.on_message(filters.command("start"))
async def start_command(client, message):

    print(f"Received /start from {message.from_user.id}")

    await message.reply_text(
        "🎵 Welcome to Saksham Music Bot!\n\n"
        "✅ Bot is online and working!\n\n"
        "Music features will be added next."
    )


# =========================
# TEST MESSAGE
# =========================

@bot.on_message(filters.text & ~filters.command(["start"]))
async def test_message(client, message):

    print(
        f"Received message from "
        f"{message.from_user.id}: {message.text}"
    )

    await message.reply_text(
        "🎵 Saksham Music Bot is online!\n\n"
        "Your message was received successfully. ✅"
    )


# =========================
# MAIN
# =========================

def main():

    # Start Flask for Render
    threading.Thread(
        target=run_web,
        daemon=True
    ).start()

    print("===================================")
    print("🎵 SAKSHAM MUSIC BOT")
    print("===================================")
    print("✅ Starting Telegram bot...")
    print("===================================")

    # Start Telegram bot
    bot.run()


if __name__ == "__main__":
    main()
