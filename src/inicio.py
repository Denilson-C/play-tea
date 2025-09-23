import pygame
import json
import os
import sys

# --- Configuração de Caminhos ---
# Obtém o diretório do script atual
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Obtém o diretório raiz do projeto (um nível acima de src)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
# Define os caminhos para assets e data
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# --- Inicialização ---
pygame.init()
pygame.mixer.init()

# --- Constantes e Configurações ---
# <--- ALTERAÇÃO: Definimos uma resolução interna (virtual) fixa ---
LARGURA_TELA_VIRTUAL = 800
ALTURA_TELA_VIRTUAL = 600

# <--- ALTERAÇÃO: A tela principal agora é redimensionável ---
tela = pygame.display.set_mode((LARGURA_TELA_VIRTUAL, ALTURA_TELA_VIRTUAL), pygame.RESIZABLE)
# <--- NOVO: Criamos a superfície interna onde o jogo será desenhado ---
tela_virtual = pygame.Surface((LARGURA_TELA_VIRTUAL, ALTURA_TELA_VIRTUAL))

pygame.display.set_caption("PLAY TEA")

# --- Estados do Jogo ---
TELA_INICIAL = "tela_inicial"
SELECAO_FASE = "selecao_fase"
JOGANDO = "jogando"
CONFIGURACOES = "configuracoes"
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
MUSICAS_DISPONIVEIS = {
    "Mudo": None,
    "Ruído Branco": os.path.join(AUDIO_DIR, "musica1.ogg"),
    "Ruído Rosa": os.path.join(AUDIO_DIR, "musica2.ogg")
}
MUSICA_ATUAL_NOME = "Mudo"

# --- Fontes ---
fonte_titulo = pygame.font.Font(None, 90)
fonte_botao = pygame.font.Font(None, 50)
fonte_config = pygame.font.Font(None, 40)

# --- Carregar imagem de fundo para menu ---
fundo_menu_img = pygame.image.load(os.path.join(IMAGES_DIR, "fundo.png"))
fundo_menu_img = pygame.transform.smoothscale(fundo_menu_img, (LARGURA_TELA_VIRTUAL, ALTURA_TELA_VIRTUAL))
# Aplicar desfoque suave
fundo_menu_img = pygame.transform.smoothscale(fundo_menu_img, (LARGURA_TELA_VIRTUAL//2, ALTURA_TELA_VIRTUAL//2))
fundo_menu_img = pygame.transform.smoothscale(fundo_menu_img, (LARGURA_TELA_VIRTUAL, ALTURA_TELA_VIRTUAL))

# --- ESTRUTURA DE FASES (usando as constantes da tela virtual) ---
FASES = {
    1: {
        "peixe_img": os.path.join(IMAGES_DIR, "peixe 1.png"),
        "fundo_img": os.path.join(IMAGES_DIR, "fundo 1.jpg"),
        "labirinto": [],  # Fase 1 não usa caminho retangular
        "raio_borda": 0,
        "chegada_img": os.path.join(IMAGES_DIR, "casa.png"),
        "pontinhos": {"habilitado": True, "espacamento": 40}
    },
    2: {
        "peixe_img": os.path.join(IMAGES_DIR, "cachorro.png"),
        "fundo_img": os.path.join(IMAGES_DIR, "fundo 3.png"),
        "labirinto": [
            # Parâmetros do traçado baseado na imagem (U com vão no topo)
            # Espessura uniforme
            pygame.Rect(50, ALTURA_TELA_VIRTUAL / 1.89 - 65, 300 - 50, 80),  # barra superior esquerda alinhada à partida
            pygame.Rect(LARGURA_TELA_VIRTUAL - 300 - 80, ALTURA_TELA_VIRTUAL / 2 - 40, 800 - 50 - (LARGURA_TELA_VIRTUAL - 300 - 80), 80),  # superior direita alinhada à chegada
            pygame.Rect(300, ALTURA_TELA_VIRTUAL / 1.89 - 65, 80, (ALTURA_TELA_VIRTUAL - 120 - 80) - (ALTURA_TELA_VIRTUAL / 1.89 - 65) + 80),  # pilar esquerdo
            pygame.Rect(LARGURA_TELA_VIRTUAL - 300 - 80, ALTURA_TELA_VIRTUAL / 2 - 40, 80, (ALTURA_TELA_VIRTUAL - 120 - 80) - (ALTURA_TELA_VIRTUAL / 2 - 40) + 80),  # pilar direito
            pygame.Rect(300, ALTURA_TELA_VIRTUAL - 120 - 80, (LARGURA_TELA_VIRTUAL - 300 - 80) + 80 - 300, 80),  # barra inferior
        ],
        "raio_borda": 0,
        #"borda_img": os.path.join(IMAGES_DIR, "parede 1.png"),
        "chegada_img": os.path.join(IMAGES_DIR, "casa.png"),
        "pontinhos": {"habilitado": True, "espacamento": 50}
    },
    3: {
        "peixe_img": os.path.join(IMAGES_DIR, "gato.png"),
        "fundo_img": os.path.join(IMAGES_DIR, "fundo 3.png"),
        "labirinto": [
            # Barra inicial alinhada ao centro vertical da partida
            pygame.Rect(50, ALTURA_TELA_VIRTUAL / 1.89 - 65, 200, 80),
            # Pilar esquerdo conectando do topo até a barra inicial
            pygame.Rect(200, 120, 80, (ALTURA_TELA_VIRTUAL / 1.89 - 65 + 80) - 120),
            # Barra superior
            pygame.Rect(200, 120, 400, 80),
            # Pilar direito descendo até a altura do centro da chegada
            pygame.Rect(520, 120, 80, ALTURA_TELA_VIRTUAL / 2 - 80),
            # Barra final alinhada ao centro vertical da chegada
            pygame.Rect(520, ALTURA_TELA_VIRTUAL / 2 - 40, 230, 80)
        ],
        "raio_borda": 0,
        "chegada_img": os.path.join(IMAGES_DIR, "casa.png"),
        "pontinhos": {"habilitado": True, "espacamento": 50}
    }
}

# --- Classe para Gerenciar Progresso do Jogo ---
class ProgressoJogo:
    def __init__(self):
        # Imagens e recursos
        self.peixinho_img_atual = None
        self.fundo_img_atual = None
        self.borda_img_atual = None
        self.chegada_img_atual = None
        
        # Áreas e posições
        self.areas_validas_atual = []
        self.area_inicio = pygame.Rect(0, ALTURA_TELA_VIRTUAL /1.89 - 60, 60, 60)
        self.area_chegada = pygame.Rect(LARGURA_TELA_VIRTUAL - 120, ALTURA_TELA_VIRTUAL / 2 - 60, 120, 120)
        self.posicao_peixinho = list(self.area_inicio.center)
        
        # Labirinto e pontinhos
        self.labirinto_atual = []
        self.pontinhos = []
        self.pontuacao = 0
        
        # Estado da fase
        self.fase_atual = None
        self.raio_borda_atual = 0
        
        # Modo de edição
        self.edit_mode = False
        self.dragging = False
        self.drag_rect_idx = None
        self.drag_offset = (0, 0)
        self.editando_ponto_inicio = False
        self.editando_ponto_chegada = False
        self.adicionando_segmento = False
        self.segmento_temporario = None
        self.desenhando_caminho = False
        self.caminho_temporario = []
        self.criando_linha_reta = False
        self.ponto_inicio_linha = None
        self.personagem_iniciou_movimento = False
    
    def resetar_edicao(self):
        """Reseta todas as variáveis de modo de edição"""
        self.edit_mode = False
        self.dragging = False
        self.drag_rect_idx = None
        self.editando_ponto_inicio = False
        self.editando_ponto_chegada = False
        self.adicionando_segmento = False
        self.segmento_temporario = None
        self.desenhando_caminho = False
        self.caminho_temporario = []
        self.criando_linha_reta = False
        self.ponto_inicio_linha = None
        self.personagem_iniciou_movimento = False
    
    def atualizar_areas_validas(self):
        """Atualiza a lista de áreas válidas com base no labirinto atual"""
        self.areas_validas_atual = self.labirinto_atual + [self.area_inicio, self.area_chegada]
    
    def resetar_pontuacao(self):
        """Reseta a pontuação para zero"""
        self.pontuacao = 0
    
    def adicionar_pontinho(self, x, y):
        """Adiciona um pontinho na posição especificada"""
        self.pontinhos.append((x, y))
    
    def remover_pontinho(self, index):
        """Remove um pontinho pelo índice"""
        if 0 <= index < len(self.pontinhos):
            self.pontinhos.pop(index)
            self.pontuacao += 10
    
    def limpar_pontinhos(self):
        """Remove todos os pontinhos"""
        self.pontinhos.clear()
    
    def criar_linha_reta_pontinhos(self, x1, y1, x2, y2, espacamento=20):
        """Cria pontinhos em linha reta entre dois pontos"""
        # Calcula a distância entre os pontos
        distancia = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        
        if distancia < espacamento:
            # Se os pontos estão muito próximos, adiciona apenas um pontinho no meio
            self.adicionar_pontinho((x1 + x2) // 2, (y1 + y2) // 2)
            return
        
        # Calcula quantos pontinhos cabem na linha
        num_pontinhos = int(distancia / espacamento)
        
        # Cria os pontinhos distribuídos uniformemente
        for i in range(num_pontinhos + 1):
            t = i / num_pontinhos if num_pontinhos > 0 else 0
            x = int(x1 + t * (x2 - x1))
            y = int(y1 + t * (y2 - y1))
            self.adicionar_pontinho(x, y)
    
    def verificar_vitoria(self):
        """Verifica se o jogador venceu (sem pontinhos restantes)"""
        return len(self.pontinhos) == 0

# --- Instância Global do Progresso ---
progresso = ProgressoJogo()

# --- Variáveis Globais e Definições de Rects (usando constantes virtuais) ---
# Mantidas para compatibilidade com código existente
peixinho_img_atual = progresso.peixinho_img_atual
fundo_img_atual = progresso.fundo_img_atual
areas_validas_atual = progresso.areas_validas_atual
raio_borda_atual = progresso.raio_borda_atual
fase_atual = progresso.fase_atual
borda_img_atual = progresso.borda_img_atual
chegada_img_atual = progresso.chegada_img_atual
pontinhos = progresso.pontinhos
pontuacao = progresso.pontuacao
labirinto_atual = progresso.labirinto_atual
edit_mode = progresso.edit_mode
dragging = progresso.dragging
drag_rect_idx = progresso.drag_rect_idx
drag_offset = progresso.drag_offset
editando_ponto_inicio = progresso.editando_ponto_inicio
editando_ponto_chegada = progresso.editando_ponto_chegada
adicionando_segmento = progresso.adicionando_segmento
segmento_temporario = progresso.segmento_temporario
desenhando_caminho = progresso.desenhando_caminho
caminho_temporario = progresso.caminho_temporario
area_inicio = progresso.area_inicio
area_chegada = progresso.area_chegada
posicao_peixinho = progresso.posicao_peixinho

botao_iniciar = pygame.Rect(LARGURA_TELA_VIRTUAL / 2 - 100, 250, 200, 60)
botao_config = pygame.Rect(LARGURA_TELA_VIRTUAL / 2 - 100, 340, 200, 60)
botao_voltar = pygame.Rect(LARGURA_TELA_VIRTUAL / 2 - 100, 500, 200, 60)
botao_sair_fase = pygame.Rect(20, 20, 100, 40)  # Canto superior esquerdo
botao_voltar_menu = pygame.Rect(LARGURA_TELA_VIRTUAL - 120, 20, 100, 40)  # Canto superior direito
botoes_fase = {
    1: pygame.Rect(LARGURA_TELA_VIRTUAL / 2 - 100, 150, 200, 60),
    2: pygame.Rect(LARGURA_TELA_VIRTUAL / 2 - 100, 240, 200, 60),
    3: pygame.Rect(LARGURA_TELA_VIRTUAL / 2 - 100, 330, 200, 60),
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
Y_INICIO_COLUNA = 180

# Botões de Cor (coluna esquerda)
y_pos_cor = Y_INICIO_COLUNA
for nome, cor in cores_disponiveis.items():
    botoes_cor[nome] = pygame.Rect(COLUNA_ESQ_X, y_pos_cor, LARG_BOTAO, ALT_BOTAO)
    y_pos_cor += ESPACO_V

# Botões de Música (coluna direita)
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
        else:
            pygame.mixer.music.load(arquivo)
            pygame.mixer.music.play(-1)
        MUSICA_ATUAL_NOME = nome
    except pygame.error as e:
        print(f"Aviso: não foi possível tocar '{nome}': {e}")

# --- Funções ---
def carregar_fase(numero_fase):
    global peixinho_img_atual, fundo_img_atual, areas_validas_atual, posicao_peixinho, raio_borda_atual, fase_atual, borda_img_atual, chegada_img_atual, pontinhos, pontuacao, labirinto_atual, edit_mode, dragging, drag_rect_idx
    fase_info = FASES[numero_fase]
    try:
        progresso.peixinho_img_atual = pygame.image.load(fase_info["peixe_img"]).convert_alpha()
        progresso.peixinho_img_atual = pygame.transform.scale(progresso.peixinho_img_atual, (80, 80))
        
        progresso.fundo_img_atual = pygame.image.load(fase_info["fundo_img"]).convert()
        # <--- ALTERAÇÃO: Escala para o tamanho da TELA VIRTUAL ---
        progresso.fundo_img_atual = pygame.transform.scale(progresso.fundo_img_atual, (LARGURA_TELA_VIRTUAL, ALTURA_TELA_VIRTUAL))
        
    except pygame.error as e:
        print(f"Erro ao carregar recursos da fase {numero_fase}: {e}")
        progresso.fundo_img_atual = pygame.Surface((LARGURA_TELA_VIRTUAL, ALTURA_TELA_VIRTUAL))
        progresso.fundo_img_atual.fill((0,0,0))
        return
    caminho_rects = fase_info["labirinto"]
    progresso.labirinto_atual = [pygame.Rect(r) for r in caminho_rects]
    progresso.atualizar_areas_validas()
    progresso.posicao_peixinho = list(progresso.area_inicio.center)
    progresso.raio_borda_atual = fase_info.get("raio_borda", 0)
    progresso.fase_atual = numero_fase
    progresso.borda_img_atual = None
    borda_path = fase_info.get("borda_img")
    if borda_path:
        try:
            progresso.borda_img_atual = pygame.image.load(borda_path).convert_alpha()
        except pygame.error as e:
            print(f"Aviso: não foi possível carregar a borda da fase {numero_fase}: {e}")
    # Carrega imagem da chegada (opcional por fase)
    progresso.chegada_img_atual = None
    chegada_path = fase_info.get("chegada_img")
    if chegada_path:
        try:
            img = pygame.image.load(chegada_path).convert_alpha()
            progresso.chegada_img_atual = pygame.transform.smoothscale(img, (progresso.area_chegada.width, progresso.area_chegada.height))
        except pygame.error as e:
            print(f"Aviso: não foi possível carregar a imagem de chegada da fase {numero_fase}: {e}")
    
    # Inicializa pontinhos por fase (se habilitado)
    progresso.resetar_pontuacao()
    progresso.limpar_pontinhos()
    
    # Tenta carregar fase editada primeiro (após definir fase_atual)
    if numero_fase in [1, 2, 3]:
        carregar_fase_editada()
    
    # Se não carregou dados editados, usa configuração padrão
    if not progresso.pontinhos:
        pont_cfg = fase_info.get("pontinhos", {"habilitado": False})
        if pont_cfg.get("habilitado"):
            espac = int(pont_cfg.get("espacamento", 20))
            if numero_fase == 1:
                # Fase 1: linha reta
                for x in range(100, LARGURA_TELA_VIRTUAL - 100, espac):
                    progresso.adicionar_pontinho(x, progresso.area_inicio.centery)
            else:
                # Fases 2 e 3: pontinhos em linha única por bloco
                for rect in progresso.labirinto_atual:
                    # Pontinhos horizontais (linha central)
                    if rect.width > rect.height:
                        for x in range(rect.left + espac//2, rect.right, espac):
                            progresso.adicionar_pontinho(x, rect.centery)
                    # Pontinhos verticais (linha central)
                    else:
                        for y in range(rect.top + espac//2, rect.bottom, espac):
                            progresso.adicionar_pontinho(rect.centerx, y)
    # reseta edição
    progresso.resetar_edicao()
    
    # Atualiza variáveis globais para compatibilidade
    peixinho_img_atual = progresso.peixinho_img_atual
    fundo_img_atual = progresso.fundo_img_atual
    areas_validas_atual = progresso.areas_validas_atual
    posicao_peixinho = progresso.posicao_peixinho
    raio_borda_atual = progresso.raio_borda_atual
    fase_atual = progresso.fase_atual
    borda_img_atual = progresso.borda_img_atual
    chegada_img_atual = progresso.chegada_img_atual
    pontinhos = progresso.pontinhos
    pontuacao = progresso.pontuacao
    labirinto_atual = progresso.labirinto_atual
    edit_mode = progresso.edit_mode
    dragging = progresso.dragging
    drag_rect_idx = progresso.drag_rect_idx
    editando_ponto_inicio = progresso.editando_ponto_inicio
    editando_ponto_chegada = progresso.editando_ponto_chegada
    adicionando_segmento = progresso.adicionando_segmento
    segmento_temporario = progresso.segmento_temporario
    desenhando_caminho = progresso.desenhando_caminho
    caminho_temporario = progresso.caminho_temporario
    area_inicio = progresso.area_inicio
    area_chegada = progresso.area_chegada
    
def salvar_fase_editada():
    """Salva as modificações da fase atual em arquivo JSON"""
    if progresso.fase_atual in [1, 2, 3]:
        dados = {
            "labirinto": [(r.x, r.y, r.width, r.height) for r in progresso.labirinto_atual],
            "pontinhos": progresso.pontinhos,
            "area_inicio": (progresso.area_inicio.x, progresso.area_inicio.y, progresso.area_inicio.width, progresso.area_inicio.height),
            "area_chegada": (progresso.area_chegada.x, progresso.area_chegada.y, progresso.area_chegada.width, progresso.area_chegada.height)
        }
        try:
            filename = f"fase{progresso.fase_atual}_editada.json"
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, "w") as f:
                json.dump(dados, f)
            print(f"Fase {progresso.fase_atual} salva com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar: {e}")

def salvar_configuracoes():
    """Salva as configurações do jogo em arquivo JSON"""
    dados = {
        "cor_pontinhos": COR_PONTINHOS,
        "musica_atual": MUSICA_ATUAL_NOME
    }
    try:
        config_path = os.path.join(DATA_DIR, "configuracoes.json")
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
            global COR_PONTINHOS, MUSICA_ATUAL_NOME
            COR_PONTINHOS = tuple(dados.get("cor_pontinhos", COR_PONTINHOS))
            MUSICA_ATUAL_NOME = dados.get("musica_atual", MUSICA_ATUAL_NOME)
            print("Configurações carregadas com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar configurações: {e}")

def carregar_fase_editada():
    """Carrega as modificações salvas da fase"""
    try:
        if progresso.fase_atual in [1, 2, 3]:
            filename = f"fase{progresso.fase_atual}_editada.json"
            filepath = os.path.join(DATA_DIR, filename)
            if os.path.exists(filepath):
                with open(filepath, "r") as f:
                    dados = json.load(f)
                
                # Restaura labirinto
                progresso.labirinto_atual = [pygame.Rect(x, y, w, h) for x, y, w, h in dados["labirinto"]]
                progresso.pontinhos = dados["pontinhos"]
                
                # Restaura áreas de início e chegada
                progresso.area_inicio = pygame.Rect(*dados["area_inicio"])
                progresso.area_chegada = pygame.Rect(*dados["area_chegada"])
                
                progresso.atualizar_areas_validas()
                print(f"Fase {progresso.fase_atual} carregada com sucesso!")
                
                # Atualiza variáveis globais para compatibilidade
                global labirinto_atual, pontinhos, areas_validas_atual, area_inicio, area_chegada
                labirinto_atual = progresso.labirinto_atual
                pontinhos = progresso.pontinhos
                areas_validas_atual = progresso.areas_validas_atual
                area_inicio = progresso.area_inicio
                area_chegada = progresso.area_chegada
    except Exception as e:
        print(f"Erro ao carregar fase editada: {e}")
        # Se der erro, continua com configuração padrão

def recomputar_pontinhos_fase_atual():
    global pontinhos
    fase_info = FASES[progresso.fase_atual]
    pont_cfg = fase_info.get("pontinhos", {"habilitado": False})
    progresso.limpar_pontinhos()
    if not pont_cfg.get("habilitado"):
        return
    espac = int(pont_cfg.get("espacamento", 20))
    if progresso.fase_atual == 1:
        for x in range(100, LARGURA_TELA_VIRTUAL - 100, espac):
            progresso.adicionar_pontinho(x, progresso.area_inicio.centery)
    else:
        for rect in progresso.labirinto_atual:
            if rect.width > rect.height:
                for x in range(rect.left + espac//2, rect.right, espac):
                    progresso.adicionar_pontinho(x, rect.centery)
            else:
                for y in range(rect.top + espac//2, rect.bottom, espac):
                    progresso.adicionar_pontinho(rect.centerx, y)
    
    # Atualiza variável global para compatibilidade
    pontinhos = progresso.pontinhos
    # Não precisamos mais setar a posição do mouse, pois ele será convertido a cada frame
    
def desenhar_texto(texto, fonte, cor, superficie, x, y):
    textobj = fonte.render(texto, True, cor)
    textrect = textobj.get_rect(center=(x, y))
    superficie.blit(textobj, textrect)

# --- Funções de Desenho das Telas (AGORA DESENHAM NA TELA_VIRTUAL) ---
def desenhar_tela_inicial(mouse_pos):
    # Desenhar fundo desfocado
    tela_virtual.blit(fundo_menu_img, (0, 0))
    # Adicionar overlay escuro para melhorar legibilidade
    overlay = pygame.Surface((LARGURA_TELA_VIRTUAL, ALTURA_TELA_VIRTUAL), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    tela_virtual.blit(overlay, (0, 0))
    
    desenhar_texto("PLAY TEA", fonte_titulo, BRANCO, tela_virtual, LARGURA_TELA_VIRTUAL / 2, 120)
    
    cor_iniciar = COR_BOTAO_HOVER if botao_iniciar.collidepoint(mouse_pos) else COR_BOTAO
    pygame.draw.rect(tela_virtual, cor_iniciar, botao_iniciar, border_radius=15)
    desenhar_texto("Jogar", fonte_botao, BRANCO, tela_virtual, botao_iniciar.centerx, botao_iniciar.centery)
    
    cor_config = COR_BOTAO_HOVER if botao_config.collidepoint(mouse_pos) else COR_BOTAO
    pygame.draw.rect(tela_virtual, cor_config, botao_config, border_radius=15)
    desenhar_texto("Opções", fonte_botao, BRANCO, tela_virtual, botao_config.centerx, botao_config.centery)

def desenhar_selecao_fase(mouse_pos):
    # Desenhar fundo desfocado
    tela_virtual.blit(fundo_menu_img, (0, 0))
    # Adicionar overlay escuro para melhorar legibilidade
    overlay = pygame.Surface((LARGURA_TELA_VIRTUAL, ALTURA_TELA_VIRTUAL), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    tela_virtual.blit(overlay, (0, 0))
    
    desenhar_texto("Selecione a Fase", fonte_titulo, BRANCO, tela_virtual, LARGURA_TELA_VIRTUAL / 2, 80)

    for num, rect in botoes_fase.items():
        cor = COR_BOTAO_HOVER if rect.collidepoint(mouse_pos) else COR_BOTAO
        pygame.draw.rect(tela_virtual, cor, rect, border_radius=15)
        desenhar_texto(f"Fase {num}", fonte_botao, BRANCO, tela_virtual, rect.centerx, rect.centery)

    cor_voltar = COR_BOTAO_HOVER if botao_voltar.collidepoint(mouse_pos) else COR_BOTAO
    pygame.draw.rect(tela_virtual, cor_voltar, botao_voltar, border_radius=15)
    desenhar_texto("Voltar", fonte_botao, BRANCO, tela_virtual, botao_voltar.centerx, botao_voltar.centery)
    

def desenhar_configuracoes(mouse_pos):
    # Desenhar fundo desfocado
    tela_virtual.blit(fundo_menu_img, (0, 0))
    # Adicionar overlay escuro para melhorar legibilidade
    overlay = pygame.Surface((LARGURA_TELA_VIRTUAL, ALTURA_TELA_VIRTUAL), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    tela_virtual.blit(overlay, (0, 0))
    
    desenhar_texto("Configurações", fonte_titulo, BRANCO, tela_virtual, LARGURA_TELA_VIRTUAL / 2, 80)
    
    # Títulos das colunas
    desenhar_texto("Cor dos pontinhos", fonte_config, BRANCO, tela_virtual, COLUNA_ESQ_X + LARG_BOTAO/2, 140)
    desenhar_texto("Música", fonte_config, BRANCO, tela_virtual, COLUNA_DIR_X + LARG_BOTAO/2, 140)

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
    
def desenhar_jogo(mouse_pos=(0, 0)):
    tela_virtual.blit(progresso.fundo_img_atual, (0, 0))
    pygame.draw.rect(tela_virtual, VERDE_INICIO, progresso.area_inicio)
    
    # Fallback: desenha caminho retangular (caso não haja pontinhos)
    # Removido: não desenha mais o caminho quando não há pontinhos

    # Se edit mode ativo, destacar elementos editáveis
    if progresso.edit_mode and progresso.fase_atual in [1, 2, 3]:
        # Destacar retângulos do labirinto
        for idx, rect in enumerate(progresso.labirinto_atual):
            cor = (255, 100, 100) if idx == progresso.drag_rect_idx else (255, 0, 0)
            pygame.draw.rect(tela_virtual, cor, rect, 2)
        
        # Destacar pontos de início e chegada
        pygame.draw.rect(tela_virtual, (0, 255, 0), progresso.area_inicio, 3)
        pygame.draw.rect(tela_virtual, (0, 255, 0), progresso.area_chegada, 3)
        
        # Mostrar instruções
        fonte_instrucoes = pygame.font.Font(None, 24)
        instrucoes = [
            "E: Sair do modo edição",
            "A: Adicionar segmento",
            "D: Deletar segmento",
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
        if progresso.criando_linha_reta:
            if progresso.ponto_inicio_linha is not None:
                # Mostrar ponto de início e linha até o mouse
                pygame.draw.circle(tela_virtual, (255, 255, 0), progresso.ponto_inicio_linha, 8)
                pygame.draw.line(tela_virtual, (255, 255, 0), progresso.ponto_inicio_linha, pos_mouse, 2)
                texto_linha = fonte_instrucoes.render("Clique para finalizar linha", True, (255, 255, 0))
                tela_virtual.blit(texto_linha, (10, 10 + len(instrucoes) * 25 + 10))
            else:
                texto_linha = fonte_instrucoes.render("Clique para iniciar linha", True, (255, 255, 0))
                tela_virtual.blit(texto_linha, (10, 10 + len(instrucoes) * 25 + 10))

    # Desenha a chegada por cima do caminho
    if progresso.chegada_img_atual is not None:
        tela_virtual.blit(progresso.chegada_img_atual, progresso.area_chegada.topleft)
    else:
        pygame.draw.rect(tela_virtual, VERDE_FIM, progresso.area_chegada)

    # Desenha pontuação no canto superior direito (se houver pontinhos)
    if True:
        fonte_pontuacao = pygame.font.Font(None, 36)
        texto_pontuacao = fonte_pontuacao.render(f"Pontos: {progresso.pontuacao}", True, BRANCO)
        tela_virtual.blit(texto_pontuacao, (LARGURA_TELA_VIRTUAL - 150, 20))
    
    # Botão para sair da fase (canto superior direito)
    try:
        cor_sair_fase = COR_BOTAO_HOVER if botao_sair_fase.collidepoint(mouse_pos) else COR_BOTAO
        pygame.draw.rect(tela_virtual, cor_sair_fase, botao_sair_fase, border_radius=10)
        desenhar_texto("Sair", fonte_config, BRANCO, tela_virtual, botao_sair_fase.centerx, botao_sair_fase.centery)
    except:
        # Fallback se mouse_pos não estiver definido
        pygame.draw.rect(tela_virtual, COR_BOTAO, botao_sair_fase, border_radius=10)
        desenhar_texto("Sair", fonte_config, BRANCO, tela_virtual, botao_sair_fase.centerx, botao_sair_fase.centery)

    peixinho_rect = progresso.peixinho_img_atual.get_rect(center=progresso.posicao_peixinho)
    tela_virtual.blit(progresso.peixinho_img_atual, peixinho_rect)
    
    # Desenha pontinhos por cima de tudo (se houver)
    if len(progresso.pontinhos) > 0:
        for x, y in progresso.pontinhos:
            pygame.draw.circle(tela_virtual, COR_PONTINHOS, (x, y), 8)

def desenhar_tela_vitoria():
    tela_virtual.blit(progresso.fundo_img_atual, (0, 0))
    sombra = pygame.Surface((LARGURA_TELA_VIRTUAL, ALTURA_TELA_VIRTUAL), pygame.SRCALPHA)
    sombra.fill((0, 0, 0, 128))
    tela_virtual.blit(sombra, (0, 0))
    desenhar_texto("Parabéns!", fonte_titulo, BRANCO, tela_virtual, LARGURA_TELA_VIRTUAL/2, ALTURA_TELA_VIRTUAL/2 - 50)
    desenhar_texto("Clique para continuar", fonte_config, BRANCO, tela_virtual, LARGURA_TELA_VIRTUAL/2, ALTURA_TELA_VIRTUAL/2 + 50)

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
estado_jogo = TELA_INICIAL
rodando = True

# Carregar configurações salvas
carregar_configuracoes()
while rodando:
    # <--- NOVO: Bloco de conversão de coordenadas do mouse ---
    pos_mouse_janela = pygame.mouse.get_pos()
    largura_janela_atual, altura_janela_atual = tela.get_size()

    escala = min(largura_janela_atual / LARGURA_TELA_VIRTUAL, altura_janela_atual / ALTURA_TELA_VIRTUAL)
    
    nova_largura_escalada = LARGURA_TELA_VIRTUAL * escala
    nova_altura_escalada = ALTURA_TELA_VIRTUAL * escala
    
    offset_x = (largura_janela_atual - nova_largura_escalada) / 2
    offset_y = (altura_janela_atual - nova_altura_escalada) / 2
    
    # Converte a posição do mouse da janela real para a virtual
    mouse_x_virtual = (pos_mouse_janela[0] - offset_x) / escala if escala > 0 else 0
    mouse_y_virtual = (pos_mouse_janela[1] - offset_y) / escala if escala > 0 else 0
    pos_mouse = (mouse_x_virtual, mouse_y_virtual)

    # --- Processamento de Eventos (usa pos_mouse virtual) ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Não usamos mais `evento.pos`, usamos a `pos_mouse` já convertida
            if estado_jogo == TELA_INICIAL:
                if botao_iniciar.collidepoint(pos_mouse): estado_jogo = SELECAO_FASE
                if botao_config.collidepoint(pos_mouse): estado_jogo = CONFIGURACOES
            
            elif estado_jogo == SELECAO_FASE:
                for num, rect in botoes_fase.items():
                    if rect.collidepoint(pos_mouse):
                        carregar_fase(num)
                        estado_jogo = JOGANDO
                if botao_voltar.collidepoint(pos_mouse): estado_jogo = TELA_INICIAL

            elif estado_jogo == CONFIGURACOES:
                if botao_voltar.collidepoint(pos_mouse): 
                    estado_jogo = TELA_INICIAL
                    salvar_configuracoes()  # Salvar ao sair das configurações
                for nome, rect in botoes_cor.items():
                    if rect.collidepoint(pos_mouse): 
                        COR_PONTINHOS = cores_disponiveis[nome]
                        salvar_configuracoes()  # Salvar imediatamente
                for nome, rect in botoes_musica.items():
                    if rect.collidepoint(pos_mouse): 
                        tocar_musica_por_nome(nome)
                        salvar_configuracoes()  # Salvar imediatamente

            elif estado_jogo == VITORIA:
                estado_jogo = SELECAO_FASE
            
            elif estado_jogo == JOGANDO:
                if botao_sair_fase.collidepoint(pos_mouse): 
                    estado_jogo = SELECAO_FASE
                elif progresso.fase_atual in [1, 2, 3] and progresso.edit_mode:
                    # Modo de edição ativo
                    if progresso.desenhando_caminho:
                        # Adicionar pontinho individual na posição clicada
                        progresso.adicionar_pontinho(int(pos_mouse[0]), int(pos_mouse[1]))
                    elif progresso.criando_linha_reta:
                        # Modo de linha reta
                        if progresso.ponto_inicio_linha is None:
                            # Primeiro clique: definir ponto de início
                            progresso.ponto_inicio_linha = (int(pos_mouse[0]), int(pos_mouse[1]))
                        else:
                            # Segundo clique: criar linha reta
                            progresso.criar_linha_reta_pontinhos(
                                progresso.ponto_inicio_linha[0], progresso.ponto_inicio_linha[1],
                                int(pos_mouse[0]), int(pos_mouse[1])
                            )
                            progresso.ponto_inicio_linha = None
                    elif progresso.adicionando_segmento:
                        # Criar novo segmento
                        if progresso.segmento_temporario is None:
                            progresso.segmento_temporario = pygame.Rect(pos_mouse[0], pos_mouse[1], 0, 0)
                        else:
                            # Finalizar segmento
                            progresso.segmento_temporario.width = pos_mouse[0] - progresso.segmento_temporario.x
                            progresso.segmento_temporario.height = pos_mouse[1] - progresso.segmento_temporario.y
                            if abs(progresso.segmento_temporario.width) > 10 and abs(progresso.segmento_temporario.height) > 10:
                                progresso.labirinto_atual.append(progresso.segmento_temporario)
                                progresso.atualizar_areas_validas()
                                recomputar_pontinhos_fase_atual()
                            progresso.segmento_temporario = None
                            progresso.adicionando_segmento = False
                    elif progresso.editando_ponto_inicio:
                        # Mover ponto de início
                        progresso.area_inicio.center = pos_mouse
                        progresso.atualizar_areas_validas()
                        progresso.posicao_peixinho = list(progresso.area_inicio.center)
                    elif progresso.editando_ponto_chegada:
                        # Mover ponto de chegada
                        progresso.area_chegada.center = pos_mouse
                        progresso.atualizar_areas_validas()
                    else:
                        # Início de drag de algum retângulo
                        for idx, r in enumerate(progresso.labirinto_atual):
                            if r.collidepoint(pos_mouse):
                                progresso.dragging = True
                                progresso.drag_rect_idx = idx
                                progresso.drag_offset = (pos_mouse[0] - r.x, pos_mouse[1] - r.y)
                                break

        if evento.type == pygame.MOUSEBUTTONUP:
            if progresso.dragging:
                progresso.dragging = False
                progresso.drag_rect_idx = None
                recomputar_pontinhos_fase_atual()

        if evento.type == pygame.KEYDOWN:
            if estado_jogo == JOGANDO and progresso.fase_atual in [1, 2, 3]:
                if evento.key == pygame.K_e:
                    progresso.edit_mode = not progresso.edit_mode
                    # Resetar modos de edição ao sair
                    if not progresso.edit_mode:
                        progresso.resetar_edicao()
                elif progresso.edit_mode:
                    if evento.key == pygame.K_a:
                        progresso.adicionando_segmento = True
                        progresso.segmento_temporario = None
                    elif evento.key == pygame.K_d:
                        # Deletar segmento mais próximo do mouse
                        if progresso.labirinto_atual:
                            distancias = [((r.centerx - pos_mouse[0])**2 + (r.centery - pos_mouse[1])**2)**0.5 for r in progresso.labirinto_atual]
                            idx_mais_proximo = distancias.index(min(distancias))
                            progresso.labirinto_atual.pop(idx_mais_proximo)
                            progresso.atualizar_areas_validas()
                            recomputar_pontinhos_fase_atual()
                    elif evento.key == pygame.K_i:
                        progresso.editando_ponto_inicio = not progresso.editando_ponto_inicio
                        progresso.editando_ponto_chegada = False
                    elif evento.key == pygame.K_c:
                        progresso.editando_ponto_chegada = not progresso.editando_ponto_chegada
                        progresso.editando_ponto_inicio = False
                    elif evento.key == pygame.K_p:
                        progresso.desenhando_caminho = not progresso.desenhando_caminho
                        # Desativa modo linha reta quando ativa modo pontinho individual
                        if progresso.desenhando_caminho:
                            progresso.criando_linha_reta = False
                            progresso.ponto_inicio_linha = None
                    elif evento.key == pygame.K_l:
                        progresso.criando_linha_reta = not progresso.criando_linha_reta
                        # Desativa modo pontinho individual quando ativa modo linha reta
                        if progresso.criando_linha_reta:
                            progresso.desenhando_caminho = False
                        progresso.ponto_inicio_linha = None
                    elif evento.key == pygame.K_r:
                        # Limpar todos os pontinhos
                        progresso.limpar_pontinhos()
                    elif evento.key == pygame.K_s:
                        # Salvar mudanças
                        salvar_fase_editada()

    # --- Lógica do Jogo (usa pos_mouse virtual) ---
    if estado_jogo == JOGANDO:
        futuro_peixinho_rect = progresso.peixinho_img_atual.get_rect(center=pos_mouse)
        
        # Atualiza elementos editados em tempo real
        if progresso.edit_mode and progresso.fase_atual in [1, 2, 3]:
            if progresso.dragging and progresso.drag_rect_idx is not None:
                r = progresso.labirinto_atual[progresso.drag_rect_idx]
                r.x = int(pos_mouse[0] - progresso.drag_offset[0])
                r.y = int(pos_mouse[1] - progresso.drag_offset[1])
                # Reflete mudança nas áreas válidas
                progresso.atualizar_areas_validas()
            elif progresso.editando_ponto_inicio:
                progresso.area_inicio.center = pos_mouse
                progresso.atualizar_areas_validas()
                progresso.posicao_peixinho = list(progresso.area_inicio.center)
            elif progresso.editando_ponto_chegada:
                progresso.area_chegada.center = pos_mouse
                progresso.atualizar_areas_validas()

        # Movimento e coleta de pontinhos (desabilitado no modo de edição)
        if not (progresso.edit_mode and progresso.fase_atual in [1, 2, 3]):
            # Só move o personagem se o mouse estiver sendo movido ou se já iniciou o movimento
            if progresso.personagem_iniciou_movimento or pos_mouse != progresso.posicao_peixinho:
                progresso.posicao_peixinho = list(pos_mouse)
                progresso.personagem_iniciou_movimento = True
            
            # Verifica colisão com pontinhos (se existirem)
            if len(progresso.pontinhos) > 0:
                for i, (x, y) in enumerate(progresso.pontinhos[:]):
                    if ((pos_mouse[0] - x) ** 2 + (pos_mouse[1] - y) ** 2) ** 0.5 < 15:  # raio de coleta
                        progresso.remover_pontinho(i)
                        break
        else:
            # No modo de edição, apenas move o personagem sem coletar
            progresso.posicao_peixinho = list(pos_mouse)

        peixinho_rect = progresso.peixinho_img_atual.get_rect(center=progresso.posicao_peixinho)
        # Só verifica colisão com chegada se não estiver no modo de edição
        if not (progresso.edit_mode and progresso.fase_atual in [1, 2, 3]):
            if progresso.area_chegada.colliderect(peixinho_rect):
                # Vence apenas se não restarem pontinhos (quando habilitados)
                if progresso.verificar_vitoria():
                    estado_jogo = VITORIA

    # --- Desenho na Tela Virtual ---
    if estado_jogo == TELA_INICIAL:
        desenhar_tela_inicial(pos_mouse)
    elif estado_jogo == SELECAO_FASE:
        desenhar_selecao_fase(pos_mouse)
    elif estado_jogo == JOGANDO:
        desenhar_jogo(pos_mouse)
    elif estado_jogo == CONFIGURACOES:
        desenhar_configuracoes(pos_mouse)
    elif estado_jogo == VITORIA:
        desenhar_tela_vitoria()

    # <--- NOVO: Bloco final que redimensiona e desenha a tela virtual na tela real ---
    tela.fill(PRETO) # Limpa a tela real com preto para criar as "letterboxes"
    
    # Recalcula a escala e a posição para o blit final
    escala_final = min(tela.get_width() / LARGURA_TELA_VIRTUAL, tela.get_height() / ALTURA_TELA_VIRTUAL)
    nova_largura_final = int(LARGURA_TELA_VIRTUAL * escala_final)
    nova_altura_final = int(ALTURA_TELA_VIRTUAL * escala_final)
    tela_redimensionada = pygame.transform.smoothscale(tela_virtual, (nova_largura_final, nova_altura_final))
    
    pos_x_final = (tela.get_width() - nova_largura_final) // 2
    pos_y_final = (tela.get_height() - nova_altura_final) // 2
    
    tela.blit(tela_redimensionada, (pos_x_final, pos_y_final))
    pygame.display.flip()

pygame.quit()