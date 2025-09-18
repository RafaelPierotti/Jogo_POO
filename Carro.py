import pygame
from Objetos import Objetos

class Carro(Objetos):
    def __init__(self, x, y, caminho): #construtor
        self.imagem = pygame.image.load(caminho) #carrega imagem do carro
        self.imagem = pygame.transform.scale(self.imagem, (200/2, 420/2)) #imagem fica menor
        self.rect = self.imagem.get_rect() #cria a colisão do carro
        self.rect.x = x
        self.rect.y = y
        self.velocidade = 10 #"hertz" do carro // pixels por segundo

    def mover(self, teclas, esquerda, direita): #metodo de movimentação
        if teclas[esquerda]:
            self.rect.x -= 10 #movimenta 10 para esquerda
        if teclas[direita]:
            self.rect.x += 10 # movimenta 10 para direita

    def desenhar(self, tela): #metodo para desenhar veículo
        tela.blit(self.imagem, self.rect)