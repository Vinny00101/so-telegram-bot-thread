import threading
import json

class Animeloader():
    ANIMES = []
    def get_json(self, caminho: str):
        try: 
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                self.ANIMES = json.load(arquivo)
                print(f"{len(self.ANIMES)} animes carregados com sucesso!")
        except FileExistsError:
            print("Erro: Arquivo não encontrado.")
            self.ANIMES = []
        except json.JSONDecodeError:
            print("Erro: Arquivo não encontrado.")
            self.ANIMES = []

    def get_json_with_thread(self, caminho: str):
        get_json_thread = threading.Thread(target=self.get_json, args=(caminho,))
        get_json_thread.start()
        