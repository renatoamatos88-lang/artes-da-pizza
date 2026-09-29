"""
Pós-processamento das fotos geradas no DaVinci (retoque leve):
esquenta a cor, levanta a luz, dá nitidez e entrega em 1200x1200.

Uso:
    python polir_fotos.py                 -> processa tudo de Imagem Pizzas/_davinci_bruto/
    python polir_fotos.py Aliche          -> só um
Saída: Imagem Pizzas/_final/<sabor>.jpg  +  _antes_depois.jpg
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

PASTA = "Imagem Pizzas"
ENTRADA = os.path.join(PASTA, "_davinci_bruto")
SAIDA = os.path.join(PASTA, "_final")
LADO = 1200

# Forças do tratamento. Mexer aqui muda o lote inteiro.
TEMPERATURA = 1.00   # 0 = nada, 1 = neutraliza o azulado e chega ao alvo quente
LUZ = 0.10           # levantada de brilho nos tons médios
SATURACAO = 1.12
CONTRASTE = 1.06
NITIDEZ = (2.2, 90, 2)  # raio, %, limiar
ALVO_QUENTE = np.array([1.06, 1.0, 0.90], np.float32)  # ganho R,G,B após neutralizar


def polir(im):
    im = im.convert("RGB")
    im = im.resize((LADO, LADO), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255

    # neutraliza dominante fria/verde usando a média dos tons médios (60% da força)
    luma = a.mean(2)
    m = (luma > 0.2) & (luma < 0.85)
    medias = a[m].mean(0)
    ganho = 1 + (medias.mean() / medias - 1) * 0.6
    a = a * ganho
    # depois puxa para o quente
    a = a * (1 + (ALVO_QUENTE - 1) * TEMPERATURA)

    # luz: curva gama suave (levanta médios sem estourar)
    a = np.clip(a, 0, 1) ** (1 - LUZ)
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))

    im = ImageEnhance.Color(im).enhance(SATURACAO)
    im = ImageEnhance.Contrast(im).enhance(CONTRASTE)
    return im.filter(ImageFilter.UnsharpMask(*NITIDEZ))


def main():
    os.makedirs(SAIDA, exist_ok=True)
    nomes = sys.argv[1:] or sorted(os.path.splitext(f)[0] for f in os.listdir(ENTRADA) if f.lower().endswith((".png", ".jpg", ".jpeg")))
    pares = []
    for n in nomes:
        arq = next(f for f in os.listdir(ENTRADA) if os.path.splitext(f)[0] == n)
        bruto = Image.open(os.path.join(ENTRADA, arq))
        final = polir(bruto)
        final.save(os.path.join(SAIDA, n + ".jpg"), quality=93, subsampling=0)
        pares.append((n, bruto.convert("RGB"), final))
        print("ok ", n)
    t = 560
    folha = Image.new("RGB", (t * 2 + 10, len(pares) * (t + 26)), "white")
    d = ImageDraw.Draw(folha)
    for i, (n, b, f) in enumerate(pares):
        y = i * (t + 26)
        folha.paste(b.resize((t, t), Image.LANCZOS), (0, y))
        folha.paste(f.resize((t, t), Image.LANCZOS), (t + 10, y))
        d.text((6, y + t + 6), n, fill="black")
    folha.save(os.path.join(SAIDA, "_antes_depois.jpg"), quality=88)


if __name__ == "__main__":
    main()
