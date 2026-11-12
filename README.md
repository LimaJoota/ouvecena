<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/marca/ouvecena-escuro.svg">
  <img src="docs/marca/ouvecena-claro.svg" width="340" alt="Ouvecena">
</picture>

### Vídeo para texto com tempo e imagem, de graça e sem internet

Grave a tela falando e apontando. A IA recebe cada fala junto com o quadro que estava na tela naquele momento.

<a href="#instalar"><img src="https://img.shields.io/badge/Instalar_no_Mac-FF5A1F?style=for-the-badge&logo=apple&logoColor=white" alt="Instalar no Mac" height="44"></a>

[![Estrelas](https://img.shields.io/github/stars/LimaJoota/ouvecena?style=flat&label=estrelas&labelColor=15171A&color=FF5A1F)](https://github.com/LimaJoota/ouvecena/stargazers)
[![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-3A3F45?labelColor=15171A)](LICENSE)

<img src="docs/marca/ouvecena-demo.gif" width="800" alt="O Ouvecena em ação: cada fala do vídeo ao lado do quadro que estava na tela">

</div>

## Instalar

Precisa de um Mac com chip Apple (M1 ou mais novo) e do [Homebrew](https://brew.sh).

```bash
git clone https://github.com/LimaJoota/ouvecena.git
cd ouvecena
./instalar.sh
```

O script instala o `whisper-cpp` e o `ffmpeg` e baixa o modelo de voz (574 MB).

## Usar

Abra o app (`./app.py`, ou crie um atalho com o `Ouvecena.app` descrito abaixo). Uma página abre no navegador. Solte o vídeo nela.

No fim, clique em **Copiar texto para a IA**, cole no chat e arraste as imagens da pasta que **Abrir pasta com os quadros** mostra.

Prefere o terminal?

```bash
./ouvecena video.mov --contexto
```

Saem um `contexto.md` e um quadro por fala. Tudo fica em `~/Ouvecena/`.

## O que ele faz

- **Sem internet.** A voz vira texto no seu Mac e nenhum áudio sai dele.
- **A IA entende o "isso aqui".** Cada fala vem com o quadro do momento, então "sobe isso" deixa de ser mistério.
- **Tempo em tudo.** Cada trecho tem início e fim.
- **Folha de contato.** `--quadros 5` junta um quadro a cada 5 segundos numa imagem só.
- **Corte de faixas.** `--corte "iw:ih*0.36:0:ih*0.32"` tira as barras sobrando da gravação do celular.

<table>
  <tr>
    <td><img src="docs/telas/titulo.jpg" alt="Quadro do trecho: Aqui em cima fica o título da página"></td>
    <td><img src="docs/telas/precos.jpg" alt="Quadro do trecho: Tira essa tabela e coloca os depoimentos no lugar"></td>
    <td><img src="docs/telas/botao.jpg" alt="Quadro do trecho: deixa só este botão, bem grande"></td>
  </tr>
  <tr>
    <td align="center"><sub>"Aqui em cima fica o título"</sub></td>
    <td align="center"><sub>"Tira essa tabela"</sub></td>
    <td align="center"><sub>"Deixa só este botão"</sub></td>
  </tr>
</table>

## Gostou?

Deixe uma estrela. Ela ajuda mais gente a achar o Ouvecena.

<a href="https://star-history.com/#LimaJoota/ouvecena&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=LimaJoota/ouvecena&type=Date&theme=dark">
    <img src="https://api.star-history.com/svg?repos=LimaJoota/ouvecena&type=Date" width="520" alt="Estrelas do Ouvecena ao longo do tempo">
  </picture>
</a>

## Créditos

Feito com [whisper.cpp](https://github.com/ggml-org/whisper.cpp) e [ffmpeg](https://ffmpeg.org). Licença [MIT](LICENSE). Hoje só roda no Mac e o idioma é português do Brasil.
