import pygame
from sys import exit
from datetime import datetime
from sqlalchemy import desc

from Usuario import Usuario
from Ponto import Ponto
from Veiculos import Porsche, F1

LARGURA = 640 #define o tamanho da tela
ALTURA = 700

class Tela:
    def __init__(self, largura, altura): #construtor
        self.largura = largura
        self.altura = altura
        self.tela = pygame.display.set_mode((self.largura, self.altura)) #cria tela
        pygame.display.set_caption('Racing Coders') #nome da janela do jogo

        #Fundo da tela
        self.fundo_img = pygame.image.load('assets/estrada.png') #pega imagem da estrada
        self.fundo_img = pygame.transform.scale(self.fundo_img, (largura, altura))

        self.logo = pygame.image.load("assets/logo1.png")
        self.logo = pygame.transform.scale(self.logo, (400, 200))

        self.fonte_input = pygame.font.SysFont('Arial', 35, True, False)
        self.fonte_botao_grande = pygame.font.SysFont('Arial', 40, True, False)
        self.fonte_botao_media = pygame.font.SysFont('Arial', 35, True)
        self.fonte_titulo_grande = pygame.font.SysFont('Arial', 50, True)
        self.fonte_titulo_gameover = pygame.font.SysFont('Impact', 70)  # <--- Fonte mantida para Game Over
        self.fonte_pontos = pygame.font.SysFont('Arial', 28)
        self.fonte_titulo_pontos = pygame.font.SysFont('Arial', 40, True)
        self.fonte_desc = pygame.font.SysFont('Arial', 24)

    def desenhar_fundo(self):
        self.tela.blit(self.fundo_img, (0, 0))

    def atualizar(self):  # atualiza tudo o que foi desenhado até o momento
        pygame.display.update()

    #Metodo importado da main
    def tela_inicial(self, session):
        nome_usuario = ""
        input_ativo = False

        # Cores
        cor_fundo = (0, 0, 0)
        cor_input_inativo = (80, 80, 80)
        cor_input_ativo = (255, 255, 255)
        cor_texto = (0, 0, 0)
        cor_botao = (0, 150, 0)
        cor_botao_hover = (0, 200, 0)
        cor_botao_pontos = (0, 100, 200)
        cor_botao_pontos_hover = (0, 150, 255)

        # Retângulos (caixa e botão)
        input_box = pygame.Rect(self.largura // 2 - 150, 420, 300, 50)
        botao_rect = pygame.Rect(self.largura // 2 - 100, 500, 200, 60)
        botao_pontos_rect = pygame.Rect(self.largura // 2 - 100, 580, 200, 60)

        while True:
            self.tela.fill(cor_fundo)
            # Desenha logo centralizada (usando self.logo)
            self.tela.blit(self.logo, (self.largura // 2 - self.logo.get_width() // 2, 150))
            mouse = pygame.mouse.get_pos()

            # Caixa de texto
            pygame.draw.rect(self.tela, cor_input_ativo if input_ativo else cor_input_inativo, input_box, 0,
                             border_radius=8)
            texto_surface = self.fonte_input.render(nome_usuario, True, cor_texto)
            self.tela.blit(texto_surface, (input_box.x + 10, input_box.y + 10))
            pygame.draw.rect(self.tela, (255, 255, 255), input_box, 2, border_radius=8)

            # Botão "Começar"
            if nome_usuario.strip() != "":
                cor_atual = cor_botao_hover if botao_rect.collidepoint(mouse) else cor_botao
                pygame.draw.rect(self.tela, cor_atual, botao_rect, 0, border_radius=8)
                botao_texto = self.fonte_botao_grande.render("Começar", True, (255, 255, 255))
                self.tela.blit(botao_texto, (botao_rect.x + 16, botao_rect.y + 8))

            # Botão "Pontos"
            cor_pontos_atual = cor_botao_pontos_hover if botao_pontos_rect.collidepoint(mouse) else cor_botao_pontos
            pygame.draw.rect(self.tela, cor_pontos_atual, botao_pontos_rect, 0, border_radius=8)
            botao_texto_pontos = self.fonte_botao_grande.render("Pontos", True, (255, 255, 255))
            self.tela.blit(botao_texto_pontos, (botao_pontos_rect.x + 40, botao_pontos_rect.y + 8))

            self.atualizar()  # Usa o método da própria classe

            # Eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    session.close()
                    pygame.quit()
                    exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    input_ativo = input_box.collidepoint(evento.pos)

                    if botao_rect.collidepoint(evento.pos) and nome_usuario.strip() != "":
                        nome_limpo = nome_usuario.strip()
                        usuario = session.query(Usuario).filter_by(nome=nome_limpo).first()

                        if not usuario:
                            print(f"Criando novo usuário: {nome_limpo}")
                            usuario = Usuario(nome=nome_limpo)
                            session.add(usuario)
                            try:
                                session.commit()
                            except Exception as e:
                                print(f"Erro ao salvar novo usuário: {e}")
                                session.rollback()
                                continue
                        else:
                            print(f"Usuário carregado: {usuario.nome}")

                        return usuario  # Retorna o OBJETO Usuario para o Main.py

                    if botao_pontos_rect.collidepoint(evento.pos):
                        self.tela_pontos(session)  # Chama o outro método da classe

                elif evento.type == pygame.KEYDOWN and input_ativo:
                    if evento.key == pygame.K_BACKSPACE:
                        nome_usuario = nome_usuario[:-1]
                    elif len(nome_usuario) < 15:
                        nome_usuario += evento.unicode

    def tela_pontos(self, session):
        fonte_titulo = self.fonte_titulo_pontos
        fonte_pontos = self.fonte_pontos
        fonte_botao = self.fonte_input

        cor_fundo = (0, 0, 0)
        cor_texto = (255, 255, 255)
        cor_botao = (0, 100, 200)
        cor_botao_hover = (0, 150, 255)

        botao_voltar_rect = pygame.Rect(self.largura // 2 - 75, self.altura - 80, 150, 50)

        try:
            pontuacoes = session.query(Ponto).join(Usuario).order_by(desc(Ponto.pontuacao)).limit(10).all()
        except Exception as e:
            print(f"Erro ao buscar pontuações: {e}")
            pontuacoes = []

        while True:
            self.tela.fill(cor_fundo)
            mouse = pygame.mouse.get_pos()

            titulo = fonte_titulo.render("Melhores Pontuações", True, cor_texto)
            self.tela.blit(titulo, (self.largura // 2 - titulo.get_width() // 2, 50))

            cab_nome = fonte_pontos.render("Nome", True, cor_texto)
            cab_pontos = fonte_pontos.render("Pontos", True, cor_texto)
            cab_data = fonte_pontos.render("Data", True, cor_texto)
            self.tela.blit(cab_nome, (50, 120))
            self.tela.blit(cab_pontos, (300, 120))
            self.tela.blit(cab_data, (420, 120))
            pygame.draw.line(self.tela, cor_texto, (40, 150), (self.largura - 40, 150), 2)

            y_pos = 170
            for ponto in pontuacoes:
                nome_usuario = (ponto.usuario.nome[:15] + '...') if len(ponto.usuario.nome) > 15 else ponto.usuario.nome
                txt_nome = fonte_pontos.render(nome_usuario, True, cor_texto)
                txt_pontos = fonte_pontos.render(str(ponto.pontuacao), True, cor_texto)

                segundos_totais = ponto.tempo_segundos
                minutos = segundos_totais // 60
                segundos_restantes = segundos_totais % 60
                tempo_formatado = f"{minutos:02}:{segundos_restantes:02}"  # Formato 00:00

                txt_tempo = fonte_pontos.render(tempo_formatado, True, cor_texto)

                self.tela.blit(txt_nome, (50, y_pos))
                self.tela.blit(txt_pontos, (300, y_pos))
                self.tela.blit(txt_tempo, (420, y_pos))
                y_pos += 40

            cor_atual = cor_botao_hover if botao_voltar_rect.collidepoint(mouse) else cor_botao
            pygame.draw.rect(self.tela, cor_atual, botao_voltar_rect, border_radius=8)
            texto_voltar = fonte_botao.render("Voltar", True, cor_texto)
            self.tela.blit(texto_voltar, (botao_voltar_rect.centerx - texto_voltar.get_width() // 2,
                                          botao_voltar_rect.centery - texto_voltar.get_height() // 2))

            self.atualizar()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    session.close()
                    pygame.quit()
                    exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if botao_voltar_rect.collidepoint(evento.pos):
                        return
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return

    #Metodo importado da main
    def tela_game_over(self, session, usuario, pontuacao_final, duracao_segundos):
        # Tenta salvar o ponto
        try:
            novo_ponto = Ponto(usuario_id=usuario.id, pontuacao=pontuacao_final, tempo_segundos=duracao_segundos)
            session.add(novo_ponto)
            session.commit()
            print(f"Pontuação {pontuacao_final} salva para o usuário {usuario.nome}")
        except Exception as e:
            print(f"Erro ao salvar pontuação: {e}")
            session.rollback()

        # Fontes
        fonte_titulo_gameover = self.fonte_titulo_gameover  # Usando a nova fonte
        fonte_botao = self.fonte_botao_media

        # Cores
        cor_fundo = (0, 0, 0)  # <--- MUDANÇA: Fundo preto
        cor_texto_botao = (255, 255, 255)
        cor_botao_reiniciar = (200, 0, 0)
        cor_botao_reiniciar_hover = (255, 0, 0)
        cor_botao_pontos = (0, 100, 200)
        cor_botao_pontos_hover = (0, 150, 255)
        cor_botao_menu = (0, 150, 0)
        cor_botao_menu_hover = (0, 200, 0)
        cor_botao_sair = (80, 80, 80)
        cor_botao_sair_hover = (120, 120, 120)

        # Layout dos 4 botões
        espacamento = 15
        botao_largura = 220
        botao_altura = 50
        y_inicial = 420

        botao_reiniciar = pygame.Rect(self.largura // 2 - botao_largura // 2, y_inicial, botao_largura, botao_altura)
        botao_pontos = pygame.Rect(self.largura // 2 - botao_largura // 2, y_inicial + (botao_altura + espacamento),
                                   botao_largura, botao_altura)
        botao_menu = pygame.Rect(self.largura // 2 - botao_largura // 2, y_inicial + 2 * (botao_altura + espacamento),
                                 botao_largura, botao_altura)
        botao_sair = pygame.Rect(self.largura // 2 - botao_largura // 2, y_inicial + 3 * (botao_altura + espacamento),
                                 botao_largura, botao_altura)

        # Textos dos botões (Renderiza só uma vez)
        texto_reiniciar = fonte_botao.render("Reiniciar", True, cor_texto_botao)
        texto_pontos = fonte_botao.render("Pontuação", True, cor_texto_botao)
        texto_menu = fonte_botao.render("Menu Inicial", True, cor_texto_botao)
        texto_sair = fonte_botao.render("Sair", True, cor_texto_botao)

        while True:
            self.tela.fill(cor_fundo)

            self.tela.blit(self.logo, (self.largura // 2 - self.logo.get_width() // 2, 100))  # Logo mais para cima

            game_over_texto = "GAME OVER"
            titulo_gameover_principal = fonte_titulo_gameover.render(game_over_texto, True, (255, 255, 255))
            titulo_gameover_sombra = fonte_titulo_gameover.render(game_over_texto, True,
                                                                  (139, 0, 0))

            titulo_x = self.largura // 2 - titulo_gameover_principal.get_width() // 2
            titulo_y = 280
            self.tela.blit(titulo_gameover_sombra, (titulo_x + 3, titulo_y + 3))

            self.tela.blit(titulo_gameover_principal, (titulo_x, titulo_y))

            pontuacao_texto = f"{pontuacao_final} Moedas"
            pontuacao_surface = self.fonte_botao_media.render(pontuacao_texto, True,
                                                              (255, 255, 0))  # Amarelo para destacar
            self.tela.blit(pontuacao_surface, (self.largura // 2 - pontuacao_surface.get_width() // 2,
                                               titulo_y + titulo_gameover_principal.get_height() + 10))

            mouse = pygame.mouse.get_pos()

            # Botão Reiniciar
            cor_r = cor_botao_reiniciar_hover if botao_reiniciar.collidepoint(mouse) else cor_botao_reiniciar
            pygame.draw.rect(self.tela, cor_r, botao_reiniciar, border_radius=8)
            self.tela.blit(texto_reiniciar, (botao_reiniciar.centerx - texto_reiniciar.get_width() // 2,
                                             botao_reiniciar.centery - texto_reiniciar.get_height() // 2))

            # Botão Pontos
            cor_p = cor_botao_pontos_hover if botao_pontos.collidepoint(mouse) else cor_botao_pontos
            pygame.draw.rect(self.tela, cor_p, botao_pontos, border_radius=8)
            self.tela.blit(texto_pontos, (botao_pontos.centerx - texto_pontos.get_width() // 2,
                                          botao_pontos.centery - texto_pontos.get_height() // 2))

            # Botão Menu Inicial
            cor_m = cor_botao_menu_hover if botao_menu.collidepoint(mouse) else cor_botao_menu
            pygame.draw.rect(self.tela, cor_m, botao_menu, border_radius=8)
            self.tela.blit(texto_menu, (botao_menu.centerx - texto_menu.get_width() // 2,
                                        botao_menu.centery - texto_menu.get_height() // 2))

            # Botão Sair
            cor_s = cor_botao_sair_hover if botao_sair.collidepoint(mouse) else cor_botao_sair
            pygame.draw.rect(self.tela, cor_s, botao_sair, border_radius=8)
            self.tela.blit(texto_sair, (botao_sair.centerx - texto_sair.get_width() // 2,
                                        botao_sair.centery - texto_sair.get_height() // 2))

            self.atualizar()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    session.close()
                    pygame.quit()
                    exit()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return "REINICIAR"

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if botao_reiniciar.collidepoint(evento.pos):
                        return "REINICIAR"

                    if botao_pontos.collidepoint(evento.pos):
                        self.tela_pontos(session)

                    if botao_menu.collidepoint(evento.pos):
                        return "MENU"

                    if botao_sair.collidepoint(evento.pos):
                        return "SAIR"

    def tela_pausa(self, session):
        # Fontes
        fonte_titulo = self.fonte_titulo_gameover  # Reutiliza a fonte grande
        fonte_botao = self.fonte_botao_media

        # Cores
        cor_fundo = (0, 0, 0)
        cor_texto_botao = (255, 255, 255)
        cor_botao_continuar = (0, 150, 0)  # Verde
        cor_botao_continuar_hover = (0, 200, 0)
        cor_botao_menu = (0, 100, 200)  # Azul
        cor_botao_menu_hover = (0, 150, 255)
        cor_botao_sair = (80, 80, 80)  # Cinza
        cor_botao_sair_hover = (120, 120, 120)

        # Layout com 3 botões
        espacamento = 15
        botao_largura = 220
        botao_altura = 50
        y_inicial = 420

        botao_continuar = pygame.Rect(self.largura // 2 - botao_largura // 2, y_inicial, botao_largura, botao_altura)
        botao_menu = pygame.Rect(self.largura // 2 - botao_largura // 2, y_inicial + (botao_altura + espacamento),
                                 botao_largura, botao_altura)
        botao_sair = pygame.Rect(self.largura // 2 - botao_largura // 2, y_inicial + 2 * (botao_altura + espacamento),
                                 botao_largura, botao_altura)

        # Textos dos botões
        texto_continuar = fonte_botao.render("Continuar", True, cor_texto_botao)
        texto_menu = fonte_botao.render("Menu Inicial", True, cor_texto_botao)
        texto_sair = fonte_botao.render("Sair", True, cor_texto_botao)

        while True:
            self.tela.fill(cor_fundo)
            self.tela.blit(self.logo, (self.largura // 2 - self.logo.get_width() // 2, 100))

            pausa_texto = "JOGO PAUSADO"
            titulo_principal = fonte_titulo.render(pausa_texto, True, (255, 255, 255))
            titulo_sombra = fonte_titulo.render(pausa_texto, True, (100, 100, 100))  # Sombra cinza

            titulo_x = self.largura // 2 - titulo_principal.get_width() // 2
            titulo_y = 280

            self.tela.blit(titulo_sombra, (titulo_x + 3, titulo_y + 3))
            self.tela.blit(titulo_principal, (titulo_x, titulo_y))

            mouse = pygame.mouse.get_pos()

            # Botão Continuar
            cor_c = cor_botao_continuar_hover if botao_continuar.collidepoint(mouse) else cor_botao_continuar
            pygame.draw.rect(self.tela, cor_c, botao_continuar, border_radius=8)
            self.tela.blit(texto_continuar, (botao_continuar.centerx - texto_continuar.get_width() // 2,
                                             botao_continuar.centery - texto_continuar.get_height() // 2))

            # Botão Menu Inicial
            cor_m = cor_botao_menu_hover if botao_menu.collidepoint(mouse) else cor_botao_menu
            pygame.draw.rect(self.tela, cor_m, botao_menu, border_radius=8)
            self.tela.blit(texto_menu, (botao_menu.centerx - texto_menu.get_width() // 2,
                                        botao_menu.centery - texto_menu.get_height() // 2))

            # Botão Sair
            cor_s = cor_botao_sair_hover if botao_sair.collidepoint(mouse) else cor_botao_sair
            pygame.draw.rect(self.tela, cor_s, botao_sair, border_radius=8)
            self.tela.blit(texto_sair, (botao_sair.centerx - texto_sair.get_width() // 2,
                                        botao_sair.centery - texto_sair.get_height() // 2))

            self.atualizar()

            # Eventos da tela de pausa
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    session.close()
                    pygame.quit()
                    exit()

                # Se apertar ESC de novo, ele continua o jogo
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return "CONTINUAR"

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if botao_continuar.collidepoint(evento.pos):
                        return "CONTINUAR"

                    if botao_menu.collidepoint(evento.pos):
                        return "MENU"

                    if botao_sair.collidepoint(evento.pos):
                        return "SAIR"

    def tela_escolha_carro(self, session):
        carros_disponiveis = [Porsche, F1]
        selecao_idx = 0

        cor_fundo = (0, 0, 0)
        cor_texto = (255, 255, 255)
        cor_selecionado = (255, 215, 0)  # Dourado
        cor_botao = (0, 150, 0)
        cor_botao_hover = (0, 200, 0)

        botao_confirmar = pygame.Rect(self.largura // 2 - 100, self.altura - 100, 200, 50)

        imagens_carros = []
        for classe_carro in carros_disponiveis:
            carro_temp = classe_carro(0, 0)
            largura_exibicao = 100
            proporcao = carro_temp.imagem.get_height() / carro_temp.imagem.get_width()
            altura_exibicao = int(largura_exibicao * proporcao)
            img = pygame.transform.scale(carro_temp.imagem, (largura_exibicao, altura_exibicao))  # Tamanho para exibição
            imagens_carros.append((img, carro_temp.nome, carro_temp.descricao))

        while True:
            self.tela.fill(cor_fundo)
            mouse = pygame.mouse.get_pos()

            # Título
            titulo = self.fonte_titulo_pontos.render("Escolha seu Carro", True, cor_texto)
            self.tela.blit(titulo, (self.largura // 2 - titulo.get_width() // 2, 50))

            # --- Desenha os carros e stats ---
            total_carros = len(carros_disponiveis)
            espacamento_x = self.largura // (total_carros + 1)

            for i, (img, nome, desc) in enumerate(imagens_carros):
                x_pos = espacamento_x * (i + 1)

                # Desenha a imagem
                img_rect = img.get_rect(center=(x_pos, self.altura // 2 - 50))
                self.tela.blit(img, img_rect)

                # Desenha o nome
                cor_nome = cor_selecionado if i == selecao_idx else cor_texto
                texto_nome = self.fonte_botao_media.render(nome, True, cor_nome)
                self.tela.blit(texto_nome, (x_pos - texto_nome.get_width() // 2, self.altura // 2 + 80))

                # Desenha a descrição
                y_desc = self.altura // 2 + 130
                for linha in desc:
                    texto_desc = self.fonte_desc.render(linha, True, cor_texto)
                    self.tela.blit(texto_desc, (x_pos - texto_desc.get_width() // 2, y_desc))
                    y_desc += 30

                # Borda de seleção
                if i == selecao_idx:
                    pygame.draw.rect(self.tela, cor_selecionado, img_rect.inflate(10, 10), 3, border_radius=5)

            # Botão Confirmar
            cor_b = cor_botao_hover if botao_confirmar.collidepoint(mouse) else cor_botao
            pygame.draw.rect(self.tela, cor_b, botao_confirmar, border_radius=8)
            texto_b = self.fonte_botao_media.render("Confirmar", True, cor_texto)
            self.tela.blit(texto_b, (botao_confirmar.centerx - texto_b.get_width() // 2,
                                     botao_confirmar.centery - texto_b.get_height() // 2))

            self.atualizar()

            # --- Eventos ---
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    session.close()
                    pygame.quit()
                    exit()

                if evento.type == pygame.KEYDOWN:
                    # Seleciona com as setas
                    if evento.key == pygame.K_LEFT:
                        selecao_idx = (selecao_idx - 1) % total_carros
                    if evento.key == pygame.K_RIGHT:
                        selecao_idx = (selecao_idx + 1) % total_carros
                    if evento.key == pygame.K_RETURN:  # Confirma com Enter
                        return carros_disponiveis[selecao_idx]

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if botao_confirmar.collidepoint(evento.pos):
                        # Retorna a CLASSE do carro selecionado
                        return carros_disponiveis[selecao_idx]

                    # Permite clicar no carro para selecionar
                    for i, (img, _, _) in enumerate(imagens_carros):
                        x_pos = espacamento_x * (i + 1)
                        img_rect = img.get_rect(center=(x_pos, self.altura // 2 - 50))
                        if img_rect.inflate(20, 20).collidepoint(evento.pos):
                            selecao_idx = i
                            break

