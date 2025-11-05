# 🎮 PLAY TEA - Publicação no itch.io (Web/HTML5)

## 🚀 Início Rápido

### 1. Instalar Dependências
```bash
pip install pygame pygbag
```

### 2. Criar Build Web
```powershell
.\build_web.ps1
```

Ou:
```cmd
build_web.bat
```

### 3. Testar Localmente
```bash
cd build\web
python -m http.server 8000
```
Acesse: http://localhost:8000

### 4. Publicar no itch.io
1. Compacte a pasta `build\web` em ZIP
2. Acesse https://itch.io/dashboard
3. Crie novo projeto
4. Faça upload do ZIP como plataforma "HTML"
5. **IMPORTANTE:** Marque "Play in browser"

## 📚 Documentação Completa

Consulte o arquivo **`GUIA_PUBLICACAO_WEB.md`** para instruções detalhadas.

## ⚠️ Notas Importantes

- O pygbag pode ter algumas limitações com Pygame
- Teste sempre localmente antes de publicar
- Certifique-se de que "Play in browser" está marcado no itch.io
- O arquivo `index.html` deve estar na raiz do ZIP

## 🐛 Problemas?

1. Verifique o console do navegador (F12)
2. Teste localmente primeiro
3. Consulte `GUIA_PUBLICACAO_WEB.md` seção "Solução de Problemas"

