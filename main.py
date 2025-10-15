import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from bot.loader import Animeloader
from bot.handlers import handlers
import time

load_dotenv()

TOKEN = os.getenv('TOKEN')

def main():
    if not TOKEN:
        raise ValueError("❌ TELEGRAM_TOKEN não definido no arquivo .env")
    
    app = Application.builder().token(TOKEN).build()
    
    t = Animeloader.get_json_Anime("data/basedados.json", callback=lambda: print("Base pronta"))
    time.sleep(0.5)
    t = Animeloader.get_json_Generos("data/basedadosGeneros.json", callback=lambda: print("Base pronta"))
    time.sleep(0.5)
    
    app.add_handler(CommandHandler("recomenda", handlers.recomenda_command))
    app.add_handler(CommandHandler("info", handlers.info_command))
    app.add_handler(CommandHandler("novidades", handlers.novidades_command))
    app.add_handler(CommandHandler("help", handlers.help_command))
    app.add_handler(CommandHandler("generos", handlers.generos_command))
    
    print("🤖 Bot está rodando...")
    app.run_polling(allowed_updates=["message"])
    
if __name__ == "__main__":
    main()