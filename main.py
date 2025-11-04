import sys
import os

# Garante que a pasta raiz esteja no sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

# Executa o jogo (o loop é iniciado ao importar src/inicio.py)
from src import inicio  # noqa: F401


