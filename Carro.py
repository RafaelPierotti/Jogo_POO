import pygame
from Objetos import Objetos

class Carro(Objetos):
    def __init__(self, x, y, caminho): #construtor
        self.imagem = pygame.image.load(caminho) #carrega imagem do carro
        self.imagem = pygame.transform.scale(self.imagem, (200/2, 420/2)) #imagem fica menor
        self.rect = self.imagem.get_rect() #cria a colisão do carro
        self.rect.inflate_ip(-40, -60)
        self.rect.move_ip(0, -10)
        self.rect.x = x
        self.rect.y = y
        self.velocidade_normal = 10 #"hertz" do carro // pixels por segundo
        self.velocidade_lenta = 4

    def mover(self, teclas, esquerda, direita): #metodo de movimentação
        limite_pista_esq = 100
        limite_pista_direita = 540

        velocidade_atual = self.velocidade_normal

        if self.rect.left < limite_pista_esq or self.rect.right > limite_pista_direita:
            velocidade_atual = self.velocidade_lenta

        if teclas[esquerda]:
            self.rect.x -= 10 #movimenta 10 para esquerda
        if teclas[direita]:
            self.rect.x += 10 # movimenta 10 para direita

    def desenhar(self, tela): #metodo para desenhar veículo
        tela.blit(self.imagem, self.rect)
