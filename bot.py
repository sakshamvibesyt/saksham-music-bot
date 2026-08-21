```python
import os
import threading

from flask import Flask
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import MediaStream


# =========================
# ENVIRONMENT VARIABLES
# =========================

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
SESSION_STRING = os.environ["SESSION_STRING"]


# =========================
# TELEGRAM CLIENTS
# =========================

bot = Client(
    "saksham_music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True
)

assistant = Client(
    "saksham_music_assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    in_memory=True
)

calls = PyTgCalls(assistant)


# =========================
# RENDER WEB SERVER
# =========================

web_app = Flask(__name__)


@web_app.route("/")
def home():
    return "SAKSHAM MUSIC VC BOT IS RUNNING!"


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
# START COMMAND
# =========================

@bot.on_message(filters.command("start"))
async def start_command(_, message):

    await message.reply_text(
        "🎵 **SAKSHAM VC MUSIC BOT**\n\n"
        "Commands:\n\n"
        "▶️ /play <authorized_audio_url>\n"
        "⏸ /pause\n"
        "▶️ /resume\n"
        "⏹ /stop\n\n"
        "Example:\n"
        "`/play https://example.com/audio.mp3`"
    )


# =========================
# PLAY
# =========================

@bot.on_message(filters.command("play") & filters.group)
async def play_command(_, message):

    if len(message.command) < 2:
        await message.reply_text(
            "❌ Audio URL do.\n\n"
            "Example:\n"
            "`/play https://example.com/audio.mp3`"
        )
        return

    media_url = message.text.split(None, 1)[1].strip()
    chat_id = message.chat.id

    try:
        await calls.play(
            chat_id,
            MediaStream(media_url)
        )

        await message.reply_text(
            "🎵 **Playing in Voice Chat!**\n\n"
            f"🔗 Source: {media_url}"
        )

    except Exception as error:
        await message.reply_text(
            f"❌ Play error:\n`{error}`"
        )


# =========================
# PAUSE
# =========================

@bot.on_message(filters.command("pause") & filters.group)
async def pause_command(_, message):

    try:
        await calls.pause(message.chat.id)
        await message.reply_text("⏸ Music paused.")

    except Exception as error:
        await message.reply_text(
            f"❌ Error:\n`{error}`"
        )


# =========================
# RESUME
# =========================

@bot.on_message(filters.command("resume") & filters.group)
async def resume_command(_, message):

    try:
        await calls.resume(message.chat.id)
        await message.reply_text("▶️ Music resumed.")

    except Exception as error:
        await message.reply_text(
            f"❌ Error:\n`{error}`"
        )


# =========================
# STOP
# =========================

@bot.on_message(filters.command("stop") & filters.group)
async def stop_command(_, message):

    try:
        await calls.leave_call(message.chat.id)
        await message.reply_text("⏹ Music stopped and left VC.")

    except Exception as error:
        await message.reply_text(
            f"❌ Error:\n`{error}`"
        )


# =========================
# MAIN
# =========================

def main():

    # Start Flask server for Render
    threading.Thread(
        target=run_web_server,
        daemon=True
    ).start()

    # Start bot + assistant + voice calls
    bot.start()
    calls.start()

    print("🎵 SAKSHAM VC MUSIC BOT IS RUNNING...")

    idle()


if __name__ == "__main__":
    main()
```
