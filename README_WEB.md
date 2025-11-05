# 🎮 PLAY TEA - Publicação Web no itch.io

## 🚀 Início Rápido

### 1. Instalar pygbag
```bash
pip install pygbag
```

### 2. Criar Build Web
Execute:
```cmd
build_web.bat
```

Ou manualmente:
```bash
pygbag main.py
```

### 3. Testar Localmente
```bash
cd build\web
python -m http.server 8000
```
Acesse: http://localhost:8000

### 4. Publicar no itch.io
1. Vá para a pasta `build\web` (ou `web`)
2. Selecione **TODOS** os arquivos (Ctrl+A)
3. Clique com botão direito → **Enviar para** → **Pasta compactada (ZIP)**
4. Renomeie para `PLAYTEA-web.zip`
5. No itch.io:
   - Crie novo projeto
   - Upload do ZIP como plataforma **"HTML"**
   - **IMPORTANTE:** Marque **"Play in browser"**

## 📚 Documentação Completa

Consulte **`GUIA_ITCHIO_WEB.md`** para instruções detalhadas.

## ⚠️ Notas Importantes

- O pygbag pode ter algumas limitações com Pygame
- Teste sempre localmente antes de publicar
- Certifique-se de que **"Play in browser"** está marcado no itch.io
- O arquivo `index.html` deve estar na raiz do ZIP

## 🐛 Problemas?

1. Verifique o console do navegador (F12)
2. Teste localmente primeiro
3. Consulte `GUIA_ITCHIO_WEB.md` seção "Solução de Problemas"

