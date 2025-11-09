import pygame
from random import randint

class Moeda:
    def __init__(self, largura_tela, altura_tela, tamanho=50, vel_y_base=5):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.tamanho = tamanho
        self.__vel_y_base = vel_y_base
        self.vel_y = self.__vel_y_base

        # Posição inicial aleatória
        self.x = randint(100, 470)
        self.y = randint(-600, -100)

        # Carrega e redimensiona a imagem da moeda
        self.imagem = pygame.image.load("assets/moeda.png")  # nome do seu arquivo
        self.imagem = pygame.transform.scale(self.imagem, (self.tamanho, self.tamanho))

        # Retângulo de colisão
        self.rect = self.imagem.get_rect(center=(self.x, self.y))

    def atualizar(self, velocidade_jogo):
        self.vel_y = velocidade_jogo  # Atualiza a velocidade atual
        self.y += self.vel_y  # Usa a velocidade vinda do Main
        self.rect.centery = self.y

        if self.y > self.altura_tela:
            self.reposicionar()

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)

    def colidiu(self, carro_rect):
        return self.rect.colliderect(carro_rect)

    def reposicionar(self):
        self.x = randint(100, 470)
        self.y = randint(-600, -100)
        self.rect.center = (self.x, self.y)
