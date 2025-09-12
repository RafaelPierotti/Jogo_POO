import pygame
from pygame.locals import *
from sys import exit
from random import randint

from Carro import Carro
from Tela import Tela
from Moeda import Moeda
from Obstaculo import Obstaculo


#inicializando todas as funções e variaveis da biblioteca pygame
pygame.init()

#tamanho da janela
largura = 640
altura = 700

tela = Tela(largura, altura)
carro = Carro(x=largura//2, y=altura//1.5, caminho='jogo_carro.png')
moeda = Moeda(largura_tela=largura, altura_tela=altura)
musica_moeda = pygame.mixer.Sound('smw_coin.wav')

relogio = pygame.time.Clock()

OBSTACULO_LARGURA = 70
OBSTACULO_ALTURA = 90
velocidade_queda = 5
obstaculos = [
    Obstaculo(largura, altura, "parede.png"),
    Obstaculo(largura, altura, "parede.png")
]

DISTANCIA_MINIMA = 200
while abs(obstaculos[0].rect.y - obstaculos[1].rect.y) < DISTANCIA_MINIMA:
    obstaculos[1].reposicionar()

obstaculoX = randint(40, largura - OBSTACULO_LARGURA)
obstaculoY = randint(40, altura - OBSTACULO_ALTURA)

tamanho_moeda = 40
moedaX = randint(100, 470)
moedaY = randint(-600, -100)

velocidade = 120

carro_x = largura/2
carro_y = altura/2

moedas_total = 0
fonte = pygame.font.SysFont('Arial', 30, True, False)


while True:
    relogio.tick(velocidade)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    teclas = pygame.key.get_pressed()
    carro.mover(teclas, esquerda=pygame.K_a, direita=pygame.K_d)


    if carro.rect.left < 100: #limitando carro na pista
        carro.rect.left = 100
    
    if carro.rect.right > 540:
        carro.rect.right = 540

    tela.desenhar_fundo()
    carro.desenhar(tela.tela)

    for obstaculo in obstaculos:
        if obstaculo.colidiu(carro.rect):
            
            if carro.rect.bottom > obstaculo.rect.top and carro.rect.centery < obstaculo.rect.centery:
                obstaculo.parado = True
                if moedas_total > 0:
                    moedas_total -= 1
            else:
                obstaculo.parado = False
        else:
            obstaculo.parado = False

        obstaculo.atualizar()
        obstaculo.desenhar(tela.tela)

    moeda.atualizar()d

    for obstaculo in obstaculos:
        if moeda.rect.colliderect(obstaculo.rect):
            moeda.rect.bottom = obstaculo.rect.top

    moeda.desenhar(tela.tela)

    if moeda.colidiu(carro.rect):
        moedas_total += 1
        musica_moeda.play()
        moeda.reposicionar()

    
    texto =  fonte.render(f"Moedas: {moedas_total}", True, (0, 0, 0))
    tela.tela.blit(texto, (10, 10))

    tela.atualizar()