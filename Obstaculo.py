import pygame
from random import randint

from Objetos import Objetos


class Obstaculo(Objetos):
    def __init__(self, largura_tela, altura_tela, caminho, largura=100, altura=150, vel_y=5): #construtor
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.vel_y = vel_y
        self.parado = False #pausa movimento do obstaculo
        self.imagem = pygame.image.load(caminho)
        self.imagem = pygame.transform.scale(self.imagem, (largura, altura))
        x = randint(100, 470)
        y = randint(-600, -100)
        self.rect = self.imagem.get_rect(topleft=(x, y))#posiciona obstaculo
        self.rect.inflate_ip(-30, -40)

    def atualizar(self):
        if not self.parado:  # só se move se não estiver parado
            self.rect.y += self.vel_y
            if self.rect.top > self.altura_tela: #saiu da tela volta para cima
                self.reposicionar()

    def reposicionar(self): #recomeça de cima
        self.rect.x = randint(100, 470)
        self.rect.y = randint(-600, -100)

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)

    def colidiu(self, carro_rect):
        return self.rect.colliderect(carro_rect)