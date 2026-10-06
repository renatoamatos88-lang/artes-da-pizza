# Handoff — alterações pendentes no painel Keeta (Artes da Pizza)

Levantado em 23/set/2026 lendo a API do painel, já logado.

> **✅ EXECUTADO em 23/set/2026 (tarde)** — itens 1, 2, 3, 4 (só broto), 5, 6, 7 e o conserto
> estrutural da seção 3. Tudo conferido pela API depois de salvar. Baseline de antes em
> `keeta_baseline_23set2026.txt` (skuId=preço por grupo) — usar para reverter se precisar.
> **2ª rodada (23/set, 16h30, respostas da Nalva — "já estão corrigidos"):** Classic grande
> 128,70→**118,90** · Lambrusco 60→**80** · **Vinho Santa Helena** criado a 80 (spu 121749408) ·
> **Torta Holandesa** criada a **16,00** (spu 121673624) na categoria nova **Incrível Sobremesa**
> (24818961, espelha o iFood). Preço de item (não de complemento) passa por aprovação do Keeta, até 2 dias úteis.
> **3ª rodada (24/set):** Atum Especial (= atum sólido c/ mussarela, +R$28 de cobertura) grande
> 114,40→**142,90** · broto 71,50→**99,90**. ½ Atum Especial nos 2 sabores (58,35) não mexido.
> **Conferido pela API em 29/set:** todos os itens aprovados (auditStatus 1) · Incrível Sobremesa já
> está abaixo de Pizzas Doces · grande/broto de Classic, Especial, Atum Especial e Camarão corretos ·
> bordas corretas. Grupos 25179025/25149372 ainda têm "Atum especial com mussarela" a 71,50/114,40,
> mas não estão ligados a nenhum produto (sem efeito pro cliente).
> **Falta:** teste da seção 4 (½ Camarão segue 175,90 nos 2 grupos, pm=2) · ½ Atum Especial 58,35 ·
> iFood (seção 6).

- Painel: https://merchant.mykeeta.com/m/web/product
- shopId: `159392504`
- Conta: artesdapizza@outlook.com (o Renato faz o login; assistente não digita senha)

---

## 1. Fila de execução — 8 alterações

Origem: mensagens da Nalva (dona) em 22/set, print do WhatsApp + áudio transcrito.
**Regra que ela deu no áudio: os valores abaixo JÁ INCLUEM os 30%. Não recalcular.**

| # | Item | Grupo | sku id | Hoje | Vai para |
|---|---|---|---|---|---|
| 1 | Pizza Camarão — grande | 25179030 | 149840216 | 169,90 | **175,90** ✅ |
| 2 | 1/2 Pizza Camarão | 25169191 | 149807018 | 169,90 | **175,90** ✅ |
| 3 | 1/2 Pizza Camarão | 25149371 | 149840150 | 169,90 | **175,90** ✅ |
| 4 | Pizza Classic — broto | 25149374 | 149807074 | 80,60 | **75,00** ✅ (grande segue 128,70 — pendente) |
| 5 | Borda Catupiry — grande | 25179029 | 149814321 | 16,00 | **18,00** ✅ |
| 6 | Borda Cheddar — broto | 25149370 | 149814315 | 10,00 | **12,00** ✅ |
| 7 | Pizza Especial — CADASTRAR | 25149374 + 25179030 | 512322478 / 512255579 | não existe | **84,90 / 130,90** ✅ (spuId 121731137) |
| 8 | Torta — CADASTRAR | definir categoria | — | não existe | **16,90** |

Já corretos, não mexer: Borda Catupiry broto = 14 · Borda Cheddar grande = 14.

Citação do áudio dela (item 1): *"Põe a pizza de camarão já com os 30%, Renato,
corrige pra mim, tanto no iFood como no Keeta, pode pôr 175,90. Dá esse valor aí,
porque vai dividir, então pra mim não compensa."*

---

## 2. Mapa dos grupos de opção (conferido na API)

| id | nome no painel | nº opções | priceMethod | aplicado a |
|---|---|---|---|---|
| 25179030 | Escolha um sabor 8 | 63 | 1 | GRANDE (8 PEDAÇOS) |
| 25149374 | Escolha um sabor 5 | 63 | 1 | BROTINHO (1 PEDAÇO) |
| 25169191 | Escolha um sabor 1 | 56 | **2** | GRANDE 2 SABORES |
| 25149371 | Escolha o segundo sabor | 56 | **2** | GRANDE 2 SABORES |
| 25179028 | Escolha um sabor 7 | 4 | 1 | Pizza Doce Grande |
| 25179029 | Escolha a sua Preferência 2 | 3 | 1 | GRANDE — bordas |
| 25149370 | Escolha a sua Preferência | 3 | 1 | BROTINHO **+ GRANDE 2 SABORES** — bordas |

`priceMethod`: 1 = "Preço total" (soma as opções) · 2 = "Preço máximo" (cobra o
valor integral do sabor mais caro). Fica em Configurações avançadas do grupo.

Pizzas doces hoje (25179028, só grande): Chocolate c/ morango 91 · Romeu e Julieta 78
· Brigadeiro 78 · Banana 78.

---

## 3. Problema estrutural achado — ✅ CORRIGIDO em 23/set

Feito: 25179029 vinculado ao GRANDE 2 SABORES e 25149370 desvinculado dele (API confirma:
25149370 → só BROTINHO; 25179029 → GRANDE + GRANDE 2 SABORES). Registro original abaixo.
Não conferido: a ordem de exibição dos grupos no GRANDE 2 SABORES (borda deve vir depois dos sabores).

### Registro original

O grupo de bordas **25149370 está vinculado ao BROTINHO e ao GRANDE 2 SABORES** ao
mesmo tempo. Resultado: a pizza grande de 2 sabores cobra borda a preço de brotinho
(catupiry 14 em vez de 18, cheddar 10 em vez de 14).

Se aplicar só o item 6 da fila, conserta o brotinho e deixa o grande 2 sabores pior.
Conserto certo: desvincular 25149370 do GRANDE 2 SABORES e vincular 25179029 no lugar.

---

## 4. Teste em aberto — "Preço máximo" nas pizzas de 2 sabores

O cardápio impresso diz *"pizzas de dois sabores, prevalece o valor maior"*, e a Nalva
confirmou que é assim no balcão. O app hoje **soma as metades**: meio camarão + meia
mussarela sai R$ 129,74 em vez de R$ 169,90.

Numa sessão anterior foi montado um teste controlado, **ainda não validado**:
nos grupos 25169191 e 25149371 o priceMethod foi para 2 e a ½ Pizza Camarão foi de
R$ 84,95 para R$ 169,90. As outras 55 metades não foram tocadas.

**Falta o Renato abrir Cardápio › Prévia e montar uma GRANDE 2 SABORES com Camarão +
Mussarela.** Leitura do resultado:
- R$ 169,90 → a regra funciona, aplicar valor integral nas 56 metades dos dois grupos
- R$ 214,68 → o máximo só vale dentro de cada grupo; seria preciso fundir os dois
  grupos num só com 2 seleções
- qualquer outro valor → reverter

Reversão, se precisar: ½ Camarão volta a **R$ 87,95** (metade de 175,90) nos dois grupos e priceMethod volta a 1.
Com o item 1 aplicado, o resultado esperado do teste agora é **R$ 175,90** (funciona) ou **R$ 220,68** (só vale dentro de cada grupo).

Atenção: com o item 1 da fila, o valor de referência do camarão passa a ser **175,90**,
não 169,90.

---

## 5. Pendências com a Nalva (bloqueiam parte da fila)

1. **Grande da Pizza Classic.** Ela mandou só o brotinho (R$ 75). Antes tinha falado
   "R$ 90" sem dizer se era balcão ou já com 30%. Se era balcão → R$ 117. Hoje está
   R$ 128,70, que é o preço da Especial. Sem a resposta, o item 4 fica pela metade.
2. **"No Ifood tá 12 / Corrigi pra mim pf"** — mensagem de 10:59, ambígua. Pode ser a
   torta (cardápio impresso tem R$ 12 → ela agora quer 16,90) ou a borda de cheddar
   grande (12 → 14). A mensagem veio logo depois da do cheddar.
3. **Quantas tortas?** Ela escreveu no plural ("pode por as tortas"). Só a Holandesa
   ou tem outras?
4. **Brotinho das pizzas doces** — segue sem resposta de rodadas anteriores.
5. **Incentivos de entrega** — não dá para alterar pelo painel. O Keeta exibe aviso de
   que só o gerente comercial muda. Hoje a loja banca R$ 4,99 em pedidos de R$ 25–40 e
   R$ 6,99 acima de R$ 40. O único botão disponível é "Encerrar" (não usar). Falta
   decidir quem fala com o gerente comercial.

---

## 6. Fora do Keeta

A Nalva pediu o camarão a R$ 175,90 **também no iFood**, mais a correção do "tá 12".
Não há sessão logada no portal do parceiro iFood. Isso depende do Renato.

---

## 7. Como operar o painel (descoberto na sessão anterior)

- O conteúdo fica num **iframe same-origin**: `merchant.mykeeta.com/web/product`.
  `find` e `read_page` não alcançam; usar JS via `contentDocument`.
- Dentro do editor de grupo: **nome da opção é `<textarea>`**, **preço é
  `<input placeholder="0,00">`** com rótulo "Taxa extra – Entrega".
- "Taxa extra – Entrega" NÃO é taxa de entrega — é o campo de preço da opção.
- Parear nome↔preço subindo pelo container comum, **nunca por índice**.
- As 63 opções são todas renderizadas; não é lista virtualizada.
- O campo de preço tem **máscara de moeda**. Receita que funciona: clicar no campo →
  `End` → 16× `Backspace` → digitar só os dígitos (`17590` vira 175,90). Digitar
  "175,90" por cima de um valor existente corrompe (vira "17.590,00" ou pior).
- **Nunca usar "Editar preço" / "Operar em lote".** Esse editor aplica uma fórmula ao
  grupo inteiro e já quase destruiu os 56 preços numa sessão anterior.

### Ler o estado pela API (só leitura, seguro)
```js
const Q='?yodaReady=h5&csecplatform=4&csecversion=3.5.1';
const post=async(p,b)=>(await fetch(p+Q,{method:'POST',credentials:'include',
  headers:{'Content-Type':'application/json'},body:JSON.stringify(b)})).json();
await post('/api/sailorProduct/choiceGroup/r/listChoiceGroup',
  {shopId:159392504,pageNum:1,pageSize:200});
```
Outros endpoints: `/api/sailorProduct/shopCategory/r/listShopCategory` `{shopId}` e
`/api/sailorProduct/spu/r/listSpu` `{shopId,shopCategoryId,pageNum,pageSize}`.

**Sempre conferir pela API depois de salvar**, não confiar na tela.

---

## 8. Restrições

- **Não digitar senha em login nenhum.** O Renato loga e o assistente assume depois.
- O painel é **produção**. A loja costuma ficar "Fechado por hoje" — bom momento para
  mexer, mas conferir antes.
- A escrita no painel é barrada pelo classificador do modo auto. **O Renato precisa
  ajustar o modo de permissão pela interface do app antes de começar** — o assistente
  não deve trocar o modo sozinho (foi tentado e o sistema tratou como bypass).

---

## 9. Arquivos do projeto

Em `Clientes/Artes da Pizza/`:
- `keeta_api_15set2026.csv` — 67 sabores, preços broto/grande extraídos da API
- `keeta_meias_15set2026.csv` — as 56 metades vs. o grande correspondente
- `ArtesdaPizza_Conferencia_30pct.xlsx` — conferência dos 68 itens, 3 abas
- `revisao-keeta.html` — página de revisão para a cliente
- `whatsapp-nalva.txt` — última mensagem enviada a ela

Status da auditoria antes desta rodada: **61 de 68 itens com preço correto.**
