# Prompt padrão — fotos de pizza (Gemini, modo Imagens)

Uma foto por vez: anexar a foto de `Imagem Pizzas/_entrada/` + colar o prompt abaixo. Salvar o resultado em
`Imagem Pizzas/_gemini/<sabor>.jpg`.

## Regras acumuladas (o que o Renato foi apontando)

1. **Fiel à pizza real** — mesmos ingredientes, mesmas azeitonas (quantidade e lugar), mesma borda e pontos queimados.
   Não redesenhar, não embelezar, não inventar. O cliente tem que receber o que vê.
2. **Cara de pizzaria de bairro, não de revista.** Sem estúdio, sem estilo gourmet, sem tábua, sem adereço.
   (Tábua de madeira e o retoque do DaVinci foram reprovados: "muito falso".)
3. **Mantém a caixa de papelão** (limpa). É o que o cliente recebe.
4. **Chão / bancada / forno / azulejo do entorno: trocar por superfície lisa, neutra e limpa** (cinza-claro fosco).
   Sem granito, sem azulejo, sem mancha, sem sujeira. (O piso da 1ª tentativa "ficou péssimo".)
5. **Sem sombra de quem tira a foto** (nem do celular, nem da pessoa). Luz uniforme e suave; só uma sombra de contato
   discreta debaixo da caixa. (Sombra externa "como se a pessoa estivesse tirando a foto" foi reprovada.)
6. **Sem data/hora carimbada** da câmera.
7. **Vista de cima**, pizza inteira, centralizada, ~85% da largura, quadrado 1:1. Perspectiva endireitada.
8. **Cor natural e quente**, nítida. Sem realce exagerado de cor.

## Prompt (colar como está)

```
Light retouch of this real photo, not a re-creation. This is a pizza from an ordinary neighborhood pizzeria in Sao Paulo, photographed with a regular phone.

KEEP EXACTLY: the same pizza, same toppings in the same positions, same number and placement of olives, same crust and burnt spots, same cheese texture, and the same cardboard pizza box (cleaned). Do not redraw, re-render, smooth or beautify the pizza; keep its natural imperfections. Do not add or remove any ingredient.

CHANGE ONLY THIS:
- View it from directly above (top-down): straighten the perspective so the pizza looks like a round circle, centered, filling about 85% of the frame width, square 1:1.
- Replace the floor, countertop, oven, tiles and everything around the box with a clean, plain, neutral light-gray matte surface, with no tiles, no granite pattern, no stains and no dirt.
- Remove any date/time stamp text.
- Even, soft, natural lighting. NO cast shadows from outside the frame: no shadow of a person, phone or photographer, and no dramatic shadows. Only a very subtle soft contact shadow directly under the box.
- Natural warm colors and sharp detail; do not boost saturation.

DO NOT: studio look, gourmet styling, wooden board, props, text, logos, extra objects. It must look like a clean, honest photo taken by the pizzeria owner, just well framed. Output a square 1:1 image.
```
