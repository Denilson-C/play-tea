# PLAY TEA - Versão Web (Itch.io)

Este guia explica como hospedar o jogo PLAY TEA no itch.io como uma webapp HTML5.

## 📦 Arquivos Gerados

O Pygbag gerou os seguintes arquivos em `build/web/`:
- `index.html` - Página principal do jogo
- `play-tea.apk` - Arquivo empacotado com Python + assets
- `favicon.png` - Ícone do jogo

Um arquivo ZIP (`play-tea-web.zip`) foi criado contendo todos esses arquivos.

## 🚀 Como Hospedar no Itch.io

### Passo 1: Criar/Acessar Conta no Itch.io

1. Acesse https://itch.io
2. Faça login ou crie uma conta gratuita
3. Vá para o Dashboard (https://itch.io/dashboard)

### Passo 2: Criar Novo Projeto

1. Clique em "Create new project"
2. Preencha as informações básicas:
   - **Título**: PLAY TEA
   - **Tipo de projeto**: HTML
   - **Classificação**: Game

### Passo 3: Upload dos Arquivos

1. Na seção "Uploads", clique em "Upload files"
2. **Opção A - Upload do ZIP completo:**
   - Faça upload do arquivo `play-tea-web.zip`
   - Marque a opção "This file will be played in the browser"

3. **Opção B - Upload manual (alternativa):**
   - Acesse a pasta `build/web/`
   - Faça upload de TODOS os arquivos: `index.html`, `play-tea.apk`, `favicon.png`
   - Marque o arquivo `index.html` como "This file will be played in the browser"

### Passo 4: Configurações de Visualização

1. Na seção "Embed options":
   - **Viewport dimensions**:
     - Largura (Width): `800`
     - Altura (Height): `600`
   - **Embed in page**: Marque esta opção
   - **Mobile friendly**: Marque se quiser suporte mobile (opcional)

2. **Frame options**:
   - Recomendado: "Manually set size" com 800x600

### Passo 5: Configurações Adicionais

1. **Descrição**: Adicione informações sobre o jogo
   ```
   PLAY TEA - Jogo Educacional

   Um jogo desenvolvido para auxiliar crianças no desenvolvimento de habilidades motoras.

   Características:
   - Interface amigável com fonte OpenDyslexic
   - Diferentes personagens (Cachorrinho e Gatinho)
   - Sistema de pontuação e progressão
   - Ruídos de fundo configuráveis

   Desenvolvido por: Denilson Conceição, Jonathas Yoshioka, Leonardo Zanata, Matheus Garcia
   Orientador: Prof. Dr. Irapuan Glória Júnior
   Instituição: Fatec Barueri
   ```

2. **Screenshots**: Adicione capturas de tela do jogo (opcional)

3. **Tags sugeridas**:
   - educational
   - portuguese
   - kids
   - pygame
   - accessibility

### Passo 6: Publicação

1. **Visibilidade**:
   - **Public**: Qualquer pessoa pode ver
   - **Restricted**: Apenas com link direto
   - **Draft**: Rascunho (não publicado)

2. Clique em "Save & View page" para salvar

3. Se estiver satisfeito, clique em "Publish" para tornar o jogo público

## 🎮 Testando o Jogo

Após o upload, você pode:
1. Clicar em "View project" para ver a página do jogo
2. Testar diretamente no navegador
3. Compartilhar o link com outras pessoas

## 📱 Compatibilidade

A versão web funciona em:
- ✅ Google Chrome
- ✅ Firefox
- ✅ Edge
- ✅ Safari
- ⚠️ Mobile (funcionalidade limitada - recomenda-se versão Android)

## ⚙️ Configurações Recomendadas

- **Resolução**: 800x600 pixels
- **Iframe**: Habilitado
- **Fullscreen**: Opcional (pode melhorar experiência)

## 🐛 Resolução de Problemas

### Jogo não carrega
- Certifique-se de que todos os 3 arquivos foram enviados
- Verifique se `index.html` está marcado como "Play in browser"
- Limpe o cache do navegador

### Tela preta
- Aguarde alguns segundos - o jogo precisa carregar o WebAssembly
- Verifique o console do navegador (F12) para erros

### Áudio não funciona
- Alguns navegadores bloqueiam áudio automático
- O usuário precisa interagir com a página primeiro

### Performance lenta
- A versão web pode ser mais lenta que a versão desktop/mobile
- Recomende fechar outras abas do navegador

## 📄 Arquivos do Projeto

```
play-tea/
├── main.py                    # Entry point (versão web)
├── src/
│   ├── inicio.py             # Código original (desktop)
│   └── inicio_web.py         # Código adaptado (web)
├── assets/
│   ├── images/               # Sprites e imagens
│   ├── audio/                # Efeitos sonoros
│   └── fonts/                # Fonte OpenDyslexic
├── data/                     # Saves e configurações
└── build/
    └── web/                  # Arquivos gerados pelo Pygbag
        ├── index.html
        ├── play-tea.apk
        └── favicon.png
```

## 🔄 Atualizando a Versão Web

Se fizer alterações no código:

```bash
# 1. Faça as alterações em src/inicio_web.py
# 2. Regere a versão web
pygbag --build .

# 3. Crie novo ZIP
cd /home/user/play-tea
zip -r play-tea-web.zip build/web/

# 4. Faça upload do novo ZIP no itch.io
```

## 🎯 Próximos Passos

- [ ] Adicionar screenshots do jogo no itch.io
- [ ] Criar um banner/capa atrativa
- [ ] Adicionar trailer em vídeo (opcional)
- [ ] Configurar analytics (itch.io oferece estatísticas)
- [ ] Criar página de devlog para atualizações

## 📞 Suporte

**Projeto**: PLAY TEA - Trabalho de Graduação 2
**Instituição**: Fatec Barueri - Faculdade de Tecnologia
**Orientador**: Prof. Dr. Irapuan Glória Júnior

**Desenvolvedores**:
- Denilson Conceição de Oliveira
- Jonathas Yoshioka Olsen Trajano da Silva
- Leonardo Zanata de Jesus
- Matheus Garcia Bertoi

**Versão**: 1.1 Web

---

**Última atualização**: Novembro 2025
