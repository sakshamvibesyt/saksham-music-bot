import os
import asyncio
import threading

from flask import Flask
from pyrogram import Client, filters
from pytgcalls import PyTgCalls


# =========================
# ENVIRONMENT VARIABLES
# =========================

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
SESSION_STRING = os.environ["SESSION_STRING"]


# =========================
# FLASK SERVER
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
# USER SESSION
# =========================

user = Client(
    "saksham_music_assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)


# =========================
# PYTGCALLS
# =========================

calls = PyTgCalls(user)


# =========================
# START
# =========================

@bot.on_message(filters.command("start"))
async def start_command(client, message):

    await message.reply_text(
        "🎵 Welcome to Saksham Music Bot!\n\n"
        "✅ Bot is online!\n"
        "🎧 Music system is starting..."
    )


# =========================
# PLAY TEST
# =========================

@bot.on_message(filters.command("play"))
async def play_command(client, message):

    await message.reply_text(
        "🎵 Music command received!\n\n"
        "Song playback system will start next."
    )


# =========================
# MAIN
# =========================

async def main():

    threading.Thread(
        target=run_web,
        daemon=True
    ).start()

    print("===================================")
    print("🎵 SAKSHAM MUSIC BOT STARTING")
    print("===================================")

    await bot.start()

    print("✅ Telegram Bot Started")

    await user.start()

    print("✅ Assistant Session Started")

    await calls.start()

    print("✅ PyTgCalls Started")
    print("🎵 MUSIC SYSTEM READY!")

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
