"""
Gera Cardapio_Artes_da_Pizza.xlsx a partir dos dados extraídos do portal iFood.

Estrutura:
- Dados: tabela normalizada (uma linha por Sabor x Tamanho x Plataforma)
- Comparativo: pivot lado-a-lado dos 3 canais com diferenças
- Margens: taxa de iFood/Keeta editável + cálculo de líquido
- Resumo: estatísticas por categoria
- Promoções: placeholder
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule
from openpyxl.worksheet.table import Table, TableStyleInfo

# ---------- Dados extraídos do iFood ----------
# (sabor, preco_brotinho_ifood)
CABE = [
    ("Atum especial com mussarela", 88.90),
    ("Atum ralado com mussarela",   72.90),
    ("Pizza Atum",                   58.90),
    ("Pizza Lombo",                  58.90),
    ("Pizza Mussarela",              58.90),
]

IMPERDIVEIS = [
    ("Pizza Vegetariana",         75.90),
    ("Pizza Toscana",             65.90),
    ("Pizza Tomate Seco",         63.90),
    ("Pizza Strogonoff",          96.90),
    ("Pizza Siciliana",           72.90),
    ("Pizza Rúcula",              80.90),
    ("Pizza Romana",              84.90),
    ("Pizza Primeira Classe",     64.90),
    ("Pizza Portuguesa 2",        79.90),
    ("Pizza Portuguesa",          63.90),
    ("Pizza Peruana",             83.90),
    ("Pizza Pepperoni",           62.90),
    ("Pizza Palmito",             78.90),
    ("Pizza Napolitana",          61.90),
    ("Pizza Mussarela",           58.90),
    ("Pizza Mista",               61.90),
    ("Pizza Milho",               62.90),
    ("Pizza Marguerita Especial", 84.90),
    ("Pizza Marguerita",          63.90),
    ("Pizza Lombo 2",             70.90),
    ("Pizza Lombo",               58.90),
    ("Pizza Light",               83.90),
    ("Pizza Jardineira",          63.90),
    ("Pizza Frango Especial",     68.90),
    ("Pizza Frango Catupiry",     66.90),
    ("Pizza Filé Mignon",         97.90),
    ("Pizza Favorita",            59.90),
    ("Pizza Executiva",           59.90),
    ("Pizza Especial",            83.90),
    ("Pizza Espanhola",           83.90),
    ("Pizza Escarola Especial",   63.90),
    ("Pizza Escarola",            55.90),
    ("Pizza Do Pizzaiolo",        64.90),
    ("Pizza Classic",             68.90),
    ("Pizza Classe Especial",     57.90),
    ("Pizza Catupiry",            57.90),
    ("Pizza Carne Seca",          83.90),
    ("Pizza Caprichosa",          69.90),
    ("Pizza Camarão",             95.90),
    ("Pizza Calacatu",            65.90),
    ("Pizza Calabresa",           58.90),
    ("Pizza Caipira",             65.90),
    ("Pizza Búfala",              62.90),
    ("Pizza Brócolis 3",          65.90),
    ("Pizza Brócolis 2",          65.90),
    ("Pizza Brócolis",            58.90),
    ("Pizza Berinjela",           58.90),
    ("Pizza Baiana",              58.90),
    ("Pizza Bacon",               59.90),
    ("Atum Especial",             76.90),
    ("Pizza Artes Da Pizza",      64.90),
    ("Pizza Atum",                52.90),
    ("Pizza Americana",           64.90),
    ("Pizza Aliche Importado",    82.90),
    ("Pizza Alho Poró",           63.90),
    ("Pizza Alho",                63.90),
    ("Pizza Alcachofra Especial", 81.90),
    ("Pizza Alcachofra",          69.90),
    ("Pizza Aladinele",           69.90),
    ("Pizza Abobrinha",           59.90),
    ("Pizza À Moda Da Casa",      84.90),
    ("Pizza 5 Queijos",           83.90),
    ("Pizza 4 Queijos",           76.90),
    ("Pizza 2 Queijos",           68.90),
]

DOCES = [
    ("Chocolate com morango",  65.90),
    ("Pizza Romeu E Julieta",  59.90),
    ("Pizza Brigadeiro",       43.90),
    ("Pizza Banana",           43.90),
]

# Sobremesa não tem brotinho/grande — tamanho único
SOBREMESA = [
    ("Torta Holandesa", 14.90),
]

CATEGORIAS = [
    ("Cabe no seu bolso!!!", CABE),
    ("Imperdíveis Pizzas salgadas", IMPERDIVEIS),
    ("As Queridinhas Pizzas Doces", DOCES),
]

# ---------- Estilos ----------
HEADER_FONT = Font(bold=True, color="FFFFFF", size=11)
HEADER_FILL = PatternFill("solid", fgColor="EA1D2C")  # vermelho iFood
SECTION_FONT = Font(bold=True, size=12, color="333333")
SECTION_FILL = PatternFill("solid", fgColor="F5F5F5")
CENTER = Alignment(horizontal="center", vertical="center")
LEFT = Alignment(horizontal="left", vertical="center")
THIN = Side(style="thin", color="DDDDDD")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
BRL = 'R$ #,##0.00;[Red]-R$ #,##0.00'
PCT = '0.0%;[Red]-0.0%'


def style_header(ws, row, cols):
    for col in range(1, cols + 1):
        cell = ws.cell(row=row, column=col)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = CENTER
        cell.border = BORDER


def auto_width(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


# ---------- Workbook ----------
wb = Workbook()

# =================================================================
# Aba 1: Dados (fonte normalizada)
# =================================================================
ws = wb.active
ws.title = "Dados"

headers = ["Categoria", "Sabor", "Tamanho", "Plataforma", "Preço"]
ws.append(headers)
style_header(ws, 1, len(headers))

PLATAFORMAS = ["iFood", "Loja (Retirada)", "Keeta"]

row = 2
# Pizzas: 2 tamanhos x 3 plataformas
for cat_name, items in CATEGORIAS:
    for sabor, preco_brotinho in items:
        for tam in ["Brotinho", "Grande"]:
            for plat in PLATAFORMAS:
                preco = preco_brotinho if (tam == "Brotinho" and plat == "iFood") else None
                ws.cell(row=row, column=1, value=cat_name)
                ws.cell(row=row, column=2, value=sabor)
                ws.cell(row=row, column=3, value=tam)
                ws.cell(row=row, column=4, value=plat)
                c5 = ws.cell(row=row, column=5, value=preco)
                c5.number_format = BRL
                row += 1

# Sobremesa: tamanho único
for sabor, preco in SOBREMESA:
    for plat in PLATAFORMAS:
        p = preco if plat == "iFood" else None
        ws.cell(row=row, column=1, value="Incrível Sobremesa")
        ws.cell(row=row, column=2, value=sabor)
        ws.cell(row=row, column=3, value="Único")
        ws.cell(row=row, column=4, value=plat)
        c5 = ws.cell(row=row, column=5, value=p)
        c5.number_format = BRL
        row += 1

LAST_DADOS = row - 1
auto_width(ws, [28, 34, 12, 18, 14])
ws.freeze_panes = "A2"

# Tornar tabela formal para fórmulas estruturadas
tab = Table(displayName="tDados", ref=f"A1:E{LAST_DADOS}")
tab.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showRowStripes=True)
ws.add_table(tab)

# =================================================================
# Aba 2: Comparativo (pivot por Sabor x Tamanho com 3 plataformas)
# =================================================================
ws = wb.create_sheet("Comparativo")

headers = [
    "Categoria", "Sabor", "Tamanho",
    "iFood", "Loja (Retirada)", "Keeta",
    "iFood vs Loja (R$)", "iFood vs Loja (%)",
    "Keeta vs Loja (R$)", "Keeta vs Loja (%)",
    "Maior canal", "Menor canal",
]
ws.append(headers)
style_header(ws, 1, len(headers))

row = 2
def write_row(cat, sabor, tam):
    global row
    ws.cell(row=row, column=1, value=cat)
    ws.cell(row=row, column=2, value=sabor)
    ws.cell(row=row, column=3, value=tam)
    # SUMIFS para puxar preço de cada plataforma
    base = (
        f'SUMIFS(Dados!$E:$E,'
        f'Dados!$B:$B,$B{row},'
        f'Dados!$C:$C,$C{row},'
        f'Dados!$D:$D,"{{plat}}")'
    )
    for col, plat in enumerate(["iFood", "Loja (Retirada)", "Keeta"], start=4):
        c = ws.cell(row=row, column=col, value=f"={base.replace('{plat}', plat)}")
        c.number_format = BRL
    # iFood vs Loja
    ws.cell(row=row, column=7, value=f'=IFERROR(IF(E{row}=0,"",D{row}-E{row}),"")').number_format = BRL
    ws.cell(row=row, column=8, value=f'=IFERROR(IF(E{row}=0,"",(D{row}-E{row})/E{row}),"")').number_format = PCT
    # Keeta vs Loja
    ws.cell(row=row, column=9, value=f'=IFERROR(IF(E{row}=0,"",F{row}-E{row}),"")').number_format = BRL
    ws.cell(row=row, column=10, value=f'=IFERROR(IF(E{row}=0,"",(F{row}-E{row})/E{row}),"")').number_format = PCT
    # Maior / Menor canal
    ws.cell(row=row, column=11, value=(
        f'=IFERROR(INDEX($D$1:$F$1,MATCH(MAX(D{row}:F{row}),D{row}:F{row},0)),"")'
    ))
    ws.cell(row=row, column=12, value=(
        f'=IFERROR(INDEX($D$1:$F$1,MATCH(MIN(IF(D{row}:F{row}>0,D{row}:F{row})),D{row}:F{row},0)),"")'
    ))
    row += 1

for cat_name, items in CATEGORIAS:
    for sabor, _ in items:
        for tam in ["Brotinho", "Grande"]:
            write_row(cat_name, sabor, tam)

for sabor, _ in SOBREMESA:
    write_row("Incrível Sobremesa", sabor, "Único")

LAST_COMP = row - 1
auto_width(ws, [28, 34, 11, 13, 16, 13, 16, 14, 16, 14, 16, 16])
ws.freeze_panes = "D2"

# Realçar maior diferença
ws.conditional_formatting.add(
    f"H2:H{LAST_COMP}",
    ColorScaleRule(start_type="min", start_color="63BE7B",
                   mid_type="percentile", mid_value=50, mid_color="FFEB84",
                   end_type="max", end_color="F8696B")
)

# =================================================================
# Aba 3: Margens (taxa por canal → líquido por preço)
# =================================================================
ws = wb.create_sheet("Margens")

ws["A1"] = "Configuração de taxas"
ws["A1"].font = SECTION_FONT
ws.merge_cells("A1:C1")

ws.append(["Canal", "Taxa (%)", "Repasse líquido por R$ 1"])
style_header(ws, 2, 3)

# Defaults conservadores; usuário ajusta
config_rows = [
    ("iFood", 0.23),
    ("Loja (Retirada)", 0.00),
    ("Keeta", 0.18),
]
for i, (plat, taxa) in enumerate(config_rows, start=3):
    ws.cell(row=i, column=1, value=plat)
    ws.cell(row=i, column=2, value=taxa).number_format = PCT
    ws.cell(row=i, column=3, value=f"=1-B{i}").number_format = BRL

ws["A7"] = "Líquido por sabor x tamanho"
ws["A7"].font = SECTION_FONT
ws.merge_cells("A7:I7")

headers = ["Categoria", "Sabor", "Tamanho",
           "Bruto iFood", "Bruto Loja", "Bruto Keeta",
           "Líquido iFood", "Líquido Loja", "Líquido Keeta"]
ws.append(headers)
style_header(ws, 8, len(headers))

row = 9
def write_margem(cat, sabor, tam):
    global row
    ws.cell(row=row, column=1, value=cat)
    ws.cell(row=row, column=2, value=sabor)
    ws.cell(row=row, column=3, value=tam)
    # puxa brutos do Comparativo
    for src_col, dst_col in [("D", 4), ("E", 5), ("F", 6)]:
        # linha no Comparativo = row na Margens - 7 (offset entre as duas tabelas)
        # mais simples: usar MATCH para encontrar pela combinação sabor+tamanho
        f = (
            f'=IFERROR(INDEX(Comparativo!{src_col}:{src_col},'
            f'MATCH(1,(Comparativo!$B:$B=$B{row})*(Comparativo!$C:$C=$C{row}),0)),"")'
        )
        c = ws.cell(row=row, column=dst_col, value=f)
        c.number_format = BRL
    # líquidos: bruto * (1 - taxa)
    ws.cell(row=row, column=7, value=f'=IFERROR(D{row}*$C$3,"")').number_format = BRL
    ws.cell(row=row, column=8, value=f'=IFERROR(E{row}*$C$4,"")').number_format = BRL
    ws.cell(row=row, column=9, value=f'=IFERROR(F{row}*$C$5,"")').number_format = BRL
    row += 1

for cat_name, items in CATEGORIAS:
    for sabor, _ in items:
        for tam in ["Brotinho", "Grande"]:
            write_margem(cat_name, sabor, tam)
for sabor, _ in SOBREMESA:
    write_margem("Incrível Sobremesa", sabor, "Único")

LAST_MARG = row - 1
auto_width(ws, [28, 34, 11, 14, 14, 14, 14, 14, 14])
ws.freeze_panes = "D9"

# Fórmulas matriciais (INDEX+MATCH com produto) precisam Ctrl+Shift+Enter no Excel legado;
# no Excel 365 funciona como dinâmico. Marcamos comentário pro usuário.
ws["K1"] = "Edite B3:B5 (taxas) para recalcular automaticamente todos os líquidos."
ws["K1"].font = Font(italic=True, color="666666")

# =================================================================
# Aba 4: Resumo por categoria
# =================================================================
ws = wb.create_sheet("Resumo")

ws["A1"] = "Resumo por categoria (preço iFood Brotinho)"
ws["A1"].font = SECTION_FONT
ws.merge_cells("A1:F1")

ws.append(["Categoria", "Nº sabores", "Preço médio", "Mais barato", "Mais caro", "Amplitude"])
style_header(ws, 2, 6)

cat_labels = [c[0] for c in CATEGORIAS] + ["Incrível Sobremesa"]
for i, cat in enumerate(cat_labels, start=3):
    ws.cell(row=i, column=1, value=cat)
    # Filtros: Tamanho = Brotinho (ou Único) e Plataforma = iFood
    tam_cond = "Único" if cat == "Incrível Sobremesa" else "Brotinho"
    base = f',Dados!$A:$A,A{i},Dados!$C:$C,"{tam_cond}",Dados!$D:$D,"iFood"'
    ws.cell(row=i, column=2, value=f'=COUNTIFS(Dados!$A:$A,A{i},Dados!$C:$C,"{tam_cond}",Dados!$D:$D,"iFood")')
    ws.cell(row=i, column=3, value=f'=IFERROR(AVERAGEIFS(Dados!$E:$E{base}),"")').number_format = BRL
    ws.cell(row=i, column=4, value=f'=IFERROR(MINIFS(Dados!$E:$E{base}),"")').number_format = BRL
    ws.cell(row=i, column=5, value=f'=IFERROR(MAXIFS(Dados!$E:$E{base}),"")').number_format = BRL
    ws.cell(row=i, column=6, value=f"=IFERROR(E{i}-D{i},\"\")").number_format = BRL

# Resumo geral
ws.cell(row=8, column=1, value="TOTAL GERAL").font = Font(bold=True)
ws.cell(row=8, column=2, value=f"=SUM(B3:B7)").font = Font(bold=True)
ws.cell(row=8, column=3, value=f'=IFERROR(AVERAGEIFS(Dados!$E:$E,Dados!$D:$D,"iFood",Dados!$C:$C,"Brotinho"),"")')
ws.cell(row=8, column=3).number_format = BRL
ws.cell(row=8, column=3).font = Font(bold=True)

auto_width(ws, [30, 12, 14, 14, 14, 14])

# Seção: comparação canais (preenche conforme usuário preencher Loja/Keeta)
ws["A10"] = "Comparação canais (média de todos os sabores)"
ws["A10"].font = SECTION_FONT
ws.merge_cells("A10:F10")
ws.append(["Plataforma", "Preço médio Brotinho", "Preço médio Grande"])
style_header(ws, 11, 3)
for i, plat in enumerate(PLATAFORMAS, start=12):
    ws.cell(row=i, column=1, value=plat)
    ws.cell(row=i, column=2, value=f'=IFERROR(AVERAGEIFS(Dados!$E:$E,Dados!$D:$D,A{i},Dados!$C:$C,"Brotinho"),"")').number_format = BRL
    ws.cell(row=i, column=3, value=f'=IFERROR(AVERAGEIFS(Dados!$E:$E,Dados!$D:$D,A{i},Dados!$C:$C,"Grande"),"")').number_format = BRL

# =================================================================
# Aba 5: Promoções (placeholder)
# =================================================================
ws = wb.create_sheet("Promoções")
ws["A1"] = "Promoções e campanhas"
ws["A1"].font = SECTION_FONT
ws.merge_cells("A1:G1")
ws.append(["Nome", "Canal", "Sabor / Categoria", "Tamanho", "Preço normal", "Preço promo", "Desconto"])
style_header(ws, 2, 7)
# linhas em branco com fórmula de desconto pronta
for r in range(3, 30):
    ws.cell(row=r, column=7, value=f'=IFERROR(IF(E{r}=0,"",1-F{r}/E{r}),"")').number_format = PCT
auto_width(ws, [22, 18, 30, 12, 14, 14, 12])
ws["I2"] = "Preencha as colunas A-F; desconto calculado automaticamente."
ws["I2"].font = Font(italic=True, color="666666")

# =================================================================
# Aba 6: Leia-me
# =================================================================
ws = wb.create_sheet("Leia-me", 0)  # primeira aba
ws["A1"] = "Cardápio Artes da Pizza — Comparativo Multi-Canal"
ws["A1"].font = Font(bold=True, size=16, color="EA1D2C")
ws["A2"] = "Fonte: extração do portal iFood Parceiro (2025-06)"
ws["A2"].font = Font(italic=True, color="666666")

guide = [
    "",
    "COMO USAR",
    "",
    "1. Aba Dados: fonte normalizada. Preencha as colunas em branco:",
    "   - Preço Brotinho/Grande nas plataformas Loja (Retirada) e Keeta",
    "   - Preço Grande no iFood (segundo tamanho de cada sabor)",
    "   - As demais abas atualizam automaticamente.",
    "",
    "2. Aba Comparativo: pivot lado-a-lado. Mostra diferenças R$/% iFood vs Loja",
    "   e Keeta vs Loja, além do canal mais caro/barato por sabor.",
    "",
    "3. Aba Margens: edite as taxas em B3:B5. O líquido é recalculado.",
    "   Default: iFood 23%, Loja 0%, Keeta 18% — ajuste conforme contrato.",
    "",
    "4. Aba Resumo: estatísticas por categoria e por canal.",
    "",
    "5. Aba Promoções: cadastre campanhas; desconto calculado sozinho.",
    "",
    "ESTADO ATUAL DOS DADOS",
    "",
    "- 73 sabores capturados via iFood",
    "- Preços Brotinho (iFood): 100% preenchidos",
    "- Preços Grande (iFood): NÃO capturados (a UI do portal bloqueou extração)",
    "- Preços Loja e Keeta: vazios (preencher manualmente)",
    "- Sobremesa (Torta Holandesa): tamanho único R$ 14,90",
]
for i, line in enumerate(guide, start=3):
    cell = ws.cell(row=i, column=1, value=line)
    if line and line.isupper():
        cell.font = Font(bold=True, size=12)
    elif line.startswith(("1.", "2.", "3.", "4.", "5.")):
        cell.font = Font(bold=True)

ws.column_dimensions["A"].width = 110

# Salvar
out = r"C:\Users\ux-de\Desktop\Renato ProductDesigner\Clientes\Artes da Pizza\Cardapio_Artes_da_Pizza.xlsx"
wb.save(out)
print(f"Gerado: {out}")
print(f"  Aba Dados: {LAST_DADOS - 1} linhas de dados")
print(f"  Aba Comparativo: {LAST_COMP - 1} sabores x tamanhos")
print(f"  Aba Margens: {LAST_MARG - 8} linhas")
