# transcritor

Vídeo/áudio → texto em português com tempo, local e sem custo (whisper.cpp). Feito para dar contexto a LLMs.

Requisitos: `brew install whisper-cpp ffmpeg`; modelo `ggml-large-v3-turbo-q5_0.bin` (huggingface.co/ggerganov/whisper.cpp) em `modelos/`.

    ./transcrever video.mov               # .txt com [início --> fim] texto
    ./transcrever video.mov --quadros 5   # + folha de contato (1 quadro a cada 5 s)
    ./transcrever video.mov --contexto    # + contexto.md/html: um quadro por trecho de fala, casado com o texto
    ./transcrever video.mov --contexto --corte "iw:ih*0.36:0:ih*0.32"   # corta faixas sobrando (W:H:X:Y do ffmpeg)
