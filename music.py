import telebot
import os
from yt_dlp import YoutubeDL

TOKEN = "8495094901:AAFjIE8Z1yeFHrBQ70cuNEhwYNmXwFRU0yk"

bot = telebot.TeleBot(TOKEN)

DOWNLOADS = "downloads"

if not os.path.exists(DOWNLOADS):
    os.makedirs(DOWNLOADS)


@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(message.chat.id, """
🎵 Instagram Music Bot

Instagram reel link yuboring 🚀
""")


@bot.message_handler(func=lambda m: True)
def instagram(message):

    url = message.text

    if "instagram.com" not in url:

        bot.send_message(
            message.chat.id,
            "❌ Instagram link yuboring"
        )

        return

    bot.send_message(
        message.chat.id,
        "📥 Reel tekshirilmoqda..."
    )

    try:

        ydl_opts = {
            'quiet': True
        }

        with YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                url,
                download=False
            )

            title = info.get("title", "")

        bot.send_message(
            message.chat.id,
            f"🔎 Qidirildi:\n{title}"
        )

        search_song(message.chat.id, title)

    except Exception as e:

        bot.send_message(
            message.chat.id,
            f"❌ Xatolik:\n{e}"
        )


def search_song(chat_id, query):

    try:

        ydl_opts = {
            'format': 'bestaudio',
            'quiet': True,
            'outtmpl': f'{DOWNLOADS}/%(title)s.%(ext)s'
        }

        with YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                f"ytsearch1:{query}",
                download=True
            )

            video = info['entries'][0]

            filename = ydl.prepare_filename(video)

            bot.send_audio(
                chat_id,
                audio=open(filename, 'rb'),
                title=video['title']
            )

    except Exception as e:

        bot.send_message(
            chat_id,
            f"❌ Music topilmadi\n{e}"
        )


print("✅ Bot ishladi")

bot.infinity_polling()
