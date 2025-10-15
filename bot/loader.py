import threading
import json

class Animeloader:
    ANIMES = []
    ## Condições de corrida: caso estiver mais de uma thread tentando 
    ## acessa ou modifica dados, usamos o lock para garanti que o Animes sejam carregados antes de seu uso
    _lock = threading.Lock()

    @staticmethod
    def get_json_with_thread(caminho: str, callback=None):
        import threading, json

        def tarefa():
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    with Animeloader._lock:
                        Animeloader.ANIMES = dados
                print(f"{len(Animeloader.ANIMES)} animes carregados com sucesso!")
                if callback:
                    callback()
            except Exception as e:
                print("Erro ao carregar JSON:", e)

        t = threading.Thread(target=tarefa, daemon=True)
        t.start()
        return t
        