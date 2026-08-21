import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.environ["BOT_TOKEN"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 Welcome to Saksham Music Bot!\n\n"
        "Song search karne ke liye:\n"
        "/play <song name>"
    )


async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "❌ Song name likho!\n\n"
            "Example:\n/play Arijit Singh"
        )
        return

    song_name = " ".join(context.args)

    await update.message.reply_text(
        f"🔎 Searching for: {song_name}\n\n"
        "🎵 Search feature ka next part ab add karenge!"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))

    print("🎵 MUSIC BOT IS RUNNING...")

    app.run_polling()


if __name__ == "__main__":
    main()
