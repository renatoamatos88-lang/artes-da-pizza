"""
Padroniza as fotos das pizzas para iFood / Keeta — cenário "tábua de madeira".

Regra: a IA mexe no ENTORNO (caixa, bancada, luz, enquadramento), nunca na pizza.
O cliente tem que receber exatamente o que está na foto.

Uso:
    set GEMINI_API_KEY=...            (PowerShell: $env:GEMINI_API_KEY="...")
    python gerar_fotos.py             -> roda o TESTE (3 pizzas, uma por tábua)
    python gerar_fotos.py --todas     -> roda a pasta inteira, tábuas em rodízio
    python gerar_fotos.py --dry       -> só mostra o que faria, sem chamar a API
    python gerar_fotos.py --model gemini-2.5-flash-image

Saída: Imagem Pizzas/_tabua/<sabor>.jpg (1200x1200) + _comparativo.jpg (antes | depois)
"""

import argparse
import io
import os
import sys

from PIL import Image, ImageDraw

PASTA = "Imagem Pizzas"
SAIDA = os.path.join(PASTA, "_tabua")
LADO = 1200  # master quadrado

MODELOS = ["gemini-3.1-flash-image", "gemini-2.5-flash-image"]

# ---------- Variações de tábua (rodízio) ----------
# Ângulo, luz e enquadramento são FIXOS. Só a tábua e a superfície variam.
TABUAS = {
    "A": ("a round pinewood pizza board, light natural wood with visible grain and faint knife marks",
          "a dark matte slate stone table"),
    "B": ("a rectangular dark walnut wooden board with slightly worn edges",
          "a rustic dark grey concrete surface"),
    "C": ("a medium-toned oak pizza peel with a short handle pointing to the lower right corner",
          "a dark aged wooden table"),
}

# Teste: uma pizza por tábua
TESTE = [
    ("Brocolis 3.jpeg", "A"),
    ("Aliche.jpeg", "B"),
    ("Marguerita Especial.jpeg", "C"),
]

# Não mandar para a IA — foto precisa ser refeita (ver conversa de 24/set/2026)
REFAZER = {
    "Bacon.jpeg",
    "Mussarela.jpeg",
    "Calabresa.jpeg",
    "Calabresa Sadia, fatiada,pre  assada acebolada.jpeg",
}

PROMPT = """Edit this real photo of a pizza from a wood-fired pizzeria in Sao Paulo, for a food delivery app menu.

KEEP EXACTLY - do not redraw, beautify or "improve" the pizza itself:
every topping, its quantity, position and color; the number and placement of the black olives;
the cheese texture; the charred spots and the irregular shape of the crust; the slice cuts.
The customer must receive exactly what is shown. Do not add any ingredient, herb, garnish,
sauce drizzle, cheese pull or steam.

CHANGE:
- Remove the cardboard delivery box, the countertop, the oven and anything around the pizza,
  including any date/time stamp text in the corner.
- Place the pizza on {tabua}, seen from directly above (top-down, 90 degrees).
  Correct the perspective so the pizza is a round circle, not an oval.
- Background: {superficie}.
- Lighting: soft warm natural light from the upper left, like a window in the late afternoon;
  a gentle, realistic contact shadow under the board. Neutral white balance on the cheese
  (no red, orange or green cast).
- Framing: square 1:1, pizza centered, the whole pizza visible with a small margin,
  pizza fills about 80% of the frame width. Part of the board shows around it.

STYLE: a real photograph taken with a good phone camera - natural, appetizing, honest.
Not CGI, not an illustration, no glossy plastic look, no oversaturation, no heavy bokeh,
no text, no logo, no props other than the board."""


def carregar(nome):
    im = Image.open(os.path.join(PASTA, nome)).convert("RGB")
    im.thumbnail((1600, 1600))
    return im


def chamar(client, modelo, im, prompt):
    from google.genai import types

    resp = client.models.generate_content(
        model=modelo,
        contents=[prompt, im],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(aspect_ratio="1:1"),
        ),
    )
    for part in resp.parts or []:
        if part.inline_data and part.inline_data.data:
            return Image.open(io.BytesIO(part.inline_data.data)).convert("RGB")
    raise RuntimeError("a resposta veio sem imagem (pode ter sido bloqueada)")


def comparativo(pares, destino):
    t = 520
    folha = Image.new("RGB", (t * 2 + 10, len(pares) * (t + 34)), "white")
    dr = ImageDraw.Draw(folha)
    for i, (nome, antes, depois) in enumerate(pares):
        y = i * (t + 34)
        a = antes.copy(); a.thumbnail((t, t))
        folha.paste(a, ((t - a.width) // 2, y + (t - a.height) // 2))
        folha.paste(depois.resize((t, t), Image.LANCZOS), (t + 10, y))
        dr.text((6, y + t + 10), nome, fill="black")
    folha.save(destino, quality=88)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--todas", action="store_true")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--model", default=None)
    args = ap.parse_args()

    if args.todas:
        nomes = sorted(f for f in os.listdir(PASTA) if f.lower().endswith((".jpeg", ".jpg")))
        nomes = [n for n in nomes if n not in REFAZER]
        fila = [(n, "ABC"[i % 3]) for i, n in enumerate(nomes)]
    else:
        fila = TESTE

    os.makedirs(SAIDA, exist_ok=True)
    modelos = [args.model] if args.model else MODELOS

    if args.dry:
        for nome, v in fila:
            print(f"{v}  {nome}  ->  {TABUAS[v][0][:50]}...")
        print(f"\n{len(fila)} fotos, modelo(s): {modelos}")
        return

    if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
        sys.exit("Falta a chave: defina GEMINI_API_KEY (aistudio.google.com -> Get API key).")

    from google import genai
    client = genai.Client()

    pares = []
    for nome, v in fila:
        tabua, superficie = TABUAS[v]
        prompt = PROMPT.format(tabua=tabua, superficie=superficie)
        antes = carregar(nome)
        depois, erros = None, []
        for m in modelos:
            try:
                depois = chamar(client, m, antes, prompt)
                break
            except Exception as e:  # modelo inexistente, bloqueio, cota
                msg = str(e).split(".")[0]
                if "RESOURCE_EXHAUSTED" in msg:
                    msg += " (cota: modelo de imagem exige faturamento ativo no projeto)"
                erros.append(f"{m}: {msg}")
        if depois is None:
            print(f"FALHOU  {nome}\n        " + "\n        ".join(erros))
            continue
        depois = depois.resize((LADO, LADO), Image.LANCZOS)
        base = os.path.splitext(nome)[0]
        depois.save(os.path.join(SAIDA, f"{base}.jpg"), quality=92)
        pares.append((f"{nome}  [tábua {v}]", antes, depois))
        print(f"ok      {nome}  [tábua {v}]")

    if pares:
        comparativo(pares, os.path.join(SAIDA, "_comparativo.jpg"))
        print(f"\nComparativo: {os.path.join(SAIDA, '_comparativo.jpg')}")


if __name__ == "__main__":
    main()
