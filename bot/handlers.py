from telegram import Update
from .loader import Animeloader
from telegram.ext import ContextTypes

class handlers():
    @staticmethod
    async def recomenda_command(update: Update, context: ContextTypes.DEFAULT_TYPE): 
        await update.message.reply_text("Aqui vai uma recomendação!")

    @staticmethod
    async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await Update.message.reply_text("O comando precisa ser /info < name anime >", parse_mode="Markdown")
            return
        
        anime_context = " ".join(context.args).lower()
        anime_encontrado = None
        
        for anime in Animeloader.ANIMES:
            if anime["nome"].lower() == anime_context:
                anime_encontrado = anime
                break
        
        if not anime_encontrado:
            await Update.message.reply_text("*Anime não encontrado!*",parse_mode="Markdown")
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
        await Update.message.reply_text(response_anime,parse_mode="Markdown")

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