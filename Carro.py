import pygame

class Carro:
    def __init__(self, x, y, caminho):
        self.imagem = pygame.image.load(caminho)
        self.imagem = pygame.transform.scale(self.imagem, (230/2, 450/2))
        self.rect = self.imagem.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidade = 10

    def mover(self, teclas, esquerda, direita):
        if teclas[esquerda]:
            self.rect.x -= 10
        if teclas[direita]:
            self.rect.x += 10

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)