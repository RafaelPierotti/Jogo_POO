import pygame
from pygame.locals import *
from sys import exit
from random import randint

from Carro import Carro
from Tela import Tela
from Moeda import Moeda
from Obstaculo import Obstaculo

from Database import session

from Veiculos import Lambo, F1

def reiniciar_jogo(carro, obstaculos, largura, altura, dist_minima):
    carro.rect.centerx = largura // 2
    carro.rect.y = altura // 1.5
    carro.resetar_vida()
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

VELOCIDADE_JOGO_NORMAL = 8
VELOCIDADE_JOGO_LENTA = 3
velocidade_jogo_global = VELOCIDADE_JOGO_NORMAL

tela = Tela(largura, altura)
moeda = Moeda(largura_tela=largura, altura_tela=altura)
musica_moeda = pygame.mixer.Sound('assets/smw_coin.wav')
musica_game_over = pygame.mixer.Sound('assets/game_over.wav')
musica_game_over.set_volume(0.5)

obstaculos = [
    Obstaculo(largura, altura, "assets/parede.png"),
    Obstaculo(largura, altura, "assets/parede.png")
]

relogio = pygame.time.Clock()

fonte_jogo = pygame.font.SysFont('Arial', 30, True, False)

while True:

    usuario_atual = tela.tela_inicial(session)

    carro_escolhido = tela.tela_escolha_carro(session)

    carro = carro_escolhido(x=largura/2, y=altura/1.5)

    moedas_total = reiniciar_jogo(carro, obstaculos, largura, altura, DISTANCIA_MINIMA)

    start_time_ticks = pygame.time.get_ticks()

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

        if carro.esta_na_grama():
            velocidade_jogo_global = VELOCIDADE_JOGO_LENTA
        else:
            velocidade_jogo_global = VELOCIDADE_JOGO_NORMAL


        tela.desenhar_fundo(velocidade_jogo_global)
        carro.desenhar(tela.tela)

        colisao = False
        for obstaculo in obstaculos:
            if obstaculo.colidiu(carro.rect):
                #colisao = True
                #break

                if carro.receber_dano(1):
                    obstaculo.reposicionar()

                if carro.vida_atual <= 0:
                    colisao = True
                    break

        if colisao:
            musica_game_over.play()

            end_time_ticks = pygame.time.get_ticks()
            duracao_segundos = (end_time_ticks - start_time_ticks) // 1000

            acao = tela.tela_game_over(session, usuario_atual, moedas_total, duracao_segundos)

            if acao == "REINICIAR":
                moedas_total = reiniciar_jogo(carro, obstaculos, largura, altura, DISTANCIA_MINIMA)
                start_time_ticks = pygame.time.get_ticks()
                continue  # Volta ao início do loop 'rodando_jogo'

            elif acao == "MENU":
                rodando_jogo = False  # Quebra o loop 'rodando_jogo'
                continue

            elif acao == "SAIR":
                session.close()
                pygame.quit()
                exit()

        for obstaculo in obstaculos:
            obstaculo.atualizar(velocidade_jogo_global)
            obstaculo.desenhar(tela.tela)

        moeda.atualizar(velocidade_jogo_global)

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

        # Exibe a vida
        texto_vida = fonte_jogo.render(f"Vida: {carro.vida_atual} / {carro.vida_maxima}", True, (255, 0, 0))
        tela.tela.blit(texto_vida, (largura - texto_vida.get_width() - 10, 10))

        # Exibe o Tempo
        tempo_atual_seg = (pygame.time.get_ticks() - start_time_ticks) // 1000
        minutos = tempo_atual_seg // 60
        segundos = tempo_atual_seg % 60
        texto_tempo = fonte_jogo.render(f"Tempo: {minutos:02}:{segundos:02}", True, (0, 0, 0))
        tela.tela.blit(texto_tempo, (largura - texto_tempo.get_width() - 10, 40))

        tela.atualizar()