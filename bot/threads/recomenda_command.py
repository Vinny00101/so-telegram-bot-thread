from ..loader import Animeloader
import queue

class recomenda_command:
    @staticmethod
    def buscar(resultado_queue: queue.Queue):
        top_animes = [anime for anime in Animeloader.ANIMES if anime.get("nota", 0) > 8.5]
        response_anime = "\n".join(
            f'*Nome do Anime: {anime["nome"]}*\nurl: {anime["link"]}\n'
            for anime in top_animes
        )
        if not response_anime:
            resultado_queue.put(None)
        
        resultado_queue.put(response_anime)