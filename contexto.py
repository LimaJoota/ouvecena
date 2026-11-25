"""Une fala e imagem: um quadro no meio de cada segmento, em contexto.md (para LLM) e contexto.html (para gente)."""
import json, subprocess, sys, html, pathlib

def faixa(ff, video, s=1.0):
    """Acha faixa lisa (qualquer cor) nas bordas e devolve crop W:H:X:Y, ou "" se não houver."""
    p = subprocess.run([ff, "-v", "error", "-ss", str(s), "-i", video, "-frames:v", "1", "-vf", "scale=320:-2,format=gray", "-f", "rawvideo", "-"], capture_output=True)
    w = 320; px = p.stdout; h = len(px) // w
    if h < 8: return ""
    lin = lambda y: px[y * w:(y + 1) * w]
    # faixa = linhas lisas da mesma cor da borda (folga de 6 tons para a compressão)
    lisa = lambda v, c: max(v) - min(v) <= 6 and abs(v[0] - c) <= 6
    fim = lambda rg, f: next((i for i in rg if not lisa(f(i), f(rg[0])[0])), rg[0])
    t = fim(range(h), lin); b = fim(range(h - 1, -1, -1), lin)
    med = lambda v: sorted(v)[len(v) // 2]
    # é faixa só se a cor dela difere do conteúdo (margem lisa da página não é); a escala borra a borda,
    # então compara 3 linhas para dentro e corta 2 a mais
    tira = lambda borda, cont: borda is not None and abs(borda - med(cont)) > 25
    t = min(t + 2, h - 1) if tira(lin(0)[0] if t else None, lin(min(t + 3, h - 1))) else 0
    b = max(b - 2, 0) if tira(lin(h - 1)[0] if b < h - 1 else None, lin(max(b - 3, 0))) else h - 1
    col = lambda x: px[x::w][t:b + 1]  # colunas só entre as faixas de cima e de baixo
    l = fim(range(w), col); r = fim(range(w - 1, -1, -1), col)
    l = min(l + 2, w - 1) if tira(col(0)[0] if l else None, col(min(l + 3, w - 1))) else 0
    r = max(r - 2, 0) if tira(col(w - 1)[0] if r < w - 1 else None, col(max(r - 3, 0))) else w - 1
    if (t, b, l, r) == (0, h - 1, 0, w - 1) or b - t < h // 4 or r - l < w // 4: return ""
    W, H = map(int, subprocess.run(["/opt/homebrew/bin/ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", video], capture_output=True, text=True).stdout.split(",")[:2])
    k = W / w; e = lambda v: int(v * k) // 2 * 2
    return f"{e(r - l + 1)}:{e(b - t + 1)}:{e(l)}:{e(t)}"

ff, video, jsonf, out = sys.argv[1:5]; crop = sys.argv[5] if len(sys.argv) > 5 else ""
if not crop and video.lower().endswith((".mp4", ".mov", ".m4v", ".mkv", ".webm")): crop = faixa(ff, video)
out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
t = lambda ms: f"{int(ms//60000):02d}:{ms/1000%60:05.2f}"
seg = json.load(open(jsonf))["transcription"]
md, hh = ["# Vídeo: fala + quadro de cada trecho\n"], ["<meta charset=utf-8><title>Contexto</title><style>body{font:16px system-ui;max-width:760px;margin:2em auto;padding:0 16px}section{display:flex;gap:16px;margin:0 0 20px}img{height:260px;border-radius:6px}b{color:#555}</style>"]
for i, s in enumerate(seg, 1):
    a, b = s["offsets"]["from"], s["offsets"]["to"]
    f = f"q{i:02d}.jpg"
    subprocess.run([ff, "-v", "error", "-y", "-ss", str((a + b) / 2000), "-i", video, "-frames:v", "1", "-vf", (f"crop={crop}," if crop else "") + "scale=-2:480", str(out / f)], check=True)
    x = s["text"].strip()
    md.append(f"## [{t(a)} → {t(b)}]\n![quadro]({f})\n\n{x}\n")
    hh.append(f"<section><img src='{f}'><div><b>{t(a)} → {t(b)}</b><p>{html.escape(x)}</p></div></section>")
(out / "contexto.md").write_text("\n".join(md)); (out / "contexto.html").write_text("\n".join(hh))
print(out / "contexto.html")
