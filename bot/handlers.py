from telegram import Update
from telegram.ext import ContextTypes
from .threads.infor_command import infor_command
from .threads.generos_command import generos_command
from .threads.recomenda_command import recomenda_command
import queue
import threading

class handlers():
    '''
    Esta parte utilizza de thread para chama uma funcao de buscar, essa funcao de buscar roda em daemon e utiliza 
    se de queue para recebe os valores da busca
    '''
    @staticmethod
    async def recomenda_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Escolhendo as recomendaçães...")
        
        resultado_queue = queue.Queue()
        
        threading.Thread(
            target= recomenda_command.buscar,
            args=(resultado_queue,),
            daemon=True
        ).start()
        
        response_animes = resultado_queue.get()
        await update.message.reply_text(response_animes, parse_mode="Markdown")

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
        novidades_texto = (
            "*Novidades do Mundo dos Animes!*\n\n"
            "Fique por dentro dos lançamentos, trailers e notícias fresquinhas!\n"
            "Confira mais no site: [Anime News Network](https://www.animenewsnetwork.com/)"
        )
        await update.message.reply_text(novidades_texto, parse_mode="Markdown")

    @staticmethod
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = (
            "*Comandos disponíveis:*\n\n"
            "/recomenda - Receba uma recomendação personalizada\n"
            "/info - Veja informações sobre o bot\n"
            "/novidades - Veja as últimas atualizações\n"
            "/generos - Liste os gêneros disponíveis\n"
            "/help - Mostra esta mensagem de ajuda\n"
        )
        await update.message.reply_text(help_text, parse_mode="Markdown")

    @staticmethod
    async def generos_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:

            await update.message.reply_text("Todos os generos abaixo. Caso precisa achar um anime por genero digite /genero *<name genero>*\n\n", parse_mode="Markdown")
            
            resultado_queue = queue.Queue()
        
            threading.Thread(
                target=generos_command.buscar_generos,
                args=(resultado_queue,), 
                daemon=True
            ).start()
            
            response_genero = resultado_queue.get()
            
            await update.message.reply_text(response_genero, parse_mode="Markdown")
            return

        