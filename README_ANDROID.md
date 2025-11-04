# PLAY TEA - Guia de Compilação para Android (APK)

Este guia fornece instruções detalhadas para converter o jogo PLAY TEA em um APK que pode ser instalado e executado em dispositivos Android.

## Pré-requisitos

### Opção 1: Usando Linux (Recomendado)

Para compilar o APK, você precisará de um sistema Linux (Ubuntu/Debian recomendado) ou WSL2 no Windows. Os seguintes pacotes são necessários:

```bash
# Atualizar sistema
sudo apt update
sudo apt upgrade -y

# Instalar dependências básicas
sudo apt install -y python3 python3-pip git zip unzip openjdk-11-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Instalar Buildozer e Cython
pip3 install --user --upgrade buildozer cython
```

### Opção 2: Usando Docker (Alternativa)

Se preferir usar Docker para evitar conflitos de dependências:

```bash
# Pull da imagem do Buildozer
docker pull kivy/buildozer

# Execute a compilação dentro do container
docker run -v "$(pwd)":/app -it kivy/buildozer buildozer android debug
```

## Estrutura do Projeto

O projeto foi configurado com a seguinte estrutura:

```
play-tea/
├── main.py                 # Ponto de entrada principal
├── buildozer.spec         # Configuração do Buildozer
├── requirements.txt       # Dependências Python
├── src/
│   └── inicio.py          # Código principal do jogo
├── assets/
│   ├── audio/            # Arquivos de áudio (.ogg)
│   └── images/           # Imagens do jogo (.png)
└── data/                 # Dados salvos e configurações
```

## Passo a Passo para Compilar

### 1. Preparar o Ambiente

Clone o repositório e navegue até o diretório do projeto:

```bash
git clone <url-do-repositorio>
cd play-tea
```

### 2. Configurar o buildozer.spec (Opcional)

O arquivo `buildozer.spec` já está configurado, mas você pode personalizá-lo:

- **Ícone**: Descomente e configure `icon.filename` se tiver um ícone personalizado
- **Splash Screen**: Descomente e configure `presplash.filename` para uma tela de splash
- **Permissões**: Adicione mais permissões em `android.permissions` se necessário
- **Orientação**: Altere `orientation` para `portrait`, `landscape` ou `all`

### 3. Primeira Compilação (Debug)

Execute o Buildozer para compilar o APK em modo debug:

```bash
# Limpar builds anteriores (opcional, mas recomendado na primeira vez)
buildozer android clean

# Compilar o APK
buildozer android debug
```

**Observação**: A primeira compilação pode demorar de 30 minutos a 2 horas, pois o Buildozer irá baixar:
- Android SDK
- Android NDK
- Dependências Python para Android
- Bibliotecas necessárias

### 4. Compilação Release (Para Distribuição)

Para criar um APK assinado para distribuição:

```bash
# Gerar um APK release
buildozer android release

# Assinar o APK (necessário para Google Play Store)
# Você precisará gerar uma keystore primeiro:
keytool -genkey -v -keystore play-tea.keystore -alias play-tea -keyalg RSA -keysize 2048 -validity 10000

# Assinar o APK
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore play-tea.keystore bin/*.apk play-tea

# Alinhar o APK (otimização)
zipalign -v 4 bin/*-release-unsigned.apk bin/play-tea-release.apk
```

## Localização do APK

Após a compilação bem-sucedida, o APK estará localizado em:

```
play-tea/bin/playtea-1.1-arm64-v8a-debug.apk
```

## Instalar no Dispositivo Android

### Via USB (ADB)

```bash
# Instalar ADB se necessário
sudo apt install adb

# Conectar o dispositivo via USB e habilitar "Depuração USB" nas configurações do desenvolvedor
adb devices

# Instalar o APK
adb install bin/playtea-1.1-arm64-v8a-debug.apk
```

### Via Transferência Direta

1. Copie o arquivo APK para o dispositivo Android
2. Abra o arquivo no gerenciador de arquivos do Android
3. Permita a instalação de fontes desconhecidas quando solicitado
4. Instale o aplicativo

## Resolução de Problemas

### Erro: "Command failed: git -C..."

Certifique-se de que o Git está instalado:
```bash
sudo apt install git
```

### Erro: "SDK ou NDK não encontrado"

Limpe o cache do Buildozer e tente novamente:
```bash
buildozer android clean
rm -rf .buildozer
buildozer android debug
```

### Erro: "Permissão negada"

Certifique-se de que os scripts têm permissão de execução:
```bash
chmod +x main.py
```

### APK trava ao abrir

Verifique os logs do Android:
```bash
adb logcat | grep python
```

### Problemas com Áudio no Android

O código já foi otimizado para Android com configurações específicas do mixer do Pygame:
```python
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
```

## Configurações Avançadas

### Arquiteturas Suportadas

O buildozer.spec está configurado para compilar para:
- `arm64-v8a` (64-bit ARM, maioria dos dispositivos modernos)
- `armeabi-v7a` (32-bit ARM, dispositivos mais antigos)

Para compilar apenas uma arquitetura específica:
```bash
buildozer android debug --arch=arm64-v8a
```

### Otimização de Tamanho

Para reduzir o tamanho do APK:

1. Remova arquivos não utilizados antes da compilação
2. Comprima imagens PNG
3. Use formatos de áudio mais eficientes (.ogg já é eficiente)

### Testes

Teste o jogo em diferentes dispositivos:
- Tela pequena (5" ou menos)
- Tela média (5-6")
- Tela grande (6" ou mais)
- Diferentes versões do Android (API 21+)

## Suporte e Contato

**Projeto**: PLAY TEA - Trabalho de Graduação 2
**Instituição**: Fatec Barueri - Faculdade de Tecnologia
**Orientador**: Prof. Dr. Irapuan Glória Júnior

**Desenvolvedores**:
- Denilson Conceição de Oliveira
- Jonathas Yoshioka Olsen Trajano da Silva
- Leonardo Zanata de Jesus
- Matheus Garcia Bertoi

## Versão

**Versão atual**: 1.1

## Licença

[Adicione informações de licença aqui]

---

**Última atualização**: Novembro 2025
