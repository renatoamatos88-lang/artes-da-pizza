# Tabela Balcão x iFood x Keeta para a Nalva validar (24/set/2026)
# Balcão: cardápio impresso corrigido (artes_da_pizza_precos_corrigidos (2).pdf)
# Keeta: API do painel em 24/set/2026. iFood: balcão +30% (segundo a Nalva, não conferido no painel).
import unicodedata, re, html

BALCAO = """01|2 Queijos|82|51
02|4 Queijos|91|57
03|5 Queijos|99|62
04|À Moda da Casa|99|62
05|Abobrinha|75|46
06|Aladinele|85|53
07|Alcachofra|88|55
08|Alcachofra Especial|99|62
09|Alho|75|46
10|Alho Poró|75|46
11|Aliche Importado|95|61
12|Americana|91|57
13|Artes da Pizza|78|48
14|Atum|69|43
15|Atum Especial|88|55
16|Bacon|78|48
17|Baiana|72|45
18|Berinjela|72|45
19|Brócolis|72|45
20|Brócolis II|84|52
21|Brócolis III|84|52
22|Búfala|75|46
23|Caipira|83|52
24|Calabresa|69|43
25|Calacatú|83|52
26|Camarão|130|84
27|Caprichosa|89|55
28|Carne Seca|99|62
29|Catupiry|70|45
30|Classe Especial|70|45
31|Do Pizzaiolo|82|51
32|Escarola|70|45
33|Escarola Especial|82|51
34|Espanhola|99|62
35|Especial|99|62
36|Executiva|75|46
37|Favorita|75|46
38|Filé Mignon|130|84
39|Frango Catupiry|79|49
40|Frango Especial|85|53
41|Jardineira|75|46
42|Light|99|62
43|Lombo|69|43
44|Lombo II|84|52
45|Marguerita|75|46
46|Marguerita Especial|99|62
47|Milho|75|46
48|Mista|70|45
49|Mussarela|69|43
50|Napolitana|72|45
51|Palmito|94|60
52|Pepperone|84|52
53|Peruana|99|62
54|Portuguesa|75|46
55|Portuguesa II|95|61
56|Primeira Classe|75|46
57|Romana|105|65
58|Rúcula|95|61
59|Siciliana|84|52
60|Strogonoff|120|75
61|Tomate Seco|75|46
62|Toscana|80|49
63|Vegetariana|90|56
64|Banana|60|37
65|Brigadeiro|60|37
66|Romeu e Julieta|60|37
67|Chocolate com Morango|70|44"""

G = "Pizza Vegetariana=117;Pizza Toscana=104;Pizza Tomate Seco=97.5;Pizza Rúcula=123.5;Pizza Romana=136.5;Pizza Primeira Classe=97.5;Pizza Portuguesa 2=123.5;Pizza Portuguesa=97.5;Pizza Peruana=128.7;Pizza Pepperoni=109.2;Pizza Palmito=122.2;Pizza Napolitana=93.6;Pizza Mussarela=89.7;Pizza Mista=91;Pizza Milho=97.5;Pizza Marguerita Especial=128.7;Pizza Marguerita=97.5;Pizza Lombo 2=109.2;Pizza Lombo=89.7;Pizza Light=128.7;Pizza Jardineira=97.5;Pizza Filé Mignon=168.9;Pizza Favorita=97.5;Pizza Executiva=97.5;Pizza Espanhola=128.7;Pizza Escarola Especial=106.6;Pizza Escarola=91;Pizza Classic=118.9;Pizza Classe Especial=91;Pizza Catupiry=91;Pizza Carne Seca=128.7;Pizza Caprichosa=115.7;Pizza Camarão=175.9;Pizza Calacatu=107.9;Pizza Calabresa=89.7;Pizza Búfala=97.5;Pizza Brócolis 3=109.2;Pizza Brócolis 2=109.2;Pizza Brócolis=93.6;Pizza Berinjela=93.6;Pizza Baiana=93.6;Pizza Bacon=101.4;Atum Especial=142.9;Pizza Artes Da Pizza=101.4;Pizza Atum=89.7;Pizza Americana=118.3;Pizza Aliche Importado=123.5;Pizza Alho Poró=97.5;Pizza Alho=97.5;Pizza Alcachofra Especial=128.7;Pizza Alcachofra=114.4;Pizza Abobrinha=97.5;Pizza À Moda Da Casa=128.7;Pizza 5 Queijos=128.7;Pizza 4 Queijos=118.3;Pizza 2 Queijos=106.6;Pizza Aladinele=110.5;Pizza Caipira=107.9;Pizza Do Pizzaiolo=106.6;Pizza Frango Catupiry=102.7;Pizza Frango Especial=110.5;Pizza Siciliana=109.2;Pizza Strogonoff=156;Pizza Especial=130.9;Chocolate com morango=91;Pizza Romeu E Julieta=78;Pizza Brigadeiro=78;Pizza Banana=78"
B = "Pizza Vegetariana=72.8;Pizza Toscana=63.7;Pizza Tomate Seco=59.8;Pizza Rúcula=79.3;Pizza Romana=84.5;Pizza Primeira Classe=59.8;Pizza Portuguesa 2=79.3;Pizza Portuguesa=59.8;Pizza Peruana=80.6;Pizza Pepperoni=67.6;Pizza Palmito=78;Pizza Napolitana=58.5;Pizza Mussarela=55.9;Pizza Mista=58.5;Pizza Milho=59.8;Pizza Marguerita Especial=80.6;Pizza Marguerita=59.8;Pizza Lombo 2=67.6;Pizza Lombo=55.9;Pizza Light=80.6;Pizza Jardineira=59.8;Pizza Filé Mignon=109.2;Pizza Favorita=59.8;Pizza Executiva=59.8;Pizza Espanhola=80.6;Pizza Escarola Especial=66.3;Pizza Escarola=58.5;Pizza Classic=75;Pizza Classe Especial=58.5;Pizza Catupiry=58.5;Pizza Carne Seca=80.6;Pizza Caprichosa=71.5;Pizza Camarão=109.2;Pizza Calacatu=67.6;Pizza Calabresa=55.9;Pizza Búfala=59.8;Pizza Brócolis 3=67.6;Pizza Brócolis 2=67.6;Pizza Brócolis=58.5;Pizza Berinjela=58.5;Pizza Baiana=58.5;Pizza Bacon=62.4;Atum Especial=99.9;Pizza Artes Da Pizza=62.4;Pizza Atum=55.9;Pizza Americana=74.1;Pizza Aliche Importado=79.3;Pizza Alho Poró=59.8;Pizza Alho=59.8;Pizza Alcachofra Especial=80.6;Pizza Alcachofra=71.5;Pizza Abobrinha=59.8;Pizza À Moda Da Casa=80.6;Pizza 5 Queijos=80.6;Pizza 4 Queijos=74.1;Pizza 2 Queijos=66.3;Pizza Aladinele=68.9;Pizza Caipira=67.6;Pizza Do Pizzaiolo=66.3;Pizza Frango Catupiry=63.7;Pizza Frango Especial=68.9;Pizza Siciliana=67.6;Pizza Strogonoff=97.5;Pizza Especial=84.9"


def norm(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'^pizza\s+', '', s.strip())
    s = s.replace(' iii', ' 3').replace(' ii', ' 2').replace('pepperone', 'pepperoni')
    return re.sub(r'\s+', ' ', s)


def parse(x):
    return {norm(k): float(v) for k, v in (p.split('=') for p in x.split(';'))}


KG, KB = parse(G), parse(B)


def brl(v):
    return '—' if v is None else f"{v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


def r30(v):
    return round(v * 1.3 + 1e-9, 2)


# valores que a Nalva pediu fora da regra de +30%
OBS = {
    'camarao': 'Você pediu 175,90 na grande',
    'atum especial': 'Você pediu 142,90 / 99,90 (com mussarela, +28 de cobertura)',
    'especial': 'Você pediu 130,90 / 84,90',
}

rows, diverg = [], 0
for line in BALCAO.splitlines():
    n, nome, g, b = line.split('|')
    g, b = float(g), float(b)
    k = norm(nome)
    kg, kb = KG.get(k), KB.get(k)
    tg, tb = r30(g), r30(b)
    dg = kg is None or abs(kg - tg) > 0.005
    db = kb is None or abs(kb - tb) > 0.005
    diverg += dg + db
    obs = OBS.get(k, 'Keeta não tem brotinho de pizza doce' if int(n) >= 64 else '')
    rows.append((n, nome, g, tg, kg, dg, b, tb, kb, db, obs))


def cell(v, bad):
    cls = 'k bad' if bad else 'k'
    return f'<td class="{cls}">{brl(v) if v is not None else "não tem"}</td>'


def nome_td(nome, obs):
    extra = f'<small>{html.escape(obs)}</small>' if obs else ''
    return f'<td class="nome">{html.escape(nome)}{extra}</td>'


body, sec = [], None
for (n, nome, g, tg, kg, dg, b, tb, kb, db, obs) in rows:
    s = 'Pizzas doces' if int(n) >= 64 else 'Pizzas salgadas'
    if s != sec:
        body.append(f'<tr class="sec"><td colspan="8">{s}</td></tr>')
        sec = s
    body.append(f'<tr><td class="n">{n}</td>{nome_td(nome, obs)}'
                f'<td>{brl(g)}</td><td>{brl(tg)}</td>{cell(kg, dg)}'
                f'<td class="gap">{brl(b)}</td><td>{brl(tb)}</td>{cell(kb, db)}</tr>')

# Classic: existe no Keeta, não está no cardápio impresso
body.append(f'<tr><td class="n">—</td>{nome_td("Classic", "Não está no cardápio impresso. Qual o preço de balcão?")}'
            f'<td>—</td><td>—</td>{cell(KG["classic"], True)}'
            f'<td class="gap">—</td><td>—</td>{cell(KB["classic"], True)}</tr>')

outros = [
    ('Torta Holandesa', 12, 16.00, 'Você pediu 16'),
    ('Cobertura extra (catupiry ou mussarela)', 28, None, 'No Keeta não existe como opção separada'),
    ('Borda catupiry — grande', 14, 18.00, ''),
    ('Borda catupiry — brotinho', 14, 14.00, ''),
    ('Borda cheddar — grande', 10, 14.00, ''),
    ('Borda cheddar — brotinho', 10, 12.00, ''),
]
ob = []
for nome, bal, kee, obs in outros:
    t = r30(bal)
    bad = kee is None or abs(kee - t) > 0.005
    ob.append(f'<tr>{nome_td(nome, obs)}<td>{brl(bal)}</td><td>{brl(t)}</td>{cell(kee, bad)}</tr>')

CSS = """
@page { size: A4; margin: 12mm 10mm; }
:root { --vinho:#7a1214; --creme:#faf5dc; --tinta:#2a2320; --suave:#6b5f58; --linha:#e6dcc0; --alerta:#fff0a8; --alerta-borda:#d9b300; }
* { box-sizing:border-box; }
body { font-family: Arial, Helvetica, sans-serif; color:var(--tinta); margin:0; font-size:10.5px; background:#fff; }
header { border-bottom:3px solid var(--vinho); padding-bottom:8px; margin-bottom:10px; }
h1 { font-family: Georgia, serif; color:var(--vinho); font-size:20px; margin:0 0 4px; }
header p { margin:2px 0; color:var(--suave); font-size:11px; }
.legenda { margin-top:6px; font-size:10.5px; }
.sw { width:14px; height:10px; border:1px solid var(--alerta-borda); background:var(--alerta); display:inline-block; vertical-align:middle; margin-right:4px; }
table { width:100%; border-collapse:collapse; }
th, td { padding:3px 5px; border-bottom:1px solid var(--linha); text-align:right; white-space:nowrap; }
thead th { background:var(--vinho); color:#fff; font-weight:bold; font-size:10px; }
thead tr.top th { font-size:11px; text-align:center; }
td.n { color:var(--suave); text-align:left; width:22px; }
td.nome { text-align:left; white-space:normal; font-weight:bold; }
td.nome small { display:block; font-weight:normal; color:var(--vinho); font-size:9.5px; }
td.gap, th.gap { border-left:2px solid var(--vinho); }
td.k { font-weight:bold; }
td.bad { background:var(--alerta); outline:1px solid var(--alerta-borda); outline-offset:-1px; }
tr.sec td { background:var(--creme); color:var(--vinho); font-weight:bold; text-align:left; font-size:11px; }
h2 { font-family: Georgia, serif; color:var(--vinho); font-size:14px; margin:14px 0 6px; }
.outros { width:70%; }
.pede { margin-top:12px; padding:8px 10px; background:var(--creme); border-left:4px solid var(--vinho); font-size:11px; }
thead { display:table-header-group; } tr { page-break-inside:avoid; }
"""

page = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>Artes da Pizza — Balcão x iFood x Keeta</title><style>{CSS}</style></head><body>
<header>
<h1>Artes da Pizza — Balcão x iFood x Keeta</h1>
<p><b>Balcão</b>: cardápio impresso com os preços novos. <b>iFood</b>: balcão + 30%, como você aplicou. <b>Keeta</b>: o que está no app hoje (24/09).</p>
<p class="legenda"><i class="sw"></i>Keeta diferente de balcão + 30%</p>
</header>
<table>
<thead>
<tr class="top"><th colspan="2"></th><th colspan="3">GRANDE</th><th colspan="3" class="gap">BROTINHO</th></tr>
<tr><th style="text-align:left">Nº</th><th style="text-align:left">Sabor</th><th>Balcão</th><th>iFood</th><th>Keeta</th><th class="gap">Balcão</th><th>iFood</th><th>Keeta</th></tr>
</thead>
<tbody>{''.join(body)}</tbody></table>
<h2>Outros itens</h2>
<table class="outros"><thead><tr><th style="text-align:left">Item</th><th>Balcão</th><th>iFood</th><th>Keeta</th></tr></thead>
<tbody>{''.join(ob)}</tbody></table>
<div class="pede"><b>O que preciso de você:</b> confere a coluna <b>Balcão</b>. Onde estiver amarelo, me diz qual valor vale: o do Keeta ou o balcão + 30%.</div>
</body></html>"""

open('tabela-validacao-nalva.html', 'w', encoding='utf-8').write(page)
print('divergencias sabores:', diverg)
for r in rows:
    if r[5] or r[9]:
        print(r[0], r[1], '| G alvo', r[3], 'keeta', r[4], '| B alvo', r[7], 'keeta', r[8])
