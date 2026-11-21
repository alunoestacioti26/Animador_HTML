"""
HTML -> MP4
Cole o código HTML de uma animação, escolha a duração e baixe o vídeo em MP4.

Como usar:
    pip install flask playwright imageio-ffmpeg
    playwright install chromium
    python app.py
Depois abra http://localhost:5000 no navegador.
"""

import glob
import os
import shutil
import subprocess
import tempfile
import time

from flask import Flask, jsonify, request, send_file
from imageio_ffmpeg import get_ffmpeg_exe
from playwright.sync_api import sync_playwright

app = Flask(__name__)

MAX_DURATION = 120  # segundos


def render_html_to_mp4(html: str, duration: float, width: int, height: int) -> str:
    """Abre o HTML num Chromium, grava a tela e converte para MP4. Retorna o caminho do .mp4."""
    workdir = tempfile.mkdtemp(prefix="html2mp4_")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": width, "height": height},
            record_video_dir=workdir,
            record_video_size={"width": width, "height": height},
        )
        t_video_start = time.time()
        page = context.new_page()

        # o vídeo começa a gravar aqui; guardamos o atraso para cortar a parte em branco
        t_before_load = time.time()
        page.set_content(html, wait_until="load")
        try:
            page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass
        t_after_load = time.time()

        # a animação começa a contar a partir do load, então cortamos o que veio antes
        trim_start = max(0.0, t_before_load - t_video_start)

        page.wait_for_timeout(int(duration * 1000))
        context.close()  # finaliza e salva o .webm
        browser.close()

    webm_files = glob.glob(os.path.join(workdir, "*.webm"))
    if not webm_files:
        raise RuntimeError("Não foi possível gravar o vídeo.")

    out_path = os.path.join(workdir, "animacao.mp4")
    cmd = [
        get_ffmpeg_exe(),
        "-y",
        "-ss", f"{trim_start:.3f}",
        "-i", webm_files[0],
        "-t", f"{duration:.3f}",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
        "-movflags", "+faststart",
        out_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not os.path.exists(out_path):
        raise RuntimeError("Falha ao converter para MP4:\n" + result.stderr[-800:])
    return out_path


@app.post("/converter")
def converter():
    data = request.get_json(force=True)
    html = (data.get("html") or "").strip()
    if not html:
        return jsonify(erro="Cole o código HTML primeiro."), 400

    try:
        duration = float(data.get("duracao", 5))
        width = int(data.get("largura", 1280))
        height = int(data.get("altura", 720))
    except (TypeError, ValueError):
        return jsonify(erro="Valores inválidos de duração ou tamanho."), 400

    if not (1 <= duration <= MAX_DURATION):
        return jsonify(erro=f"A duração deve ficar entre 1 e {MAX_DURATION} segundos."), 400
    if not (200 <= width <= 3840 and 200 <= height <= 3840):
        return jsonify(erro="Tamanho de vídeo fora do limite."), 400

    try:
        mp4 = render_html_to_mp4(html, duration, width, height)
    except Exception as e:  # noqa: BLE001
        return jsonify(erro=str(e)), 500

    response = send_file(mp4, mimetype="video/mp4", as_attachment=False, download_name="animacao.mp4")

    @response.call_on_close
    def limpar():
        shutil.rmtree(os.path.dirname(mp4), ignore_errors=True)

    return response


@app.get("/")
def index():
    return PAGE


PAGE = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>HTML para MP4</title>
<style>
  :root {
    --bg: #f5f6f8;
    --panel: #ffffff;
    --ink: #16181d;
    --muted: #5d6573;
    --line: #dde1e8;
    --accent: #2457e6;
    --accent-ink: #ffffff;
    --danger: #b42318;
    --code-bg: #101319;
    --code-ink: #dfe5f0;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #0f1115;
      --panel: #171a21;
      --ink: #eceff4;
      --muted: #98a1b2;
      --line: #2a2f3a;
      --accent: #6d94ff;
      --accent-ink: #0b1020;
      --danger: #ff8a80;
    }
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--bg);
    color: var(--ink);
    font: 16px/1.5 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  }
  main { max-width: 860px; margin: 0 auto; padding: 32px 20px 64px; }
  h1 { font-size: 1.7rem; margin: 0 0 4px; letter-spacing: -0.01em; }
  p.sub { margin: 0 0 24px; color: var(--muted); }
  label { display: block; font-weight: 600; margin-bottom: 6px; }
  textarea {
    width: 100%; min-height: 320px; resize: vertical;
    background: var(--code-bg); color: var(--code-ink);
    border: 1px solid var(--line); border-radius: 8px; padding: 14px;
    font: 13.5px/1.55 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    tab-size: 2;
  }
  textarea:focus, select:focus, input:focus, button:focus-visible, a.btn:focus-visible {
    outline: 2px solid var(--accent); outline-offset: 2px;
  }
  .row { display: flex; gap: 14px; flex-wrap: wrap; margin: 16px 0 20px; }
  .row > div { flex: 1 1 180px; }
  select, input[type=number] {
    width: 100%; padding: 10px 12px; font: inherit; color: var(--ink);
    background: var(--panel); border: 1px solid var(--line); border-radius: 8px;
  }
  .btn {
    display: inline-block; padding: 12px 22px; font: inherit; font-weight: 600;
    border: 0; border-radius: 8px; cursor: pointer; text-decoration: none;
    background: var(--accent); color: var(--accent-ink);
  }
  .btn:disabled { opacity: .55; cursor: wait; }
  #status { margin: 16px 0 0; color: var(--muted); min-height: 1.5em; }
  #status.erro { color: var(--danger); white-space: pre-wrap; }
  #resultado { display: none; margin-top: 28px; padding-top: 24px; border-top: 1px solid var(--line); }
  #resultado video { width: 100%; max-height: 480px; background: #000; border-radius: 8px; display: block; margin-bottom: 16px; }
  @media (prefers-reduced-motion: no-preference) {
    .btn { transition: opacity .15s; }
  }
</style>
</head>
<body>
<main>
  <h1>HTML para MP4</h1>
  <p class="sub">Cole o código da sua animação, escolha a duração e baixe o vídeo.</p>

  <label for="html">Código HTML</label>
  <textarea id="html" spellcheck="false">&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
&lt;style&gt;
  html, body { margin: 0; height: 100%; background: #0e1530; overflow: hidden; }
  .bola {
    position: absolute; left: 50%; top: 0; width: 90px; height: 90px; margin-left: -45px;
    border-radius: 50%; background: #ffb703;
    animation: pula 1.4s cubic-bezier(.5, 0, .5, 1) infinite alternate;
  }
  @keyframes pula { to { top: calc(100% - 90px); background: #fb5607; } }
&lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;&lt;div class="bola"&gt;&lt;/div&gt;&lt;/body&gt;
&lt;/html&gt;</textarea>

  <div class="row">
    <div>
      <label for="duracao">Duração (segundos)</label>
      <input id="duracao" type="number" min="1" max="120" step="0.5" value="5">
    </div>
    <div>
      <label for="tamanho">Tamanho do vídeo</label>
      <select id="tamanho">
        <option value="1280x720">1280 × 720 (HD, horizontal)</option>
        <option value="1920x1080">1920 × 1080 (Full HD, horizontal)</option>
        <option value="1080x1080">1080 × 1080 (quadrado)</option>
        <option value="1080x1920">1080 × 1920 (vertical, Stories/Reels)</option>
      </select>
    </div>
  </div>

  <button class="btn" id="gerar">Gerar MP4</button>
  <p id="status" role="status"></p>

  <section id="resultado">
    <video id="preview" controls loop></video>
    <a class="btn" id="baixar" download="animacao.mp4">Baixar MP4</a>
  </section>
</main>

<script>
const $ = (id) => document.getElementById(id);
const gerar = $("gerar"), status = $("status"), resultado = $("resultado");
let urlAtual = null;

// o texto padrão está escapado dentro do textarea; aqui só garantimos que o valor lido é HTML puro
gerar.addEventListener("click", async () => {
  const [largura, altura] = $("tamanho").value.split("x").map(Number);
  const duracao = parseFloat($("duracao").value);

  gerar.disabled = true;
  resultado.style.display = "none";
  status.className = "";
  status.textContent = "Gravando a animação… isso leva um pouco mais que a duração escolhida.";

  try {
    const resp = await fetch("/converter", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ html: $("html").value, duracao, largura, altura })
    });

    if (!resp.ok) {
      const erro = await resp.json().catch(() => ({ erro: "Erro desconhecido." }));
      throw new Error(erro.erro);
    }

    const blob = await resp.blob();
    if (urlAtual) URL.revokeObjectURL(urlAtual);
    urlAtual = URL.createObjectURL(blob);

    $("preview").src = urlAtual;
    $("baixar").href = urlAtual;
    resultado.style.display = "block";
    status.textContent = "Pronto! O vídeo está abaixo.";
  } catch (e) {
    status.className = "erro";
    status.textContent = e.message;
  } finally {
    gerar.disabled = false;
  }
});
</script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", 5000)), threaded=False)
