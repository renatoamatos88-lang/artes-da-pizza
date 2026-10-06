# -*- coding: utf-8 -*-
"""
Gera ArtesdaPizza_Comparativo.xlsx com 4 abas:
1. Comparativo Geral
2. iFood (extraido)
3. Margem real por canal
4. Preço sugerido WhatsApp
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.utils import get_column_letter

# ============================================================
# DADOS — preços extraídos dos 22 screenshots do iFood
# Formato: nome_ifood -> (brotinho, grande)
# ============================================================
IFOOD = {
    # Salgadas
    "Pizza 2 Queijos": (68.90, 99.90),
    "Pizza 4 Queijos": (76.90, 110.90),
    "Pizza 5 Queijos": (83.90, 128.90),
    "Pizza À Moda Da Casa": (84.90, 128.90),
    "Pizza Abobrinha": (59.90, 93.90),
    "Pizza Aladinele": (69.90, 99.90),
    "Pizza Alcachofra": (69.90, 110.90),
    "Pizza Alcachofra Especial": (81.90, 125.90),
    "Pizza Alho": (63.90, 98.90),
    "Pizza Alho Poró": (63.90, 93.90),
    "Pizza Aliche Importado": (82.90, 125.90),
    "Pizza Americana": (64.90, 105.90),
    "Pizza Artes Da Pizza": (64.90, 102.90),
    "Pizza Atum": (52.90, 79.90),
    "Atum Especial": (76.90, 116.90),
    "Pizza Bacon": (59.90, 97.90),
    "Pizza Baiana": (58.90, 88.90),
    "Pizza Berinjela": (58.90, 88.90),
    "Pizza Brócolis": (58.90, 89.90),
    "Pizza Brócolis 2": (65.90, 99.90),
    "Pizza Brócolis 3": (65.90, 99.90),
    "Pizza Búfala": (62.90, 92.90),
    "Pizza Caipira": (65.90, 98.90),
    "Pizza Calabresa": (58.90, 88.90),
    "Pizza Calacatu": (65.90, 99.90),
    "Pizza Camarão": (95.90, 162.90),
    "Pizza Caprichosa": (69.90, 109.90),
    "Pizza Carne Seca": (83.90, 126.90),
    "Pizza Catupiry": (57.90, 87.90),
    "Pizza Classe Especial": (57.90, 89.90),
    "Pizza Do Pizzaiolo": (64.90, 96.90),
    "Pizza Escarola": (55.90, 85.90),
    "Pizza Escarola Especial": (63.90, 96.90),
    "Pizza Espanhola": (83.90, 128.90),
    "Pizza Especial": (83.90, 128.90),
    "Pizza Executiva": (59.90, 87.90),
    "Pizza Favorita": (59.90, 93.90),
    "Pizza Filé Mignon": (97.90, 161.90),
    "Pizza Frango Catupiry": (66.90, 98.90),
    "Pizza Frango Especial": (68.90, 102.90),
    "Pizza Jardineira": (63.90, 93.90),
    "Pizza Light": (83.90, 128.90),
    "Pizza Lombo": (58.90, 89.90),
    "Pizza Lombo 2": (70.90, 104.90),
    "Pizza Marguerita": (63.90, 97.90),
    "Pizza Marguerita Especial": (84.90, 129.90),
    "Pizza Milho": (62.90, 93.90),
    "Pizza Mista": (61.90, 89.90),
    "Pizza Mussarela": (58.90, 89.90),
    "Pizza Napolitana": (61.90, 93.90),
    "Pizza Palmito": (78.90, 128.90),
    "Pizza Pepperoni": (62.90, 103.90),
    "Pizza Peruana": (83.90, 123.90),
    "Pizza Portuguesa": (63.90, 94.90),
    "Pizza Portuguesa 2": (79.90, 122.90),
    "Pizza Primeira Classe": (64.90, 94.90),
    "Pizza Romana": (84.90, 129.90),
    "Pizza Rúcula": (80.90, 122.90),
    "Pizza Siciliana": (72.90, 108.90),
    "Pizza Strogonoff": (96.90, 148.90),
    "Pizza Tomate Seco": (63.90, 98.90),
    "Pizza Toscana": (65.90, 102.90),
    "Pizza Vegetariana": (75.90, 115.90),
    # Doces
    "Pizza Banana": (43.90, 69.90),
    "Pizza Brigadeiro": (43.90, 69.90),
    "Pizza Romeu E Julieta": (59.90, 89.90),
    "Chocolate com morango": (65.90, 89.90),
}

# ============================================================
# PREÇOS WHATSAPP — artes_da_pizza_precos_corrigidos.pdf (jun/2026)
# Formato: nº -> (brotinho, grande)
# ============================================================
WHATSAPP = {
    1: (51.00, 82.00),   2: (57.00, 91.00),   3: (62.00, 99.00),
    4: (62.00, 99.00),   5: (46.00, 75.00),   6: (53.00, 85.00),
    7: (55.00, 88.00),   8: (62.00, 99.00),   9: (46.00, 75.00),
    10: (46.00, 75.00),  11: (61.00, 95.00),  12: (57.00, 91.00),
    13: (48.00, 78.00),  14: (43.00, 69.00),  15: (55.00, 88.00),
    16: (48.00, 78.00),  17: (45.00, 72.00),  18: (45.00, 72.00),
    19: (45.00, 72.00),  20: (52.00, 84.00),  21: (52.00, 84.00),
    22: (46.00, 75.00),  23: (52.00, 83.00),  24: (43.00, 69.00),
    25: (52.00, 83.00),  26: (84.00, 130.00), 27: (55.00, 89.00),
    28: (62.00, 99.00),  29: (45.00, 70.00),  30: (45.00, 70.00),
    31: (51.00, 82.00),  32: (45.00, 70.00),  33: (52.00, 82.00),
    34: (62.00, 99.00),  35: (62.00, 99.00),  36: (46.00, 75.00),
    37: (46.00, 75.00),  38: (84.00, 130.00), 39: (49.00, 79.00),
    40: (53.00, 85.00),  41: (46.00, 75.00),  42: (62.00, 99.00),
    43: (43.00, 69.00),  44: (52.00, 84.00),  45: (46.00, 75.00),
    46: (62.00, 99.00),  47: (46.00, 75.00),  48: (45.00, 70.00),
    49: (43.00, 69.00),  50: (45.00, 72.00),  51: (60.00, 94.00),
    52: (52.00, 84.00),  53: (62.00, 99.00),  54: (46.00, 75.00),
    55: (61.00, 95.00),  56: (46.00, 75.00),  57: (65.00, 105.00),
    58: (61.00, 95.00),  59: (52.00, 84.00),  60: (75.00, 120.00),
    61: (46.00, 75.00),  62: (49.00, 80.00),  63: (56.00, 90.00),
    # Doces
    64: (37.00, 60.00),  65: (37.00, 60.00),  66: (37.00, 60.00),
    67: (44.00, 70.00),  68: (12.00, None),   # Torta Holandesa unidade
}

# Itens iFood SEM correspondência clara na tabela oficial
IFOOD_EXTRAS = {
    "Atum especial com mussarela": (88.90, 146.90),
    "Atum ralado com mussarela": (72.90, 120.90),
    "Pizza Atum (variante)": (58.90, 89.90),
    "Pizza Classic": (68.90, 99.90),
    "Torta Holandesa (unidade)": (14.90, None),
}

# Mapeamento № da tabela oficial -> nome iFood
MAP = {
    1: "Pizza 2 Queijos", 2: "Pizza 4 Queijos", 3: "Pizza 5 Queijos",
    4: "Pizza À Moda Da Casa", 5: "Pizza Abobrinha", 6: "Pizza Aladinele",
    7: "Pizza Alcachofra", 8: "Pizza Alcachofra Especial", 9: "Pizza Alho",
    10: "Pizza Alho Poró", 11: "Pizza Aliche Importado", 12: "Pizza Americana",
    13: "Pizza Artes Da Pizza", 14: "Pizza Atum", 15: "Atum Especial",
    16: "Pizza Bacon", 17: "Pizza Baiana", 18: "Pizza Berinjela",
    19: "Pizza Brócolis", 20: "Pizza Brócolis 2", 21: "Pizza Brócolis 3",
    22: "Pizza Búfala", 23: "Pizza Caipira", 24: "Pizza Calabresa",
    25: "Pizza Calacatu", 26: "Pizza Camarão", 27: "Pizza Caprichosa",
    28: "Pizza Carne Seca", 29: "Pizza Catupiry", 30: "Pizza Classe Especial",
    31: "Pizza Do Pizzaiolo", 32: "Pizza Escarola", 33: "Pizza Escarola Especial",
    34: "Pizza Espanhola", 35: "Pizza Especial", 36: "Pizza Executiva",
    37: "Pizza Favorita", 38: "Pizza Filé Mignon", 39: "Pizza Frango Catupiry",
    40: "Pizza Frango Especial", 41: "Pizza Jardineira", 42: "Pizza Light",
    43: "Pizza Lombo", 44: "Pizza Lombo 2", 45: "Pizza Marguerita",
    46: "Pizza Marguerita Especial", 47: "Pizza Milho", 48: "Pizza Mista",
    49: "Pizza Mussarela", 50: "Pizza Napolitana", 51: "Pizza Palmito",
    52: "Pizza Pepperoni", 53: "Pizza Peruana", 54: "Pizza Portuguesa",
    55: "Pizza Portuguesa 2", 56: "Pizza Primeira Classe", 57: "Pizza Romana",
    58: "Pizza Rúcula", 59: "Pizza Siciliana", 60: "Pizza Strogonoff",
    61: "Pizza Tomate Seco", 62: "Pizza Toscana", 63: "Pizza Vegetariana",
    64: "Pizza Banana", 65: "Pizza Brigadeiro", 66: "Pizza Romeu E Julieta",
    67: "Chocolate com morango", 68: None,  # Torta Holandesa = unidade, fora do esquema broto/grande
}

# ============================================================
# Ler tabela oficial (nomes e ingredientes)
# ============================================================
wb_src = load_workbook("ArtesdaPizza_tabelaPreço.xlsx", data_only=True)
ws_src = wb_src["Cardápio de Preços"]

pizzas = []  # lista de (num, nome, ingredientes, categoria)
categoria_atual = "Salgada"
for row in ws_src.iter_rows(min_row=6, values_only=True):
    num, nome, ingr = row[0], row[1], row[2]
    if num is None and nome is None:
        continue
    if isinstance(nome, str) and "DOCES" in nome.upper():
        categoria_atual = "Doce"
        continue
    if isinstance(nome, str) and "SALGADAS" in nome.upper():
        categoria_atual = "Salgada"
        continue
    if num and str(num).strip().isdigit():
        pizzas.append((int(num), nome, ingr or "", categoria_atual))

print(f"Pizzas lidas: {len(pizzas)}")

# ============================================================
# Estilos
# ============================================================
THIN = Side(border_style="thin", color="CCCCCC")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
HEADER_FILL = PatternFill("solid", fgColor="2E1A0F")  # marrom escuro pizza
HEADER_FONT = Font(bold=True, color="FFFFFF", size=10)
SUBHEADER_FILL = PatternFill("solid", fgColor="C0392B")
SUBHEADER_FONT = Font(bold=True, color="FFFFFF", size=10)
GROUP_FILL = PatternFill("solid", fgColor="F4D6B0")
GROUP_FONT = Font(bold=True, color="2E1A0F", size=11)
EDITABLE_FILL = PatternFill("solid", fgColor="FFF9C4")  # amarelo p/ campos editaveis
INFO_FILL = PatternFill("solid", fgColor="EAF4E6")
TITLE_FONT = Font(bold=True, size=14, color="2E1A0F")

def fmt_price(cell):
    cell.number_format = 'R$ #,##0.00'
    cell.alignment = Alignment(horizontal="right", vertical="center")
    cell.border = BORDER

def fmt_pct(cell):
    cell.number_format = '0.0%'
    cell.alignment = Alignment(horizontal="right", vertical="center")
    cell.border = BORDER

# ============================================================
# CRIAR WORKBOOK
# ============================================================
wb = Workbook()
wb.remove(wb.active)

# ------------------------------------------------------------
# ABA 1 — COMPARATIVO GERAL
# ------------------------------------------------------------
ws = wb.create_sheet("Comparativo Geral")
ws["A1"] = "ARTES DA PIZZA — Comparativo de Preços por Canal"
ws["A1"].font = TITLE_FONT
ws.merge_cells("A1:K1")

ws["A2"] = ("Compare o que o cliente paga em cada canal. As colunas Δ mostram quanto o iFood/Keeta cobram a MAIS "
            "que o WhatsApp (em %). Δ negativo = canal mais barato que o WhatsApp = atenção (você pode estar perdendo).")
ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
ws.merge_cells("A2:K2")
ws.row_dimensions[2].height = 32

# Cabeçalho de grupo (linha 4)
groups = [
    (4, "WhatsApp / Instagram", "4B6B3A"),
    (6, "iFood", "E11919"),
    (8, "Keeta", "FFB300"),
    (10, "Δ iFood vs WA", "888888"),
]
ws.cell(row=4, column=1, value="").fill = HEADER_FILL
ws.cell(row=4, column=2, value="").fill = HEADER_FILL
ws.cell(row=4, column=3, value="").fill = HEADER_FILL
for col, label, color in [(4, "WhatsApp / Instagram", "4B6B3A"),
                           (6, "iFood", "E11919"),
                           (8, "Keeta", "FFB300")]:
    c = ws.cell(row=4, column=col, value=label)
    c.fill = PatternFill("solid", fgColor=color)
    c.font = Font(bold=True, color="FFFFFF")
    c.alignment = Alignment(horizontal="center")
    ws.merge_cells(start_row=4, start_column=col, end_row=4, end_column=col+1)

c = ws.cell(row=4, column=10, value="Δ iFood vs WA")
c.fill = PatternFill("solid", fgColor="888888")
c.font = Font(bold=True, color="FFFFFF")
c.alignment = Alignment(horizontal="center")
ws.merge_cells("J4:K4")

# Linha 5 — headers de coluna
headers = ["Nº", "Pizza", "Ingredientes",
           "Broto", "Grande", "Broto", "Grande", "Broto", "Grande",
           "Broto", "Grande"]
for i, h in enumerate(headers, 1):
    c = ws.cell(row=5, column=i, value=h)
    c.fill = HEADER_FILL
    c.font = HEADER_FONT
    c.alignment = Alignment(horizontal="center", vertical="center")
    c.border = BORDER

# Linhas de pizza
row = 6
ws.cell(row=row, column=1, value="PIZZAS SALGADAS").fill = GROUP_FILL
ws.cell(row=row, column=1).font = GROUP_FONT
ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=11)
row += 1

doces_inserted = False
for num, nome, ingr, cat in pizzas:
    if cat == "Doce" and not doces_inserted:
        ws.cell(row=row, column=1, value="PIZZAS DOCES").fill = GROUP_FILL
        ws.cell(row=row, column=1).font = GROUP_FONT
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=11)
        row += 1
        doces_inserted = True

    ws.cell(row=row, column=1, value=num).alignment = Alignment(horizontal="center")
    ws.cell(row=row, column=2, value=nome).font = Font(bold=True)
    ws.cell(row=row, column=3, value=ingr).alignment = Alignment(wrap_text=True, vertical="center")

    # WhatsApp — preenchido com PDF
    wa_b, wa_g = WHATSAPP.get(num, (None, None))
    c = ws.cell(row=row, column=4, value=wa_b); fmt_price(c)
    c = ws.cell(row=row, column=5, value=wa_g); fmt_price(c)

    # iFood — preenchido com extração
    ifood_name = MAP.get(num)
    ifood_b, ifood_g = (None, None)
    if ifood_name and ifood_name in IFOOD:
        ifood_b, ifood_g = IFOOD[ifood_name]
    cb = ws.cell(row=row, column=6, value=ifood_b); fmt_price(cb)
    cg = ws.cell(row=row, column=7, value=ifood_g); fmt_price(cg)

    # Keeta = WhatsApp + 30%
    for keeta_col, wa_col in [(8, 4), (9, 5)]:
        formula = f"=IFERROR({get_column_letter(wa_col)}{row}*1.3,\"\")"
        c = ws.cell(row=row, column=keeta_col, value=formula)
        fmt_price(c)

    # Δ iFood vs WhatsApp = (iFood - WA) / WA
    for delta_col, ifood_col, wa_col in [(10, 6, 4), (11, 7, 5)]:
        formula = f"=IFERROR(({get_column_letter(ifood_col)}{row}-{get_column_letter(wa_col)}{row})/{get_column_letter(wa_col)}{row},\"\")"
        c = ws.cell(row=row, column=delta_col, value=formula)
        fmt_pct(c)

    row += 1

last_row = row - 1

# Conditional formatting nas colunas Δ (J e K)
red_fill = PatternFill("solid", fgColor="F8C8C8")
green_fill = PatternFill("solid", fgColor="C8E6C8")
ws.conditional_formatting.add(f"J7:K{last_row}",
    CellIsRule(operator='lessThan', formula=['0'], fill=red_fill))
ws.conditional_formatting.add(f"J7:K{last_row}",
    CellIsRule(operator='greaterThanOrEqual', formula=['0'], fill=green_fill))

# Larguras
widths = {"A": 5, "B": 24, "C": 50, "D": 11, "E": 11, "F": 11, "G": 11,
          "H": 11, "I": 11, "J": 12, "K": 12}
for col, w in widths.items():
    ws.column_dimensions[col].width = w
ws.freeze_panes = "D6"

# ------------------------------------------------------------
# ABA 2 — iFood (extraído)
# ------------------------------------------------------------
ws2 = wb.create_sheet("iFood (extraído)")
ws2["A1"] = "Preços extraídos do iFood — 11/06/2026"
ws2["A1"].font = TITLE_FONT
ws2.merge_cells("A1:D1")
ws2["A2"] = ("Trilha de auditoria. Cada linha é um item exatamente como aparece no cardápio do iFood. "
             "Itens em laranja são EXTRAS que não têm correspondência direta na tabela oficial — vale revisar se ainda fazem sentido.")
ws2["A2"].alignment = Alignment(wrap_text=True, vertical="top")
ws2.merge_cells("A2:D2")
ws2.row_dimensions[2].height = 32

for i, h in enumerate(["Nome no iFood", "Brotinho", "Grande", "Status"], 1):
    c = ws2.cell(row=4, column=i, value=h)
    c.fill = HEADER_FILL; c.font = HEADER_FONT
    c.alignment = Alignment(horizontal="center"); c.border = BORDER

r = 5
for nome, (b, g) in sorted(IFOOD.items()):
    ws2.cell(row=r, column=1, value=nome).border = BORDER
    cb = ws2.cell(row=r, column=2, value=b); fmt_price(cb)
    cg = ws2.cell(row=r, column=3, value=g); fmt_price(cg)
    ws2.cell(row=r, column=4, value="OK").alignment = Alignment(horizontal="center")
    ws2.cell(row=r, column=4).border = BORDER
    r += 1

orange = PatternFill("solid", fgColor="FFE0B2")
for nome, (b, g) in IFOOD_EXTRAS.items():
    ws2.cell(row=r, column=1, value=nome).fill = orange
    cb = ws2.cell(row=r, column=2, value=b); fmt_price(cb); cb.fill = orange
    if g is not None:
        cg = ws2.cell(row=r, column=3, value=g); fmt_price(cg); cg.fill = orange
    else:
        ws2.cell(row=r, column=3, value="—").alignment = Alignment(horizontal="center")
        ws2.cell(row=r, column=3).fill = orange
    s = ws2.cell(row=r, column=4, value="Sem correspondência")
    s.alignment = Alignment(horizontal="center"); s.fill = orange; s.border = BORDER
    r += 1

ws2.column_dimensions["A"].width = 36
ws2.column_dimensions["B"].width = 13
ws2.column_dimensions["C"].width = 13
ws2.column_dimensions["D"].width = 22
ws2.freeze_panes = "A5"

# ------------------------------------------------------------
# ABA 3 — Margem real por canal
# ------------------------------------------------------------
ws3 = wb.create_sheet("Margem real")
ws3["A1"] = "Margem real por canal — quanto entra no caixa depois da comissão"
ws3["A1"].font = TITLE_FONT
ws3.merge_cells("A1:H1")
ws3["A2"] = ("Calcula o valor LÍQUIDO que entra no caixa em cada canal, descontando a comissão da plataforma. "
             "Ajuste os % de comissão nas células amarelas — a planilha recalcula tudo.")
ws3["A2"].alignment = Alignment(wrap_text=True, vertical="top")
ws3.merge_cells("A2:H2")
ws3.row_dimensions[2].height = 32

# Parâmetros editáveis
ws3["A4"] = "Comissão iFood:"
ws3["A4"].font = Font(bold=True)
ws3["B4"] = 0.147  # 12% comissão + 3,1% taxa pagto online = 14,7% (confirmado no extrato iFood)
ws3["B4"].fill = EDITABLE_FILL
ws3["B4"].number_format = '0.0%'
ws3["B4"].border = BORDER

ws3["D4"] = "Comissão Keeta:"
ws3["D4"].font = Font(bold=True)
ws3["E4"] = 0.18
ws3["E4"].fill = EDITABLE_FILL
ws3["E4"].number_format = '0.0%'
ws3["E4"].border = BORDER

ws3["G4"] = "iFood: 12% comissão + 3,1% taxa pagto online = 14,7% (extrato real). Keeta: placeholder."
ws3["G4"].font = Font(italic=True, color="888888")

# Headers
ws3_headers = ["Nº", "Pizza", "iFood bruto G", "iFood líquido G",
               "Keeta bruto G", "Keeta líquido G", "WhatsApp G", "Melhor canal (líquido)"]
for i, h in enumerate(ws3_headers, 1):
    c = ws3.cell(row=6, column=i, value=h)
    c.fill = HEADER_FILL; c.font = HEADER_FONT
    c.alignment = Alignment(horizontal="center", vertical="center"); c.border = BORDER

# Linhas (espelhando "Comparativo Geral" — Grande apenas, para simplificar)
# Apontamos para a aba Comparativo Geral
r = 7
# Mapear cada pizza para sua linha em "Comparativo Geral"
comp_row = 7  # começa em 7 (linha 6 é "PIZZAS SALGADAS")
for num, nome, ingr, cat in pizzas:
    if cat == "Doce" and r == 7 + len([p for p in pizzas if p[3] == "Salgada"]):
        pass  # tratar abaixo
    ws3.cell(row=r, column=1, value=num).alignment = Alignment(horizontal="center")
    ws3.cell(row=r, column=2, value=nome).font = Font(bold=True)
    # iFood bruto G — referenciar Comparativo Geral, mas precisamos pular as linhas de grupo
    r += 1

# Re-fazer com cálculo correto das linhas no Comparativo Geral
ws3.delete_rows(7, r-7)

r = 7
comp_row = 7  # linha 6 = "PIZZAS SALGADAS"; linhas começam em 7
salg_count = sum(1 for p in pizzas if p[3] == "Salgada")
for idx, (num, nome, ingr, cat) in enumerate(pizzas):
    # Calcular linha no Comparativo Geral
    if cat == "Salgada":
        cg_row = 7 + idx
    else:
        cg_row = 7 + idx + 1  # +1 por causa da linha "PIZZAS DOCES"

    ws3.cell(row=r, column=1, value=num).alignment = Alignment(horizontal="center")
    ws3.cell(row=r, column=2, value=nome).font = Font(bold=True)

    # iFood bruto G = Comparativo Geral G{cg_row}
    cb = ws3.cell(row=r, column=3, value=f"='Comparativo Geral'!G{cg_row}"); fmt_price(cb)
    # iFood líquido = bruto * (1 - comissão)
    cl = ws3.cell(row=r, column=4, value=f"=IFERROR(C{r}*(1-$B$4),\"\")"); fmt_price(cl)
    cl.font = Font(bold=True, color="2E7D32")
    # Keeta bruto = Comparativo Geral I{cg_row}
    kb = ws3.cell(row=r, column=5, value=f"='Comparativo Geral'!I{cg_row}"); fmt_price(kb)
    # Keeta líquido
    kl = ws3.cell(row=r, column=6, value=f"=IFERROR(E{r}*(1-$E$4),\"\")"); fmt_price(kl)
    kl.font = Font(bold=True, color="2E7D32")
    # WhatsApp G = Comparativo Geral E{cg_row}
    wa = ws3.cell(row=r, column=7, value=f"='Comparativo Geral'!E{cg_row}"); fmt_price(wa)
    # Melhor canal (maior líquido entre iFood líquido, Keeta líquido e WhatsApp)
    melhor = (f'=IFERROR(IF(MAX(D{r},F{r},G{r})=G{r},"WhatsApp",'
              f'IF(MAX(D{r},F{r},G{r})=D{r},"iFood","Keeta")),"")')
    mc = ws3.cell(row=r, column=8, value=melhor)
    mc.alignment = Alignment(horizontal="center"); mc.border = BORDER
    mc.font = Font(bold=True)
    r += 1

ws3.column_dimensions["A"].width = 5
ws3.column_dimensions["B"].width = 24
for col in "CDEFG":
    ws3.column_dimensions[col].width = 15
ws3.column_dimensions["H"].width = 20
ws3.freeze_panes = "C7"

# ------------------------------------------------------------
# ABA 4 — Preço sugerido WhatsApp
# ------------------------------------------------------------
ws4 = wb.create_sheet("Preço sugerido WhatsApp")
ws4["A1"] = "Preço sugerido WhatsApp — ganhar X% a mais que o iFood líquido"
ws4["A1"].font = TITLE_FONT
ws4.merge_cells("A1:F1")
ws4["A2"] = ("Define um preço-alvo para o WhatsApp que supere o líquido do iFood em um % de margem desejado. "
             "Mexa na célula amarela B4 para mudar o objetivo de margem; tudo recalcula.")
ws4["A2"].alignment = Alignment(wrap_text=True, vertical="top")
ws4.merge_cells("A2:F2")
ws4.row_dimensions[2].height = 32

ws4["A4"] = "Margem-alvo sobre iFood líquido:"
ws4["A4"].font = Font(bold=True)
ws4["B4"] = 0.15
ws4["B4"].fill = EDITABLE_FILL
ws4["B4"].number_format = '0.0%'
ws4["B4"].border = BORDER
ws4["D4"] = "(ex: 15% = WhatsApp deve render 15% a mais que o iFood líquido)"
ws4["D4"].font = Font(italic=True, color="888888")
ws4.merge_cells("D4:F4")

headers4 = ["Nº", "Pizza", "iFood líquido Broto", "Sugerido WA Broto",
            "iFood líquido Grande", "Sugerido WA Grande"]
for i, h in enumerate(headers4, 1):
    c = ws4.cell(row=6, column=i, value=h)
    c.fill = HEADER_FILL; c.font = HEADER_FONT
    c.alignment = Alignment(horizontal="center", vertical="center"); c.border = BORDER

r = 7
for idx, (num, nome, ingr, cat) in enumerate(pizzas):
    if cat == "Salgada":
        cg_row = 7 + idx
    else:
        cg_row = 7 + idx + 1

    ws4.cell(row=r, column=1, value=num).alignment = Alignment(horizontal="center")
    ws4.cell(row=r, column=2, value=nome).font = Font(bold=True)

    # iFood líquido Broto = Comparativo Geral F{cg_row} * (1 - comissão iFood na aba Margem real)
    lb = ws4.cell(row=r, column=3,
                  value=f"=IFERROR('Comparativo Geral'!F{cg_row}*(1-'Margem real'!$B$4),\"\")")
    fmt_price(lb)
    # Sugerido WA Broto = liquido * (1 + margem alvo)
    sb = ws4.cell(row=r, column=4, value=f"=IFERROR(C{r}*(1+$B$4),\"\")")
    fmt_price(sb); sb.font = Font(bold=True, color="2E7D32"); sb.fill = PatternFill("solid", fgColor="E8F5E9")

    lg = ws4.cell(row=r, column=5,
                  value=f"=IFERROR('Comparativo Geral'!G{cg_row}*(1-'Margem real'!$B$4),\"\")")
    fmt_price(lg)
    sg = ws4.cell(row=r, column=6, value=f"=IFERROR(E{r}*(1+$B$4),\"\")")
    fmt_price(sg); sg.font = Font(bold=True, color="2E7D32"); sg.fill = PatternFill("solid", fgColor="E8F5E9")
    r += 1

ws4.column_dimensions["A"].width = 5
ws4.column_dimensions["B"].width = 24
for col in "CDEF":
    ws4.column_dimensions[col].width = 18
ws4.freeze_panes = "C7"

# ------------------------------------------------------------
# SALVAR
# ------------------------------------------------------------
out = "ArtesdaPizza_Comparativo.xlsx"
wb.save(out)
print(f"OK → {out}")
print(f"Pizzas mapeadas: {len(pizzas)}")
print(f"Pizzas com preço iFood: {sum(1 for n,_,_,_ in pizzas if MAP.get(n) in IFOOD)}")
print(f"iFood extras (sem match): {len(IFOOD_EXTRAS)}")
