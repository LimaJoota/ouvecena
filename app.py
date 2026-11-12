#!/usr/bin/env python3
"""Interface do Ouvecena: solte o vídeo no navegador e receba fala + quadros para a IA.
Roda só neste Mac (127.0.0.1) e se encerra sozinha após 20 min sem uso."""
import json, os, re, subprocess, sys, threading, time, uuid, pathlib
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

AQUI = pathlib.Path(__file__).resolve().parent
SAIDA = pathlib.Path.home() / "Ouvecena"
PORTA = 8765
JOBS, ultimo = {}, [time.time()]

def processar(jid, video):
    pasta = SAIDA / jid
    r = subprocess.run([str(AQUI / "ouvecena"), str(video), "--contexto", "--saida", str(pasta)], capture_output=True, text=True)
    txt = pasta / "video.txt"
    if r.returncode or not txt.exists():
        JOBS[jid] = {"estado": "erro", "erro": (r.stderr or "falhou")[-300:]}; return
    segs = [{"de": a, "ate": b, "texto": t, "quadro": f"/r/{jid}/video/q{i:02d}.jpg"}
            for i, (a, b, t) in enumerate(re.findall(r"\[(\S+) --> (\S+)\] (.*)", txt.read_text()), 1)]
    JOBS[jid] = {"estado": "pronto", "segs": segs, "pasta": str(pasta / "video")}

PAGINA = """<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Ouvecena</title>
<style>
:root{--t:#15171A;--c:#FF5A1F;--f:#F6F3EE}*{box-sizing:border-box}
body{margin:0;background:var(--f);color:var(--t);font:18px/1.45 -apple-system,"Helvetica Neue",sans-serif}
main{max-width:760px;margin:0 auto;padding:40px 20px 80px}
h1{font-size:34px;margin:0 0 6px}h1 i{display:inline-block;width:10px;height:34px;background:var(--c);border-radius:3px;margin-right:10px;vertical-align:-5px}
p.s{margin:0 0 28px;color:#555}
#drop{border:2px dashed #b9b2a6;border-radius:16px;padding:70px 20px;text-align:center;cursor:pointer;background:#fff;transition:.15s}
#drop.on{border-color:var(--c);background:#fff4ee}#drop b{font-size:24px;display:block;margin-bottom:6px}
button{font:inherit;font-weight:600;border:0;border-radius:10px;padding:14px 22px;cursor:pointer;background:var(--c);color:#fff}
button.g{background:#fff;color:var(--t);border:1px solid #cfc8bb}button:focus-visible,#drop:focus-visible{outline:3px solid var(--t);outline-offset:2px}
.seg{display:flex;gap:16px;margin:18px 0;align-items:flex-start}.seg img{width:200px;border-radius:8px;flex:none}
.seg b{color:var(--c);font-variant-numeric:tabular-nums}.acoes{display:flex;gap:10px;flex-wrap:wrap;margin:22px 0}
@media(max-width:560px){.seg{flex-direction:column}.seg img{width:100%}}
@media(prefers-reduced-motion:no-preference){.sp{animation:g 1s linear infinite}}@keyframes g{to{transform:rotate(360deg)}}
.sp{display:inline-block;width:18px;height:18px;border:3px solid #ddd;border-top-color:var(--c);border-radius:50%;vertical-align:-3px;margin-right:8px}
</style><main>
<h1><i></i>Ouvecena</h1><p class=s>Solte um vídeo da sua tela. Você recebe a fala com o tempo e o quadro de cada trecho, pronto para a IA.</p>
<div id=drop tabindex=0 role=button><b>Solte o vídeo aqui</b>ou clique para escolher o arquivo</div>
<input id=arq type=file accept="video/*,audio/*" hidden><div id=res aria-live=polite></div></main>
<script>
const $=s=>document.querySelector(s),d=$('#drop'),r=$('#res');
d.onclick=()=>$('#arq').click();d.onkeydown=e=>{if(e.key=='Enter'||e.key==' ')$('#arq').click()};
$('#arq').onchange=e=>e.target.files[0]&&enviar(e.target.files[0]);
['dragover','dragenter'].forEach(n=>d.addEventListener(n,e=>{e.preventDefault();d.classList.add('on')}));
['dragleave','drop'].forEach(n=>d.addEventListener(n,e=>{e.preventDefault();d.classList.remove('on')}));
d.addEventListener('drop',e=>e.dataTransfer.files[0]&&enviar(e.dataTransfer.files[0]));
async function enviar(f){
  r.innerHTML='<p><span class=sp></span>Enviando…</p>';
  const j=await (await fetch('/enviar',{method:'POST',headers:{'X-Nome':encodeURIComponent(f.name)},body:f})).json();
  const t0=Date.now();r.innerHTML='<p><span class=sp></span>Ouvindo e olhando o vídeo… pode levar alguns minutos.</p>';
  const iv=setInterval(async()=>{const s=await (await fetch('/status/'+j.id)).json();
    if(s.estado=='pronto'){clearInterval(iv);mostrar(s)}
    else if(s.estado=='erro'){clearInterval(iv);r.innerHTML='<p>Deu erro: '+s.erro.replace(/</g,'&lt;')+'</p>'}
    else r.querySelector('p').lastChild.textContent='Ouvindo e olhando o vídeo… '+Math.round((Date.now()-t0)/1000)+' s'},1500)}
function mostrar(s){
  const txt=s.segs.map((g,i)=>`[${g.de} → ${g.ate}] (quadro ${i+1}) ${g.texto}`).join('\\n');
  const prompt='Esta é a transcrição de um vídeo de tela, com o tempo de cada fala. Anexei um quadro por trecho, na mesma ordem (quadro 1, 2, 3…), mostrando o que estava na tela naquele momento. Entenda o que a pessoa aponta quando diz "isso", "aqui" e "esse", e faça o que ela pede.\\n\\n'+txt;
  r.innerHTML='<div class=acoes><button id=cp>Copiar texto para a IA</button><button class=g id=ab>Abrir pasta com os quadros</button></div><p class=s>Cole o texto no chat da IA e arraste as imagens da pasta junto, na ordem.</p>'+
    s.segs.map((g,i)=>`<div class=seg><img src="${g.quadro}" alt="Quadro ${i+1}"><div><b>${g.de} → ${g.ate}</b><br>${g.texto.replace(/</g,'&lt;')}</div></div>`).join('');
  $('#cp').onclick=async e=>{await navigator.clipboard.writeText(prompt);e.target.textContent='Copiado!'};
  $('#ab').onclick=()=>fetch('/abrir/'+s.id,{method:'POST'});
}
</script>"""

class H(BaseHTTPRequestHandler):
    def _j(self, o, c=200):
        b = json.dumps(o).encode(); self.send_response(c); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def _ok(self):  # só aceita pedidos feitos por esta máquina
        ultimo[0] = time.time(); return self.headers.get("Host", "").split(":")[0] in ("127.0.0.1", "localhost")
    def do_GET(self):
        if not self._ok(): return self.send_error(403)
        p = self.path
        if p == "/":
            b = PAGINA.encode(); self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
        elif p.startswith("/status/"):
            jid = p[8:]; s = dict(JOBS.get(jid, {"estado": "ouvindo"})); s["id"] = jid; self._j(s)
        elif p.startswith("/r/") and ".." not in p:
            f = SAIDA / p[3:]
            if not f.is_file(): return self.send_error(404)
            b = f.read_bytes(); self.send_response(200); self.send_header("Content-Type", "image/jpeg"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
        else: self.send_error(404)
    def do_POST(self):
        if not self._ok(): return self.send_error(403)
        if self.path == "/enviar":
            jid = time.strftime("%Y-%m-%d-%H%M%S") + "-" + uuid.uuid4().hex[:4]
            pasta = SAIDA / jid; pasta.mkdir(parents=True)
            ext = pathlib.Path(self.headers.get("X-Nome", "v.mov")).suffix or ".mov"
            from urllib.parse import unquote
            ext = pathlib.Path(unquote(self.headers.get("X-Nome", "v.mov"))).suffix or ".mov"
            v = pasta / f"video{ext}"; n = int(self.headers["Content-Length"])
            with open(v, "wb") as f:
                while n > 0:
                    c = self.rfile.read(min(1 << 20, n)); f.write(c); n -= len(c)
            threading.Thread(target=processar, args=(jid, v), daemon=True).start()
            self._j({"id": jid})
        elif self.path.startswith("/abrir/") and ".." not in self.path:
            subprocess.run(["open", str(SAIDA / self.path[7:] / "video")]); self._j({})
        else: self.send_error(404)
    def log_message(self, *a): pass

def vigiar():
    while time.time() - ultimo[0] < 1200: time.sleep(30)
    os._exit(0)

if __name__ == "__main__":
    SAIDA.mkdir(exist_ok=True)
    threading.Thread(target=vigiar, daemon=True).start()
    ThreadingHTTPServer(("127.0.0.1", PORTA), H).serve_forever()
