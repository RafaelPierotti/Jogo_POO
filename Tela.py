import pygame

LARGURA = 640
ALTURA = 700

class Tela:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption('Racing Coders')
        self.fundo_img = pygame.image.load('estrada.png')
        self.fundo_img = pygame.transform.scale(self.fundo_img, (largura, altura))

    def desenhar_fundo(self):
        self.tela.blit(self.fundo_img, (0, 0))

    def obstaculo(self, cor, x, y, largura, altura):
        rect = pygame.Rect(x, y, largura, altura)
        pygame.draw.rect(self.tela, cor, rect)
        return rect

    def atualizar(self):
        pygame.display.update()