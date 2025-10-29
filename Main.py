import pygame
from pygame.locals import *
from sys import exit
from random import randint

from Carro import Carro
from Tela import Tela
from Moeda import Moeda
from Obstaculo import Obstaculo

from Database import session

def reiniciar_jogo(carro, obstaculos, largura, altura, dist_minima):
    carro.rect.centerx = largura // 2
    carro.rect.y = altura // 1.5
    for obs in obstaculos:
        obs.reposicionar()

    # Garante distância mínima inicial
    while abs(obstaculos[0].rect.y - obstaculos[1].rect.y) < dist_minima:
        obstaculos[1].reposicionar()

    return 0

pygame.init()

largura = 640
altura = 700
DISTANCIA_MINIMA = 200
velocidade = 120

tela = Tela(largura, altura)
carro = Carro(x=largura // 2, y=altura // 1.5, caminho='jogo_carro.png')
moeda = Moeda(largura_tela=largura, altura_tela=altura)
musica_moeda = pygame.mixer.Sound('smw_coin.wav')

obstaculos = [
    Obstaculo(largura, altura, "parede.png"),
    Obstaculo(largura, altura, "parede.png")
]

relogio = pygame.time.Clock()

fonte_jogo = pygame.font.SysFont('Arial', 30, True, False)

while True:

    usuario_atual = tela.tela_inicial(session)

    moedas_total = reiniciar_jogo(carro, obstaculos, largura, altura, DISTANCIA_MINIMA)

    rodando_jogo = True

    while rodando_jogo:
        relogio.tick(velocidade)

        for event in pygame.event.get():
            if event.type == QUIT:
                session.close()
                pygame.quit()
                exit()

            if event.type == KEYDOWN: #Pressiona o ESC
                if event.key == K_ESCAPE:
                    # Chama a nova tela de pausa
                    acao_pausa = tela.tela_pausa(session)

                    if acao_pausa == "CONTINUAR":
                        # Apenas sai deste loop de eventos e continua o jogo
                        break

                    elif acao_pausa == "MENU":
                        rodando_jogo = False  # Quebra o loop 'rodando_jogo'
                        break  # Sai do loop de eventos

                    elif acao_pausa == "SAIR":
                        session.close() #Sai do jogo
                        pygame.quit()
                        exit()

        if not rodando_jogo:
            continue

        teclas = pygame.key.get_pressed()
        carro.mover(teclas, esquerda=pygame.K_a, direita=pygame.K_d)

        if carro.rect.left < 0:
            carro.rect.left = 0
        if carro.rect.right > largura:
            carro.rect.right = largura

        tela.desenhar_fundo()
        carro.desenhar(tela.tela)

        colisao = False
        for obstaculo in obstaculos:
            if obstaculo.colidiu(carro.rect):
                colisao = True
                break

        if colisao:
            acao = tela.tela_game_over(session, usuario_atual, moedas_total)

            if acao == "REINICIAR":
                moedas_total = reiniciar_jogo(carro, obstaculos, largura, altura, DISTANCIA_MINIMA)
                continue  # Volta ao início do loop 'rodando_jogo'

            elif acao == "MENU":
                rodando_jogo = False  # Quebra o loop 'rodando_jogo'
                continue

            elif acao == "SAIR":
                session.close()
                pygame.quit()
                exit()

        for obstaculo in obstaculos:
            obstaculo.atualizar()
            obstaculo.desenhar(tela.tela)

        moeda.atualizar()

        for obstaculo in obstaculos:
            if moeda.rect.colliderect(obstaculo.rect):
                moeda.rect.bottom = obstaculo.rect.top

        moeda.desenhar(tela.tela)

        if moeda.colidiu(carro.rect):
            moedas_total += 1
            musica_moeda.play()
            moeda.reposicionar()

        texto_pontos = fonte_jogo.render(f"Moedas: {moedas_total}", True, (0, 0, 0))
        tela.tela.blit(texto_pontos, (10, 10))

        texto_nome = fonte_jogo.render(f"Jogador: {usuario_atual.nome}", True, (0, 0, 0))
        tela.tela.blit(texto_nome, (10, 40))

        tela.atualizar()