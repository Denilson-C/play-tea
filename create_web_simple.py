#!/usr/bin/env python3
"""Cria versão web simplificada"""

with open('src/inicio.py', 'r') as f:
    lines = f.readlines()

output = []
i = 0

while i < len(lines):
    line = lines[i]

    # Adiciona import asyncio após import sys
    if line.strip() == 'import sys':
        output.append(line)
        output.append('import asyncio\n')
        i += 1
        continue

    # Remove pygame.RESIZABLE
    if 'pygame.RESIZABLE' in line:
        line = line.replace(', pygame.RESIZABLE', '')

    # Converte loop principal em função async
    if line.startswith('# --- Loop Principal ---'):
        output.append('# --- Loop Principal Assíncrono ---\n')
        output.append('async def main():\n')
        output.append('    global estado_jogo, rodando\n')
        i += 1
        # Pula linhas vazias
        while i < len(lines) and not lines[i].strip():
            i += 1
        # Adiciona as variáveis do loop com indentação
        while i < len(lines) and not lines[i].startswith('while rodando:'):
            output.append('    ' + lines[i])
            i += 1
        # Adiciona o while com indentação extra
        if i < len(lines):
            output.append('    ' + lines[i])  # while rodando:
            i += 1
            # Adiciona o corpo do while com indentação extra (mais 4 espaços)
            while i < len(lines) and not lines[i].startswith('pygame.quit()'):
                # Simplifica blocos específicos
                if '# <--- NOVO: Bloco de conversão de coordenadas do mouse ---' in lines[i]:
                    output.append('        pos_mouse = pygame.mouse.get_pos()\n')
                    output.append('\n')
                    # Pula até encontrar "# --- Processamento de Eventos"
                    while i < len(lines) and '# --- Processamento de Eventos' not in lines[i]:
                        i += 1
                    i -= 1  # Volta um para não pular o comentário
                elif '# <--- NOVO: Bloco final que redimensiona' in lines[i]:
                    output.append('        tela.blit(tela_virtual, (0, 0))\n')
                    output.append('        pygame.display.flip()\n')
                    output.append('        await asyncio.sleep(0)\n')
                    # Pula até pygame.quit()
                    while i < len(lines) and not lines[i].startswith('pygame.quit()'):
                        i += 1
                    break
                else:
                    # Adiciona linha normal com indentação extra
                    if lines[i].strip():
                        output.append('    ' + lines[i])
                    else:
                        output.append(lines[i])
                i += 1
            # Adiciona pygame.quit() com indentação
            output.append('    pygame.quit()\n')
        break

    output.append(line)
    i += 1

# Salva
with open('src/inicio_web.py', 'w') as f:
    f.writelines(output)

print("✅ Criado com sucesso!")
