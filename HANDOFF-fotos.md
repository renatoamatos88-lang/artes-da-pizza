# Handoff — fotos das pizzas para iFood / Keeta

Sessão de 24–29/set/2026. Objetivo: padronizar as fotos das pizzas para subir no iFood e no Keeta.

## Decisões

- **A IA mexe no entorno, nunca na pizza.** Nada de gerar ou redesenhar cobertura: o cliente
  precisa receber o que vê na foto, senão chega reclamação no iFood.
- **Custo zero.** O Renato não quer pagar API. O Gemini (`gerar_fotos.py`) foi testado e todos
  os modelos de imagem exigem faturamento ativo (cota gratuita = 0). Caminho parado.
- **Cenário escolhido: tábua de madeira**, vista de cima, fundo escuro, luz quente vinda de cima à esquerda.

## O que existe

| Arquivo | O que faz |
|---|---|
| `compor_fotos.py` | Pipeline local e grátis (rembg + PIL). Recorta a pizza, tira a caixa pelo contorno oval, corrige perspectiva e cor |
| `compor_fotos.py --todas --fechado` | **Versão em uso.** Plano fechado: pizza redonda ocupando o quadro 1200×1200, cantos em pedra escura. Saída em `Imagem Pizzas/_fechado/` (+ `_prancha.jpg`) |
| `compor_fotos.py --todas` | Versão na tábua. **Não serve com as fotos atuais**: elas cortam a pizza na borda e aparece uma borda reta. Tábua é provisória (feita por código); usa `Imagem Pizzas/_fundos/tabua.jpg` se existir |
| `gerar_fotos.py` | Versão paga via Gemini. Parada |

Dependências: `pip install "rembg[cpu]" pillow numpy`. Na primeira execução o rembg baixa os modelos `isnet-general-use` e `u2net`.

## Status das 21 fotos

- **17 prontas em plano fechado** (`Imagem Pizzas/_fechado/`).
- **Retoque pendente:** Frango Especial (resto de caixa em cima à direita) e Alho-poró (embaixo à direita).
- **Destoam, sem borda visível** (a foto original cortava a pizza): Marguerita Especial, 2 Queijos, Rúcula.
- **Refazer a foto:** Bacon (figurinha de story, pizza minúscula), Mussarela (metade e borrada),
  Calabresa e Calabresa Sadia (parecem crua, antes do forno — confirmar com a Nalva).
- Faltam fotos: são 21 para ~63 sabores no cardápio.

## Próximos passos

1. Conferir no painel do iFood e do Keeta o tamanho mínimo de foto (usamos 1200×1200 sem verificar).
2. Mensagem para a Nalva com o guia de foto: mesma tábua, celular paralelo à mesa, pizza inteira
   com um dedo de sobra em volta, luz de janela, sem flash. Com isso, `compor_fotos.py --todas`
   monta a versão tábua sem inventar nada.
3. Pedir à Nalva uma foto de cima de uma tábua vazia → salvar em `Imagem Pizzas/_fundos/tabua.jpg`.

---

## Atualização 29/set — caminho DaVinci (retoque leve)

**Decisão final de estilo:** "retoque leve" (mantém caixa/luz de pizzaria de bairro; só enquadra, endireita
perspectiva e tira data) + cor quente + nitidez local. O cenário de tábua foi descartado: "muito falso".

**Pipeline atual (3 passos):**
1. `preparar_entrada.py` → recorta quadrado centrado na pizza em `Imagem Pizzas/_entrada/` (17 fotos prontas).
2. DaVinci (Nano Banana 2, 1:1, 0.5K → sai 512px), prompt "Light retouch…" (ver `PROMPT` no histórico do DaVinci
   ou no bloco abaixo). Baixar e salvar em `Imagem Pizzas/_davinci_bruto/<sabor>.png`.
3. `polir_fotos.py` → esquenta cor, luz, nitidez, 1200×1200 em `Imagem Pizzas/_final/`.

**Feitas (3/17):** Aliche, 2 queijos, 4 queijos → `_final/`.
**Bloqueio:** créditos da assinatura do DaVinci acabaram (pop-up "Garanta mais créditos"). Baixar não gasta crédito;
gerar sim. Restam 14 pizzas: Alcachofra especial, Alho poró, Alho, Brocolis 3, Caipira, Carne seca, Chocolate com
Morango, Escarola, Frango Especial, Lombo 2, Marguerita Especial, Napolitana, Rucula, Toscana.

**Lições de automação (DaVinci não tem lote):** uma imagem por geração; o upscale do DaVinci (2x, gasta crédito)
é dispensável — nitidez local resolve no tamanho do app. Digitar o prompt com `type` falha intermitente após upload;
funciona inserir via JS (`document.execCommand('insertText')` no `[role=textbox]`). Refs do file input mudam entre
páginas: sempre `read_page` antes do `file_upload`.

**Prompt usado:** "Light retouch of this real photo, not a re-creation. This is a pizza from an ordinary neighborhood
pizzeria in Sao Paulo, photographed with a regular phone. Keep the photo exactly as it is: the same pizza, same toppings
in the same positions, same olives, same crust and burnt spots, same ordinary lighting and colors, and keep whatever
the pizza sits on (cardboard box, tray or oven floor) as it is. Do not redraw, re-render, smooth or beautify the pizza;
keep natural imperfections, uneven cheese and slight oil shine. ONLY do this: crop to a square 1:1 so the whole pizza is
visible, centered and fills about 85% of the frame width (crop closer if the pizza is small in the frame), gently
straighten the perspective so the pizza looks less tilted, remove any date/time stamp text, and clean small dirt on the
box and countertop. No studio look, no dramatic shadows, no color boost, no gourmet styling, no wooden board, no new
props. It must look like a genuine snapshot taken by the pizzeria owner, just well framed."
