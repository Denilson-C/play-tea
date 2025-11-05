#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLAY TEA - Jogo Educacional
Versão Web com Pygbag
"""

import asyncio
import os
import sys

# Adiciona o diretório src ao path para permitir imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importa o módulo principal do jogo
import inicio_web

# Executa o jogo assíncrono
if __name__ == '__main__':
    asyncio.run(inicio_web.main())
