[app]
title = PLAY TEA
package.name = playtea
package.domain = org.playtea
source.dir = .
source.include_exts = py,pyc,txt,kv,png,jpg,ogg,wav,mp3,json
version = 1.1
orientation = landscape
fullscreen = 1
android.sdk_path = /home/webner/.buildozer/android/platform/android-sdk
android.sdk_dir = /home/webner/.buildozer/android/platform/android-sdk

# Requisitos: python3 + pygame
requirements = python==3.11.8, pygame

# Entry point
entrypoint = main.py

# Opções comuns
android.api = 31
android.minapi = 21
android.archs = armeabi-v7a, arm64-v8a
android.ndk = 25b
# ADICIONE ESTA LINHA ABAIXO:
android.sdk = 4333796 

[buildozer]
log_level = 3
warn_on_root = 0


