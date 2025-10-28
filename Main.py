import pygame
from pygame.locals import *
from sys import exit
from random import randint

from Carro import Carro
from Tela import Tela
from Moeda import Moeda
from Obstaculo import Obstaculo

pygame.init()

# Configurações da janela
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

velocidade = 120
moedas_total = 0
fonte = pygame.font.SysFont('Arial', 30, True, False)


# === FUNÇÃO TELA INICIAL (fundo preto, logo e botão começar) ===
def tela_inicial():
    # Carrega o logo
    logo = pygame.image.load("logo1.png")
    logo = pygame.transform.scale(logo, (400, 200))

    # Fontes
    fonte_input = pygame.font.SysFont('Arial', 35, True, False)
    fonte_botao = pygame.font.SysFont('Arial', 40, True, False)

    nome_usuario = ""
    input_ativo = False

    # Cores
    cor_fundo = (0, 0, 0)
    cor_input_inativo = (80, 80, 80)
    cor_input_ativo = (255, 255, 255)
    cor_texto = (0, 0, 0)
    cor_botao = (0, 150, 0)
    cor_botao_hover = (0, 200, 0)

    # Retângulos (caixa e botão)
    input_box = pygame.Rect(largura//2 - 150, 420, 300, 50)
    botao_rect = pygame.Rect(largura//2 - 100, 500, 200, 60)

    while True:
        tela.tela.fill(cor_fundo)

        # Desenha logo centralizada
        tela.tela.blit(logo, (largura//2 - logo.get_width()//2, 150))

        # Caixa de texto
        pygame.draw.rect(tela.tela, cor_input_ativo if input_ativo else cor_input_inativo, input_box, 0, border_radius=8)
        texto_surface = fonte_input.render(nome_usuario, True, cor_texto)
        tela.tela.blit(texto_surface, (input_box.x + 10, input_box.y + 10))
        pygame.draw.rect(tela.tela, (255, 255, 255), input_box, 2, border_radius=8)

        # Exibe botão "Começar" se o nome for digitado
        mouse = pygame.mouse.get_pos()
        if nome_usuario.strip() != "":
            if botao_rect.collidepoint(mouse):
                pygame.draw.rect(tela.tela, cor_botao_hover, botao_rect, 0, border_radius=8)
            else:
                pygame.draw.rect(tela.tela, cor_botao, botao_rect, 0, border_radius=8)

            botao_texto = fonte_botao.render("Começar", True, (255, 255, 255))
            tela.tela.blit(botao_texto, (botao_rect.x + 16, botao_rect.y + 8))

        pygame.display.update()

        # Eventos
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()
            elif evento.type == MOUSEBUTTONDOWN:
                if input_box.collidepoint(evento.pos):
                    input_ativo = True
                else:
                    input_ativo = False
                if botao_rect.collidepoint(evento.pos) and nome_usuario.strip() != "":
                    return nome_usuario  # Retorna o nome e inicia o jogo
            elif evento.type == KEYDOWN and input_ativo:
                if evento.key == K_BACKSPACE:
                    nome_usuario = nome_usuario[:-1]
                elif len(nome_usuario) < 15:
                    nome_usuario += evento.unicode


# === EXECUTA A TELA INICIAL ===
nome_jogador = tela_inicial()
print(f"Jogador: {nome_jogador}")  # depois pode salvar no banco


def tela_game_over():
    #carrega o logo
    logo = pygame.image.load("logo1.png")
    logo = pygame.transform.scale(logo, (400, 200))

    #fontes
    fonte_titulo = pygame.font.SysFont('Arial', 50, True)
    fonte_botao = pygame.font.SysFont('Arial', 40, True)

    # cores
    cor_fundo = (0, 0, 0)
    cor_botao = (200, 0, 0)
    cor_botao_hover = (255, 0, 0)
    cor_botao_sair = (80, 80, 80)
    cor_botao_sair_hover = (120, 120, 120)

    # botões (centralizados)
    espacamento = 20
    botao_largura = 200
    botao_altura = 60

    botao_reiniciar = pygame.Rect(largura // 2 - botao_largura // 2, 480, botao_largura, botao_altura)
    botao_sair = pygame.Rect(largura // 2 - botao_largura // 2, 480 + botao_altura + espacamento, botao_largura, botao_altura)

    #loop principal da tela de game over
    while True:
        tela.tela.fill(cor_fundo)

        # logo e título
        tela.tela.blit(logo, (largura // 2 - logo.get_width() // 2, 150))
        titulo = fonte_titulo.render("GAME OVER", True, (255, 255, 255))
        tela.tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, 380))

        #posição do mouse
        mouse = pygame.mouse.get_pos()

        # botão reiniciar
        # muda de cor quando o mouse passa por cima
        if botao_reiniciar.collidepoint(mouse):
            pygame.draw.rect(tela.tela, cor_botao_hover, botao_reiniciar, border_radius=8)
        else:
            pygame.draw.rect(tela.tela, cor_botao, botao_reiniciar, border_radius=8)
        texto_reiniciar = fonte_botao.render("Reiniciar", True, (255, 255, 255))
        tela.tela.blit(
            texto_reiniciar,
            (botao_reiniciar.centerx - texto_reiniciar.get_width() // 2,
             botao_reiniciar.centery - texto_reiniciar.get_height() // 2)
        )

        # botão sair
        if botao_sair.collidepoint(mouse):
            pygame.draw.rect(tela.tela, cor_botao_sair_hover, botao_sair, border_radius=8)
        else:
            pygame.draw.rect(tela.tela, cor_botao_sair, botao_sair, border_radius=8)
        texto_sair = fonte_botao.render("Sair", True, (255, 255, 255))
        tela.tela.blit(
            texto_sair,
            (botao_sair.centerx - texto_sair.get_width() // 2,
             botao_sair.centery - texto_sair.get_height() // 2)
        )

        # Atualiza tudo que foi desenhado na tela
        pygame.display.update()

        # eventos (cliques, fechar janela, etc)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit() #aqui fecha o jogo
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_reiniciar.collidepoint(evento.pos):
                    return  # volta pro jogo
                elif botao_sair.collidepoint(evento.pos):
                    pygame.quit()
                    exit() #novamente fecha o jogo

while True:
    relogio.tick(velocidade)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    teclas = pygame.key.get_pressed()
    carro.mover(teclas, esquerda=pygame.K_a, direita=pygame.K_d)

    # Limites da pista
    if carro.rect.left < 100:
        carro.rect.left = 100
    if carro.rect.right > 540:
        carro.rect.right = 540

    tela.desenhar_fundo()
    carro.desenhar(tela.tela)

    #colisão com o obstáculo
    colisao = False
    for obstaculo in obstaculos:
        if obstaculo.colidiu(carro.rect):
            colisao = True
            break  # se colidiu com qualquer obstáculo, encerra o loop

    if colisao:
        tela_game_over()  # mostra a tela de game over
        # Reinicia o jogo
        carro.rect.centerx = largura // 2
        carro.rect.y = altura // 1.5 #reposiciona o carro de onde começou
        moedas_total = 0
        for obs in obstaculos:  # reposiciona todos os obstáculos
            obs.reposicionar()
        continue  # volta pro início do loop

    # --- ATUALIZA OBSTÁCULOS E MOEDAS ---
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

    # --- EXIBE PONTUAÇÃO ---
    texto = fonte.render(f"Moedas: {moedas_total}", True, (0, 0, 0))
    tela.tela.blit(texto, (10, 10))

    tela.atualizar()
