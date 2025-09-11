import pygame
from pygame.locals import *
from sys import exit
from random import randint
from Carro import Carro
from Tela import Tela

#inicializando todas as funções e variaveis da biblioteca pygame
pygame.init()

#tamanho da janela
largura = 640
altura = 700

tela = Tela(largura, altura)
carro = Carro(x=largura// y=altura/2, caminho='jogo_carro.png')
musica_moeda = pygame.mixer.Sound('smw_coin.wav')

relogio = pygame.time.Clock()

obstaculoX = randint(40, largura - OBSTACULO_LARGURA)
obstaculoY = randint(40, altura - OBSTACULO_ALTURA)

OBSTACULO_LARGURA = 70
OBSTACULO_ALTURA = 90

velocidade = 120

carro_x = largura/2
carro_y = altura/2


while True:
    relogio.tick(velocidade)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    teclas = pygame.key.get_pressed()
    carro.mover(teclas, esquerda=pygame.K_a, direita=pygame.K_d)

    tela.desenhar_fundo()
    carro.desenhar(tela.tela)

    obstaculo_rect = tela.obstaculo(cor=(255, 255, 255), x=obstaculoX, y=obstaculoY, largura=OBSTACULO_LARGURA, altura=OBSTACULO_ALTURA)


    if carro.rect.colliderect(obstaculo_rect):
        musica_moeda.play()
        obstaculoX = randint(40, 640 - 70)
        obstaculoY = randint(40, 700 - 90)
        velocidade = max(30, velocidade - 5)


    tela.atualizar()