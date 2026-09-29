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
