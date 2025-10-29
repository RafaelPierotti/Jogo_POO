# audio_manager.py
import os
import pygame

class AudioManager:
    def __init__(self, sons_dir="sons"):
        # inicializa o mixer se ainda não inic
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
            except Exception as e:
                print("Aviso: não foi possível inicializar pygame.mixer:", e)
                self._ok = False
                return
        self._ok = True
        self.sons_dir = sons_dir
        self.sons = {}
        # defina os nomes de som que você usará aqui e os arquivos correspondentes
        defaults = {
            "moeda": "smw_coin.wav",
            "colisao": "colisao.wav",
            "gameover": "gameover.wav",
            "clique": "clique.wav"
        }
        for key, filename in defaults.items():
            caminho = os.path.join(self.sons_dir, filename)
            if os.path.isfile(caminho):
                try:
                    self.sons[key] = pygame.mixer.Sound(caminho)
                except Exception as e:
                    print(f"Erro ao carregar som {caminho}: {e}")
            else:
                # apenas um aviso; o jogo continua sem esse som
                print(f"Atenção: arquivo de som não encontrado: {caminho}")

    def tocar(self, nome):
        """Toca um som já carregado; ignora se não existir ou mixer não iniciado."""
        if not getattr(self, "_ok", False):
            return
        s = self.sons.get(nome)
        if s:
            try:
                s.play()
            except Exception as e:
                print(f"Erro ao tocar som {nome}: {e}")

# instância global (use init_audio() para inicializar)
audio = None

def init_audio(sons_dir="sons"):
    """Inicializa a instância global audio. Chame uma vez no início do jogo."""
    global audio
    if audio is None:
        audio = AudioManager(sons_dir)
    return audio
