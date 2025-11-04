#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLAY TEA - Jogo Educacional
Ponto de entrada principal para a aplicação Android
"""

import os
import sys

# Adiciona o diretório src ao path para permitir imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importa e executa o jogo
if __name__ == '__main__':
    # Import do módulo principal do jogo
    import inicio
