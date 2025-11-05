#!/usr/bin/env python3
"""Script para corrigir inicio_web.py com as mudanças necessárias para Pygbag"""

# Lê o arquivo original
with open('src/inicio.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Mudança 1: Adiciona import asyncio
content = content.replace(
    'import pygame\nimport json\nimport os\nimport sys',
    'import pygame\nimport json\nimport os\nimport sys\nimport asyncio'
)

# Mudança 2: Remove pygame.RESIZABLE
content = content.replace(
    'tela = pygame.display.set_mode((LARGURA_TELA_VIRTUAL, ALTURA_TELA_VIRTUAL), pygame.RESIZABLE)',
    'tela = pygame.display.set_mode((LARGURA_TELA_VIRTUAL, ALTURA_TELA_VIRTUAL))'
)

# Mudança 3: Transforma o loop principal em função assíncrona
# Encontra o início do loop principal
loop_start = content.find('# --- Loop Principal ---')
before_loop = content[:loop_start]

# Extrai a parte do loop
loop_section = content[loop_start:]

# Remove as linhas de inicialização que serão movidas para dentro da função
lines_to_move = [
    'estado_jogo = TELA_INICIAL',
    'rodando = True',
    '# Carregar configurações',
    'carregar_configuracoes()',
    '# Carregar som de vitória',
    'carregar_som_vitoria()',
    '# Tocar música automaticamente',
    'if MUSICA_ATUAL_NOME != "Mudo":',
    '    tocar_musica_por_nome(MUSICA_ATUAL_NOME)',
    'while rodando:'
]

# Cria a função assíncrona
async_function = '''# --- Loop Principal Assíncrono para Web ---
async def main():
    """Loop principal assíncrono para compatibilidade com Pygbag"""
    global estado_jogo, rodando

    estado_jogo = TELA_INICIAL
    rodando = True

    # Carregar configurações salvas
    carregar_configuracoes()
    # Carregar som de vitória
    carregar_som_vitoria()
    # Tocar música automaticamente se não estiver em modo mudo
    if MUSICA_ATUAL_NOME != "Mudo":
        tocar_musica_por_nome(MUSICA_ATUAL_NOME)

    while rodando:
'''

# Processa o conteúdo do loop
loop_content_start = loop_section.find('while rodando:')
loop_body_start = loop_section.find('    # <--- NOVO: Bloco de conversão', loop_content_start)

if loop_body_start == -1:
    # Fallback: procura por qualquer comentário após while rodando
    loop_body_start = loop_section.find('\n', loop_content_start) + 1

# Pega tudo após o while rodando:
loop_body = loop_section[loop_body_start:]

# Remove pygame.quit() do final
loop_body = loop_body.replace('\npygame.quit()', '')

# Simplifica o bloco de conversão de mouse para tela fixa
loop_body = loop_body.replace(
    '''    # <--- NOVO: Bloco de conversão de coordenadas do mouse ---
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
    pos_mouse = (mouse_x_virtual, mouse_y_virtual)''',
    '        # Posição do mouse (tela fixa)\n        pos_mouse = pygame.mouse.get_pos()'
)

# Simplifica o bloco de renderização final
loop_body = loop_body.replace(
    '''    # <--- NOVO: Bloco final que redimensiona e desenha a tela virtual na tela real ---
    tela.fill(PRETO) # Limpa a tela real com preto para criar as "letterboxes"

    # Recalcula a escala e a posição para o blit final
    escala_final = min(tela.get_width() / LARGURA_TELA_VIRTUAL, tela.get_height() / ALTURA_TELA_VIRTUAL)
    nova_largura_final = int(LARGURA_TELA_VIRTUAL * escala_final)
    nova_altura_final = int(ALTURA_TELA_VIRTUAL * escala_final)
    tela_redimensionada = pygame.transform.smoothscale(tela_virtual, (nova_largura_final, nova_altura_final))

    pos_x_final = (tela.get_width() - nova_largura_final) // 2
    pos_y_final = (tela.get_height() - nova_altura_final) // 2

    tela.blit(tela_redimensionada, (pos_x_final, pos_y_final))
    pygame.display.flip()''',
    '''        # Desenha na tela
        tela.blit(tela_virtual, (0, 0))
        pygame.display.flip()

        # Permite que o navegador respire (necessário para Pygbag)
        await asyncio.sleep(0)'''
)

# Remove linhas de inicialização do loop_section que serão movidas para a função
for line in lines_to_move:
    loop_section = loop_section.replace(line + '\n', '')

# Monta o arquivo final
final_content = before_loop + async_function + loop_body + '\n    pygame.quit()\n'

# Salva o arquivo
with open('src/inicio_web.py', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("✅ inicio_web.py corrigido com sucesso!")
