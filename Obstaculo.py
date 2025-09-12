import pygame
from random import randint

class Obstaculo:
    def __init__(self, largura_tela, altura_tela, caminho, largura=150, altura=150, vel_y=5):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.vel_y = vel_y
        self.parado = False
        self.imagem = pygame.image.load(caminho)
        self.imagem = pygame.transform.scale(self.imagem, (largura, altura))
        x = randint(100, 470)
        y = randint(-600, -100)
        self.rect = self.imagem.get_rect(topleft=(x, y))

    def atualizar(self):
        if not self.parado:  # só se move se não estiver parado
            self.rect.y += self.vel_y
            if self.rect.top > self.altura_tela:
                self.reposicionar()

    def reposicionar(self):
        self.rect.x = randint(100, 470)
        self.rect.y = randint(-600, -100)

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)

    def colidiu(self, carro_rect):
        return self.rect.colliderect(carro_rect)