"""
Padroniza as fotos das pizzas para iFood / Keeta — cenário "tábua de madeira", 100% local e grátis.

Diferente do gerar_fotos.py (IA generativa, pago), aqui nenhum pixel da pizza é inventado:
1. recorta a pizza da foto original (rembg, roda na máquina)
2. limpa sobra de caixa pelo contorno oval da pizza
3. corrige a perspectiva (oval -> círculo) e dá um acerto leve de cor
4. monta sobre tábua + superfície escura, com sombra e luz quente vinda da esquerda

Tábua: se existir Imagem Pizzas/_fundos/tabua.jpg (foto de cima de uma tábua vazia,
tirada na pizzaria), ela é usada. Senão, gera uma tábua provisória por código.

Uso:
    python compor_fotos.py            -> teste (3 pizzas)
    python compor_fotos.py --todas    -> pasta inteira, menos as que precisam refazer
    python compor_fotos.py --todas --fechado -> plano fechado (serve com as fotos atuais)

Saída: Imagem Pizzas/_tabua/<sabor>.jpg (1200x1200) + _comparativo.jpg
"""

import argparse
import os

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

PASTA = "Imagem Pizzas"
SAIDA = os.path.join(PASTA, "_tabua")
TABUA_FOTO = os.path.join(PASTA, "_fundos", "tabua.jpg")

LADO = 1200          # master quadrado
D_TABUA = 1110       # diâmetro da tábua
D_PIZZA = 960        # diâmetro da pizza (~80% do quadro)
LUZ = (-0.45, -0.55)  # direção de onde vem a luz (canto superior esquerdo)

TESTE = ["Aliche.jpeg", "4 queijos.jpeg", "Chocolate com Morango.jpeg"]

# Não entram — foto precisa ser refeita, ou a pizza está cortada pela borda da foto
REFAZER = {
    "Bacon.jpeg", "Mussarela.jpeg", "Calabresa.jpeg",
    "Calabresa Sadia, fatiada,pre  assada acebolada.jpeg",
}

RNG = np.random.default_rng(7)


# ---------- recorte ----------

MODELOS_RECORTE = ["isnet-general-use", "u2net"]


def nota(mask, el):
    """Quanto a máscara parece uma pizza: IoU entre a máscara e o oval ajustado."""
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy, rx, ry = el
    oval = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1
    return (mask & oval).sum() / max(1, (mask | oval).sum())


def recortar(im, sessoes):
    """Roda os modelos de recorte e fica com o que deu a máscara mais "redonda".
    Se nenhum achou a pizza (ela ocupa a foto toda e o modelo pegou só as azeitonas),
    usa o oval inscrito na foto."""
    from rembg import remove
    melhor, melhor_nota = None, 0.0
    for s in sessoes:
        rgba = np.asarray(remove(im, session=s)).astype(np.float32)
        m = rgba[..., 3] > 100
        if m.mean() < 0.15:
            continue
        n = nota(m, elipse(m))
        if n > melhor_nota:
            melhor, melhor_nota = rgba, n
    if melhor is None:
        rgba = np.dstack([np.asarray(im).astype(np.float32), np.zeros(im.size[::-1], np.float32)])
        h, w = rgba.shape[:2]
        yy, xx = np.mgrid[0:h, 0:w]
        rgba[..., 3] = (((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2 <= 1) * 255
        melhor = rgba
    return melhor


def elipse(mask):
    """Oval da pizza: lança raios do centro, pega a borda em cada ângulo e ajusta
    1/r² = cos²/rx² + sin²/ry² descartando os raios que fogem (sobra de caixa)."""
    ys, xs = np.nonzero(mask)
    cx, cy = xs.mean(), ys.mean()
    h, w = mask.shape
    ang = np.radians(np.arange(0, 360, 2))
    passos = np.arange(0, max(h, w), 1.0)
    raios, validos = [], []
    for t in ang:
        px = (cx + np.cos(t) * passos).astype(int)
        py = (cy + np.sin(t) * passos).astype(int)
        na_foto = (px >= 0) & (px < w) & (py >= 0) & (py < h)
        px, py = px[na_foto], py[na_foto]
        fora = np.nonzero(~mask[py, px])[0]
        # raio que chega na borda da foto sem sair da pizza = pizza cortada ali; não conta
        validos.append(len(fora) > 0)
        raios.append(passos[fora[0]] if len(fora) else passos[len(px) - 1])
    raios, validos = np.array(raios), np.array(validos)
    ang, raios = ang[validos], raios[validos]
    # pontos da borda -> ajuste de elipse com centro livre: A x² + C y² + D x + E y = 1
    esc = max(h, w)  # normaliza para o ajuste não ficar mal-condicionado
    bx, by = (cx + np.cos(ang) * raios) / esc, (cy + np.sin(ang) * raios) / esc
    M = np.stack([bx ** 2, by ** 2, bx, by], 1)
    ok = np.ones(len(ang), bool)
    for _ in range(4):
        A, C, D, E = np.linalg.lstsq(M[ok], np.ones(ok.sum()), rcond=None)[0]
        ex, ey = -D / (2 * A), -E / (2 * C)
        k = 1 + D ** 2 / (4 * A) + E ** 2 / (4 * C)
        rx, ry = np.sqrt(k / A), np.sqrt(k / C)
        erro = np.abs(np.hypot((bx - ex) / rx, (by - ey) / ry) - 1)
        ok = erro < max(0.02, np.percentile(erro, 70))  # sobra de caixa fica de fora
    cx, cy, rx, ry = ex * esc, ey * esc, rx * esc, ry * esc
    # ajuste instável (pizza muito cortada pela foto): cai para a caixa da máscara
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    if not (x0 <= cx <= x1 and y0 <= cy <= y1 and 0.6 < rx / ry < 1.7
            and rx < w and ry < h and np.isfinite(rx + ry)):
        cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    return cx, cy, rx, ry


def limpar(rgba):
    """Tira sobra de caixa: tudo fora do oval da pizza (+1,5%) vai embora."""
    a = rgba[..., 3]
    h, w = a.shape
    yy, xx = np.mgrid[0:h, 0:w]
    el = elipse(a > 100)
    cx, cy, rx, ry = el
    d = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
    corte = np.clip((1.015 - d) / 0.01, 0, 1)
    # alpha firme: some o halo escuro da borda
    firme = np.clip((a - 70) / 110, 0, 1)
    rgba[..., 3] = firme * corte * 255
    return rgba, el


def cor(rgb, alpha):
    """Acerto leve de branco: os tons claros da pizza viram neutros-quentes (50% da força)."""
    px = rgb[alpha > 200]
    hi = np.percentile(px, 98, axis=0)
    alvo = np.array([250, 244, 232], np.float32)  # branco quente de queijo
    ganho = 1 + (alvo / hi - 1) * 0.5
    return np.clip(rgb * ganho, 0, 255)


def pizza_redonda(rgba, el):
    cx, cy, rx, ry = el
    box = (int(cx - rx * 1.04), int(cy - ry * 1.04), int(cx + rx * 1.04), int(cy + ry * 1.04))
    rgba[..., :3] = cor(rgba[..., :3], rgba[..., 3])
    im = Image.fromarray(rgba.clip(0, 255).astype(np.uint8), "RGBA").crop(box)
    im = im.resize((int(D_PIZZA * 1.04), int(D_PIZZA * 1.04)), Image.LANCZOS)  # oval -> círculo
    r, g, b, a = im.split()
    a = a.filter(ImageFilter.GaussianBlur(0.8))  # borda menos "recortada"
    rgb = ImageEnhance.Color(Image.merge("RGB", (r, g, b))).enhance(1.08)
    rgb = rgb.filter(ImageFilter.UnsharpMask(2, 50, 3))
    rgb.putalpha(a)
    return rgb


# ---------- cenário ----------

def ruido(h, w, cel_x, cel_y):
    """Ruído liso: sorteia uma grade grossa e amplia com bicúbica.
    cel_x != cel_y dá veio alongado."""
    gw, gh = max(2, w // cel_x), max(2, h // cel_y)
    n = RNG.standard_normal((gh, gw)).astype(np.float32)
    im = Image.fromarray(n, "F").resize((w, h), Image.BICUBIC)
    a = np.asarray(im)
    return (a - a.mean()) / (a.std() + 1e-6)


def superficie():
    """Pedra escura fosca: manchas largas bem suaves + grão fino."""
    base = np.array([46, 42, 38], np.float32)
    n = (ruido(LADO, LADO, 150, 150) * 4 + ruido(LADO, LADO, 12, 12) * 2
         + RNG.standard_normal((LADO, LADO)) * 2.5)
    return np.clip(base + n[..., None], 0, 255)


def madeira_procedural():
    """Tábua provisória — trocar por foto real em _fundos/tabua.jpg."""
    h = w = D_TABUA
    torcao = ruido(h, w, 220, 160) * 18                # ondula os anéis
    faixa = ruido(h, w, 400, 9)                        # faixas longas, largura variável
    yy = np.mgrid[0:h, 0:w][0].astype(np.float32)
    anel = np.sin((yy + torcao) / 11.0 + faixa * 1.4) * 0.5
    fibra = ruido(h, w, 90, 2) * 0.35 + RNG.standard_normal((h, w)) * 0.06
    t = np.clip(0.55 + (anel + fibra) * 0.22, 0, 1)[..., None]
    claro = np.array([200, 162, 112], np.float32)
    escuro = np.array([166, 124, 80], np.float32)
    rgb = escuro + (claro - escuro) * t
    # leve queda de luz no centro-borda e aro
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.hypot(xx - w / 2, yy - h / 2) / (w / 2)
    rgb *= (1 - 0.06 * r ** 2)[..., None]
    rgb *= (1 - np.clip((r - 0.975) / 0.025, 0, 1) * 0.22)[..., None]
    return rgb


def tabua():
    if os.path.exists(TABUA_FOTO):
        im = Image.open(TABUA_FOTO).convert("RGB")
        lado = min(im.size)
        im = im.crop(((im.width - lado) // 2, (im.height - lado) // 2,
                      (im.width + lado) // 2, (im.height + lado) // 2))
        return im.resize((D_TABUA, D_TABUA), Image.LANCZOS)
    rgb = madeira_procedural()
    return Image.fromarray(rgb.clip(0, 255).astype(np.uint8))


def circulo(d, blur=0):
    m = Image.new("L", (d, d), 0)
    ImageDraw.Draw(m).ellipse((0, 0, d - 1, d - 1), fill=255)
    return m.filter(ImageFilter.GaussianBlur(blur)) if blur else m


def sombra(canvas, d, centro, deslocamento, blur, opacidade):
    pad = blur * 3
    m = Image.new("L", (d + pad * 2, d + pad * 2), 0)
    ImageDraw.Draw(m).ellipse((pad, pad, pad + d, pad + d), fill=int(255 * opacidade))
    m = m.filter(ImageFilter.GaussianBlur(blur))
    x = int(centro - d / 2 - pad + deslocamento[0])
    y = int(centro - d / 2 - pad + deslocamento[1])
    preto = Image.new("RGBA", m.size, (12, 8, 5, 0))
    preto.putalpha(m)
    canvas.alpha_composite(preto, (x, y))


def luz(canvas):
    """Luz quente vindo de cima à esquerda + vinheta suave."""
    yy, xx = np.mgrid[0:LADO, 0:LADO].astype(np.float32)
    u = (xx / LADO - 0.5) * 2
    v = (yy / LADO - 0.5) * 2
    direcional = 1 + 0.10 * (u * LUZ[0] + v * LUZ[1])  # mais claro do lado da luz
    vinheta = 1 - 0.28 * np.clip(np.hypot(u, v) - 0.55, 0, None) ** 1.5
    ganho = (direcional * vinheta)[..., None] * np.array([1.03, 1.0, 0.95], np.float32)
    a = np.asarray(canvas.convert("RGB")).astype(np.float32) * ganho
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def compor(pizza):
    c = LADO / 2
    canvas = Image.fromarray(superficie().astype(np.uint8)).convert("RGBA")
    dx, dy = -LUZ[0], -LUZ[1]  # sombra cai do lado oposto à luz
    sombra(canvas, D_TABUA, c, (dx * 30, dy * 30), 28, 0.75)
    t = tabua().convert("RGBA")
    t.putalpha(circulo(D_TABUA, 1))
    canvas.alpha_composite(t, (int(c - D_TABUA / 2), int(c - D_TABUA / 2)))
    sombra(canvas, D_PIZZA - 30, c, (dx * 16, dy * 16), 16, 0.5)
    sombra(canvas, D_PIZZA - 40, c, (dx * 4, dy * 4), 5, 0.45)   # contato
    canvas.alpha_composite(pizza, (int(c - pizza.width / 2), int(c - pizza.height / 2)))
    return luz(canvas)


def fechado(rgba, el):
    """Plano fechado: pizza redonda ocupando o quadro todo, cantos em pedra escura.
    O quadrado fica sempre dentro da foto original, então a borda cortada da foto
    nunca aparece; caixa e data da câmera caem nos cantos e somem."""
    cx, cy, rx, ry = el
    rgba[..., :3] = cor(rgba[..., :3], rgba[..., 3])
    h, w = rgba.shape[:2]
    k = rx / ry                                    # oval -> círculo
    im = Image.fromarray(rgba.clip(0, 255).astype(np.uint8), "RGBA").resize((w, int(h * k)), Image.LANCZOS)
    cy *= k
    meio = min(rx * 1.03, cx, w - cx, cy, im.height - cy)
    im = im.crop((int(cx - meio), int(cy - meio), int(cx + meio), int(cy + meio))).resize((LADO, LADO), Image.LANCZOS)
    r, g, b, a = im.split()
    rgb = ImageEnhance.Color(Image.merge("RGB", (r, g, b))).enhance(1.08)
    rgb = rgb.filter(ImageFilter.UnsharpMask(2, 50, 3))
    # nada sai do círculo inscrito: sobra de caixa que o recorte deixou passar vai embora
    borda = np.asarray(circulo(LADO - 8, 2)).astype(np.float32) / 255
    borda = np.pad(borda, 4)
    a = Image.fromarray((np.asarray(a).astype(np.float32) * borda).astype(np.uint8))
    rgb.putalpha(a.filter(ImageFilter.GaussianBlur(0.8)))
    canvas = Image.fromarray(superficie().astype(np.uint8)).convert("RGBA")
    d = min(int(rx * LADO / meio), LADO - 8)                      # diâmetro da pizza no quadro
    sombra(canvas, d - 20, LADO / 2, (-LUZ[0] * 14, -LUZ[1] * 14), 16, 0.6)
    canvas.alpha_composite(rgb)
    return luz(canvas)


# ---------- saída ----------

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
    ap.add_argument("--fechado", action="store_true", help="plano fechado, sem tábua")
    args = ap.parse_args()
    saida = os.path.join(PASTA, "_fechado") if args.fechado else SAIDA

    if args.todas:
        fila = sorted(f for f in os.listdir(PASTA)
                      if f.lower().endswith((".jpeg", ".jpg")) and f not in REFAZER)
    else:
        fila = TESTE

    from rembg import new_session
    sessoes = [new_session(m) for m in MODELOS_RECORTE]
    os.makedirs(saida, exist_ok=True)

    pares = []
    for nome in fila:
        antes = Image.open(os.path.join(PASTA, nome)).convert("RGB")
        antes.thumbnail((1600, 1600))
        rgba, el = limpar(recortar(antes, sessoes))
        final = fechado(rgba, el) if args.fechado else compor(pizza_redonda(rgba, el))
        final.save(os.path.join(saida, os.path.splitext(nome)[0] + ".jpg"), quality=92)
        pares.append((nome, antes, final))
        print("ok ", nome)

    comparativo(pares, os.path.join(saida, "_comparativo.jpg"))
    print("\nComparativo:", os.path.join(saida, "_comparativo.jpg"))


if __name__ == "__main__":
    main()
