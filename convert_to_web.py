#!/usr/bin/env python3
"""Script para converter inicio.py para versão web compatível com Pygbag"""

def converter_para_web():
    with open('src/inicio.py', 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    saida = []
    dentro_do_loop = False
    loop_encontrado = False

    for i, linha in enumerate(linhas):
        # Adiciona import asyncio no início
        if linha.strip() == 'import sys':
            saida.append(linha)
            saida.append('import asyncio\n')
            continue

        # Remove pygame.RESIZABLE
        if 'pygame.RESIZABLE' in linha:
            linha = linha.replace(', pygame.RESIZABLE', '')
            linha = linha.replace('# <--- ALTERAÇÃO: A tela principal agora é redimensionável ---',
                                '# <--- ALTERAÇÃO WEB: Tela fixa para compatibilidade com navegador ---')

        # Encontra início do loop principal
        if '# --- Loop Principal ---' in linha:
            saida.append('# --- Loop Principal Assíncrono para Web ---\n')
            saida.append('async def main():\n')
            saida.append('    """Loop principal assíncrono para compatibilidade com Pygbag/Web"""\n')
            saida.append('    global estado_jogo, rodando\n')
            saida.append('\n')
            loop_encontrado = True
            continue

        # Após encontrar o loop, começa a indentar
        if loop_encontrado and not dentro_do_loop:
            if linha.strip().startswith('estado_jogo =') or \
               linha.strip().startswith('rodando =') or \
               linha.strip().startswith('# Carregar') or \
               linha.strip().startswith('carregar_') or \
               linha.strip().startswith('if MUSICA_') or \
               linha.strip().startswith('tocar_musica'):
                saida.append('    ' + linha)
                continue
            if 'while rodando:' in linha:
                saida.append('    while rodando:\n')
                dentro_do_loop = True
                continue

        # Dentro do loop principal, adiciona indentação extra
        if dentro_do_loop:
            # Simplifica conversão de mouse (não precisa mais)
            if '# <--- NOVO: Bloco de conversão' in linha:
                saida.append('        # <--- WEB: Posição do mouse (tela fixa) ---\n')
                # Pula as próximas linhas até chegar ao processamento de eventos
                j = i + 1
                while j < len(linhas) and '# --- Processamento de Eventos' not in linhas[j]:
                    j += 1
                continue

            if 'pos_mouse_janela = pygame.mouse.get_pos()' in linha:
                continue  # Pula esta linha
            if 'largura_janela_atual, altura_janela_atual' in linha:
                continue
            if 'escala = min(largura_janela_atual' in linha:
                continue
            if 'nova_largura_escalada' in linha:
                continue
            if 'nova_altura_escalada' in linha:
                continue
            if 'offset_x' in linha or 'offset_y' in linha:
                continue
            if 'mouse_x_virtual' in linha or 'mouse_y_virtual' in linha:
                continue
            if linha.strip() == 'pos_mouse = (mouse_x_virtual, mouse_y_virtual)':
                saida.append('        pos_mouse = pygame.mouse.get_pos()\n')
                saida.append('\n')
                continue

            # Simplifica bloco final (remove redimensionamento)
            if '# <--- NOVO: Bloco final que redimensiona' in linha:
                saida.append('        # <--- WEB: Desenha diretamente na tela ---\n')
                saida.append('        tela.blit(tela_virtual, (0, 0))\n')
                saida.append('        pygame.display.flip()\n')
                saida.append('\n')
                saida.append('        # Permite que o navegador respire\n')
                saida.append('        await asyncio.sleep(0)\n')
                # Pula até pygame.quit()
                j = i + 1
                while j < len(linhas) and 'pygame.quit()' not in linhas[j]:
                    j += 1
                break

            # Remove bloco de redimensionamento
            if 'tela.fill(PRETO)' in linha and i > 1300:
                continue
            if 'escala_final' in linha or 'nova_largura_final' in linha or 'nova_altura_final' in linha:
                continue
            if 'tela_redimensionada' in linha:
                continue
            if 'pos_x_final' in linha or 'pos_y_final' in linha:
                continue
            if linha.strip() == 'tela.blit(tela_redimensionada, (pos_x_final, pos_y_final))':
                continue
            if linha.strip() == 'pygame.display.flip()' and i > 1300:
                continue

            # Adiciona indentação extra (4 espaços)
            if linha.strip():
                saida.append('    ' + linha)
            else:
                saida.append(linha)
            continue

        saida.append(linha)

    # Adiciona o final da função
    saida.append('\n')
    saida.append('    pygame.quit()\n')

    # Salva o arquivo
    with open('src/inicio_web.py', 'w', encoding='utf-8') as f:
        f.writelines(saida)

    print("Conversão concluída! Arquivo salvo em src/inicio_web.py")

if __name__ == '__main__':
    converter_para_web()
