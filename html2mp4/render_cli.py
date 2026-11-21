"""Converte um arquivo HTML em MP4 pela linha de comando (usado pelo GitHub Actions)."""
import argparse
import shutil

from app import render_html_to_mp4

p = argparse.ArgumentParser()
p.add_argument("arquivo", help="caminho do .html")
p.add_argument("--duracao", type=float, default=5)
p.add_argument("--largura", type=int, default=1280)
p.add_argument("--altura", type=int, default=720)
p.add_argument("--saida", default="animacao.mp4")
a = p.parse_args()

html = open(a.arquivo, encoding="utf-8").read()
mp4 = render_html_to_mp4(html, a.duracao, a.largura, a.altura)
shutil.copy(mp4, a.saida)
print("Vídeo salvo em", a.saida)
