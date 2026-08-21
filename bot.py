import os
import asyncio
import threading

from flask import Flask
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream


# =========================
# ENVIRONMENT VARIABLES
# =========================

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
SESSION_STRING = os.environ["SESSION_STRING"]


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
# TELEGRAM CLIENTS
# =========================

bot = Client(
    "saksham_music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

user = Client(
    "saksham_music_assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    in_memory=True
)

calls = PyTgCalls(user)


# =========================
# COMMANDS
# =========================

@bot.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(
        "🎵 Welcome to Saksham Music Bot!\n\n"
        "Use:\n"
        "/play <audio URL>\n\n"
        "Example:\n"
        "/play https://example.com/song.mp3"
    )


@bot.on_message(filters.command("play"))
async def play_command(client, message):

    if len(message.command) < 2:
        await message.reply_text(
            "❌ Usage:\n"
            "/play <audio URL>"
        )
        return

    if not message.chat.id:
        return

    audio_url = message.text.split(
        None,
        1
    )[1]

    try:
        await message.reply_text(
            "🎵 Starting music..."
        )

        await calls.play(
            message.chat.id,
            MediaStream(audio_url)
        )

        await message.reply_text(
            "▶️ Music started in voice chat!"
        )

    except Exception as error:
        await message.reply_text(
            f"❌ Error:\n{error}"
        )


@bot.on_message(filters.command("stop"))
async def stop_command(client, message):

    try:
        await calls.leave_call(
            message.chat.id
        )

        await message.reply_text(
            "⏹ Music stopped!"
        )

    except Exception as error:
        await message.reply_text(
            f"❌ Error:\n{error}"
        )


# =========================
# MAIN
# =========================

async def main():

    await bot.start()

    await calls.start()

    print("🎵 SAKSHAM MUSIC BOT IS RUNNING!")

    await asyncio.Event().wait()


if __name__ == "__main__":

    threading.Thread(
        target=run_web,
        daemon=True
    ).start()

    asyncio.run(main())
