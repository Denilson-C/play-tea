#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLAY TEA - Jogo Educacional
Funciona tanto para Android/Desktop quanto para Web
"""

import os
import sys

# Adiciona o diretório src ao path para permitir imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Detecta se está rodando no ambiente web (Pygbag)
try:
    import asyncio
    import platform

    # Se estiver no navegador (Emscripten/WASM)
    if platform.system() == 'Emscripten':
        # Importa versão web (assíncrona)
        import inicio_web
        asyncio.run(inicio_web.main())
    else:
        # Versão desktop/Android (síncrona)
        import inicio
except ImportError:
    # Fallback para versão desktop/Android
    import inicio
