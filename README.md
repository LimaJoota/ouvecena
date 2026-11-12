<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/marca/ouvecena-escuro.svg">
  <img src="docs/marca/ouvecena-claro.svg" width="340" alt="Ouvecena">
</picture>

### Vídeo vira texto com tempo e imagem, para a IA entender, de graça e sem internet

Grave a tela falando e apontando. O Ouvecena entrega cada fala junto com o quadro que estava na tela naquele momento.

</div>

## Por que existe

A IA não ouve vídeo. Se você grava a tela explicando uma mudança ("sobe isso aqui, tira aquilo"), ela perde o "isso" e o "aqui". O Ouvecena resolve: transcreve a fala em português com início e fim, tira um quadro no meio de cada trecho e junta os dois num arquivo que a IA lê.

## Instalar

Precisa de um Mac com chip Apple e do [Homebrew](https://brew.sh).

```bash
git clone https://github.com/LimaJoota/ouvecena.git
cd ouvecena
./instalar.sh
```

O script instala o `whisper-cpp` e o `ffmpeg` e baixa o modelo de voz (574 MB). Tudo roda no seu Mac e nenhum áudio sai dele.

## Usar

```bash
./ouvecena video.mov                # texto com [início --> fim]
./ouvecena video.mov --contexto     # + um quadro por fala (contexto.md e contexto.html)
./ouvecena video.mov --quadros 5    # + folha de contato, um quadro a cada 5 s
./ouvecena video.mov --contexto --corte "iw:ih*0.36:0:ih*0.32"   # corta faixas sobrando (W:H:X:Y do ffmpeg)
```

Mande o `contexto.md` e as imagens para a IA. Cada trecho vem assim:

```
## [00:08.68 → 00:14.52]
![quadro](q02.jpg)

Como funciona, tu mantém esse daqui, só que você vai subir tudo isso daqui.
```

## Limites

Hoje só roda no Mac e o idioma fixo é português do Brasil. O corte de faixas é manual.

Feito com [whisper.cpp](https://github.com/ggml-org/whisper.cpp) e [ffmpeg](https://ffmpeg.org). Licença MIT.
