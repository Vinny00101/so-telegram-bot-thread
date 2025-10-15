import threading
import json

class Animeloader:
    ANIMES = []
    GENEROS = []
    ## Condições de corrida: caso estiver mais de uma thread tentando 
    ## acessa ou modifica dados, usamos o lock para garanti que o Animes sejam carregados antes de seu uso
    _lock = threading.Lock()
    
    def data(caminho: str):
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
            with Animeloader._lock:
                print(dados)
                return dados

    @staticmethod
    def get_json_Anime(caminho: str, callback=None):

        def tarefa():
            try:
                Animeloader.ANIMES = Animeloader.data(caminho)
                print(f"{len(Animeloader.ANIMES)} animes carregados com sucesso!")
                if callback:
                    callback()
            except Exception as e:
                print("Erro ao carregar JSON:", e)

        t = threading.Thread(target=tarefa, daemon=True)
        t.start()
        return t
    
    @staticmethod
    def get_json_Generos(caminho: str, callback=None):

        def tarefa():
            try:
                Animeloader.GENEROS = Animeloader.data(caminho)
                print(f"{len(Animeloader.ANIMES)} Generos carregados com sucesso!")
                if callback:
                    callback()
            except Exception as e:
                print("Erro ao carregar JSON:", e)

        t = threading.Thread(target=tarefa, daemon=True)
        t.start()
        return t
        