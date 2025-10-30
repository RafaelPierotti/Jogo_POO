import pygame
from Objetos import Objetos

class Carro(Objetos):
    def __init__(self, x, y, caminho, vida_maxima, vel_normal, vel_lenta): #construtor
        self.imagem = pygame.image.load(caminho) #carrega imagem do carro
        self.imagem = pygame.transform.scale(self.imagem, (200/2, 420/2)) #imagem fica menor
        self.rect = self.imagem.get_rect() #cria a colisão do carro
        self.rect.inflate_ip(-40, -60)
        self.rect.move_ip(0, -10)

        self.rect.x = x
        self.rect.y = y

        self.velocidade_normal = vel_normal
        self.velocidade_lenta = vel_lenta
        self.vida_maxima = vida_maxima
        self.vida_atual = vida_maxima

        self.invencivel = False
        self.invencivel_timer = 0

        self.limite_pista_esq = 100
        self.limite_pista_dir = 540


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
        if self.invencivel:
            self.invencivel_timer -= 1
            if self.invencivel_timer <= 0:
                self.invencivel = False

            if self.invencivel_timer % 4 < 2:
                pass
            else:
                tela.blit(self.imagem, self.rect)
        else:
            tela.blit(self.imagem, self.rect)

    def receber_dano(self, dano):
        if not self.invencivel:
            self.vida_atual -= dano
            self.invencivel = True
            self.invencivel_timer = 60
            return True
        return False

    def resetar_vida(self):
        self.vida_atual = self.vida_maxima
        self.invencivel = False
        self.invencivel_timer = 0

    def esta_na_grama(self):
        return self.rect.left < self.limite_pista_esq or self.rect.right > self.limite_pista_dir