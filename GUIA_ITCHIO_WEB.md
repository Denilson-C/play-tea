# 🎮 Guia de Publicação - PLAY TEA no itch.io (Web/HTML5)

Este guia explica como preparar e publicar o jogo PLAY TEA na plataforma itch.io como jogo web (HTML5).

## 📋 Pré-requisitos

1. **Python 3.8+** instalado
2. **pygbag** para compilar Pygame para Web
3. **Conta no itch.io** (crie em https://itch.io)

## 🛠️ Passo 1: Instalar pygbag

```bash
pip install pygbag
```

## 📦 Passo 2: Criar Build Web

### Opção A: Usando o script automático

Execute no terminal:
```cmd
build_web.bat
```

### Opção B: Manualmente

```bash
# Limpar builds anteriores (opcional)
rmdir /s /q build\web
rmdir /s /q web

# Compilar para web
pygbag main.py
```

O build será criado em `build/web/` ou `web/`

## ✅ Passo 3: Testar Localmente

Antes de publicar, **SEMPRE teste localmente**:

```bash
cd build\web
python -m http.server 8000
```

Depois acesse no navegador: **http://localhost:8000**

### O que verificar:
- ✅ Jogo carrega corretamente
- ✅ Imagens aparecem
- ✅ Sons funcionam (pode precisar clicar na tela primeiro)
- ✅ Fontes carregam
- ✅ Controles funcionam (mouse)
- ✅ Todas as fases funcionam
- ✅ Menu e configurações funcionam

## 📁 Passo 4: Preparar Arquivos para Upload

### Compactar em ZIP:

1. Vá para a pasta `build\web` (ou `web`)
2. Selecione **TODOS** os arquivos (Ctrl+A)
3. Clique com botão direito → **Enviar para** → **Pasta compactada (em zip)**
4. Renomeie o arquivo para `PLAYTEA-web.zip`

**Importante:** O arquivo `index.html` deve estar na **raiz** do ZIP.

## 🚀 Passo 5: Publicar no itch.io

### 5.1 Criar Projeto

1. Acesse https://itch.io/dashboard
2. Clique em **"Create new project"**
3. Preencha:
   - **Project title:** PLAY TEA
   - **Project URL:** (será gerado automaticamente)
   - **Classification:** Game
   - **Genre:** Educational
   - **Tags:** educacional, terapia, crianças, dislexia, web

### 5.2 Configurar a Página

#### Descrição:
```
PLAY TEA é um jogo educacional desenvolvido para auxiliar no processo terapêutico de crianças, com foco em acessibilidade e inclusão.

Características:
- Fonte OpenDyslexic para melhorar a leitura
- Personalização de cores e sons
- Múltiplas fases de aprendizado
- Interface acessível e intuitiva
- Jogável diretamente no navegador!
```

#### Capturas de Tela:
- Adicione 3-5 imagens do jogo
- Primeira imagem deve ser a mais atrativa
- Use formato PNG ou JPG

#### Informações:
- **Versão:** 1.1
- **Plataformas:** Web (HTML5)
- **Linguagem:** Português (Brasil)
- **Preço:** Gratuito ou valor sugerido

### 5.3 Upload dos Arquivos

1. Vá em **"Upload files"**
2. Selecione **"HTML"** como plataforma
3. Faça upload do arquivo `PLAYTEA-web.zip`
4. **CRÍTICO:** Marque a opção **"This file will be played in the browser"**
5. Clique em **"Save"**

### 5.4 Configurações de Distribuição

- ✅ **"This game will be distributed for free"** (se for gratuito)
- ✅ **"Allow comments"**
- ✅ **"Allow ratings"**
- **Classificação:** Selecione apropriada (provavelmente "Everyone")

### 5.5 Preview e Publicação

1. Clique em **"Save"** para salvar
2. Use **"Preview"** para testar o jogo diretamente no itch.io
3. Quando estiver satisfeito, clique em **"Save & view page"**
4. Para publicar, clique em **"Edit"** → **"Status"** → **"Public"**

## 📝 Checklist de Publicação

- [ ] pygbag instalado e funcionando
- [ ] Build web criado sem erros
- [ ] Testado localmente (http://localhost:8000)
- [ ] Todos os assets carregam corretamente
- [ ] Sons funcionam no navegador
- [ ] Fontes carregam corretamente
- [ ] Controles (mouse) funcionam
- [ ] Todas as fases testadas
- [ ] Menu e configurações testados
- [ ] Capturas de tela prontas
- [ ] Descrição completa escrita
- [ ] Tags e categorias definidas
- [ ] Arquivos ZIP compactados
- [ ] Upload feito como "HTML"
- [ ] **"Play in browser" marcado**
- [ ] Preview testado no itch.io
- [ ] Status definido como "Public"

## 🐛 Solução de Problemas

### Erro: "pygbag não encontrado"
```bash
pip install pygbag
```

### Erro: "Module not found" durante o build
- Verifique se todas as dependências estão instaladas
- Execute: `pip install -r requirements.txt`

### Assets não carregam no navegador
- Verifique se os caminhos estão corretos
- Assets devem estar na mesma estrutura de pastas
- Verifique o console do navegador (F12) para erros

### Sons não funcionam
- Alguns navegadores bloqueiam áudio automático
- O usuário pode precisar clicar na tela primeiro
- Verifique se os formatos são suportados (OGG é geralmente bom)

### Fontes não carregam
- Verifique se todos os arquivos de fonte estão incluídos
- Alguns navegadores podem ter limitações com fontes personalizadas

### Jogo não carrega no itch.io
- **Certifique-se de que "Play in browser" está marcado**
- Verifique se o `index.html` está na raiz do ZIP
- Teste o arquivo ZIP localmente antes de fazer upload

### Performance lenta
- Otimize imagens (use compressão)
- Reduza tamanho de arquivos de áudio
- Considere usar spritesheets

## 🔧 Otimizações para Web

### 1. Compressão de Assets
- Comprima imagens PNG/JPG
- Use formatos OGG para áudio (já está usando!)
- Minimize tamanho de arquivos JSON

### 2. Teste em Múltiplos Navegadores
- Chrome/Edge (Chromium)
- Firefox
- Safari (se possível)

## 💡 Dicas

1. **Teste extensivamente:** Teste em diferentes navegadores e dispositivos
2. **Otimize assets:** Menor tamanho = carregamento mais rápido
3. **Feedback:** Adicione uma mensagem de carregamento se necessário
4. **Mobile:** Considere se o jogo funciona em dispositivos móveis
5. **Analytics:** O itch.io fornece estatísticas de jogos

## ⚠️ Limitações Conhecidas

- Pygame para web pode ter algumas limitações
- Algumas funcionalidades podem não funcionar exatamente como no desktop
- Performance pode variar entre navegadores
- Áudio pode precisar de interação do usuário primeiro

## 📚 Recursos

- [Documentação do itch.io](https://itch.io/docs)
- [Documentação do pygbag](https://pypi.org/project/pygbag/)
- [Pygame Web](https://pygame-web.github.io/)

---

**Boa sorte com a publicação! 🎮**

