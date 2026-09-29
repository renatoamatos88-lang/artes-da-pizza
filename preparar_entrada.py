"""
Recorta cada foto original num quadrado centrado na pizza (com folga) para subir no DaVinci.
Enquadramento igual na entrada => resultado mais parecido entre si na saída.
Saída: Imagem Pizzas/_entrada/<sabor>.jpg
"""
import os
import numpy as np
from PIL import Image
import compor_fotos as cf
from rembg import new_session

PASTA = "Imagem Pizzas"
SAIDA = os.path.join(PASTA, "_entrada")
FOLGA = 1.14

def main():
    os.makedirs(SAIDA, exist_ok=True)
    sess = [new_session(m) for m in cf.MODELOS_RECORTE]
    fila = sorted(f for f in os.listdir(PASTA) if f.lower().endswith((".jpeg", ".jpg")) and f not in cf.REFAZER)
    for nome in fila:
        im = Image.open(os.path.join(PASTA, nome)).convert("RGB")
        im.thumbnail((1600, 1600))
        w, h = im.size
        rgba, (cx, cy, rx, ry) = cf.limpar(cf.recortar(im, sess))
        lado = int(min(2 * max(rx, ry) * FOLGA, w, h))
        x0 = int(min(max(cx - lado / 2, 0), w - lado))
        y0 = int(min(max(cy - lado / 2, 0), h - lado))
        im.crop((x0, y0, x0 + lado, y0 + lado)).save(os.path.join(SAIDA, os.path.splitext(nome)[0] + ".jpg"), quality=95)
        print(f"ok  {nome}  lado={lado}")

if __name__ == "__main__":
    main()
