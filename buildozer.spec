[app]

# (str) Título da aplicação
title = PLAY TEA

# (str) Nome do pacote
package.name = playtea

# (str) Domínio do pacote (necessário para Android/iOS)
package.domain = org.fatecbarueri

# (str) Diretório de origem onde o main.py está localizado
source.dir = .

# (list) Arquivos de código fonte a incluir (deixe vazio para incluir todos)
source.include_exts = py,png,jpg,ogg,json,ttf

# (list) Lista de inclusões usando padrão de correspondência
source.include_patterns = assets/*,data/*,src/*

# (str) Versão da aplicação
version = 1.1

# (list) Requisitos da aplicação
requirements = python3,pygame

# (str) Versão do python-for-android a usar
p4a.branch = develop

# (str) Permissões do Android
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (str) Orientação suportada (landscape, portrait ou all)
orientation = landscape

# (bool) Indicar se a aplicação deve ser fullscreen ou não
fullscreen = 1

# (str) Ícone da aplicação
#icon.filename = %(source.dir)s/assets/images/icon.png

# (str) Splash screen
#presplash.filename = %(source.dir)s/assets/images/splash.png

# (int) Versão da API do Android a ser usada (mínimo 21 para Pygame)
android.api = 31

# (int) Versão mínima da API
android.minapi = 21

# (int) Versão do NDK do Android
android.ndk = 23b

# (int) Versão do SDK do Android
android.sdk = 31

# (bool) Usar --private data storage (útil para salvar dados do jogo)
android.private_storage = True

# (str) Arquitetura Android (pode ser armeabi-v7a, arm64-v8a, x86, x86_64)
android.archs = arm64-v8a

# (bool) Ativar backup do Android
android.allow_backup = True

[buildozer]

# (int) Nível de log (0 = apenas erro, 1 = info, 2 = debug - default é 2)
log_level = 2

# (int) Exibir avisos se buildozer estiver usando funções obsoletas
warn_on_root = 1
