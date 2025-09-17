import pygame
from random import randint

class Moeda:
    def __init__(self, largura_tela, altura_tela, tamanho=40, vel_y=5): #construtor
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.tamanho = tamanho
        self.vel_y = vel_y
        self.x = randint(100, 470)
        self.y = randint(-600, -100)
        self.rect = pygame.Rect(self.x - tamanho // 2, self.y - tamanho // 2, tamanho, tamanho) #cria colisão da moeda

    def atualizar(self): #move moeda para baixo
        self.y += self.vel_y
        self.rect.y = self.y - self.tamanho // 2

        if self.y > self.altura_tela: #passa limite da tela, reposiciona
            self.reposicionar()

    def desenhar(self, tela):
        pygame.draw.circle(tela, (255, 223, 0), (self.x, self.y), self.tamanho // 2)

    def colidiu(self, carro_rect): #colisão da moeda
        return self.rect.colliderect(carro_rect)

    def reposicionar(self):#reposiciona a moeda
        self.x = randint(100, 470)
        self.y = randint(-600, -100)
        self.rect.x = self.x - self.tamanho // 2 #posição aleatória
        self.rect.y = self.y - self.tamanho // 2