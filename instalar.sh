#!/bin/bash
# Instala as dependências e baixa o modelo de voz (574 MB) para ./modelos
set -e
cd "$(dirname "$0")"
brew install whisper-cpp ffmpeg
mkdir -p modelos
curl -L -o modelos/ggml-large-v3-turbo-q5_0.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin
echo "Pronto. Rode: ./ouvecena video.mov --contexto"
