import difflib
import asyncio
import queue
from telegram import Update
from telegram.ext import ContextTypes
from ..loader import Animeloader

class infor_command:
    @staticmethod
    def buscar(anime_context: str, resultado_queue: queue.Queue):
        nomes = [anime["nome"].lower() for anime in Animeloader.ANIMES]

        correspondencias = difflib.get_close_matches(anime_context, nomes, n=1, cutoff=0.5)
        
        if not correspondencias:
            resultado_queue.put(None)
            return
            
        anime_encontrado = next(a for a in Animeloader.ANIMES if a["nome"].lower() == correspondencias[0])
        resultado_queue.put(anime_encontrado)
