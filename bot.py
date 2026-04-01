import os
import subprocess
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def start(update, context):
    update.message.reply_text("Salut ! Envoie-moi une vidéo, je vais la compresser pour toi.")

def compress_video(update, context):
    msg = update.message.reply_text("Téléchargement et compression en cours... Patiente un peu ⏳")
    video_file = context.bot.get_file(update.message.video.file_id)
    video_file.download("input.mp4")
    
    # Commande magique FFmpeg pour diviser la taille par 4
    cmd = "ffmpeg -i input.mp4 -vcodec libx264 -crf 28 output.mp4 -y"
    subprocess.run(cmd, shell=True)
    
    with open("output.mp4", "rb") as f:
        context.bot.send_video(chat_id=update.message.chat_id, video=f, caption="Et voilà ! Ta vidéo compressée ⚡")
    
    os.remove("input.mp4")
    os.remove("output.mp4")
    msg.delete()

updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.video, compress_video))
updater.start_polling()
updater.idle()
