#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLAY TEA - Jogo Educacional
Versão Web compatível com Pygbag
"""

import asyncio
import os
import sys

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importa a versão web (assíncrona)
import inicio_web

# Executa o loop principal
asyncio.run(inicio_web.main())
