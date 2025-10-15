from ..loader import Animeloader
import queue

class generos_command:
    @staticmethod
    def buscar_generos(response_queue: queue.Queue):
        generos = "\n".join(
            f'{genero}\n' 
            for genero in Animeloader.GENEROS["generos"]
        )
        if not generos:
            response_queue.put(None)
        
        response_queue.put(generos)
        
    @staticmethod
    def buscar_anime_genero():
        pass