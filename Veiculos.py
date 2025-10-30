import pygame
from Carro import Carro

IMG_LAMBO = 'assets/lambo.png'
IMG_F1 = 'assets/jogo_carro.png'
IMG_FUSCA 'assets/
class Lambo(Carro):
    def __init__(self,x, y):
        super().__init__(x, y, IMG_LAMBO,
                         vida_maxima=3,
                         vel_normal=7,
                         vel_lenta=5)
        self.nome = "Lamborguini"
        self.descricao = ["Velocidade: Alta", "Resistência: Baixa"]

        tamanho_in_game = (140, 150)

        # Cria a imagem do jogo e o rect
        self.imagem = pygame.transform.scale(self.imagem_original, tamanho_in_game)
        self.rect = self.imagem.get_rect()
        self.rect.inflate_ip(-20, -40)  # Ajuste da colisão
        self.rect.move_ip(0, -10)
        self.rect.x = x
        self.rect.y = y

class F1(Carro):
    def __init__(self,x, y):
        super().__init__(x, y, IMG_F1,
                         vida_maxima=2,
                         vel_normal=12,
                         vel_lenta=5)
        self.nome = "F1"
        self.descricao = ["Velocidade: Alta", "Resistência: Baixa"]

        tamanho_in_game = (80, 168)

        # Cria a imagem do jogo e o rect
        self.imagem = pygame.transform.scale(self.imagem_original, tamanho_in_game)
        self.rect = self.imagem.get_rect()
        self.rect.inflate_ip(-20, -40)  # Ajuste da colisão
        self.rect.move_ip(0, -10)
        self.rect.x = x
        self.rect.y = y 
       
        class Fusca(Carro):
    def __init__(self,x, y):
        super().__init__(x, y, IMG_FUSCA,
                         vida_maxima=5,
                         vel_normal=10,
                         vel_lenta=6)
        self.nome = "Fusca"
        self.descricao = ["Velocidade: Baixa", "Resistência: ALta"]

        tamanho_in_game = (80, 168)

        # Cria a imagem do jogo e o rect
        self.imagem = pygame.transform.scale(self.imagem_original, tamanho_in_game)
        self.rect = self.imagem.get_rect()
        self.rect.inflate_ip(-20, -40)  # Ajuste da colisão
        self.rect.move_ip(0, -10)
        self.rect.x = x
        self.rect.y = y 
        self.rect.y = y
