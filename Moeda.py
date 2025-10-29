import pygame
from random import randint

class Moeda:
    def __init__(self, largura_tela, altura_tela, tamanho=50, vel_y=5):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.tamanho = tamanho
        self.vel_y = vel_y

        # Posição inicial aleatória
        self.x = randint(100, 470)
        self.y = randint(-600, -100)

        # Carrega e redimensiona a imagem da moeda
        self.imagem = pygame.image.load("assets/moeda.png")  # nome do seu arquivo
        self.imagem = pygame.transform.scale(self.imagem, (self.tamanho, self.tamanho))

        # Retângulo de colisão
        self.rect = self.imagem.get_rect(center=(self.x, self.y))

    def atualizar(self):
        self.y += self.vel_y
        self.rect.centery = self.y

        # Quando sair da tela, reposiciona
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
