#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLAY TEA - Jogo Educacional
Ponto de entrada principal para a aplicação
"""

import pygame
import json
import os
import sys
import asyncio

# --- Configuração de Caminhos ---
# Os caminhos são relativos ao main.py para compatibilidade com pygbag
ASSETS_DIR = "assets"
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
DATA_DIR = "data"

# --- Inicialização ---
pygame.init()
try:
    pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
    pygame.mixer.init()
except:
    pygame.mixer.init()

# --- Constantes e Configurações ---
LARGURA_TELA_VIRTUAL = 800
ALTURA_TELA_VIRTUAL = 600

tela = pygame.display.set_mode((LARGURA_TELA_VIRTUAL, ALTURA_TELA_VIRTUAL), pygame.RESIZABLE)
tela_virtual = pygame.Surface((LARGURA_TELA_VIRTUAL, ALTURA_TELA_VIRTUAL))

pygame.display.set_caption("PLAY TEA")

# --- Fontes (OpenDyslexic) ---
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

def carregar_fonte(tamanho, negrito=False, italico=False):
    """Tenta carregar a fonte OpenDyslexic. Fallback para fonte padrão.

    A ordem é:
    1) Arquivo local em assets/fonts (vários nomes/formatos comuns)
    2) Fonte instalada no sistema (match_font com nomes conhecidos)
    3) Fonte padrão do pygame
    """
    # 1) Tenta arquivos locais comuns
    possiveis_arquivos = [
        "OpenDyslexic-Regular.otf",
        "OpenDyslexic-Regular.ttf",
        "OpenDyslexic3-Regular.otf",
        "OpenDyslexic3-Regular.ttf",
        "OpenDyslexic.otf",
        "OpenDyslexic.ttf",
    ]
    for nome_arquivo in possiveis_arquivos:
        caminho = os.path.join(FONTS_DIR, nome_arquivo)
        if os.path.exists(caminho):
            try:
                fonte = pygame.font.Font(caminho, tamanho)
                fonte.set_bold(negrito)
                fonte.set_italic(italico)
                return fonte
            except Exception:
                pass

    # 2) Tenta via fonte instalada no sistema (Pode falhar no browser, por isso é a 2ª)
    nomes_sistema = [
        "OpenDyslexic", "OpenDyslexic3", "opendyslexic", "opendyslexic3",
        "Open Dyslexic", "Open Dyslexic 3"
    ]
    for nome in nomes_sistema:
        try:
            caminho_match = pygame.font.match_font(nome, bold=negrito, italic=italico)
            if caminho_match:
                return pygame.font.Font(caminho_match, tamanho)
        except Exception:
            pass

    # 3) Fallback padrão (mais seguro no browser)
    try:
        fonte = pygame.font.SysFont(None, tamanho, bold=negrito, italic=italico)
        return fonte
    except Exception:
        return pygame.font.Font(None, tamanho)

# --- Estados do Jogo ---
TELA_INICIAL = "tela_inicial"
SELECAO_FASE = "selecao_fase"
JOGANDO = "jogando"
CONFIGURACOES = "configuracoes"
SOBRE = "sobre"
VITORIA = "vitoria"

# --- Cores ---
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0) # Cor para as barras pretas
VERDE_INICIO = (144, 238, 144)
VERDE_FIM = (60, 179, 113)
COR_BOTAO = (100, 100, 200)
COR_BOTAO_HOVER = (150, 150, 255)

# --- Variáveis de Configuração ---
COR_PONTINHOS = (255, 255, 0)  # Amarelo padrão para pontinhos
INICIO_ESCALA_RELATIVA = 1.3  # Escala do portão em relação ao tamanho da casa
MUSICAS_DISPONIVEIS = {
    "Mudo": None,
    "Ruído 1": os.path.join(AUDIO_DIR, "musica1.ogg"),
    "Ruído 2": os.path.join(AUDIO_DIR, "musica2.ogg")
}
MUSICA_ATUAL_NOME = "Mudo"

# Campos de usuário
NOME_CRIANCA = "Criança"
NOME_RESPONSAVEL = "Responsável"

# Controle de edição de texto
editando_nome_crianca = False
editando_nome_responsavel = False
texto_temporario_crianca = ""
texto_temporario_responsavel = ""
teclado_ativo = False

#Requisitos para desbloquear fases

REQUISITOS_FASES = {
1: 0, # Fase 1 sempre desbloqueada
}

# --- Progresso do Jogador ---
PONTOS_ACUMULADOS = 0  # Pontos totais ganhos em todas as fases
FASES_LIBERADAS = {1, 2, 3}  # Todas as fases liberadas
REPETICOES_POR_FASE = 5  # Número de repetições necessárias para completar uma fase
REPETICOES_ATUAIS = {}  # Contador de repetições por fase

# --- Controle de Fases ---
FASE_ATUAL_NUMERO = 1  # Controla qual fase o jogador está (1, 2 ou 3)
REPETICOES_FASE = {1: 0, 2: 0, 3: 0}  # Controla as repetições de cada fase

# --- Nomes das Fases ---
NOMES_FASES = {
    1: "Fase 1",
    2: "Fase 2", 
    3: "Fase 3"
}



# --- Fontes ---
fonte_titulo = carregar_fonte(48)
fonte_botao = carregar_fonte(24)
fonte_config = carregar_fonte(22)

# --- Carregar imagem de fundo para menu ---
fundo_menu_img = pygame.image.load(os.path.join(IMAGES_DIR, "fundo.png"))
fundo_menu_img = pygame.transform.smoothscale(fundo_menu_img, (LARGURA_TELA_VIRTUAL, ALTURA_TELA_VIRTUAL))
# Aplicar desfoque suave
fundo_menu_img = pygame.transform.smoothscale(fundo_menu_img, (LARGURA_TELA_VIRTUAL//2, ALTURA_TELA_VIRTUAL//2))
fundo_menu_img = pygame.transform.smoothscale(fundo_menu_img, (LARGURA_TELA_VIRTUAL, ALTURA_TELA_VIRTUAL))

# --- ESTRUTURA DE FASES ---
FASES = {
    1: {
        "peixe_img": os.path.join(IMAGES_DIR, "cachorro.png"),
        "fundo_img": os.path.join(IMAGES_DIR, "fundo 3.png"),
        "chegada_img": os.path.join(IMAGES_DIR, "casa.png"),
        "pontinhos": {"habilitado": True, "espacamento": 40}
    },
    2: {
        "peixe_img": os.path.join(IMAGES_DIR, "cachorro.png"),
        "fundo_img": os.path.join(IMAGES_DIR, "fundo 3.png"),
        "chegada_img": os.path.join(IMAGES_DIR, "casa.png"),
        "pontinhos": {"habilitado": True, "espacamento": 35}
    },
    3: {
        "peixe_img": os.path.join(IMAGES_DIR, "cachorro.png"),
        "fundo_img": os.path.join(IMAGES_DIR, "fundo 3.png"),
        "chegada_img": os.path.join(IMAGES_DIR, "casa.png"),
        "pontinhos": {"habilitado": True, "espacamento": 30}
    }
}

# --- Variáveis Globais do Jogo ---
# Imagens e recursos
peixinho_img_atual = None
fundo_img_atual = None
borda_img_atual = None
chegada_img_atual = None
inicio_img_original = None

# Áreas e posições
areas_validas_atual = []
area_inicio = pygame.Rect(0, ALTURA_TELA_VIRTUAL /1.89 - 60, 60, 60)
area_chegada = pygame.Rect(LARGURA_TELA_VIRTUAL - 120, ALTURA_TELA_VIRTUAL / 2 - 60, 120, 120)
posicao_peixinho = list(area_inicio.center)

# Pontinhos
pontinhos = []
pontuacao = 0

# Estado da fase
fase_atual = None
raio_borda_atual = 0

# Modo de edição
edit_mode = False
dragging = False
drag_rect_idx = None
editando_ponto_inicio = False
editando_ponto_chegada = False
adicionando_segmento = False
segmento_temporario = None
desenhando_caminho = False
caminho_temporario = []
criando_linha_reta = False
ponto_inicio_linha = None
personagem_iniciou_movimento = False

# Efeito de vitória
efeito_vitoria_ativo = False
tempo_efeito_vitoria = 0
DURACAO_EFEITO_VITORIA = 2000  # 2 segundos em milissegundos
som_vitoria = None

# --- Funções de Gerenciamento ---
def resetar_edicao():
    """Reseta todas as variáveis de modo de edição"""
    global edit_mode, dragging, drag_rect_idx, editando_ponto_inicio, editando_ponto_chegada
    global adicionando_segmento, segmento_temporario, desenhando_caminho, caminho_temporario
    global criando_linha_reta, ponto_inicio_linha, personagem_iniciou_movimento
    
    edit_mode = False
    dragging = False
    drag_rect_idx = None
    editando_ponto_inicio = False
    editando_ponto_chegada = False
    adicionando_segmento = False
    segmento_temporario = None
    desenhando_caminho = False
    caminho_temporario = []
    criando_linha_reta = False
    ponto_inicio_linha = None
    personagem_iniciou_movimento = False

def atualizar_areas_validas():
    """Atualiza a lista de áreas válidas"""
    global areas_validas_atual
    areas_validas_atual = [area_inicio, area_chegada]

def resetar_pontuacao():
    """Reseta a pontuação para zero"""
    global pontuacao
    pontuacao = 0

def adicionar_pontinho(x, y):
    """Adiciona um pontinho na posição especificada"""
    global pontinhos
    pontinhos.append((x, y))

def remover_pontinho(index):
    """Remove um pontinho pelo índice"""
    global pontinhos, pontuacao
    if 0 <= index < len(pontinhos):
        pontinhos.pop(index)
        pontuacao += 1

def limpar_pontinhos():
    """Remove todos os pontinhos"""
    global pontinhos
    pontinhos.clear()

def criar_linha_reta_pontinhos(x1, y1, x2, y2, espacamento=20):
    """Cria pontinhos em linha reta entre dois pontos"""
    # Calcula a distância entre os pontos
    distancia = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    
    if distancia < espacamento:
        # Se os pontos estão muito próximos, adiciona apenas um pontinho no meio
        adicionar_pontinho((x1 + x2) // 2, (y1 + y2) // 2)
        return
    
    # Calcula quantos pontinhos cabem na linha
    num_pontinhos = int(distancia / espacamento)
    
    # Cria os pontinhos distribuídos uniformemente
    for i in range(num_pontinhos + 1):
        t = i / num_pontinhos if num_pontinhos > 0 else 0
        x = int(x1 + t * (x2 - x1))
        y = int(y1 + t * (y2 - y1))
        adicionar_pontinho(x, y)

def verificar_vitoria():
    """Verifica se o jogador venceu (sem pontinhos restantes)"""
    return len(pontinhos) == 0

# --- Funções auxiliares para modificar variáveis globais ---

def set_area_inicio_center(pos):
    global area_inicio
    area_inicio.center = pos

def set_area_chegada_center(pos):
    global area_chegada
    area_chegada.center = pos

def set_posicao_peixinho(pos):
    global posicao_peixinho
    posicao_peixinho = list(pos)

botao_iniciar = pygame.Rect(LARGURA_TELA_VIRTUAL / 2 - 125, 250, 250, 60)
botao_config = pygame.Rect(LARGURA_TELA_VIRTUAL / 2 - 125, 340, 250, 60)
botao_sobre = pygame.Rect(LARGURA_TELA_VIRTUAL / 2 - 125, 430, 250, 60)
botao_voltar = pygame.Rect(LARGURA_TELA_VIRTUAL / 2 - 125, 500, 250, 60)
botao_sair_fase = pygame.Rect(20, 20, 100, 40)  # Canto superior esquerdo
botao_musica_fase = pygame.Rect(20, 70, 100, 40)  # Abaixo do botão sair
botao_voltar_menu = pygame.Rect(LARGURA_TELA_VIRTUAL - 120, 20, 100, 40)  # Canto superior direito
botoes_fase = {
    1: pygame.Rect(LARGURA_TELA_VIRTUAL / 2 - 100, 200, 200, 60),  # Cachorrinho (vai para fase 1)
    2: pygame.Rect(LARGURA_TELA_VIRTUAL / 2 - 100, 290, 200, 60),  # Gatinho (vai para fase 1)
}
cores_disponiveis = {"Areia": (255, 235, 153), "Grama": (152, 251, 152), "Terra": (210, 180, 140)}
botoes_cor = {}
botoes_musica = {}

# Layout em duas colunas
COLUNA_ESQ_X = LARGURA_TELA_VIRTUAL / 2 - 350
COLUNA_DIR_X = LARGURA_TELA_VIRTUAL / 2 + 50
LARG_BOTAO = 300
ALT_BOTAO = 50
ESPACO_V = 70
Y_INICIO_COLUNA = 260

# Campos de texto para nomes
campo_nome_crianca = pygame.Rect(LARGURA_TELA_VIRTUAL / 2 - 150, 120, 300, 35)
campo_nome_responsavel = pygame.Rect(LARGURA_TELA_VIRTUAL / 2 - 150, 160, 300, 35)
botao_salvar_nomes = pygame.Rect(LARGURA_TELA_VIRTUAL / 2 + 170, 140, 140, 40)

# Botões de Cor (coluna esquerda)
y_pos_cor = Y_INICIO_COLUNA
for nome, cor in cores_disponiveis.items():
    botoes_cor[nome] = pygame.Rect(COLUNA_ESQ_X, y_pos_cor, LARG_BOTAO, ALT_BOTAO)
    y_pos_cor += ESPACO_V

# Botões de Ruído de fundo (coluna direita)
y_pos_mus = Y_INICIO_COLUNA
for nome in MUSICAS_DISPONIVEIS.keys():
    botoes_musica[nome] = pygame.Rect(COLUNA_DIR_X, y_pos_mus, LARG_BOTAO, ALT_BOTAO)
    y_pos_mus += ESPACO_V

def tocar_musica_por_nome(nome):
    global MUSICA_ATUAL_NOME
    arquivo = MUSICAS_DISPONIVEIS.get(nome)
    try:
        if arquivo is None:
            pygame.mixer.music.stop()
            print(f"Musica parada (Mudo)")
        else:
            # Verifica se o arquivo existe
            if not os.path.exists(arquivo):
                print(f"Erro: arquivo de música não encontrado: {arquivo}")
                return
            
            # Para a música atual antes de carregar a nova
            pygame.mixer.music.stop()
            pygame.mixer.music.load(arquivo)
            pygame.mixer.music.play(-1)
            print(f"Musica tocando: {nome}")
        MUSICA_ATUAL_NOME = nome
    except pygame.error as e:
        print(f"Aviso: não foi possível tocar '{nome}': {e}")
        # Tenta reinicializar o mixer em caso de erro
        try:
            pygame.mixer.quit()
            pygame.mixer.init()
            print("Mixer reinicializado")
        except:
            print("Erro ao reinicializar mixer")

def iniciar_teclado_texto(rect_alvo=None):
    global teclado_ativo
    try:
        pygame.key.start_text_input()
        if rect_alvo is not None:
            # Define a área onde o cursor/IME deve focar
            pygame.key.set_text_input_rect(rect_alvo)
        teclado_ativo = True
    except Exception:
        teclado_ativo = False

def encerrar_teclado_texto():
    global teclado_ativo
    try:
        pygame.key.stop_text_input()
        teclado_ativo = False
    except Exception:
        teclado_ativo = False

def carregar_som_vitoria():
    """Carrega o som de vitória"""
    global som_vitoria
    try:
            arquivo_som = os.path.join(AUDIO_DIR, "vitoria.ogg")
        if os.path.exists(arquivo_som):
            som_vitoria = pygame.mixer.Sound(arquivo_som)
            print("Som de vitória carregado com sucesso!")
        else:
            print("Aviso: arquivo de som de vitória não encontrado")
    except pygame.error as e:
        print(f"Erro ao carregar som de vitória: {e}")

def tocar_som_vitoria():
    """Toca o som de vitória"""
    global som_vitoria
    try:
        if som_vitoria is not None:
            som_vitoria.play()
            print("Som de vitória tocado!")
    except pygame.error as e:
        print(f"Erro ao tocar som de vitória: {e}")

def iniciar_efeito_vitoria():
    """Inicia o efeito de vitória"""
    global efeito_vitoria_ativo, tempo_efeito_vitoria
    efeito_vitoria_ativo = True
    tempo_efeito_vitoria = pygame.time.get_ticks()
    tocar_som_vitoria()
    print("Efeito de vitória iniciado!")

# --- Funções ---
def carregar_fase(numero_fase):
    global peixinho_img_atual, fundo_img_atual, areas_validas_atual, posicao_peixinho, raio_borda_atual, fase_atual, borda_img_atual, chegada_img_atual, pontinhos, pontuacao, edit_mode, dragging, drag_rect_idx
    global editando_ponto_inicio, editando_ponto_chegada, adicionando_segmento, segmento_temporario, desenhando_caminho, caminho_temporario, area_inicio, area_chegada
    
    # Usa a fase atual definida por FASE_ATUAL_NUMERO, diferença apenas no sprite
    fase_info = FASES[FASE_ATUAL_NUMERO].copy()
    if numero_fase == 2:
            fase_info["peixe_img"] = os.path.join(IMAGES_DIR, "gato.png")  # Gatinho usa sprite do gato
    else:
            fase_info["peixe_img"] = os.path.join(IMAGES_DIR, "cachorro.png")  # Cachorrinho usa sprite do cachorro
    try:
        peixinho_img_atual = pygame.image.load(fase_info["peixe_img"]).convert_alpha()
        peixinho_img_atual = pygame.transform.scale(peixinho_img_atual, (80, 80))
        
        fundo_img_atual = pygame.image.load(fase_info["fundo_img"]).convert()
        fundo_img_atual = pygame.transform.scale(fundo_img_atual, (LARGURA_TELA_VIRTUAL, ALTURA_TELA_VIRTUAL))
        
        # Carrega imagem da área de início (portão)
        global inicio_img_original
        inicio_img_original = None
        try:
                    caminho_inicio = os.path.join(IMAGES_DIR, "portao.png")
            if os.path.exists(caminho_inicio):
                inicio_img_original = pygame.image.load(caminho_inicio).convert_alpha()
        except pygame.error as e:
            print(f"Aviso: não foi possível carregar imagem de início: {e}")
        
    except pygame.error as e:
        print(f"Erro ao carregar recursos da fase {numero_fase}: {e}")
        fundo_img_atual = pygame.Surface((LARGURA_TELA_VIRTUAL, ALTURA_TELA_VIRTUAL))
        fundo_img_atual.fill((0,0,0))
        return
    atualizar_areas_validas()
    posicao_peixinho = list(area_inicio.center)
    raio_borda_atual = 0
    fase_atual = numero_fase
    borda_img_atual = None
    
    # Inicializa contador de repetições para esta fase
    inicializar_repeticoes_fase(FASE_ATUAL_NUMERO)
    
    # Carrega imagem da chegada (opcional por fase)
    chegada_img_atual = None
    chegada_path = fase_info.get("chegada_img")
    if chegada_path:
        try:
            img = pygame.image.load(chegada_path).convert_alpha()
            chegada_img_atual = pygame.transform.smoothscale(img, (area_chegada.width, area_chegada.height))
        except pygame.error as e:
            print(f"Aviso: não foi possível carregar a imagem de chegada da fase {numero_fase}: {e}")
    
    # Inicializa pontinhos por fase (se habilitado)
    # Não reseta pontuação - deve ser cumulativa
    limpar_pontinhos()
    
    # Tenta carregar fase editada primeiro (após definir fase_atual)
    if numero_fase in [1, 2]:  # Ambos usam dados da fase 1
        carregar_fase_editada()
    
    # Se não carregou dados editados, usa configuração padrão
    if not pontinhos:
        pont_cfg = fase_info.get("pontinhos", {"habilitado": False})
        if pont_cfg.get("habilitado"):
            espac = int(pont_cfg.get("espacamento", 20))
            if numero_fase == 1:
                # Fase 1: linha reta
                for x in range(100, LARGURA_TELA_VIRTUAL - 100, espac):
                    adicionar_pontinho(x, area_inicio.centery)
            else:
                # Fases 2 e 3: pontinhos em linha reta simples
                for x in range(100, LARGURA_TELA_VIRTUAL - 100, espac):
                    adicionar_pontinho(x, area_inicio.centery)
    # reseta edição
    resetar_edicao()
    
def salvar_fase_editada():
    """Salva as modificações da fase atual em arquivo JSON"""
    dados = {
        "pontinhos": pontinhos,
        "area_inicio": (area_inicio.x, area_inicio.y, area_inicio.width, area_inicio.height),
        "area_chegada": (area_chegada.x, area_chegada.y, area_chegada.width, area_chegada.height)
    }
    try:
        filename = f"fase{FASE_ATUAL_NUMERO}_editada.json"
        filepath = os.path.join(DATA_DIR, filename)

        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        with open(filepath, "w") as f:
            json.dump(dados, f)
        print(f"Fase {FASE_ATUAL_NUMERO} salva com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar: {e}")

def salvar_configuracoes():
    """Salva as configurações do jogo em arquivo JSON"""
    dados = {
        "cor_pontinhos": COR_PONTINHOS,
        "musica_atual": MUSICA_ATUAL_NOME,
        "repeticoes_atuais": REPETICOES_ATUAIS,
        "fase_atual_numero": FASE_ATUAL_NUMERO,
        "repeticoes_fase": REPETICOES_FASE,
        "pontos_acumulados": PONTOS_ACUMULADOS,
        "nome_crianca": NOME_CRIANCA,
        "nome_responsavel": NOME_RESPONSAVEL
    }
    try:
            config_path = os.path.join(DATA_DIR, "configuracoes.json")

        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        with open(config_path, "w") as f:
            json.dump(dados, f)
        print("Configurações salvas com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar configurações: {e}")

def carregar_configuracoes():
    """Carrega as configurações do jogo do arquivo JSON"""
    try:
            config_path = os.path.join(DATA_DIR, "configuracoes.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                dados = json.load(f)
            global COR_PONTINHOS, MUSICA_ATUAL_NOME, REPETICOES_ATUAIS, FASE_ATUAL_NUMERO, REPETICOES_FASE, PONTOS_ACUMULADOS, NOME_CRIANCA, NOME_RESPONSAVEL
            COR_PONTINHOS = tuple(dados.get("cor_pontinhos", COR_PONTINHOS))
            MUSICA_ATUAL_NOME = dados.get("musica_atual", MUSICA_ATUAL_NOME)
            REPETICOES_ATUAIS = dados.get("repeticoes_atuais", {})
            FASE_ATUAL_NUMERO = dados.get("fase_atual_numero", FASE_ATUAL_NUMERO)
            REPETICOES_FASE = dados.get("repeticoes_fase", REPETICOES_FASE)
            PONTOS_ACUMULADOS = dados.get("pontos_acumulados", PONTOS_ACUMULADOS)
            NOME_CRIANCA = dados.get("nome_crianca", NOME_CRIANCA)
            NOME_RESPONSAVEL = dados.get("nome_responsavel", NOME_RESPONSAVEL)
            print("Configurações carregadas com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar configurações: {e}")

def inicializar_repeticoes_fase(fase):
    """Inicializa o contador de repetições para uma fase se não existir"""
    if fase not in REPETICOES_FASE:
        REPETICOES_FASE[fase] = 0


def carregar_fase_editada():
    """Carrega as modificações salvas da fase"""
    global pontinhos, area_inicio, area_chegada, areas_validas_atual
    try:
        filename = f"fase{FASE_ATUAL_NUMERO}_editada.json"
            filepath = os.path.join(DATA_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                dados = json.load(f)
            
            # Restaura pontinhos
            pontinhos = dados["pontinhos"]
            
            # Restaura áreas de início e chegada
            area_inicio = pygame.Rect(*dados["area_inicio"])
            area_chegada = pygame.Rect(*dados["area_chegada"])
            
            atualizar_areas_validas()
            print(f"Fase {FASE_ATUAL_NUMERO} carregada com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar fase editada: {e}")
        # Se der erro, continua com configuração padrão

def avancar_para_proxima_fase():
    """Avança para a próxima fase"""
    global FASE_ATUAL_NUMERO
    if FASE_ATUAL_NUMERO < 3:
        FASE_ATUAL_NUMERO += 1
        print(f"Avançando para {NOMES_FASES[FASE_ATUAL_NUMERO]}")
    else:
        # Volta para seleção de personagens após completar fase 3
        FASE_ATUAL_NUMERO = 1
        print("Todas as fases completadas! Voltando para seleção de personagens.")


def recomputar_pontinhos_fase_atual():
    global pontinhos
    fase_info = FASES[FASE_ATUAL_NUMERO]
    pont_cfg = fase_info.get("pontinhos", {"habilitado": False})
    limpar_pontinhos()
    if not pont_cfg.get("habilitado"):
        return
    espac = int(pont_cfg.get("espacamento", 20))
    # Todas as fases usam linha reta simples
    for x in range(100, LARGURA_TELA_VIRTUAL - 100, espac):
        adicionar_pontinho(x, area_inicio.centery)
    
def desenhar_texto(texto, fonte, cor, superficie, x, y):
    textobj = fonte.render(texto, True, cor)
    textrect = textobj.get_rect(center=(x, y))
    superficie.blit(textobj, textrect)

def desenhar_botao(rect, texto, fonte, cor_normal, cor_hover, mouse_pos, superficie):
    """Função genérica para desenhar botões"""
    cor = cor_hover if rect.collidepoint(mouse_pos) else cor_normal
    pygame.draw.rect(superficie, cor, rect, border_radius=15)
    desenhar_texto(texto, fonte, BRANCO, superficie, rect.centerx, rect.centery)

def desenhar_fundo_com_overlay():
    """Função genérica para desenhar fundo com overlay escuro"""
    tela_virtual.blit(fundo_menu_img, (0, 0))
    overlay = pygame.Surface((LARGURA_TELA_VIRTUAL, ALTURA_TELA_VIRTUAL), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    tela_virtual.blit(overlay, (0, 0))

def desenhar_efeito_vitoria():
    """Desenha o efeito de vitória com brilho amarelo"""
    global efeito_vitoria_ativo
    
    if not efeito_vitoria_ativo:
        return
    
    tempo_atual = pygame.time.get_ticks()
    tempo_decorrido = tempo_atual - tempo_efeito_vitoria
    
    if tempo_decorrido >= DURACAO_EFEITO_VITORIA:
        # Efeito terminou
        efeito_vitoria_ativo = False
        return
    
    # Calcula a intensidade do efeito (fade in e fade out)
    progresso = tempo_decorrido / DURACAO_EFEITO_VITORIA
    
    if progresso <= 0.5:
        # Fade in (primeira metade)
        intensidade = int(255 * (progresso * 2))
    else:
        # Fade out (segunda metade)
        intensidade = int(255 * (2 - progresso * 2))
    
    # Cria overlay amarelo transparente
    overlay_amarelo = pygame.Surface((LARGURA_TELA_VIRTUAL, ALTURA_TELA_VIRTUAL), pygame.SRCALPHA)
    overlay_amarelo.fill((255, 255, 0, intensidade // 3))  # Amarelo com transparência
    tela_virtual.blit(overlay_amarelo, (0, 0))

# --- Funções de Desenho das Telas (AGORA DESENHAM NA TELA_VIRTUAL) ---
def desenhar_tela_inicial(mouse_pos):
    desenhar_fundo_com_overlay()
    
    desenhar_texto("PLAY TEA", fonte_titulo, BRANCO, tela_virtual, LARGURA_TELA_VIRTUAL / 2, 120)
    
    desenhar_botao(botao_iniciar, "Jogar", fonte_botao, COR_BOTAO, COR_BOTAO_HOVER, mouse_pos, tela_virtual)
    desenhar_botao(botao_config, "Configurações", fonte_botao, COR_BOTAO, COR_BOTAO_HOVER, mouse_pos, tela_virtual)
    desenhar_botao(botao_sobre, "Sobre", fonte_botao, COR_BOTAO, COR_BOTAO_HOVER, mouse_pos, tela_virtual)

def desenhar_selecao_fase(mouse_pos):
    desenhar_fundo_com_overlay()
    
    desenhar_texto("Selecione o Personagem", fonte_titulo, BRANCO, tela_virtual, LARGURA_TELA_VIRTUAL / 2, 80)

    for num, rect in botoes_fase.items():
        nome_personagem = "Cachorrinho" if num == 1 else "Gatinho"
        desenhar_botao(rect, nome_personagem, fonte_botao, COR_BOTAO, COR_BOTAO_HOVER, mouse_pos, tela_virtual)

    desenhar_botao(botao_voltar, "Voltar", fonte_botao, COR_BOTAO, COR_BOTAO_HOVER, mouse_pos, tela_virtual)


def desenhar_configuracoes(mouse_pos):
    desenhar_fundo_com_overlay()
    
    desenhar_texto("Configurações", fonte_titulo, BRANCO, tela_virtual, LARGURA_TELA_VIRTUAL / 2, 50)
    
    # Campos de nome
    fonte_label = carregar_fonte(20)
    desenhar_texto("Criança:", fonte_label, BRANCO, tela_virtual, LARGURA_TELA_VIRTUAL / 2.2 - 180, 140)
    desenhar_texto("Responsável:", fonte_label, BRANCO, tela_virtual, LARGURA_TELA_VIRTUAL / 2.35 - 180, 180)
    
    # Campos de texto para nomes
    cor_campo_crianca = (255, 255, 255) if editando_nome_crianca else (200, 200, 200)
    cor_campo_responsavel = (255, 255, 255) if editando_nome_responsavel else (200, 200, 200)
    
    pygame.draw.rect(tela_virtual, cor_campo_crianca, campo_nome_crianca, border_radius=5)
    pygame.draw.rect(tela_virtual, PRETO, campo_nome_crianca, 2, border_radius=5)
    
    pygame.draw.rect(tela_virtual, cor_campo_responsavel, campo_nome_responsavel, border_radius=5)
    pygame.draw.rect(tela_virtual, PRETO, campo_nome_responsavel, 2, border_radius=5)
    
    # Texto dos campos
    fonte_campo = carregar_fonte(18)
    texto_crianca = texto_temporario_crianca if editando_nome_crianca else NOME_CRIANCA
    texto_responsavel = texto_temporario_responsavel if editando_nome_responsavel else NOME_RESPONSAVEL
    
    desenhar_texto(texto_crianca, fonte_campo, PRETO, tela_virtual, campo_nome_crianca.centerx, campo_nome_crianca.centery)
    desenhar_texto(texto_responsavel, fonte_campo, PRETO, tela_virtual, campo_nome_responsavel.centerx, campo_nome_responsavel.centery)
    
    # Botão único de salvar
    cor_btn_salvar = COR_BOTAO_HOVER if botao_salvar_nomes.collidepoint(mouse_pos) else COR_BOTAO
    pygame.draw.rect(tela_virtual, cor_btn_salvar, botao_salvar_nomes, border_radius=8)
    fonte_btn = carregar_fonte(18)
    desenhar_texto("Salvar", fonte_btn, BRANCO, tela_virtual, botao_salvar_nomes.centerx, botao_salvar_nomes.centery)
    
    # Títulos das colunas (movidos para baixo)
    desenhar_texto("Cor dos pontinhos", fonte_config, BRANCO, tela_virtual, COLUNA_ESQ_X + LARG_BOTAO/2, 220)
    desenhar_texto("Ruído de fundo", fonte_config, BRANCO, tela_virtual, COLUNA_DIR_X + LARG_BOTAO/2, 220)

    # Coluna esquerda: cores
    for nome, rect in botoes_cor.items():
        cor_rgb = cores_disponiveis[nome]
        pygame.draw.rect(tela_virtual, cor_rgb, rect, border_radius=10)
        desenhar_texto(nome, fonte_botao, PRETO, tela_virtual, rect.centerx, rect.centery)
        if COR_PONTINHOS == cor_rgb: pygame.draw.rect(tela_virtual, PRETO, rect, 4, border_radius=10)

    # Coluna direita: músicas
    for nome, rect in botoes_musica.items():
        cor_btn = (60, 60, 120) if MUSICA_ATUAL_NOME != nome else (120, 180, 120)
        pygame.draw.rect(tela_virtual, cor_btn, rect, border_radius=10)
        desenhar_texto(nome, fonte_botao, BRANCO, tela_virtual, rect.centerx, rect.centery)
        if rect.collidepoint(mouse_pos) and MUSICA_ATUAL_NOME != nome:
            pygame.draw.rect(tela_virtual, (180, 180, 240), rect, 3, border_radius=10)
    
    cor_voltar = COR_BOTAO_HOVER if botao_voltar.collidepoint(mouse_pos) else COR_BOTAO
    pygame.draw.rect(tela_virtual, cor_voltar, botao_voltar, border_radius=15)
    desenhar_texto("Voltar", fonte_botao, BRANCO, tela_virtual, botao_voltar.centerx, botao_voltar.centery)

def desenhar_tela_sobre(mouse_pos):
    desenhar_fundo_com_overlay()
    
    # Carregar logo (vai ser exibida ao final, centralizada na parte inferior)
    try:
            logo_fatec = pygame.image.load(os.path.join(IMAGES_DIR, "logo.png")).convert_alpha()
        logo_fatec = pygame.transform.smoothscale(logo_fatec, (120, 60))
    except pygame.error as e:
        logo_fatec = None
        print(f"Aviso: não foi possível carregar o logo da Fatec: {e}")
    
    # Painel de fundo semitransparente para os textos (cinza)
    painel_x = 60
    painel_y = 60
    painel_larg = LARGURA_TELA_VIRTUAL - 2 * painel_x
    painel_alt = ALTURA_TELA_VIRTUAL - 2 * painel_y
    painel = pygame.Surface((painel_larg, painel_alt), pygame.SRCALPHA)
    pygame.draw.rect(painel, (128, 128, 128, 160), painel.get_rect(), border_radius=20)
    tela_virtual.blit(painel, (painel_x, painel_y))

    # Título principal
    desenhar_texto("PLAY TEA", fonte_titulo, BRANCO, tela_virtual, LARGURA_TELA_VIRTUAL / 2, 100)
    
    # Fontes para diferentes seções
    fonte_titulo_secao = carregar_fonte(24)
    fonte_info = carregar_fonte(22)
    fonte_desenvolvedores = carregar_fonte(20)
    fonte_pequena = carregar_fonte(16)
    
    # Seção: Informações do Projeto removida conforme solicitação
    
    
    # Seção: Desenvolvedores (centralizados)
    desenhar_texto("Desenvolvedores", fonte_titulo_secao, BRANCO, tela_virtual, LARGURA_TELA_VIRTUAL / 2, 200)
    y_desenvolvedores = 240
    desenvolvedores = [
        "DENILSON CONCEIÇÃO DE OLIVEIRA",
        "JONATHAS YOSHIOKA OLSEN TRAJANO DA SILVA",
        "LEONARDO ZANATA DE JESUS",
        "MATHEUS GARCIA BERTOI"
    ]
    for dev in desenvolvedores:
        nome_formatado = dev.title()
        desenhar_texto(nome_formatado, fonte_desenvolvedores, BRANCO, tela_virtual, LARGURA_TELA_VIRTUAL / 2, y_desenvolvedores)
        y_desenvolvedores += 30
    
    # Orientador junto aos demais nomes
    y_desenvolvedores += 10
    desenhar_texto("Orientador", fonte_titulo_secao, BRANCO, tela_virtual, LARGURA_TELA_VIRTUAL / 2, y_desenvolvedores)
    y_desenvolvedores += 30
    desenhar_texto("Prof. Dr. Irapuan Glória Júnior", fonte_info, BRANCO, tela_virtual, LARGURA_TELA_VIRTUAL / 2, y_desenvolvedores)
    
    # Exibir logo centralizada na parte inferior do painel cinza (dentro do retângulo)
    if logo_fatec is not None:
        logo_rect = logo_fatec.get_rect()
        logo_rect.centerx = LARGURA_TELA_VIRTUAL // 2
        logo_rect.bottom = painel_y + painel_alt - 20
        tela_virtual.blit(logo_fatec, logo_rect)

    # Versão no canto inferior direito
    texto_versao = fonte_pequena.render("Versão 1.1", True, BRANCO)
    rect_versao = texto_versao.get_rect()
    rect_versao.bottomright = (LARGURA_TELA_VIRTUAL - 20, ALTURA_TELA_VIRTUAL - 20)
    tela_virtual.blit(texto_versao, rect_versao)
    
    # Botão voltar no canto superior esquerdo
    botao_voltar_sobre = pygame.Rect(20, 20, 100, 40)
    cor_voltar = COR_BOTAO_HOVER if botao_voltar_sobre.collidepoint(mouse_pos) else COR_BOTAO
    pygame.draw.rect(tela_virtual, cor_voltar, botao_voltar_sobre, border_radius=10)
    desenhar_texto("Voltar", fonte_config, BRANCO, tela_virtual, botao_voltar_sobre.centerx, botao_voltar_sobre.centery)
    
def desenhar_jogo(mouse_pos=(0, 0)):
    tela_virtual.blit(fundo_img_atual, (0, 0))
    # Desenha a área de início com imagem (fallback: retângulo verde)
    if inicio_img_original is not None:
        try:
            # Usa o tamanho da chegada (sprite da casa) com escala relativa
            largura_chegada = int(area_chegada.width * INICIO_ESCALA_RELATIVA)
            altura_chegada = int(area_chegada.height * INICIO_ESCALA_RELATIVA)
            img_inicio = pygame.transform.smoothscale(inicio_img_original, (largura_chegada, altura_chegada))
            rect_img_inicio = img_inicio.get_rect(center=area_inicio.center)
            tela_virtual.blit(img_inicio, rect_img_inicio)
        except Exception:
            pygame.draw.rect(tela_virtual, VERDE_INICIO, area_inicio)
    else:
        pygame.draw.rect(tela_virtual, VERDE_INICIO, area_inicio)
    
    # Fallback: desenha caminho retangular (caso não haja pontinhos)
    # Removido: não desenha mais o caminho quando não há pontinhos

    # Se edit mode ativo, destacar elementos editáveis
    if edit_mode and fase_atual in [1, 2, 3]:
        # Destacar pontos de início e chegada
        pygame.draw.rect(tela_virtual, (0, 255, 0), area_inicio, 3)
        pygame.draw.rect(tela_virtual, (0, 255, 0), area_chegada, 3)
        
        # Mostrar instruções
        fonte_instrucoes = carregar_fonte(16)
        instrucoes = [
            "E: Sair do modo edição",
            "I: Mover início",
            "C: Mover chegada",
            "P: Adicionar pontinhos",
            "L: Linha reta de pontinhos",
            "R: Limpar pontinhos",
            "S: Salvar mudanças",
            "Clique: Posicionar pontinho",
            "L+Clique: Criar linha reta"
        ]
        for i, texto in enumerate(instrucoes):
            tela_virtual.blit(fonte_instrucoes.render(texto, True, BRANCO), (10, 10 + i * 25))
        
        # Mostrar indicador de modo linha reta
        if criando_linha_reta:
            if ponto_inicio_linha is not None:
                # Mostrar ponto de início e linha até o mouse
                pygame.draw.circle(tela_virtual, (255, 255, 0), ponto_inicio_linha, 8)
                pygame.draw.line(tela_virtual, (255, 255, 0), ponto_inicio_linha, mouse_pos, 2)
                texto_linha = fonte_instrucoes.render("Clique para finalizar linha", True, (255, 255, 0))
                tela_virtual.blit(texto_linha, (10, 10 + len(instrucoes) * 25 + 10))
            else:
                texto_linha = fonte_instrucoes.render("Clique para iniciar linha", True, (255, 255, 0))
                tela_virtual.blit(texto_linha, (10, 10 + len(instrucoes) * 25 + 10))

    # Desenha a chegada por cima do caminho
    if chegada_img_atual is not None:
        tela_virtual.blit(chegada_img_atual, area_chegada.topleft)
    else:
        pygame.draw.rect(tela_virtual, VERDE_FIM, area_chegada)

    # Nome da fase no topo centralizado
    fonte_fase = carregar_fonte(28)
    nome_fase = NOMES_FASES.get(FASE_ATUAL_NUMERO, f"Fase {FASE_ATUAL_NUMERO}")
    desenhar_texto(nome_fase, fonte_fase, BRANCO, tela_virtual, LARGURA_TELA_VIRTUAL / 2, 30)
    
    # Desenha pontuação no canto superior direito (se houver pontinhos)
    if True:
        fonte_pontuacao = carregar_fonte(18)
        texto_pontuacao = fonte_pontuacao.render(f"Pontos: {PONTOS_ACUMULADOS + pontuacao}", True, BRANCO)
        tela_virtual.blit(texto_pontuacao, (LARGURA_TELA_VIRTUAL - 150, 20))
        
        # Progresso de repetições mantido internamente (não exibido na tela)
    
    # Botão para sair da fase (canto superior esquerdo)
    try:
        cor_sair_fase = COR_BOTAO_HOVER if botao_sair_fase.collidepoint(mouse_pos) else COR_BOTAO
        pygame.draw.rect(tela_virtual, cor_sair_fase, botao_sair_fase, border_radius=10)
        desenhar_texto("Sair", fonte_config, BRANCO, tela_virtual, botao_sair_fase.centerx, botao_sair_fase.centery)
    except:
        # Fallback se mouse_pos não estiver definido
        pygame.draw.rect(tela_virtual, COR_BOTAO, botao_sair_fase, border_radius=10)
        desenhar_texto("Sair", fonte_config, BRANCO, tela_virtual, botao_sair_fase.centerx, botao_sair_fase.centery)
    
    # Nome da criança (ao lado do botão sair)
    fonte_nome = carregar_fonte(18)
    texto_nome_crianca = fonte_nome.render(f"Criança: {NOME_CRIANCA}", True, BRANCO)
    # Posiciona o texto ao lado do botão sair
    tela_virtual.blit(texto_nome_crianca, (botao_sair_fase.right + 10, botao_sair_fase.centery - 10))
    
    # Botão para alternar música (abaixo do botão sair)
    try:
        cor_musica_fase = COR_BOTAO_HOVER if botao_musica_fase.collidepoint(mouse_pos) else COR_BOTAO
        pygame.draw.rect(tela_virtual, cor_musica_fase, botao_musica_fase, border_radius=10)
        # Mostra o nome da música atual ou "Ruído de fundo"
        texto_musica = MUSICA_ATUAL_NOME if len(MUSICA_ATUAL_NOME) <= 8 else "Ruído de fundo"
        desenhar_texto(texto_musica, fonte_config, BRANCO, tela_virtual, botao_musica_fase.centerx, botao_musica_fase.centery)
    except:
        # Fallback se mouse_pos não estiver definido
        pygame.draw.rect(tela_virtual, COR_BOTAO, botao_musica_fase, border_radius=10)
        desenhar_texto("Ruído de fundo", fonte_config, BRANCO, tela_virtual, botao_musica_fase.centerx, botao_musica_fase.centery)

    peixinho_rect = peixinho_img_atual.get_rect(center=posicao_peixinho)
    tela_virtual.blit(peixinho_img_atual, peixinho_rect)
    
    # Desenha pontinhos por cima de tudo (se houver)
    if len(pontinhos) > 0:
        for x, y in pontinhos:
            pygame.draw.circle(tela_virtual, COR_PONTINHOS, (x, y), 8)
    
    # Desenha efeito de vitória por cima de tudo
    desenhar_efeito_vitoria()

def desenhar_tela_vitoria():
    tela_virtual.blit(fundo_img_atual, (0, 0))
    sombra = pygame.Surface((LARGURA_TELA_VIRTUAL, ALTURA_TELA_VIRTUAL), pygame.SRCALPHA)
    sombra.fill((0, 0, 0, 128))
    tela_virtual.blit(sombra, (0, 0))
    desenhar_texto("Parabéns!", fonte_titulo, BRANCO, tela_virtual, LARGURA_TELA_VIRTUAL/2, ALTURA_TELA_VIRTUAL/2 - 100)
    
    nome_fase = NOMES_FASES.get(FASE_ATUAL_NUMERO, f"Fase {FASE_ATUAL_NUMERO}")
    desenhar_texto(f"{nome_fase} completada!", fonte_config, BRANCO, tela_virtual, LARGURA_TELA_VIRTUAL/2, ALTURA_TELA_VIRTUAL/2 - 50)
    desenhar_texto(f"Repetições: {REPETICOES_FASE.get(FASE_ATUAL_NUMERO, 0)}/{REPETICOES_POR_FASE}", fonte_config, BRANCO, tela_virtual, LARGURA_TELA_VIRTUAL/2, ALTURA_TELA_VIRTUAL/2)
    
    # Verifica se há próxima fase
    if FASE_ATUAL_NUMERO < 3:
        desenhar_texto("Clique para continuar para a próxima fase", fonte_config, BRANCO, tela_virtual, LARGURA_TELA_VIRTUAL/2, ALTURA_TELA_VIRTUAL/2 + 50)
    else:
        desenhar_texto("Todas as fases completadas!", fonte_config, (255, 255, 0), tela_virtual, LARGURA_TELA_VIRTUAL/2, ALTURA_TELA_VIRTUAL/2 + 30)
        desenhar_texto("Clique para voltar à seleção de personagens", fonte_config, (255, 255, 0), tela_virtual, LARGURA_TELA_VIRTUAL/2, ALTURA_TELA_VIRTUAL/2 + 60)

def desenhar_borda_texturizada(superficie, rect, imagem, thickness=16):
    tile_w, tile_h = imagem.get_size()
    # Topo
    x = rect.left
    while x < rect.right:
        largura = min(tile_w, rect.right - x)
        tile = pygame.transform.smoothscale(imagem, (largura, thickness))
        superficie.blit(tile, (x, rect.top - thickness // 2))
        x += largura
    # Base
    x = rect.left
    while x < rect.right:
        largura = min(tile_w, rect.right - x)
        tile = pygame.transform.smoothscale(imagem, (largura, thickness))
        superficie.blit(tile, (x, rect.bottom - thickness // 2))
        x += largura
    # Esquerda
    y = rect.top
    while y < rect.bottom:
        altura = min(tile_h, rect.bottom - y)
        tile = pygame.transform.smoothscale(imagem, (thickness, altura))
        superficie.blit(tile, (rect.left - thickness // 2, y))
        y += altura
    # Direita
    y = rect.top
    while y < rect.bottom:
        altura = min(tile_h, rect.bottom - y)
        tile = pygame.transform.smoothscale(imagem, (thickness, altura))
        superficie.blit(tile, (rect.right - thickness // 2, y))
        y += altura

# --- Loop Principal ---
async def main_loop():
    global rodando, estado_jogo, pos_mouse, editando_nome_crianca, \
           editando_nome_responsavel, texto_temporario_crianca, \
           texto_temporario_responsavel, NOME_CRIANCA, NOME_RESPONSAVEL, \
           COR_PONTINHOS, MUSICA_ATUAL_NOME, FASE_ATUAL_NUMERO, \
           dragging, drag_rect_idx, ponto_inicio_linha, \
           personagem_iniciou_movimento, PONTOS_ACUMULADOS, \
           edit_mode, editando_ponto_inicio, editando_ponto_chegada, \
           desenhando_caminho, criando_linha_reta

    while rodando:
        pos_mouse_janela = pygame.mouse.get_pos()
        largura_janela_atual, altura_janela_atual = tela.get_size()

        escala = min(largura_janela_atual / LARGURA_TELA_VIRTUAL, altura_janela_atual / ALTURA_TELA_VIRTUAL)
        
        nova_largura_escalada = LARGURA_TELA_VIRTUAL * escala
        nova_altura_escalada = ALTURA_TELA_VIRTUAL * escala
        
        offset_x = (largura_janela_atual - nova_largura_escalada) / 2
        offset_y = (altura_janela_atual - nova_altura_escalada) / 2

        mouse_x_virtual = (pos_mouse_janela[0] - offset_x) / escala if escala > 0 else 0
        mouse_y_virtual = (pos_mouse_janela[1] - offset_y) / escala if escala > 0 else 0
        pos_mouse = (mouse_x_virtual, mouse_y_virtual)

        # --- Processamento de Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if estado_jogo == TELA_INICIAL:
                    if botao_iniciar.collidepoint(pos_mouse): estado_jogo = SELECAO_FASE
                    if botao_config.collidepoint(pos_mouse): estado_jogo = CONFIGURACOES
                    if botao_sobre.collidepoint(pos_mouse): estado_jogo = SOBRE

                elif estado_jogo == SELECAO_FASE:
                    for num, rect in botoes_fase.items():
                        if rect.collidepoint(pos_mouse):
                            carregar_fase(num)
                            estado_jogo = JOGANDO
                    if botao_voltar.collidepoint(pos_mouse):
                        estado_jogo = TELA_INICIAL


                elif estado_jogo == CONFIGURACOES:
                    if botao_voltar.collidepoint(pos_mouse): 
                        estado_jogo = TELA_INICIAL
                        salvar_configuracoes()  # Salvar ao sair das configurações
                        # Encerra qualquer edição e teclado
                        editando_nome_crianca = False
                        editando_nome_responsavel = False
                        texto_temporario_crianca = ""
                        texto_temporario_responsavel = ""
                        encerrar_teclado_texto()
                    elif campo_nome_crianca.collidepoint(pos_mouse):
                        editando_nome_crianca = True
                        texto_temporario_crianca = NOME_CRIANCA
                        editando_nome_responsavel = False
                        iniciar_teclado_texto(campo_nome_crianca)
                    elif campo_nome_responsavel.collidepoint(pos_mouse):
                        editando_nome_responsavel = True
                        texto_temporario_responsavel = NOME_RESPONSAVEL
                        editando_nome_crianca = False
                        iniciar_teclado_texto(campo_nome_responsavel)
                    elif botao_salvar_nomes.collidepoint(pos_mouse):
                        # Salvar ambos os campos (se estiverem em edição) e sair da edição
                        if editando_nome_crianca:
                            NOME_CRIANCA = texto_temporario_crianca
                        if editando_nome_responsavel:
                            NOME_RESPONSAVEL = texto_temporario_responsavel
                        salvar_configuracoes()
                        editando_nome_crianca = False
                        editando_nome_responsavel = False
                        texto_temporario_crianca = ""
                        texto_temporario_responsavel = ""
                        encerrar_teclado_texto()
                    for nome, rect in botoes_cor.items():
                        if rect.collidepoint(pos_mouse): 
                            COR_PONTINHOS = cores_disponiveis[nome]
                            salvar_configuracoes()  # Salvar imediatamente
                    for nome, rect in botoes_musica.items():
                        if rect.collidepoint(pos_mouse): 
                            tocar_musica_por_nome(nome)
                            salvar_configuracoes()  # Salvar imediatamente
                
                elif estado_jogo == SOBRE:
                    # Botão voltar específico da tela sobre
                    botao_voltar_sobre = pygame.Rect(20, 20, 100, 40)
                    if botao_voltar_sobre.collidepoint(pos_mouse): 
                        estado_jogo = TELA_INICIAL

                elif estado_jogo == VITORIA:
                    # Verifica se há próxima fase ou volta para seleção
                    if FASE_ATUAL_NUMERO < 3:
                        # Avança para próxima fase
                        avancar_para_proxima_fase()
                        carregar_fase(fase_atual)
                        estado_jogo = JOGANDO
                    else:
                        # Volta para seleção de personagens
                        FASE_ATUAL_NUMERO = 1
                        estado_jogo = SELECAO_FASE
                
                elif estado_jogo == JOGANDO:
                    if botao_sair_fase.collidepoint(pos_mouse): 
                        estado_jogo = SELECAO_FASE
                    elif botao_musica_fase.collidepoint(pos_mouse):
                        # Alternar para próxima música
                        musicas_lista = list(MUSICAS_DISPONIVEIS.keys())
                        try:
                            indice_atual = musicas_lista.index(MUSICA_ATUAL_NOME)
                            proxima_musica = musicas_lista[(indice_atual + 1) % len(musicas_lista)]
                        except ValueError:
                            proxima_musica = musicas_lista[0]
                        
                        tocar_musica_por_nome(proxima_musica)
                        salvar_configuracoes()  # Salvar a mudança
                    elif fase_atual in [1, 2, 3] and edit_mode:
                        # Modo de edição ativo
                        if desenhando_caminho:
                            # Adicionar pontinho individual na posição clicada
                            adicionar_pontinho(int(pos_mouse[0]), int(pos_mouse[1]))
                        elif criando_linha_reta:
                            # Modo de linha reta
                            if ponto_inicio_linha is None:
                                # Primeiro clique: definir ponto de início
                                ponto_inicio_linha = (int(pos_mouse[0]), int(pos_mouse[1]))
                            else:
                                # Segundo clique: criar linha reta
                                criar_linha_reta_pontinhos(
                                    ponto_inicio_linha[0], ponto_inicio_linha[1],
                                    int(pos_mouse[0]), int(pos_mouse[1])
                                )
                                ponto_inicio_linha = None
                        elif editando_ponto_inicio:
                            # Mover ponto de início
                            set_area_inicio_center(pos_mouse)
                            atualizar_areas_validas()
                            set_posicao_peixinho(area_inicio.center)
                        elif editando_ponto_chegada:
                            # Mover ponto de chegada
                            set_area_chegada_center(pos_mouse)
                            atualizar_areas_validas()

            if evento.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    dragging = False
                    drag_rect_idx = None
                    recomputar_pontinhos_fase_atual()

            if evento.type == pygame.TEXTINPUT:
                if estado_jogo == CONFIGURACOES:
                    texto_digitado = evento.text
                    if editando_nome_crianca:
                        if len(texto_temporario_crianca) < 20:
                            texto_temporario_crianca += texto_digitado
                    elif editando_nome_responsavel:
                        if len(texto_temporario_responsavel) < 20:
                            texto_temporario_responsavel += texto_digitado

            if evento.type == pygame.KEYDOWN:
                # Tratamento de texto para configurações
                if estado_jogo == CONFIGURACOES:
                    if editando_nome_crianca:
                        if evento.key == pygame.K_RETURN:
                            # Salvar nome da criança
                            NOME_CRIANCA = texto_temporario_crianca
                            editando_nome_crianca = False
                            salvar_configuracoes()
                            encerrar_teclado_texto()
                        elif evento.key == pygame.K_ESCAPE:
                            # Cancelar edição
                            editando_nome_crianca = False
                            texto_temporario_crianca = ""
                            encerrar_teclado_texto()
                        elif evento.key == pygame.K_BACKSPACE:
                            # Apagar caractere
                            texto_temporario_crianca = texto_temporario_crianca[:-1]
                        else:
                            # Adicionar caractere (limitado a 20 caracteres)
                            if len(texto_temporario_crianca) < 20 and getattr(evento, 'unicode', '').isprintable():
                                texto_temporario_crianca += evento.unicode
                    elif editando_nome_responsavel:
                        if evento.key == pygame.K_RETURN:
                            # Salvar nome do responsável
                            NOME_RESPONSAVEL = texto_temporario_responsavel
                            editando_nome_responsavel = False
                            salvar_configuracoes()
                            encerrar_teclado_texto()
                        elif evento.key == pygame.K_ESCAPE:
                            # Cancelar edição
                            editando_nome_responsavel = False
                            texto_temporario_responsavel = ""
                            encerrar_teclado_texto()
                        elif evento.key == pygame.K_BACKSPACE:
                            # Apagar caractere
                            texto_temporario_responsavel = texto_temporario_responsavel[:-1]
                        else:
                            # Adicionar caractere (limitado a 20 caracteres)
                            if len(texto_temporario_responsavel) < 20 and getattr(evento, 'unicode', '').isprintable():
                                texto_temporario_responsavel += evento.unicode
                
                elif estado_jogo == JOGANDO and fase_atual in [1, 2, 3]:
                    if evento.key == pygame.K_e:
                        edit_mode = not edit_mode
                        # Resetar modos de edição ao sair
                        if not edit_mode:
                            resetar_edicao()
                    elif edit_mode:
                        if evento.key == pygame.K_i:
                            editando_ponto_inicio = not editando_ponto_inicio
                            editando_ponto_chegada = False
                        elif evento.key == pygame.K_c:
                            editando_ponto_chegada = not editando_ponto_chegada
                            editando_ponto_inicio = False
                        elif evento.key == pygame.K_p:
                            desenhando_caminho = not desenhando_caminho
                            # Desativa modo linha reta quando ativa modo pontinho individual
                            if desenhando_caminho:
                                criando_linha_reta = False
                                ponto_inicio_linha = None
                        elif evento.key == pygame.K_l:
                            criando_linha_reta = not criando_linha_reta
                            # Desativa modo pontinho individual quando ativa modo linha reta
                            if criando_linha_reta:
                                desenhando_caminho = False
                            ponto_inicio_linha = None
                        elif evento.key == pygame.K_r:
                            # Limpar todos os pontinhos
                            limpar_pontinhos()
                        elif evento.key == pygame.K_s:
                            salvar_fase_editada()

        # --- Lógica do Jogo ---
        if estado_jogo == JOGANDO:
            futuro_peixinho_rect = peixinho_img_atual.get_rect(center=pos_mouse)
            
            # Atualiza elementos editados em tempo real
            if edit_mode and fase_atual in [1, 2, 3]:
                if editando_ponto_inicio:
                    set_area_inicio_center(pos_mouse)
                    atualizar_areas_validas()
                    set_posicao_peixinho(area_inicio.center)
                elif editando_ponto_chegada:
                    set_area_chegada_center(pos_mouse)
                    atualizar_areas_validas()

            # Movimento e coleta de pontinhos (desabilitado no modo de edição)
            if not (edit_mode and fase_atual in [1, 2, 3]):
                # Só move o personagem se o mouse estiver sendo movido ou se já iniciou o movimento
                if personagem_iniciou_movimento or pos_mouse != posicao_peixinho:
                    set_posicao_peixinho(pos_mouse)
                    personagem_iniciou_movimento = True
                
                # Verifica colisão com pontinhos (se existirem)
                if len(pontinhos) > 0:
                    for i, (x, y) in enumerate(pontinhos[:]):
                        if ((pos_mouse[0] - x) ** 2 + (pos_mouse[1] - y) ** 2) ** 0.5 < 25:  # raio de coleta aumentado
                            remover_pontinho(i)
                            break
            else:
                # No modo de edição, apenas move o personagem sem coletar
                set_posicao_peixinho(pos_mouse)

            peixinho_rect = peixinho_img_atual.get_rect(center=posicao_peixinho)
                    # Só verifica colisão com chegada se não estiver no modo de edição
            if not (edit_mode and fase_atual in [1, 2, 3]):
                if area_chegada.colliderect(peixinho_rect):
                    # Vence apenas se não restarem pontinhos (quando habilitados)
                    if verificar_vitoria():
                        # Inicia efeito de vitória
                        iniciar_efeito_vitoria()
                        
                        # Incrementa contador de repetições da fase atual
                        REPETICOES_FASE[FASE_ATUAL_NUMERO] += 1
                        nome_fase = NOMES_FASES.get(FASE_ATUAL_NUMERO, f"Fase {FASE_ATUAL_NUMERO}")
                        print(f"{nome_fase} completada! Repetições: {REPETICOES_FASE[FASE_ATUAL_NUMERO]}/{REPETICOES_POR_FASE}")
                        
                        # Atualiza pontuação acumulada
                        PONTOS_ACUMULADOS += pontuacao  
                        
                        # Verifica se completou as 5 repetições necessárias
                        if REPETICOES_FASE[FASE_ATUAL_NUMERO] >= REPETICOES_POR_FASE:
                            # Fase completamente finalizada - vai para tela de vitória
                            estado_jogo = VITORIA
                        else:
                            # Ainda precisa de mais repetições - reinicia a fase após o efeito
                            # Reseta apenas a pontuação local, mantém a acumulada
                            resetar_pontuacao()
                            # Respawn automático do personagem na linha de partida
                            set_posicao_peixinho(area_inicio.center)
                            # Recarrega os pontinhos da fase
                            recomputar_pontinhos_fase_atual()
                        
                        # Salva progresso
                        salvar_configuracoes()


        # --- Desenho na Tela Virtual ---
        if estado_jogo == TELA_INICIAL:
            desenhar_tela_inicial(pos_mouse)
        elif estado_jogo == SELECAO_FASE:
            desenhar_selecao_fase(pos_mouse)
        elif estado_jogo == JOGANDO:
            desenhar_jogo(pos_mouse)
        elif estado_jogo == CONFIGURACOES:
            desenhar_configuracoes(pos_mouse)
        elif estado_jogo == SOBRE:
            desenhar_tela_sobre(pos_mouse)
        elif estado_jogo == VITORIA:
            desenhar_tela_vitoria()

        # Redimensionamento e renderização
        tela.fill(PRETO)

        escala_final = min(tela.get_width() / LARGURA_TELA_VIRTUAL, tela.get_height() / ALTURA_TELA_VIRTUAL)
        nova_largura_final = int(LARGURA_TELA_VIRTUAL * escala_final)
        nova_altura_final = int(ALTURA_TELA_VIRTUAL * escala_final)

        if nova_largura_final > 0 and nova_altura_final > 0:
            tela_redimensionada = pygame.transform.smoothscale(tela_virtual, (nova_largura_final, nova_altura_final))
            
            pos_x_final = (tela.get_width() - nova_largura_final) // 2
            pos_y_final = (tela.get_height() - nova_altura_final) // 2
            
            tela.blit(tela_redimensionada, (pos_x_final, pos_y_final))
        
        pygame.display.flip()

        await asyncio.sleep(0)

    pygame.quit()

# --- Inicialização ---
estado_jogo = TELA_INICIAL
rodando = True
pos_mouse = (0, 0)

carregar_configuracoes()
carregar_som_vitoria()
if MUSICA_ATUAL_NOME != "Mudo":
    tocar_musica_por_nome(MUSICA_ATUAL_NOME)

# --- Ponto de Entrada ---
if __name__ == "__main__":
    asyncio.run(main_loop())