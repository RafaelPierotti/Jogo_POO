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
carro = Carro(x=largura//2, y=altura//1.3, caminho='jogo_carro.png')
musica_moeda = pygame.mixer.Sound('smw_coin.wav')

relogio = pygame.time.Clock()

OBSTACULO_LARGURA = 70
OBSTACULO_ALTURA = 90
velocidade_queda = 5
obstaculos = [
    [randint(100, 470), randint(40, altura - OBSTACULO_ALTURA)],
    [randint(100, 470), randint(40, altura - OBSTACULO_ALTURA)]
]

obstaculoX = randint(40, largura - OBSTACULO_LARGURA)
obstaculoY = randint(40, altura - OBSTACULO_ALTURA)

tamanho_moeda = 40
moedaX = randint(100, 470)
moedaY = randint(-600, -100)
moedas_total = 0

velocidade = 120

carro_x = largura/2
carro_y = altura/2

fonte = pygame.font.SysFont('Arial', 30, True, False)


while True:
    relogio.tick(velocidade)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    teclas = pygame.key.get_pressed()
    carro.mover(teclas, esquerda=pygame.K_a, direita=pygame.K_d)

    if carro.rect.left < 100:
        carro.rect.left = 100
    
    if carro.rect.right > 540:
        carro.rect.right = 540

    tela.desenhar_fundo()
    carro.desenhar(tela.tela)

    for i in range(len(obstaculos)):
        obstaculos[i][1] += velocidade_queda
        ox, oy = obstaculos[i]
        obstaculo_rect = tela.obstaculo((255, 255, 255), ox, oy, OBSTACULO_LARGURA, OBSTACULO_ALTURA)

        if oy > altura:
            novo_x = randint(100, 470)
            novo_y = randint(-600, -100)

            outro_obstaculo = 1 - i

            while abs(novo_x - obstaculos[outro_obstaculo][0]) < OBSTACULO_LARGURA and abs(novo_y - obstaculos[outro_obstaculo][1]) < OBSTACULO_ALTURA:
                novo_x = randint(100, 470)
                novo_y = randint(-600, -100)

            obstaculos[i][0] = novo_x
            obstaculos[i][1] = novo_y

            #if carro.rect.colliderect(obstaculo_rect):
             #   obstaculos[i][0] = randint(100, 470)
              #  obstaculos[i][1] = randint(40, altura - OBSTACULO_ALTURA)


    moedaY += velocidade_queda
    moeda_rect = pygame.draw.circle(tela.tela, (255, 223, 0), (moedaX, moedaY), tamanho_moeda // 2)

    if carro.rect.colliderect(moeda_rect):
        musica_moeda.play()
        obstaculoX = randint(100, 470)
        obstaculoY = randint(-600, -100)
        moedas_total += 1
    
    texto =  fonte.render(f"Moedas: {moedas_total}", True, (0, 0, 0))
    tela.tela.blit(texto, (10, 10))

    tela.atualizar()