#!/usr/bin/env python3
"""
PLAY TEA - Jogo de Labirinto
Arquivo principal para executar o jogo
"""

import sys
import os

# Adiciona o diretório src ao path para importar o módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importa e executa o jogo
from inicio import *

if __name__ == "__main__":
    # O jogo já é executado quando o módulo é importado
    pass
