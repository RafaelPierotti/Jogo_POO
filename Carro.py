import pygame
from Objetos import Objetos

class Carro(Objetos):
    def __init__(self, x, y, caminho, vida_maxima, vel_normal, vel_lenta): #construtor
        self.imagem_original = pygame.image.load(caminho) #carrega imagem do carro
        self.imagem = None
        self.rect = None #cria a colisão do carro
        #self.rect.inflate_ip(-40, -60)
        #self.rect.move_ip(0, -10)

        #self.rect.x = x
        #self.rect.y = y

        self.velocidade_normal = vel_normal
        self.velocidade_lenta = vel_lenta
        self.vida_maxima = vida_maxima
        self.vida_atual = vida_maxima

        self.__invencivel = False
        self.__invencivel_timer = 0

        self.__limite_pista_esq = 100
        self.__limite_pista_dir = 540


    def mover(self, teclas, esquerda, direita): #metodo de movimentação


        velocidade_atual = self.velocidade_normal

        if self.esta_na_grama():
            velocidade_atual = self.velocidade_lenta

        if teclas[esquerda]:
            self.rect.x -= 10 #movimenta 10 para esquerda
        if teclas[direita]:
            self.rect.x += 10 # movimenta 10 para direita

    def desenhar(self, tela): #metodo para desenhar veículo
        if self.__invencivel:
            self.__invencivel_timer -= 1
            if self.__invencivel_timer <= 0:
                self.__invencivel = False

            if self.__invencivel_timer % 4 < 2:
                pass
            else:
                tela.blit(self.imagem, self.rect)
        else:
            tela.blit(self.imagem, self.rect)

    def receber_dano(self, dano):
        if not self.__invencivel:
            self.vida_atual -= dano
            self.__invencivel = True
            self.__invencivel_timer = 60
            return True
        return False

    def resetar_vida(self):
        self.vida_atual = self.vida_maxima
        self.__invencivel = False
        self.__invencivel_timer = 0

    def esta_na_grama(self):
        return self.rect.left < self.__limite_pista_esq or self.rect.right > self.__limite_pista_dir