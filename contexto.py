"""Une fala e imagem: um quadro no meio de cada segmento, em contexto.md (para LLM) e contexto.html (para gente)."""
import json, subprocess, sys, html, pathlib
ff, video, jsonf, out = sys.argv[1:5]; crop = sys.argv[5] if len(sys.argv) > 5 else ""
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
