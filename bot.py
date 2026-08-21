```python
import os
from urllib.parse import quote_plus

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes


BOT_TOKEN = os.environ["BOT_TOKEN"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 Welcome to Saksham Music Bot!\n\n"
        "🔎 Song search karne ke liye:\n"
        "/play <song name>\n\n"
        "Example:\n"
        "/play Arijit Singh"
    )


async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "❌ Song name likho!\n\n"
            "Example:\n"
            "/play Arijit Singh"
        )
        return

    song_name = " ".join(context.args)

    # YouTube search URL
    search_query = quote_plus(song_name)
    youtube_url = f"https://www.youtube.com/results?search_query={search_query}"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "▶️ SEARCH ON YOUTUBE",
                url=youtube_url
            )
        ]
    ])

    await update.message.reply_text(
        f"🎵 *Song:* {song_name}\n\n"
        "🔎 YouTube par search karne ke liye niche button dabao 👇",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 *SAKSHAM MUSIC BOT COMMANDS*\n\n"
        "/start - Start the bot\n"
        "/play <song name> - Search a song on YouTube\n"
        "/help - Show commands",
        parse_mode="Markdown"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))
    app.add_handler(CommandHandler("help", help_command))

    print("🎵 SAKSHAM MUSIC BOT IS RUNNING...")

    app.run_polling()


if __name__ == "__main__":
    main()
```
