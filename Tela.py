import pygame

LARGURA = 640 #define o tamanho da tela
ALTURA = 700

class Tela:
    def __init__(self, largura, altura): #construtor
        self.largura = largura
        self.altura = altura
        self.tela = pygame.display.set_mode((self.largura, self.altura)) #cria tela
        pygame.display.set_caption('Racing Coders') #nome da janela do jogo
        self.fundo_img = pygame.image.load('estrada.png') #pega imagem da estrada
        self.fundo_img = pygame.transform.scale(self.fundo_img, (largura, altura))

    def desenhar_fundo(self):
        self.tela.blit(self.fundo_img, (0, 0))

    def atualizar(self): #atualiza tudo o que foi desenhado até o momento
        pygame.display.update()