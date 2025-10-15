from telegram import Update
from .loader import Animeloader
from telegram.ext import ContextTypes
from .threads.infor_command import infor_command
import queue
import threading

class handlers():
    @staticmethod
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Bem vindo ao Anispeed, para mais informações de comandos use o */info*", parse_mode="Markdown")
        
    @staticmethod
    async def recomenda_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Aqui vai uma recomendação!")

    '''
    Este método utiliza threading para executar a busca de um anime em paralelo, evitando bloquear
    o loop assíncrono do bot do Telegram. A ideia e usar uma thread separada para fazer a buscar no json e um
    `queue.Queue()` para fazer a ligacao do codigo principal com o de buscar.
    '''
    @staticmethod
    async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("O comando precisa ser /info *<name anime>*", parse_mode="Markdown")
            return
        
        anime_context = " ".join(context.args).strip().lower()
        await update.message.reply_text("Buscando anime...",parse_mode="Markdown")
        
        resultado_queue = queue.Queue()
        
        threading.Thread(
            target=infor_command.buscar,
            args=(anime_context, resultado_queue), 
            daemon=True
        ).start()
        
        anime_encontrado = resultado_queue.get()
        
        if not anime_encontrado:
            await update.message.reply_text("*Anime não encontrado!*", parse_mode="Markdown")
            return
        
        response_anime = (
            f'Nome do Anine: {anime_encontrado["nome"]}\n\n'
            f"Gêneros: {', '.join(anime_encontrado['generos'])}\n"
            f"Estúdio: {anime_encontrado['estudio']}\n"
            f"Ano: {anime_encontrado['ano']}\n"
            f"Episódios: {anime_encontrado['episodios']}\n"
            f"Status: {anime_encontrado['status']}\n\n"
            f"{anime_encontrado['descricao']}\n"
            f"[Mais detalhes]({anime_encontrado['link']})"
        )
        await update.message.reply_text(response_anime, parse_mode="Markdown", disable_web_page_preview=True)

    @staticmethod
    async def novidades_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Últimas novidades!")

    @staticmethod
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = (
            "🤖 *Comandos disponíveis:*\n\n"
            "/recomenda - Receba uma recomendação personalizada\n"
            "/info - Veja informações sobre o bot\n"
            "/novidades - Veja as últimas atualizações\n"
            "/generos - Liste os gêneros disponíveis\n"
            "/help - Mostra esta mensagem de ajuda\n"
        )
        await update.message.reply_text(help_text, parse_mode="Markdown")

    @staticmethod
    async def generos_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Lista de gêneros aqui!")