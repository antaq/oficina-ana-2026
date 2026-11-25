#!/usr/bin/env python3
"""Gera os slides do deck "Fiscalização Responsiva na ANTAQ".

2ª Oficina de Integração sobre Fiscalização do Uso de Recursos Hídricos (ANA, Brasília),
25/11/2026, 8h30 às 10h30. Público: fiscalizadores dos órgãos gestores estaduais e da ANA.

Mesmo template HTML do deck desempenho-aquaviario-2025 (ApresentacaoSFC), que por sua vez
segue apresentacao_sfc_diretoria, apresentacao_paf_diretoria e planejamento-inteligencia-2026.

  01 capa
  Origem    · 02 a teoria responsiva · 03 por que mudar · 04 seis anos de fiscalização responsiva
  IPR 2.0   · 05 o que a prática ensinou · 06 risco inerente como piso · 07 da faixa à solução fiscal
  PAF 2027  · 08 o que entra no plano · 09 sorteio auditável · 10 o plano é viável com a equipe atual?
              11 equalização · 12 o plano inteiro em horas
  Lições    · 13 governança · 14 desafios e alternativas
  15 encerramento

Fontes:
  - Nota Técnica nº 35/2026/GPF/SFC (SEI 3067498), processo 50300.021025/2024-16: universo,
    faixas, composição, sorteio, força de trabalho, equalização, calendário e governança do
    PAF 2027 (extração oficial, data de referência 30/09/2026).
  - Nota Técnica nº 36/2026/GPF/SFC (SEI 3067503): extraordinárias, operacionais, temáticas e
    rito próprio do PAF 2027.
  - Notas Técnicas nº 19 e 20/2026/GPF/SFC e especificação do IPR 2.0 (repositório IPR-PAF,
    docs/IPR_2_0_Especificacao_Tecnica.md): diagnóstico do IPR anterior (extração de abril/2026).
  - Pesos vigentes do IPR 2.0: tabela ipr.pesos_ipr (soma 21), lida em 24/11/2026.
  - Apresentações antigas da pasta FiscalizacaoResponsiva/ (2020 a 2022): modelo tradicional,
    números de 2014 a 2022, pirâmide de Ayres e Braithwaite, evolução do IPR.

ATENÇÃO: o PAF 2027 está em deliberação na Diretoria Colegiada (NT 35 assinada em 05/11/2026).
Os números do plano aparecem como proposta.

Todo o deck sai deste script, inclusive capa e encerramento. Para regerar: python3 build_slides.py
"""

import hashlib
import json
from pathlib import Path

DST = Path(__file__).resolve().parent
TOTAL = 15
RODAPE = "Fiscalização Responsiva na ANTAQ · 2ª Oficina de Integração · ANA, 25/11/2026 · SFC — ANTAQ"
TITULO_DECK = "Fiscalização Responsiva na ANTAQ"

def versiona(html):
    """Acrescenta ?v=<hash> aos scripts locais. O hash muda quando o arquivo muda, e o
    navegador (o Pages guarda cópia por 10 min) passa a buscar a versão nova."""
    for arq in ("zoom.js", "anim.js", "graficos.js"):
        h = hashlib.sha1((DST / arq).read_bytes()).hexdigest()[:8]
        html = html.replace(f'<script src="{arq}"></script>', f'<script src="{arq}?v={h}"></script>')
    return html


ECHARTS = '<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.1/dist/echarts.min.js"></script>'

BASE_CSS = """
:root { --grA:#15803D; --grB:#0066CC; --grC:#DC2626; }
body { margin:0; padding:0; overflow:hidden; font-family:'Open Sans',sans-serif; }
.slide { width:100vw; height:100vh; position:relative; display:flex; flex-direction:column; overflow:hidden; background:#ffffff; }
.font-montserrat { font-family:'Montserrat',sans-serif; }
.text-brand { color:#003366; } .bg-brand { background-color:#003366; }
.text-accent { color:#0066CC; } .bg-accent { background-color:#0066CC; }
.header-bar { height:10px; background:#003366; width:100%; }
.secondary-bar { height:4px; background:#0066CC; width:100%; }
.stat-card { background:linear-gradient(135deg,#003366,#004d99); border-radius:16px; padding:18px 16px; text-align:center; color:white; position:relative; overflow:hidden; }
.stat-num { font-family:'Montserrat',sans-serif; font-weight:900; font-size:calc(46px * var(--tz)); line-height:1; margin:0; }
.stat-num small { font-size:.5em; font-weight:700; color:#FFD700; }
.stat-lbl { font-size:calc(16px * var(--tz)); line-height:1.3; color:#BFD3E8; margin:6px 0 0; }
.card { display:flex; align-items:flex-start; gap:16px; padding:14px 20px; background:#F8FAFC; border-radius:14px; border-left:5px solid #0066CC; }
.card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); border-left-color:#22C55E; }
.card-amber { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); border-left-color:#F59E0B; }
.card-red   { background:linear-gradient(135deg,#FEF2F2,#FEE2E2); border-left-color:#EF4444; }
.card-gold  { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); border-left-color:#FFD700; }
.ico { width:50px; height:50px; border-radius:12px; flex-shrink:0; display:flex; align-items:center; justify-content:center; background:#DBEAFE; }
.ico i { color:#0066CC; font-size:calc(22px * var(--tz)); }
.card-amber .ico { background:#FDE68A; } .card-amber .ico i { color:#B45309; }
.card-green .ico { background:#BBF7D0; } .card-green .ico i { color:#15803D; }
.card-red .ico { background:#FECACA; } .card-red .ico i { color:#B91C1C; }
.ct { font-family:'Montserrat',sans-serif; font-weight:700; color:#003366; font-size:calc(21px * var(--tz)); line-height:1.25; margin:0; }
.cd { color:#475569; font-size:calc(17px * var(--tz)); line-height:1.45; margin:3px 0 0; }
.cd b, .cd strong { color:#003366; }
.pill { display:inline-block; padding:3px 12px; border-radius:999px; font-family:'Montserrat',sans-serif; font-weight:700; font-size:calc(14px * var(--tz)); letter-spacing:0.04em; }
.pill-a { background:#DCFCE7; color:#166534; } .pill-b { background:#DBEAFE; color:#1E40AF; }
.pill-c { background:#FEE2E2; color:#991B1B; } .pill-gold { background:#FEF3C7; color:#92400E; }
.destaque { background:linear-gradient(135deg,#003366,#0066CC); color:#fff; border-radius:16px; padding:18px 26px; }
.destaque p { margin:0; }
.destaque b { color:#FFD700; }
.legenda { color:#64748B; font-size:calc(14px * var(--tz)); line-height:1.5; margin:0; }
.sec { font-family:'Montserrat',sans-serif; font-weight:700; font-size:calc(15px * var(--tz)); letter-spacing:.12em; text-transform:uppercase; color:#64748B; margin:0; }
.hdr .text-5xl { font-size:46px; line-height:1; } .hdr .text-lg { font-size:19px; line-height:1.5; } .ftr .text-sm { font-size:14px; line-height:1.4; }
.gap-3 { row-gap:22px; } .gap-4 { row-gap:24px; } .gap-5 { row-gap:26px; } .gap-6 { row-gap:28px; }
.painel { background:#fff; border:1px solid #E2E8F0; border-radius:16px; padding:16px 22px 8px; box-shadow:0 1px 3px rgba(15,23,42,.05); }
.painel .ct { margin-bottom:2px; }
.graf { width:100%; }
.segbar { display:flex; gap:3px; height:46px; width:100%; }
.segbar .seg { border-radius:6px; display:flex; align-items:center; padding:0 14px; color:#fff; font-family:'Montserrat',sans-serif; font-weight:700; font-size:calc(18px * var(--tz)); white-space:nowrap; min-width:0; overflow:hidden; }
.sw { display:inline-block; width:14px; height:14px; border-radius:4px; vertical-align:-1px; margin-right:7px; }
.chaves { display:flex; flex-wrap:wrap; gap:6px 22px; color:#475569; font-family:'Montserrat',sans-serif; font-weight:600; font-size:calc(15px * var(--tz)); }
.num-r { font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(30px * var(--tz)); line-height:1; margin:0; }
.big { font-family:'Montserrat',sans-serif; font-weight:900; line-height:1; margin:0; }
"""

HEAD = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{title}</title>
<link rel="icon" type="image/png" href="favicon.png">
<link rel="icon" type="image/x-icon" href="favicon.ico">
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;900&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet"/>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet"/>
{head_extra}
<style>{css}</style>
</head>
<body>
<div class="slide">
  <div class="header-bar"></div>
  <div class="secondary-bar"></div>

  <div class="px-16 pt-6 pb-2 hdr">
    <div class="flex items-center gap-3">
      <div style="width:5px;height:44px;" class="bg-accent"></div>
      <div>
        <p class="font-montserrat font-bold text-gray-400 text-lg uppercase tracking-widest">{kicker}</p>
        <p class="text-5xl font-montserrat font-bold text-brand uppercase tracking-tight">{titulo}</p>
      </div>
      <div class="ml-auto flex items-center gap-3">
        <span class="font-montserrat font-bold text-accent uppercase tracking-widest" style="font-size:15px;"><i class="fas {tagico}"></i>&nbsp; {tag}</span>
        <img src="assets/logo-antaq-azul.png" alt="ANTAQ" style="height:32px;">
        <p class="font-montserrat font-bold text-gray-400 tracking-wider" style="font-size:12px; line-height:1.35;">SFC<br/>GPF</p>
      </div>
    </div>
  </div>

{body}

  <div class="px-16 pb-4 flex justify-between items-center border-t border-gray-100 pt-3 mx-8 ftr">
    <p class="text-gray-400 text-sm">{rodape}</p>
    <p class="text-gray-300 text-sm font-mono">{n} / {total}</p>
  </div>
</div>
<script src="zoom.js"></script>
<script src="anim.js"></script>
{js_extra}
<script>document.addEventListener("keydown",function(e){{if(["ArrowRight","ArrowLeft","PageDown","PageUp","Home","End"," ","f","F"].indexOf(e.key)!==-1){{e.preventDefault();window.parent.postMessage({{type:"slide-nav",key:e.key}},"*");}}}});</script>
</body>
</html>
"""

MODULOS = {
    1: ("Origem", "fa-seedling"),
    2: ("IPR 2.0", "fa-gauge-high"),
    3: ("PAF 2027", "fa-calendar-check"),
    4: ("Lições", "fa-lightbulb"),
}

SLIDES = []
BASES = {2: 1.3, 3: 1.25, 4: 1.35, 5: 1.2, 6: 1.2, 7: 1.15, 8: 1.25, 9: 1.15, 10: 1.2, 11: 1.15, 12: 1.35, 13: 1.35, 14: 1.35}


def slide(n, mod, title, kicker, titulo, body, extra_css="", base=1.0, head_extra="", js_extra=""):
    SLIDES.append(dict(n=n, mod=mod, title=title, kicker=kicker, titulo=titulo, body=body,
                       extra_css=extra_css, base=BASES.get(n, base), head_extra=head_extra, js_extra=js_extra))


def card(icon, titulo, texto, cls=""):
    return (f'<div class="card {cls}"><div class="ico"><i class="fas {icon}"></i></div>'
            f'<div><p class="ct">{titulo}</p><p class="cd">{texto}</p></div></div>')


def stat(num, rotulo):
    return f'<div class="stat-card"><p class="stat-num">{num}</p><p class="stat-lbl">{rotulo}</p></div>'


def br(v, d=0):
    """Número no padrão brasileiro: 1.234 ou 12,3."""
    s = f"{v:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def segbar(partes, altura=46):
    """Barra segmentada alta: partes = [(rótulo dentro, valor, cor)]. Larguras proporcionais."""
    tot = sum(v for _, v, _ in partes)
    segs = "".join(
        f'<div class="seg" style="width:{100 * v / tot:.2f}%; background:{c};" title="{r}">{r}</div>'
        for r, v, c in partes)
    return f'<div class="bar-row"><div class="bar-trk segbar" style="height:{altura}px;">{segs}</div></div>'


def chaves(itens):
    return '<div class="chaves">' + "".join(
        f'<span><span class="sw" style="background:{c};"></span>{t}</span>' for t, c in itens) + '</div>'


def graficos(js):
    return ECHARTS + '\n<script src="graficos.js"></script>\n<script>\n(function(){ var C = G.C;\n' + js + '\n})();\n</script>'


GA, GB, GC = "var(--grA)", "var(--grB)", "var(--grC)"


# ---------------------------------------------------------------------------
# 03 — Por que mudar
# ---------------------------------------------------------------------------
# Serviços regulados: apresentações de 2020 a 2022 (2014, 2016, 2019, 2022) e universo do
# ciclo PAF 2027 (NT 35, 2.467 outorgas em 30/09/2026). Servidores na fiscalização: 204 em
# 2016 e 164 em 2022 (apresentação ao Prêmio FGV, 2022). Fiscalizações: 1.120 em 2014 e
# 1.465 em 2019 (apresentações de 2020 e 2021).
REG = [("2014", 1272), ("2016", 1540), ("2019", 2080), ("2022", 2124), ("2026", 2467)]
js2 = f"""
var anos = {json.dumps([a for a, _ in REG])}, v = {[x for _, x in REG]};
G.desenha('g-reg', {{
  grid: {{ left: 20, right: 20, top: 40, bottom: 34 }},
  tooltip: G.dica({{ trigger: 'axis', axisPointer: {{ type: 'shadow', shadowStyle: {{ color: 'rgba(148,163,184,.14)' }} }},
    formatter: function (ps) {{ return '<b>' + ps[0].name + '</b><br/>' + G.num(ps[0].value) + ' serviços regulados'; }} }}),
  xAxis: G.eixoCat(anos),
  yAxis: G.eixoVal({{ show: false, max: 2700 }}),
  series: [{{ type: 'bar', data: v, barWidth: '52%',
    itemStyle: {{ color: function (p) {{ return p.dataIndex === v.length - 1 ? C.marca : C.porto; }}, borderRadius: [6, 6, 0, 0] }},
    label: {{ show: true, position: 'top', distance: 8, color: C.tinta, fontFamily: G.FT, fontWeight: 700, fontSize: 20,
      formatter: function (p) {{ return G.num(p.value); }} }} }}]
}});
"""
slide(3, 1, "Por que mudar", "O ponto de partida · 2017 a 2019", "Por que mudar", f"""
  <div class="flex-1 px-16 pb-4 grid grid-cols-12 gap-10 items-center min-h-0">
    <div class="col-span-5 flex flex-col gap-4">
      <p class="sec">O modelo tradicional · PPF 2017–2019</p>
      <div class="card" style="flex-direction:column; gap:10px;">
        <p class="ct">Um terço do universo por ano</p>
        <div class="grid grid-cols-3 gap-3 w-full">
          <div class="text-center" style="background:#DBEAFE; border-radius:10px; padding:10px 6px;"><p class="ct" style="font-size:calc(19px * var(--tz));">PAF 2017</p><p class="cd" style="margin:0;">1/3 do universo</p></div>
          <div class="text-center" style="background:#DBEAFE; border-radius:10px; padding:10px 6px;"><p class="ct" style="font-size:calc(19px * var(--tz));">PAF 2018</p><p class="cd" style="margin:0;">1/3 do universo</p></div>
          <div class="text-center" style="background:#DBEAFE; border-radius:10px; padding:10px 6px;"><p class="ct" style="font-size:calc(19px * var(--tz));">PAF 2019</p><p class="cd" style="margin:0;">1/3 do universo</p></div>
        </div>
        <p class="cd" style="margin:0;">mais as empresas autuadas e as novas outorgas. Todo regulado recebia a mesma ação, com lógica de <b>comando e controle</b>, herdada dos anos 1990.</p>
      </div>
      <div class="grid grid-cols-2 gap-4">
        {stat("−20%", "servidores na fiscalização<br/>204 em 2016 · 164 em 2022")}
        {stat("+31%", "fiscalizações por ano<br/>1.120 em 2014 · 1.465 em 2019")}
      </div>
      {card("fa-crosshairs", "A pergunta que faltava responder", "Quem, quando, onde e como fiscalizar, com a equipe que se tem, para chegar à <b>conformidade</b> e não apenas à autuação.", "card-gold")}
    </div>
    <div class="col-span-7 flex flex-col gap-4">
      <div class="painel">
        <p class="ct">Serviços regulados pela ANTAQ</p>
        <p class="cd" style="margin:0;">Portos, terminais, navegação marítima e navegação interior: quase o dobro em doze anos</p>
        <div id="g-reg" class="graf" style="height:470px;"></div>
      </div>
      <div class="destaque flex items-center gap-6">
        <p class="big" style="font-size:calc(64px * var(--tz)); color:#FFD700;">+94%</p>
        <p style="font-size:calc(19px * var(--tz)); color:#DBEAFE; line-height:1.45;">de regulados entre 2014 e 2026, com <b>menos</b> gente para fiscalizar. Repetir a mesma ação para todos deixou de ser viável.</p>
      </div>
      <p class="legenda">Fontes: apresentações da SFC de 2020 a 2022 (séries de 2014 a 2022); 2026: universo do ciclo PAF 2027, 2.467 outorgas em 30/09/2026 (Nota Técnica nº 35/2026/GPF/SFC).</p>
    </div>
  </div>""", js_extra=graficos(js2), base=1.05)


# ---------------------------------------------------------------------------
# 02 — A teoria responsiva
# ---------------------------------------------------------------------------
PIR_CSS = """
.pir { display:flex; flex-direction:column; align-items:center; gap:6px; }
.pir-n { display:flex; align-items:center; justify-content:center; color:#fff; border-radius:8px; height:118px; text-align:center; padding:0 18px; }
.pir-n p { margin:0; }
.pir-a { font-family:'Montserrat',sans-serif; font-weight:800; font-size:calc(21px * var(--tz)); line-height:1.15; }
.pir-c { font-size:calc(15px * var(--tz)); opacity:.9; line-height:1.25; margin-top:3px !important; }
.lado { display:flex; flex-direction:column; justify-content:space-around; height:100%; }
.lado p { margin:0; font-size:calc(16px * var(--tz)); color:#475569; line-height:1.3; }
.lado b { color:#003366; font-family:'Montserrat',sans-serif; }
"""
NIVEIS = [  # (largura %, cor, ação da fiscalização, comportamento do regulado)
    (40, "#991B1B", "Mão forte do regulador", "decididos a não cooperar"),
    (60, "#DC2626", "Medidas coercitivas", "não querem cooperar"),
    (80, "#0066CC", "Instruir e assistir", "tentam, mas nem sempre conseguem"),
    (100, "#15803D", "Simplificar e facilitar", "querem fazer a coisa certa"),
]
pir = "\n".join(
    f'<div class="pir-n" style="width:{w}%; background:{c};"><div><p class="pir-a">{a}</p><p class="pir-c">{b}</p></div></div>'
    for w, c, a, b in NIVEIS)
slide(2, 1, "A teoria responsiva", "Ayres e Braithwaite, 1992 · OCDE", "A teoria responsiva", f"""
  <div class="flex-1 px-16 pb-4 grid grid-cols-12 gap-10 items-center min-h-0">
    <div class="col-span-7 flex flex-col gap-4">
      <div class="flex items-end justify-between"><p class="sec">Pirâmide da fiscalização</p><p class="legenda">ação da fiscalização · <i>comportamento do regulado</i></p></div>
      <div class="painel" style="padding:22px 22px;">
        <div class="grid grid-cols-12 gap-4" style="align-items:stretch;">
          <div class="col-span-10 pir">{pir}</div>
          <div class="col-span-2 flex flex-col items-center justify-between" style="padding:6px 0;">
            <p class="sec" style="color:#991B1B; text-align:center;">Custo<br/>alto</p>
            <div style="flex:1; width:4px; margin:10px 0; background:linear-gradient(#991B1B,#15803D); border-radius:2px;"></div>
            <p class="sec" style="color:#15803D; text-align:center;">Custo<br/>baixo</p>
          </div>
        </div>
      </div>
      <p class="legenda">Adaptado de Ayres e Braithwaite (1992), <i>Responsive Regulation</i>, na versão apresentada no Congresso Brasileiro de Regulação da ABAR.</p>
    </div>
    <div class="col-span-5 flex flex-col gap-4">
      {card("fa-scale-balanced", "Resposta proporcional", "Infrações parecidas não recebem, necessariamente, o mesmo tratamento: a resposta depende do <b>histórico e da disposição</b> de quem regulamos.")}
      {card("fa-layer-group", "Esforço piramidal", "A base é larga e barata: orientar, simplificar, acompanhar. As sanções pesadas são raras, mas <b>precisam existir e ser usadas</b>, porque é o topo que faz a base funcionar.")}
      {card("fa-bullseye", "O objetivo é a conformidade", "A medida de sucesso é o regulado cumprindo a norma, não o número de autos lavrados.")}
      <div class="card card-gold" style="flex-direction:column; gap:8px;">
        <p class="ct">A prateleira de instrumentos da ANTAQ</p>
        <div class="flex flex-wrap gap-2">
          <span class="pill pill-gold">fiscalização educativa</span><span class="pill pill-gold">cartilhas</span><span class="pill pill-gold">plano de melhorias</span>
          <span class="pill pill-gold">presença do fiscal</span><span class="pill pill-gold">relatório individualizado</span><span class="pill pill-gold">ranking de risco</span>
          <span class="pill pill-gold">processo sancionador</span><span class="pill pill-gold">medida cautelar</span>
        </div>
      </div>
    </div>
  </div>""", extra_css=PIR_CSS, base=1.1)


# ---------------------------------------------------------------------------
# 04 — Seis anos de fiscalização responsiva
# ---------------------------------------------------------------------------
LT_CSS = """
.crono { position:relative; }
.crono .trilho { position:absolute; left:0; right:0; top:42px; height:4px; background:linear-gradient(90deg,#94A3B8,#0066CC 60%,#003366); border-radius:2px; }
.marco { position:relative; height:100%; display:flex; flex-direction:column; align-items:center; text-align:center; }
.marco .ano { font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(26px * var(--tz)); line-height:1; margin:0 0 10px; height:28px; }
.marco .bola { width:22px; height:22px; border-radius:50%; background:#fff; border:5px solid #0066CC; margin-bottom:16px; }
.marco.ouro .bola { border-color:#FFD700; background:#003366; }
.marco .cx { background:#F8FAFC; border-radius:14px; padding:14px 14px; border-top:4px solid #0066CC; width:100%; flex:1; }
.marco.ouro .cx { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); border-top-color:#FFD700; }
.marco.cinza .cx { border-top-color:#94A3B8; } .marco.cinza .bola { border-color:#94A3B8; }
.marco .cx p { margin:0; }
.marco .cx .ct { font-size:calc(19px * var(--tz)); margin-bottom:6px; }
.marco .cx .cd { font-size:calc(15.5px * var(--tz)); line-height:1.42; text-align:left; }
"""
MARCOS = [
    ("cinza", "2017", "Tradicional", "Um terço do universo por ano, mais autuadas e novas outorgas. Mesma ação para todos."),
    ("", "2020", "Primeira pirâmide", "Índice de Perfil ao Risco (<b>IPR</b>), grupos A, B e C, faixas A1 a C4 e soluções fiscais por faixa. Pesquisa com os servidores aponta o que melhorar."),
    ("", "2021", "Pesos por gravidade", "Todos os indicadores na mesma direção; reincidência e infração crítica pesam 3 vezes mais (Nota Técnica nº 9/2021)."),
    ("", "2022", "Faixas fixas", "Escala de 0 a 100, faixas fixas em vez de percentuais, indicador de <b>gravidade</b> e cálculo por outorga, não por CNPJ."),
    ("", "2025", "Modelo consolidado", "O Plano Plurianual de Fiscalização 2025–2028 adota a fiscalização responsiva como modelo da Agência."),
    ("ouro", "2026", "IPR 2.0 e PAF 2027", "Risco inerente como piso, cinco indicadores novos e um plano <b>medido em horas</b> contra a força de trabalho."),
]
marcos = "\n".join(
    f'<div class="marco {c}"><p class="ano">{a}</p><div class="bola"></div><div class="cx"><p class="ct">{t}</p><p class="cd">{d}</p></div></div>'
    for c, a, t, d in MARCOS)
slide(4, 1, "Seis anos de fiscalização responsiva", "Da primeira pirâmide ao IPR 2.0", "Uma trajetória de ajustes", f"""
  <div class="flex-1 px-16 pb-4 flex flex-col gap-6 min-h-0" style="justify-content:center;">
    <div class="crono">
      <div class="trilho"></div>
      <div class="grid grid-cols-6 gap-5" style="position:relative; align-items:stretch;">{marcos}</div>
    </div>
    <div class="grid grid-cols-3 gap-6">
      {card("fa-comments", "O que os fiscais disseram em 2020", "52 comentários na pesquisa de percepção. Os pontos mais citados: <b>classificar melhor o risco</b>, rever a frequência das fiscalizações e capacitar as equipes no modelo.", "card-amber")}
      {card("fa-shuffle", "O efeito pirâmide maia", "Com percentuais fixos por grupo, a melhora de um regulado empurrava outro para cima. As faixas fixas, de 2022, acabaram com isso.")}
      {card("fa-award", "Reconhecimento", "O modelo foi apresentado ao Prêmio FGV de Boas Práticas em Regulação em novembro de 2022.", "card-gold")}
    </div>
  </div>""", extra_css=LT_CSS, base=1.05)


# ---------------------------------------------------------------------------
# 05 — O que a prática ensinou
# ---------------------------------------------------------------------------
# Diagnóstico do IPR anterior, extração de abril/2026 (2.543 outorgas), NT 19/2026 e
# especificação do IPR 2.0, seção 3. Paradoxo da inspeção múltipla: IPR médio por número
# de fiscalizações nos 5 anos.
PARAD = [("1", 2.59), ("2–3", 5.86), ("4–7", 9.31), ("8–15", 9.78), ("16–30", 7.85), ("31+", 8.20)]
js5 = f"""
var cats = {json.dumps([c for c, _ in PARAD], ensure_ascii=False)}, v = {[x for _, x in PARAD]};
G.desenha('g-parad', {{
  grid: {{ left: 20, right: 20, top: 40, bottom: 60 }},
  tooltip: G.dica({{ trigger: 'axis', axisPointer: {{ type: 'shadow', shadowStyle: {{ color: 'rgba(148,163,184,.14)' }} }},
    formatter: function (ps) {{ return '<b>' + ps[0].name + ' fiscalizações</b><br/>IPR médio: ' + G.num(ps[0].value, 2); }} }}),
  xAxis: G.eixoCat(cats, {{ name: 'fiscalizações recebidas em 5 anos', nameLocation: 'middle', nameGap: 40,
    nameTextStyle: {{ color: C.apagado, fontFamily: G.FC, fontSize: 16 }} }}),
  yAxis: G.eixoVal({{ show: false, max: 11.5 }}),
  series: [{{ type: 'bar', data: v, barWidth: '54%', itemStyle: {{ color: '#D97706', borderRadius: [6, 6, 0, 0] }},
    label: {{ show: true, position: 'top', distance: 8, color: C.tinta, fontFamily: G.FT, fontWeight: 700, fontSize: 19,
      formatter: function (p) {{ return G.num(p.value, 1); }} }} }}]
}});
"""
slide(5, 2, "O que a prática ensinou", "Diagnóstico do IPR anterior · abril de 2026", "O que a prática ensinou", f"""
  <div class="flex-1 px-16 pb-4 grid grid-cols-12 gap-10 items-center min-h-0">
    <div class="col-span-6 flex flex-col gap-4">
      <p class="sec">Três defeitos estruturais</p>
      <div class="card card-red" style="align-items:center;">
        <p class="big" style="font-size:calc(52px * var(--tz)); color:#B91C1C; min-width:180px;">36,1%</p>
        <div><p class="ct">Invisibilidade</p><p class="cd">917 outorgas nunca fiscalizadas em 5 anos, e <b>99,6% delas classificadas como A1</b>, o menor risco. Sem dado, o modelo lia ausência como bom comportamento.</p></div>
      </div>
      <div class="card card-amber" style="align-items:center;">
        <p class="big" style="font-size:calc(52px * var(--tz)); color:#B45309; min-width:180px;">5 de 6</p>
        <div><p class="ct">Dependência de fiscalização prévia</p><p class="cd">Cinco dos seis indicadores só tinham valor para quem já tinha sido fiscalizado.</p></div>
      </div>
      <div class="card card-amber" style="align-items:center;">
        <p class="big" style="font-size:calc(52px * var(--tz)); color:#B45309; min-width:180px;">83,7%</p>
        <div><p class="ct">Distribuição colapsada</p><p class="cd">Quase tudo em A1; as faixas C3 e C4 ficaram <b>vazias</b>. Oito faixas, das quais só quatro ou cinco funcionavam.</p></div>
      </div>
      {card("fa-anchor", "Um exemplo: instalações portuárias com registro", "Atividade de risco inerente alto. Das 359 classificadas como A1, <b>303 nunca tinham sido fiscalizadas</b>.")}
    </div>
    <div class="col-span-6 flex flex-col gap-4">
      <div class="painel">
        <p class="ct">O paradoxo da fiscalização repetida</p>
        <p class="cd" style="margin:0;">IPR médio conforme o número de fiscalizações recebidas: quem é mais visto parece mais arriscado</p>
        <div id="g-parad" class="graf" style="height:440px;"></div>
      </div>
      <div class="destaque">
        <p style="font-size:calc(19px * var(--tz)); line-height:1.5;">Um modelo que só aprende com a fiscalização <b>não enxerga quem nunca foi fiscalizado</b>, e tende a mandar o fiscal sempre aos mesmos lugares.</p>
      </div>
      <p class="legenda">Fonte: diagnóstico do IPR anterior sobre a extração de abril de 2026 (2.543 outorgas), base das Notas Técnicas nº 19 e 20/2026/GPF/SFC.</p>
    </div>
  </div>""", js_extra=graficos(js5), base=1.05)


# ---------------------------------------------------------------------------
# 06 — IPR 2.0: risco inerente como piso
# ---------------------------------------------------------------------------
# Pesos vigentes (ipr.pesos_ipr, soma 21). "Novo" = indicador introduzido ou refeito no
# IPR 2.0, segundo a NT 35, § 2.2 (ICF, IVO, IOU consolidado, ICD, IMA).
PESOS = [
    ("ICF", "Cobertura: há quanto tempo não é fiscalizada", 3, True),
    ("IGI", "Gravidade das infrações", 3, False),
    ("IOC", "Ocorrência de infração crítica", 3, False),
    ("IRI", "Reincidência", 3, False),
    ("INN", "Notificações não atendidas", 2, False),
    ("IOU", "Manifestações na Ouvidoria", 2, True),
    ("IVO", "Volume operacional", 2, True),
    ("IIN", "Irregularidade normativa", 1, False),
    ("ICD", "Custo-distância: classe de acesso", 1, True),
    ("IMA", "Maturidade: idade e porte da empresa", 1, True),
]
assert sum(p for *_, p, _ in PESOS) == 21
js6 = f"""
var d = {json.dumps([[s, t, p, nv] for s, t, p, nv in PESOS], ensure_ascii=False)};
G.desenha('g-pesos', {{
  grid: {{ left: 470, right: 50, top: 10, bottom: 6 }},
  tooltip: G.dica({{ trigger: 'item', formatter: function (p) {{ var x = d[p.dataIndex];
    return '<b>' + x[0] + '</b> · ' + x[1] + '<br/>Peso ' + G.num(x[2]) + ' de 21' + (x[3] ? '<br/>Novo no IPR 2.0' : ''); }} }}),
  xAxis: G.eixoVal({{ show: false, max: 3.3 }}),
  yAxis: G.eixoCat(d.map(function (x) {{ return x[0] + '  ' + x[1]; }}), {{ inverse: true, axisLine: {{ show: false }},
    axisLabel: {{ color: C.tinta2, fontFamily: G.FT, fontSize: 16.5, fontWeight: 600, margin: 14,
      formatter: function (v) {{ var i = v.indexOf('  '); return '{{s|' + v.slice(0, i) + '}}  ' + v.slice(i + 2); }},
      rich: {{ s: {{ fontFamily: G.FT, fontWeight: 900, fontSize: 17, color: C.marca }} }} }} }}),
  series: [{{ type: 'bar', barWidth: 22, data: d.map(function (x) {{ return {{ value: x[2],
      itemStyle: {{ color: x[3] ? '#D97706' : C.porto, borderRadius: [0, 5, 5, 0] }} }}; }}),
    label: {{ show: true, position: 'right', distance: 8, color: C.tinta, fontFamily: G.FT, fontWeight: 700, fontSize: 18 }} }}]
}});
"""
FASE_CSS = """
.fase { border-radius:16px; padding:16px 20px; color:#fff; }
.fase p { margin:0; }
.fase .ft { font-family:'Montserrat',sans-serif; font-weight:800; font-size:calc(21px * var(--tz)); }
.fase .fd { font-size:calc(16px * var(--tz)); line-height:1.45; color:#E2E8F0; margin-top:4px !important; }
.dim { display:flex; justify-content:space-between; font-size:calc(15px * var(--tz)); color:#fff; background:rgba(255,255,255,.12); border-radius:8px; padding:5px 12px; }
.formula { background:#F8FAFC; border:2px dashed #0066CC; border-radius:16px; padding:16px 20px; text-align:center; }
.formula p { margin:0; }
"""
slide(6, 2, "IPR 2.0: risco inerente como piso", "Índice de Perfil ao Risco · Notas Técnicas nº 19 e 20/2026", "IPR 2.0: duas fases", f"""
  <div class="flex-1 px-16 pb-4 grid grid-cols-12 gap-10 items-center min-h-0">
    <div class="col-span-5 flex flex-col gap-4">
      <div class="fase" style="background:linear-gradient(135deg,#7C2D12,#B45309);">
        <p class="ft"><i class="fas fa-industry"></i>&nbsp; Fase 1 · Risco da atividade (IRA)</p>
        <p class="fd">Propriedade da modalidade, não da empresa. Uma travessia tem o mesmo risco inerente, seja quem for o operador. <b style="color:#FFD700;">Não depende de fiscalização.</b></p>
        <div class="grid grid-cols-2 gap-2" style="margin-top:10px;">
          <div class="dim"><span>Segurança</span><b>35%</b></div><div class="dim"><span>Econômica</span><b>25%</b></div>
          <div class="dim"><span>Ambiental</span><b>20%</b></div><div class="dim"><span>Usuário</span><b>20%</b></div>
        </div>
      </div>
      <div class="fase" style="background:linear-gradient(135deg,#003366,#0066CC);">
        <p class="ft"><i class="fas fa-chart-column"></i>&nbsp; Fase 2 · Comportamento (IPR base)</p>
        <p class="fd">Dez indicadores ponderados, pesos somando 21. Cinco deles são novos e quatro não dependem de ter havido fiscalização.</p>
      </div>
      <div class="formula">
        <p class="font-montserrat font-black text-brand" style="font-size:calc(30px * var(--tz));">IPR = maior entre piso e base</p>
        <p class="cd" style="margin-top:6px !important;">Regulado de alto risco inerente <b>não cai em faixa de baixa prioridade</b> só por não ter histórico de infração.</p>
      </div>
    </div>
    <div class="col-span-7 flex flex-col gap-4">
      <div class="painel">
        <div class="flex items-end justify-between"><div><p class="ct">Os dez indicadores e seus pesos</p>
          <p class="cd" style="margin:0;">Peso de cada um no IPR base</p></div>
          {chaves([("Vigente, corrigido", "#0066CC"), ("Novo ou refeito no IPR 2.0", "#D97706")])}</div>
        <div id="g-pesos" class="graf" style="height:600px;"></div>
      </div>
      <p class="legenda">Fonte: Notas Técnicas nº 19 e 20/2026/GPF/SFC; pesos vigentes no Painel de Risco da Fiscalização em 24/11/2026. O ICD mede a classe de acesso ao local (mesma sede, viatura, barco ou avião), não a distância em linha reta.</p>
    </div>
  </div>""", extra_css=FASE_CSS, js_extra=graficos(js6), base=1.0)


# ---------------------------------------------------------------------------
# 07 — Da faixa à solução fiscal
# ---------------------------------------------------------------------------
# NT 35, Quadro 2: outorgas ativas por faixa, ciclo PAF 2027 (2.427 = 2.467 − 40 retiradas).
FAIXAS = [  # faixa, solução fiscal, outorgas ativas, grupo
    ("C4", "Intervenção técnica, com possível medida cautelar", 37, "C"),
    ("C3", "Ação presencial intensiva", 90, "C"),
    ("C2", "Ação presencial sem aviso prévio", 190, "C"),
    ("C1", "Ação presencial programada", 265, "C"),
    ("B2", "Ação remota com ação à distância", 505, "B"),
    ("B1", "Ação remota documental", 908, "B"),
    ("A2", "Monitoramento e sorteio", 154, "A"),
    ("A1", "Monitoramento e sorteio", 278, "A"),
]
TOT_ATIVAS = sum(x[2] for x in FAIXAS)
assert TOT_ATIVAS == 2427
NOVO = {f: round(100 * v / TOT_ATIVAS, 1) for f, _, v, _ in FAIXAS}
ANTIGO = {"A1": 83.7, "A2": 5.2, "B1": 8.8, "B2": 1.5, "C1": 0.7, "C2": 0.1, "C3": 0.0, "C4": 0.0}
COR_G = {"A": "#15803D", "B": "#0066CC", "C": "#DC2626"}
TONS = {"C4": "#7F1D1D", "C3": "#991B1B", "C2": "#B91C1C", "C1": "#DC2626", "B2": "#1E40AF", "B1": "#0066CC", "A2": "#15803D", "A1": "#16A34A"}
PIR7_CSS = """
.pf { display:flex; align-items:center; gap:14px; }
.pf .bloco { height:58px; border-radius:8px; display:flex; align-items:center; justify-content:space-between; padding:0 18px; color:#fff; margin:0 auto; }
.pf .bloco p { margin:0; }
.pf .fx { font-family:'Montserrat',sans-serif; font-weight:900; font-size:calc(24px * var(--tz)); }
.pf .sol { font-size:calc(15.5px * var(--tz)); line-height:1.2; text-align:center; flex:1; padding:0 10px; }
.pf .qt { font-family:'Montserrat',sans-serif; font-weight:800; font-size:calc(20px * var(--tz)); }
"""
blocos = []
for i, (f, sol, v, g) in enumerate(FAIXAS):
    w = 46 + i * 54 / 7
    blocos.append(f'<div class="pf"><div class="bloco" style="width:{w:.1f}%; background:{TONS[f]};"><p class="fx">{f}</p><p class="sol">{sol}</p><p class="qt">{br(v)}</p></div></div>')
pir7 = "\n".join(blocos)
# Barras horizontais, na mesma ordem da pirâmide ao lado: C4 em cima, A1 embaixo.
ordem = ["C4", "C3", "C2", "C1", "B2", "B1", "A2", "A1"]
js7 = f"""
var fx = {json.dumps(ordem)}, antes = {[ANTIGO[f] for f in ordem]}, depois = {[NOVO[f] for f in ordem]};
G.desenha('g-dist', {{
  grid: {{ left: 62, right: 60, top: 44, bottom: 4 }},
  legend: G.legenda({{ data: ['IPR anterior · abr/2026', 'IPR 2.0 · ciclo 2027'] }}),
  tooltip: G.dica({{ trigger: 'axis', axisPointer: {{ type: 'shadow', shadowStyle: {{ color: 'rgba(148,163,184,.14)' }} }},
    formatter: function (ps) {{ return '<b>' + ps[0].name + '</b><br/>' + ps.map(function (p) {{ return p.marker + p.seriesName + ': <b>' + G.pct(p.value) + '</b>'; }}).join('<br/>'); }} }}),
  xAxis: G.eixoVal({{ show: false, max: 92 }}),
  yAxis: G.eixoCat(fx, {{ inverse: true, axisLine: {{ show: false }},
    axisLabel: {{ color: C.marca, fontFamily: G.FT, fontSize: 18, fontWeight: 800, margin: 12 }} }}),
  series: [
    {{ name: 'IPR anterior · abr/2026', type: 'bar', data: antes, barGap: '12%', barWidth: '38%', itemStyle: {{ color: C.antes, borderRadius: [0, 4, 4, 0] }},
       label: {{ show: true, position: 'right', distance: 6, color: C.apagado, fontFamily: G.FT, fontWeight: 700, fontSize: 15,
         formatter: function (p) {{ return p.value >= 1 ? G.pct(p.value, 0) : (p.value > 0 ? '<1%' : '0%'); }} }} }},
    {{ name: 'IPR 2.0 · ciclo 2027', type: 'bar', data: depois, barWidth: '38%', itemStyle: {{ color: C.marca, borderRadius: [0, 4, 4, 0] }},
       label: {{ show: true, position: 'right', distance: 6, color: C.tinta, fontFamily: G.FT, fontWeight: 700, fontSize: 15,
         formatter: function (p) {{ return G.pct(p.value, 0); }} }} }}
  ]
}});
"""
slide(7, 2, "Da faixa à solução fiscal", "Pirâmide ANTAQ · ciclo PAF 2027", "Da faixa à solução fiscal", f"""
  <div class="flex-1 px-16 pb-4 grid grid-cols-12 gap-10 items-center min-h-0">
    <div class="col-span-6 flex flex-col gap-3">
      <div class="flex items-end justify-between"><p class="sec">Faixa · solução fiscal · outorgas ativas</p>
        {chaves([("Grupo A", "#15803D"), ("Grupo B", "#0066CC"), ("Grupo C", "#DC2626")])}</div>
      <div class="painel flex flex-col" style="gap:6px; padding:16px 18px;">{pir7}</div>
      {card("fa-file-lines", "A forma muda, a faixa não", "Na navegação marítima e na interior longitudinal de carga, a ação é sempre documental, porque a verificação se cumpre por documentos. A dispensa alcança 191 outorgas do Grupo C.")}
    </div>
    <div class="col-span-6 flex flex-col gap-4">
      <div class="painel">
        <p class="ct">A pirâmide voltou a ter forma</p>
        <p class="cd" style="margin:0;">Distribuição das outorgas por faixa, antes e depois do IPR 2.0</p>
        <div id="g-dist" class="graf" style="height:450px;"></div>
      </div>
      <div class="destaque flex items-center gap-6">
        <p class="big" style="font-size:calc(58px * var(--tz)); color:#FFD700;">{br(TOT_ATIVAS)}</p>
        <p style="font-size:calc(18px * var(--tz)); color:#DBEAFE; line-height:1.45;">outorgas ativas classificadas. Em A1, caiu de <b>83,7%</b> para <b>{br(NOVO['A1'], 1)}%</b>; C3 e C4, antes vazias, têm <b>127</b> outorgas.</p>
      </div>
      <p class="legenda">Fonte: Nota Técnica nº 35/2026/GPF/SFC, Quadro 2 (data de referência 30/09/2026) e diagnóstico de abril de 2026 (2.543 outorgas). As faixas do IPR 2.0 foram recalibradas sobre o ciclo 2027.</p>
    </div>
  </div>""", extra_css=PIR7_CSS, js_extra=graficos(js7), base=1.0)


# ---------------------------------------------------------------------------
# 08 — O que entra no plano
# ---------------------------------------------------------------------------
FUN_CSS = """
.fun { display:flex; align-items:center; gap:14px; }
.fun .bx { border-radius:12px; padding:12px 18px; background:#F1F5F9; display:flex; align-items:center; justify-content:space-between; gap:14px; }
.fun .bx p { margin:0; }
.fun .n { font-family:'Montserrat',sans-serif; font-weight:900; font-size:calc(30px * var(--tz)); color:#003366; line-height:1; }
.fun .t { font-size:calc(16px * var(--tz)); color:#475569; line-height:1.3; }
.fun .menos { font-family:'Montserrat',sans-serif; font-weight:800; color:#B91C1C; font-size:calc(18px * var(--tz)); min-width:70px; text-align:right; }
.grp { border-radius:16px; padding:16px 20px; color:#fff; display:flex; flex-direction:column; gap:4px; }
.grp p { margin:0; }
.grp .gn { font-family:'Montserrat',sans-serif; font-weight:900; font-size:calc(56px * var(--tz)); line-height:1; }
.grp .gt { font-family:'Montserrat',sans-serif; font-weight:800; font-size:calc(21px * var(--tz)); white-space:nowrap; }
.grp .gd { font-size:calc(16px * var(--tz)); line-height:1.4; color:rgba(255,255,255,.9); }
"""
slide(8, 3, "O que entra no plano", "Composição do grupo de risco · PAF 2027", "Do ranking ao plano", f"""
  <div class="flex-1 px-16 pb-4 grid grid-cols-12 gap-10 items-center min-h-0">
    <div class="col-span-5 flex flex-col gap-3">
      <p class="sec">Do universo à lista</p>
      <div class="fun"><div class="bx" style="flex:1;"><p class="t">Universo do ciclo, de 2.126 empresas</p><p class="n">2.467</p></div></div>
      <div class="fun"><div class="bx card-red" style="flex:1; margin-left:30px;"><p class="t">CNPJ baixado ou suspenso na Receita Federal: sai da lista, não do universo</p><p class="n" style="color:#B91C1C;">40</p></div></div>
      <div class="fun"><div class="bx" style="flex:1; margin-left:60px;"><p class="t">Outorgas ativas com faixa de risco</p><p class="n">2.427</p></div></div>
      <div class="fun"><div class="bx card-amber" style="flex:1; margin-left:90px;"><p class="t">Arrendamentos portuários: rito próprio, fora do grupo de risco</p><p class="n" style="color:#B45309;">136</p></div></div>
      <div class="destaque flex items-center justify-between" style="margin-left:120px;">
        <p style="font-size:calc(18px * var(--tz)); color:#DBEAFE;">Grupo de risco<br/>do PAF 2027</p>
        <p class="big" style="font-size:calc(60px * var(--tz)); color:#FFD700;">696</p>
      </div>
      {card("fa-ruler-horizontal", "Antes: um corte fixo em 200", "A lista dos ciclos anteriores era recortada em 200 outorgas, número sem ato, sem versão e <b>menor que o próprio Grupo C</b>.", "card-amber")}
    </div>
    <div class="col-span-7 flex flex-col gap-4">
      <p class="sec">Uma regra por grupo, e não um número escolhido</p>
      <div class="grid grid-cols-3 gap-5" style="align-items:stretch;">
        <div class="grp" style="background:linear-gradient(160deg,#7F1D1D,#DC2626);">
          <p class="gt">Grupo C <span style="font-weight:600; font-size:.8em; opacity:.85;">· maior risco</span></p><p class="gn">572</p><p class="gd"><b>Entra inteiro.</b> Fiscalizar o maior risco é obrigação do modelo, não escolha de escopo. É o piso do plano.</p>
        </div>
        <div class="grp" style="background:linear-gradient(160deg,#1E3A8A,#0066CC);">
          <p class="gt">Grupo B <span style="font-weight:600; font-size:.8em; opacity:.85;">· intermediário</span></p><p class="gn">89</p><p class="gd"><b>Entra até esgotar as horas</b>, de 1.287, na ordem estrita do ranking. Para na primeira outorga que ultrapassa o saldo; não se pula ninguém.</p>
        </div>
        <div class="grp" style="background:linear-gradient(160deg,#14532D,#15803D);">
          <p class="gt">Grupo A <span style="font-weight:600; font-size:.8em; opacity:.85;">· menor risco</span></p><p class="gn">35</p><p class="gd"><b>Entra por sorteio</b>, de 432. Sorteadas são fiscalizadas como as do Grupo C.</p>
        </div>
      </div>
      <div class="grid grid-cols-2 gap-5">
        {card("fa-id-card", "Cadastro antes do plano", "Cada outorga é conferida com a base de CNPJ da Receita: programar fiscalização contra empresa extinta consome horas e gera auto sem destinatário.")}
        {card("fa-list-check", "Cada linha diz por que entrou", "A lista publicada indica o motivo de cada outorga: Grupo C, sorteio do Grupo A ou posição no ranking do Grupo B.")}
      </div>
      <p class="legenda">Fonte: Nota Técnica nº 35/2026/GPF/SFC, §§ 3.1 a 3.8 e Quadro 3. Composição proposta à Diretoria Colegiada, em deliberação. Desempate no Grupo B: tempo sem fiscalização, dificuldade de acesso e maturidade da empresa.</p>
    </div>
  </div>""", extra_css=FUN_CSS, base=1.0)


# ---------------------------------------------------------------------------
# 09 — Sorteio auditável do Grupo A
# ---------------------------------------------------------------------------
PASSO_CSS = """
.passo { display:flex; gap:16px; align-items:flex-start; }
.passo .nb { width:52px; height:52px; border-radius:50%; background:#003366; color:#FFD700; font-family:'Montserrat',sans-serif; font-weight:900; font-size:calc(22px * var(--tz)); display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.hash { font-family:ui-monospace,Menlo,monospace; font-size:calc(14px * var(--tz)); color:#475569; background:#F1F5F9; border-radius:6px; padding:2px 8px; }
.taxa { border-radius:14px; padding:14px; text-align:center; }
.taxa p { margin:0; }
"""
slide(9, 3, "Sorteio auditável do Grupo A", "Amostragem aleatória · executada em 16/10/2026", "Sorteio que qualquer um confere", f"""
  <div class="flex-1 px-16 pb-4 grid grid-cols-12 gap-10 items-center min-h-0">
    <div class="col-span-6 flex flex-col gap-4">
      {card("fa-eye-slash", "Por que sortear o baixo risco", "Deixar o Grupo A fora do plano criaria uma <b>zona de ausência previsível</b>: o próprio regulado saberia que não será visitado. O sorteio mantém a chance, sem que ninguém escolha quem.", "card-gold")}
      <p class="sec" style="margin-top:4px;">Em duas fases</p>
      <div class="card passo"><div class="nb">1</div><div><p class="ct">Compromisso</p><p class="cd">A Agência registra a lista de elegíveis, as taxas e a regra, e grava a impressão digital (<span class="hash">SHA-256</span>) desse conjunto <b>antes</b> de conhecer o número aleatório.</p></div></div>
      <div class="card passo"><div class="nb">2</div><div><p class="ct">Execução</p><p class="cd">A semente é o número publicado pelo <b>NIST Randomness Beacon</b> (pulso 1986097), um serviço público que divulga a cada minuto um número aleatório certificado. Ninguém o conhecia antes; todos podem consultá-lo depois.</p></div></div>
      <div class="card passo card-green"><div class="nb" style="background:#15803D; color:#fff;"><i class="fas fa-check"></i></div><div><p class="ct">Conferência</p><p class="cd">Ata e programa estão no processo. O programa roda em qualquer computador com Python, sem acesso aos sistemas da Agência, e <b>falha se qualquer outorga for incluída, retirada ou trocada</b>.</p></div></div>
    </div>
    <div class="col-span-6 flex flex-col gap-4">
      <p class="sec">Quanto maior o risco da atividade, maior a chance</p>
      <div class="grid grid-cols-3 gap-4">
        <div class="taxa" style="background:#FEE2E2;"><p class="big" style="font-size:calc(50px * var(--tz)); color:#991B1B;">10%</p><p class="cd">risco da atividade<br/><b>alto</b></p></div>
        <div class="taxa" style="background:#FEF3C7;"><p class="big" style="font-size:calc(50px * var(--tz)); color:#92400E;">7%</p><p class="cd">risco da atividade<br/><b>médio</b></p></div>
        <div class="taxa" style="background:#DCFCE7;"><p class="big" style="font-size:calc(50px * var(--tz)); color:#166534;">5%</p><p class="cd">risco da atividade<br/><b>baixo</b></p></div>
      </div>
      <div class="destaque flex items-center gap-6">
        <p class="big" style="font-size:calc(58px * var(--tz)); color:#FFD700; white-space:nowrap;">35<span style="font-size:.45em; color:#DBEAFE;"> de 432</span></p>
        <p style="font-size:calc(19px * var(--tz)); color:#DBEAFE; line-height:1.45;">outorgas de menor risco sorteadas para 2027. <b style="color:#fff;">A sorteada é fiscalizada como as de maior risco.</b></p>
      </div>
      {card("fa-clone", "Serve para qualquer cadastro", "Basta uma lista de regulados, uma regra de sorteio e um número público. O procedimento não depende dos sistemas da ANTAQ e pode ser refeito por qualquer pessoa.", "card-green")}
      <p class="legenda">Fonte: Nota Técnica nº 35/2026/GPF/SFC, seção 5. Em 2027, todas as atividades do Grupo A estavam na faixa de risco médio, e a taxa aplicada foi de 7%.</p>
    </div>
  </div>""", extra_css=PASSO_CSS, base=1.0)


# ---------------------------------------------------------------------------
# 10 — O plano é viável com a equipe atual?
# ---------------------------------------------------------------------------
HORAS = [("Porto organizado", 120), ("Terminal de uso privado", 84), ("Demais outorgas", 72), ("Travessia e registro", 58)]
ANTES = [("Santana (AP)", 1281, 5204, 406.3), ("Belém (PA)", 8070, 11384, 141.1),
         ("Manaus (AM)", 7532, 9605, 127.5), ("Porto Alegre (RS)", 1768, 1831, 103.6)]
HOR_CSS = """
.hr { width:100%; display:flex; align-items:center; justify-content:space-between; padding:8px 0; border-bottom:1px solid #E2E8F0; }
.hr:last-child { border-bottom:0; }
.hr p { margin:0; }
.fase-b { display:flex; height:54px; border-radius:10px; overflow:hidden; }
.fase-b div { display:flex; align-items:center; justify-content:center; color:#fff; font-family:'Montserrat',sans-serif; font-weight:700; font-size:calc(16px * var(--tz)); text-align:center; line-height:1.15; }
table.tbl { width:100%; border-collapse:collapse; }
table.tbl th { font-family:'Montserrat',sans-serif; font-size:calc(14px * var(--tz)); color:#64748B; text-transform:uppercase; letter-spacing:.06em; text-align:right; padding:6px 10px; border-bottom:2px solid #CBD5E1; }
table.tbl th:first-child, table.tbl td:first-child { text-align:left; }
table.tbl td { font-size:calc(18px * var(--tz)); color:#334155; text-align:right; padding:9px 10px; border-bottom:1px solid #E2E8F0; }
table.tbl td.oc { font-family:'Montserrat',sans-serif; font-weight:900; color:#B91C1C; }
table.tbl tr.tot td { font-weight:700; color:#003366; border-top:2px solid #CBD5E1; border-bottom:0; }
table.tbl tr.tot td.oc { color:#15803D; }
"""
horas_html = "".join(f'<div class="hr"><p class="cd" style="margin:0;">{m}</p><p class="num-r" style="font-size:calc(24px * var(--tz));">{h} h</p></div>' for m, h in HORAS)
linhas = "".join(f'<tr><td>{u}</td><td>{br(c)}</td><td>{br(d)}</td><td class="oc">{br(o, 1)}%</td></tr>' for u, c, d, o in ANTES)
slide(10, 3, "O plano é viável com a equipe atual?", "Força de trabalho · planos de trabalho do PGD", "O plano é viável com a equipe atual?", f"""
  <div class="flex-1 px-16 pb-4 grid grid-cols-12 gap-10 items-center min-h-0">
    <div class="col-span-5 flex flex-col gap-4">
      <p class="sec">A régua: horas, não número de outorgas</p>
      <div class="card" style="flex-direction:column; gap:2px; padding:12px 20px;">
        <p class="ct" style="margin-bottom:4px;">Custo normativo por fiscalização</p>
        {horas_html}
      </div>
      <div class="flex flex-col gap-2">
        <p class="sec">Três fases; só uma exige presença</p>
        <div class="bar-row"><div class="bar-trk fase-b">
          <div class="seg" style="width:40%; background:#0066CC;">Planejamento e<br/>notificação · 40%</div>
          <div class="seg" style="width:20%; background:#D97706;">Vistoria<br/>20%</div>
          <div class="seg" style="width:40%; background:#003366;">Relatório<br/>40%</div>
        </div></div>
        <p class="legenda">As fases de escritório podem ser feitas por equipe de outra unidade, sem viajar.</p>
      </div>
      {card("fa-user-clock", "Capacidade: 35% das horas líquidas", "Medida nos planos de trabalho do PGD, por servidor, em 12 meses. A mesma fração para todas as unidades, descontados estagiários e grupos especializados e somados os novos servidores do concurso.")}
    </div>
    <div class="col-span-7 flex flex-col gap-4">
      <div class="grid grid-cols-3 gap-4">
        {stat("47.207 h", "demanda do grupo<br/>de risco")}
        {stat("55.560 h", "capacidade nacional<br/>para o PAF")}
        <div class="stat-card" style="background:linear-gradient(135deg,#14532D,#15803D);"><p class="stat-num">85%</p><p class="stat-lbl" style="color:#DCFCE7;">de ocupação<br/>no agregado</p></div>
      </div>
      <div class="destaque">
        <p class="font-montserrat font-bold" style="font-size:calc(26px * var(--tz));">No total há folga, <span style="color:#FFD700;">mas não onde a carga está.</span></p>
      </div>
      <div class="painel" style="padding:14px 22px 12px;">
        <p class="ct" style="margin-bottom:8px;">Unidades acima do limite, antes de redistribuir</p>
        <table class="tbl">
          <thead><tr><th>Unidade</th><th>Capacidade (h)</th><th>Demanda (h)</th><th>Ocupação</th></tr></thead>
          <tbody>{linhas}
            <tr class="tot"><td>Outras 10 unidades</td><td>36.909</td><td>19.183</td><td class="oc">17% a 88%</td></tr>
          </tbody>
        </table>
      </div>
      <p class="legenda">Fonte: Nota Técnica nº 35/2026/GPF/SFC, seções 4 e 6, Quadros 4 e 6; Tabela de Atividades da SFC. Ocupação de 100% quer dizer que o PAF preencheu a fração de 35%, não que o servidor está 100% ocupado.</p>
    </div>
  </div>""", extra_css=HOR_CSS, base=1.0)


# ---------------------------------------------------------------------------
# 11 — Equalização
# ---------------------------------------------------------------------------
DEPOIS = {"Santana (AP)": 98.1, "Belém (PA)": 99.1, "Manaus (AM)": 99.9, "Porto Alegre (RS)": 94.0}
js11 = f"""
var u = {json.dumps([a[0] for a in ANTES], ensure_ascii=False)}, antes = {[a[3] for a in ANTES]}, depois = {[DEPOIS[a[0]] for a in ANTES]};
G.desenha('g-eq', {{
  grid: {{ left: 190, right: 90, top: 46, bottom: 34 }},
  legend: G.legenda({{ data: ['Antes', 'Depois da equalização'] }}),
  tooltip: G.dica({{ trigger: 'axis', axisPointer: {{ type: 'shadow', shadowStyle: {{ color: 'rgba(148,163,184,.14)' }} }},
    formatter: function (ps) {{ return '<b>' + ps[0].name + '</b><br/>' + ps.map(function (p) {{ return p.marker + p.seriesName + ': <b>' + G.pct(p.value) + '</b>'; }}).join('<br/>'); }} }}),
  xAxis: G.eixoVal({{ show: false, max: 440 }}),
  yAxis: G.eixoCat(u, {{ inverse: true, axisLine: {{ show: false }}, axisLabel: {{ color: C.tinta2, fontFamily: G.FT, fontSize: 18, fontWeight: 600, margin: 14 }} }}),
  series: [
    {{ name: 'Antes', type: 'bar', data: antes, barWidth: 22, barGap: '25%', itemStyle: {{ color: '#DC2626', borderRadius: [0, 5, 5, 0] }},
       label: {{ show: true, position: 'right', color: C.tinta, fontFamily: G.FT, fontWeight: 700, fontSize: 17, formatter: function (p) {{ return G.pct(p.value, 0); }} }},
       markLine: {{ symbol: 'none', silent: true, data: [{{ xAxis: 100 }}], lineStyle: {{ color: '#003366', type: 'dashed', width: 2 }},
         label: {{ position: 'end', formatter: 'limite 100%', color: '#003366', fontFamily: G.FT, fontWeight: 700, fontSize: 15 }} }} }},
    {{ name: 'Depois da equalização', type: 'bar', data: depois, barWidth: 22, itemStyle: {{ color: '#15803D', borderRadius: [0, 5, 5, 0] }},
       label: {{ show: true, position: 'right', color: C.tinta, fontFamily: G.FT, fontWeight: 700, fontSize: 17, formatter: function (p) {{ return G.pct(p.value, 1); }} }} }}
  ]
}});
"""
slide(11, 3, "Equalização da carga", "Redistribuir com regra e registro", "Equalização da carga", f"""
  <div class="flex-1 px-16 pb-4 grid grid-cols-12 gap-10 items-center min-h-0">
    <div class="col-span-5 flex flex-col gap-4">
      {card("fa-boxes-stacked", "Lotes que se movem inteiros", "Outorgas da mesma unidade, localidade e modalidade viajam juntas: fiscalizar vinte travessias num lugar custa, em deslocamento, quase o mesmo que fiscalizar uma.")}
      {card("fa-people-arrows", "Dois instrumentos", "<b>Transferência</b>: outra unidade executa no ciclo. <b>Missão de apoio</b>: a origem conduz o processo e outra unidade faz a vistoria, as fases de escritório ou tudo.")}
      {card("fa-scale-unbalanced-flip", "Critérios ponderados de destino", "Folga da receptora <b>40%</b> · proximidade <b>35%</b> · afinidade com a carteira <b>15%</b> · jurisdição <b>10%</b>. Nenhuma receptora passa de 90% nem absorve mais de 45% do excesso.")}
      {card("fa-gavel", "A regra propõe, o gestor decide", "Cada movimento é aprovado, rejeitado ou redirecionado, com autor e fundamento. A jurisdição não muda: a camada vale para o ciclo.", "card-gold")}
    </div>
    <div class="col-span-7 flex flex-col gap-4">
      <div class="painel">
        <p class="ct">Ocupação da capacidade para o PAF</p>
        <p class="cd" style="margin:0;">As quatro unidades acima do limite, antes e depois dos movimentos aprovados</p>
        <div id="g-eq" class="graf" style="height:400px;"></div>
      </div>
      <div class="grid grid-cols-3 gap-4">
        {stat("46", "movimentos propostos,<br/>todos aprovados")}
        {stat("152", "outorgas alcançadas<br/>de 1.981 lotes")}
        {stat("9.584 h", "redistribuídas entre<br/>as unidades")}
      </div>
      <div class="destaque flex items-center gap-5">
        <i class="fas fa-route" style="font-size:calc(40px * var(--tz)); color:#FFD700;"></i>
        <p style="font-size:calc(17px * var(--tz)); color:#DBEAFE; line-height:1.5;"><b>Travessias do Oiapoque (AP)</b>: 56 outorgas da unidade de Santana. A vistoria é feita pela equipe de São Luís e o escritório pela de Salvador, <b>numa única ida ao local</b>.</p>
      </div>
      <p class="legenda">Fonte: Nota Técnica nº 35/2026/GPF/SFC, seção 8 e Quadro 7. 28 transferências (2.304 h) e 18 missões de apoio (7.280 h).</p>
    </div>
  </div>""", js_extra=graficos(js11), base=1.0)


# ---------------------------------------------------------------------------
# 12 — O plano inteiro em horas (NT 35 seção 9 + NT 36)
# ---------------------------------------------------------------------------
# NT 36, conclusões: temáticas até 3.960 h; operacionais 4.608 h; rito próprio das unidades
# 5.916 h. Grupo de risco 47.207 h (NT 35). Soma 61.691 h contra 55.560 h de capacidade:
# excesso de 6.131 h, coberto pela reserva de extraordinárias.
PARC = [("Grupo de risco", 47207, "#003366"), ("Rito próprio", 5916, "#0066CC"),
        ("Operacionais", 4608, "#D97706"), ("Temáticas", 3960, "#15803D")]
assert sum(v for _, v, _ in PARC) - 55560 == 6131
ORC_CSS = """
.orc { display:flex; align-items:center; gap:16px; }
.orc p { margin:0; }
.orc-r { font-family:'Montserrat',sans-serif; font-weight:700; color:#475569; font-size:calc(16px * var(--tz)); width:130px; }
.orc-v { font-family:'Montserrat',sans-serif; font-weight:900; color:#003366; font-size:calc(22px * var(--tz)); width:150px; text-align:right; white-space:nowrap; }
"""
slide(12, 3, "O plano inteiro em horas", "PAF 2027 · Notas Técnicas nº 35 e 36/2026", "Um orçamento fechado de horas", f"""
  <div class="flex-1 px-16 pb-4 flex flex-col gap-5 min-h-0" style="justify-content:center;">
    <div class="painel flex flex-col gap-3" style="padding:18px 24px;">
      <div class="flex items-end justify-between"><p class="ct">Parcelas programadas do PAF 2027, em horas</p>
        {chaves([(f"{n} · {br(v)}", c) for n, v, c in PARC])}</div>
      <div class="orc"><p class="orc-r">Programado</p><div style="flex:1;">{segbar([("Grupo de risco · 47.207 h", 47207, "#003366"), ("", 5916, "#0066CC"), ("", 4608, "#D97706"), ("", 3960, "#15803D")], altura=50)}</div><p class="orc-v">61.691 h</p></div>
      <div class="orc"><p class="orc-r">Capacidade</p><div style="flex:1; display:flex; gap:3px;">
        <div class="bar-row" style="width:{100 * 55560 / 61691:.2f}%;"><div class="bar-trk segbar" style="height:50px;"><div class="seg" style="width:100%; background:#64748B;">Capacidade para o PAF · 35% das horas líquidas</div></div></div>
        <div style="flex:1; border:2px dashed #DC2626; border-radius:6px; display:flex; align-items:center; justify-content:center; color:#B91C1C; font-family:'Montserrat',sans-serif; font-weight:800; font-size:calc(17px * var(--tz));">−6.131</div>
      </div><p class="orc-v">55.560 h</p></div>
      <p class="cd" style="margin:0;">O excesso de <b>6.131 horas</b> é coberto pela reserva de extraordinárias, unidade a unidade, <b>sem aumentar o total de horas de fiscalização</b>.</p>
    </div>
    <div class="grid grid-cols-3 gap-6" style="align-items:stretch;">
      <div class="card" style="flex-direction:column; gap:8px;">
        <div class="flex items-center gap-3"><div class="ico"><i class="fas fa-bolt"></i></div><p class="ct">Extraordinárias: previsíveis em volume</p></div>
        <p class="cd">Não se sabe qual, mas se sabe quantas: de 500 a 600 por ano desde 2019. Para 2027, <b>542</b> previstas e uma reserva de <b>16.266 h</b>. A autorização prévia da Superintendência filtra os pedidos.</p>
      </div>
      <div class="card" style="flex-direction:column; gap:8px;">
        <div class="flex items-center gap-3"><div class="ico"><i class="fas fa-calendar-days"></i></div><p class="ct">Calendário que economiza viagem</p></div>
        <p class="cd">Além de 120 km da sede, <b>tudo da mesma localidade no mesmo mês</b>, numa só missão. São 108 missões presenciais, estimadas em <b>R$ 171,9 mil</b>. A chefia escolhe o mês.</p>
      </div>
      <div class="card card-gold" style="flex-direction:column; gap:8px;">
        <div class="flex items-center gap-3"><div class="ico" style="background:#FDE68A;"><i class="fas fa-right-left" style="color:#B45309;"></i></div><p class="ct">Regra de troca</p></div>
        <p class="cd"><b>Demanda nova só entra se outra sair</b>, com decisão registrada em processo. Ordem de saída: reserva, operações e temáticas não iniciadas e, por último, o fim do ranking do Grupo B. Grupo C e sorteadas não entram na troca.</p>
      </div>
    </div>
    <p class="legenda">Fontes: Nota Técnica nº 35/2026/GPF/SFC, seção 9 (calendário e deslocamento); Nota Técnica nº 36/2026/GPF/SFC (extraordinárias, operacionais, temáticas e rito próprio). Estimativa de deslocamento a partir do histórico de viagens da Agência (Portal da Transparência, 2019–2026), com dois fiscais por missão.</p>
  </div>""", extra_css=ORC_CSS)


# ---------------------------------------------------------------------------
# 13 — Governança
# ---------------------------------------------------------------------------
CAD_CSS = """
.etapa { display:flex; flex-direction:column; align-items:center; text-align:center; gap:8px; background:#F8FAFC; border-radius:14px; padding:14px 10px; border-top:4px solid #0066CC; }
.etapa p { margin:0; }
.etapa .ei { width:54px; height:54px; border-radius:50%; background:#DBEAFE; display:flex; align-items:center; justify-content:center; }
.etapa .ei i { color:#0066CC; font-size:calc(22px * var(--tz)); }
.etapa .en { font-family:'Montserrat',sans-serif; font-weight:800; font-size:calc(13px * var(--tz)); color:#64748B; letter-spacing:.08em; }
.etapa .et { font-family:'Montserrat',sans-serif; font-weight:700; color:#003366; font-size:calc(17px * var(--tz)); line-height:1.25; }
.seta { display:flex; align-items:center; justify-content:center; color:#94A3B8; font-size:calc(20px * var(--tz)); }
"""
ETAPAS = [("1", "fa-rotate", "Sincroniza e preserva decisões"), ("2", "fa-database", "Extrai universo e indicadores"),
          ("3", "fa-id-card", "Verifica o cadastro na Receita"), ("4–8", "fa-gauge-high", "Recalcula o IPR e aplica retiradas"),
          ("9–12", "fa-user-clock", "Mede a força de trabalho no PGD"), ("13–16", "fa-calendar-check", "Dimensiona, custeia, equaliza e agenda")]
cadeia = '<div class="seta"><i class="fas fa-chevron-right"></i></div>'.join(
    f'<div class="etapa" style="flex:1;"><p class="en">ETAPA {n}</p><div class="ei"><i class="fas {i}"></i></div><p class="et">{t}</p></div>' for n, i, t in ETAPAS)
slide(13, 4, "Governança do plano", "Cadeia de elaboração · Painel de Risco da Fiscalização", "Um plano que se audita", f"""
  <div class="flex-1 px-16 pb-4 flex flex-col gap-6 min-h-0" style="justify-content:center;">
    <div class="flex flex-col gap-3">
      <p class="sec">Dezesseis etapas encadeadas, executadas a partir do Painel de Risco da Fiscalização</p>
      <div class="painel flex items-stretch gap-2" style="padding:16px;">{cadeia}</div>
    </div>
    <div class="grid grid-cols-2 gap-6">
      {card("fa-fingerprint", "Reprodutibilidade", "Cada etapa registra a impressão digital dos dados e parâmetros que usou. As mesmas entradas dão o mesmo resultado, e qualquer alteração fica evidente.")}
      {card("fa-table-list", "Parâmetros em tabela, com vigência", "Pesos, faixas, soluções fiscais, custos, fração de dedicação, taxas de sorteio e critérios de equalização. Mudar uma regra é <b>abrir nova vigência</b>, preservando a anterior.")}
      {card("fa-hand", "Conferências que interrompem", "Etapas que dependem de outras conferem os números de partida. Se divergem, a execução para, em vez de produzir resultado inconsistente.")}
      {card("fa-user-shield", "A decisão dos responsáveis prevalece", "Aprovações de movimentos, escolhas de mês e reversões de inativação ficam registradas com autor e fundamento, e sobrevivem às recargas de dados. A chefia decide só sobre a própria unidade.", "card-gold")}
    </div>
    <p class="legenda">Fonte: Nota Técnica nº 35/2026/GPF/SFC, seção 10 e Quadro 8. O Painel de Risco da Fiscalização é a planilha desenvolvida para o IPR 2.0; os dados pessoais de servidores ficam restritos à consulta autenticada.</p>
  </div>""", extra_css=CAD_CSS, base=1.12)


# ---------------------------------------------------------------------------
# 14 — Desafios e alternativas
# ---------------------------------------------------------------------------
DA_CSS = """
.da { display:grid; grid-template-columns: 1fr 56px 1.15fr; align-items:stretch; gap:0; }
.da > div { display:flex; align-items:center; }
.da .d { background:#FEF2F2; border-radius:12px 0 0 12px; padding:10px 18px; border-left:5px solid #EF4444; }
.da .s { justify-content:center; background:linear-gradient(90deg,#FEF2F2,#F0FDF4); color:#64748B; }
.da .a { background:#F0FDF4; border-radius:0 12px 12px 0; padding:10px 18px; }
.da p { margin:0; font-size:calc(16.5px * var(--tz)); line-height:1.35; color:#334155; }
.da b { color:#003366; font-family:'Montserrat',sans-serif; }
.aberto { display:flex; gap:12px; align-items:flex-start; }
.aberto i { color:#B45309; margin-top:4px; font-size:calc(18px * var(--tz)); }
.aberto p { margin:0; font-size:calc(16.5px * var(--tz)); line-height:1.4; color:#334155; }
.aberto b { color:#003366; }
"""
PARES = [
    ("Quem nunca foi fiscalizado parecia de baixo risco", "<b>Tempo sem fiscalização</b> como indicador e <b>risco inerente da atividade</b> como piso"),
    ("O baixo risco virava zona previsível", "<b>Sorteio auditável</b>, com semente pública e conferência por qualquer pessoa"),
    ("Lista com número fixo, sem relação com a equipe", "Plano <b>medido em horas</b> contra os planos de trabalho de cada unidade"),
    ("Carga concentrada onde falta gente", "<b>Equalização</b> com missões de apoio e fases de escritório feitas a distância"),
    ("Viagem cara e mal aproveitada", "<b>Agrupar por localidade</b> e medir a dificuldade de acesso pela rota real"),
    ("Demanda nova sem limite", "<b>Reserva</b> para extraordinárias, autorização prévia e <b>regra de troca</b>"),
    ("Cadastro desatualizado", "<b>Verificação na Receita Federal</b> antes de montar o plano"),
]
pares = "\n".join(f'<div class="da"><div class="d"><p>{d}</p></div><div class="s"><i class="fas fa-arrow-right"></i></div><div class="a"><p>{a}</p></div></div>' for d, a in PARES)
slide(14, 4, "Desafios e alternativas", "O que a ANTAQ enfrentou e o que ainda está aberto", "Desafios e alternativas", f"""
  <div class="flex-1 px-16 pb-4 grid grid-cols-12 gap-10 items-center min-h-0">
    <div class="col-span-8 flex flex-col gap-3">
      <div class="grid" style="grid-template-columns: 1fr 56px 1.15fr;"><p class="sec" style="color:#B91C1C;">Desafio</p><span></span><p class="sec" style="color:#15803D;">Alternativa adotada</p></div>
      <div class="flex flex-col" style="gap:9px;">{pares}</div>
    </div>
    <div class="col-span-4 flex flex-col gap-4">
      <div class="card card-amber" style="flex-direction:column; gap:12px;">
        <p class="ct">O que ainda está aberto</p>
        <div class="aberto"><i class="fas fa-circle-half-stroke"></i><p><b>Cobertura do Grupo B: 6,9%</b> (89 de 1.287). O limite é a distribuição geográfica da equipe, não o método.</p></div>
        <div class="aberto"><i class="fas fa-map-location-dot"></i><p><b>Norte no limite</b> mesmo depois de redistribuir. Ampliar o plano depende de lotação.</p></div>
        <div class="aberto"><i class="fas fa-clipboard-question"></i><p><b>Qualidade do registro</b> nos planos de trabalho: o balanço é tão bom quanto o dado.</p></div>
        <div class="aberto"><i class="fas fa-percent"></i><p><b>35% para todos</b> é decisão de planejamento: unidades abaixo disso terão de reorganizar a agenda.</p></div>
        <div class="aberto"><i class="fas fa-hand-holding-heart"></i><p><b>Incentivos</b>: a base da pirâmide (orientação, reconhecimento) ainda tem menos instrumentos que o topo.</p></div>
      </div>
      <p class="legenda">Fonte: Nota Técnica nº 35/2026/GPF/SFC, seção 11 (limitações); apresentações da SFC de 2022 (instrumentos e incentivos).</p>
    </div>
  </div>""", extra_css=DA_CSS, base=1.05)


# ---------------------------------------------------------------------------
# 01 — Capa e 15 — Encerramento
# ---------------------------------------------------------------------------
ESCURO_CSS = """
body { margin:0; padding:0; overflow:hidden; font-family:'Open Sans',sans-serif; }
.slide { width:100vw; height:100vh; position:relative; display:flex; flex-direction:column; overflow:hidden; background: linear-gradient(135deg, #001a33 0%, #003366 45%, #004d99 100%); }
.font-montserrat { font-family:'Montserrat',sans-serif; }
.gold { color:#FFD700; } .bg-gold { background-color:#FFD700; }
.shape-circle { position:absolute; bottom:-140px; left:-140px; width:520px; height:520px; border-radius:50%; border:2px solid rgba(255,215,0,0.07); }
.shape-circle2 { position:absolute; top:-120px; right:-120px; width:420px; height:420px; border-radius:50%; border:2px solid rgba(255,215,0,0.06); }
.shape-right { position:absolute; top:0; right:0; width:40%; height:100%; background:linear-gradient(135deg, rgba(0,102,204,0.3) 0%, rgba(0,51,102,0.6) 100%); clip-path:polygon(30% 0, 100% 0, 100% 100%, 0% 100%); }
.recado { background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12); border-radius:16px; padding:14px 22px; display:flex; gap:16px; align-items:flex-start; }
.recado i { color:#FFD700; font-size:calc(22px * var(--tz)); margin-top:3px; width:28px; text-align:center; }
.recado p { margin:0; }
.recado-t { font-family:'Montserrat',sans-serif; font-weight:700; color:#fff; font-size:calc(19px * var(--tz)); }
.recado-d { color:#BFD3E8; font-size:calc(16px * var(--tz)); line-height:1.5; margin-top:3px !important; }
.perg { border-left:3px solid #FFD700; padding:4px 0 4px 16px; color:#E2E8F0; font-size:calc(17px * var(--tz)); line-height:1.45; margin:0; }
.gap-4 { row-gap:24px; }
"""

ESCURO_HEAD = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{title}</title>
<link rel="icon" type="image/png" href="favicon.png">
<link rel="icon" type="image/x-icon" href="favicon.ico">
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;700;900&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet"/>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet"/>
<style>
:root {{ --tz-base: {base}; }}
{css}
</style>
</head>
"""
NAV = '<script>document.addEventListener("keydown",function(e){if(["ArrowRight","ArrowLeft","PageDown","PageUp","Home","End"," ","f","F"].indexOf(e.key)!==-1){e.preventDefault();window.parent.postMessage({type:"slide-nav",key:e.key},"*");}});</script>'


def chip(ic, rot, val):
    return f"""      <div class="flex items-center gap-3">
        <div class="w-12 h-12 rounded-full flex items-center justify-center" style="background:rgba(255,215,0,0.15);"><i class="fas {ic} gold text-lg"></i></div>
        <div><p class="text-gray-400 text-sm uppercase tracking-wider font-semibold">{rot}</p><p class="text-white font-semibold text-lg">{val}</p></div>
      </div>"""


CAPA = ESCURO_HEAD.format(title=f"Abertura — {TITULO_DECK}", base="1.15", css=ESCURO_CSS) + f"""<body>
<div class="slide">
  <div class="shape-right"></div>
  <div style="height:6px; background:#FFD700; width:100%;"></div>
  <div class="relative z-10 flex flex-col justify-center flex-1 pl-24 pr-16">
    <div class="absolute top-16 left-24 flex items-center gap-3">
      <div class="bg-gold" style="width:40px;height:3px;"></div>
      <p class="text-gray-400 text-lg font-montserrat font-medium tracking-widest uppercase">2ª Oficina de Integração · Fiscalização do Uso de Recursos Hídricos</p>
    </div>
    <div class="mt-4">
      <p class="font-montserrat font-black text-white leading-none" style="font-size:calc(76px * var(--tz));">Fiscalização</p>
      <p class="font-montserrat font-black gold leading-none mt-2" style="font-size:calc(92px * var(--tz));">Responsiva</p>
      <div class="bg-gold mt-6 mb-8" style="width:100px; height:4px;"></div>
      <p class="text-2xl text-gray-300 font-light leading-relaxed max-w-3xl">A experiência da ANTAQ: do ranking de risco<br/>a um plano na medida da equipe</p>
    </div>
    <div class="flex gap-10 mt-12">
{chip("fa-water", "Evento", "ANA · Sede, Brasília (DF)")}
{chip("fa-calendar-day", "Data", "25 de novembro de 2026")}
{chip("fa-user-tie", "Apresentação", "Pedro Henrique Soares · GPF/SFC")}
    </div>
  </div>
  <div class="relative z-10 px-24 pb-10 flex justify-between items-end border-t border-gray-700 pt-6 mx-8">
    <div class="flex items-center gap-4">
      <div class="flex items-center gap-2 text-gray-400 text-sm"><i class="fas fa-sitemap"></i><span>SFC · Superintendência de Fiscalização e Coordenação das Unidades Regionais</span></div>
      <div class="flex items-center gap-2 text-gray-400 text-sm"><i class="fas fa-globe"></i><span>www.gov.br/antaq</span></div>
    </div>
    <p class="text-gray-500 text-sm font-montserrat font-bold tracking-wider">1 / {TOTAL}</p>
  </div>
  <div class="absolute top-1/2 right-12 transform -translate-y-1/2 opacity-5" style="z-index:0;"><img src="assets/logo-antaq-branca-vertical.png" alt="" style="height:400px;"></div>
</div>
<script src="zoom.js"></script>
{NAV}
</body>
</html>
"""

RECADOS = [
    ("fa-eye", "Ausência de dado não é baixo risco", "Meça o tempo sem fiscalização e use o risco inerente da atividade como piso."),
    ("fa-dice", "Sorteie o baixo risco", "Uma amostra aleatória, com semente pública, evita a zona previsível, sem que ninguém escolha quem."),
    ("fa-hourglass-half", "Planeje em horas", "O tamanho do plano é medido contra a equipe de cada unidade, não escolhido."),
    ("fa-table-list", "Regra em tabela, decisão registrada", "Parâmetros com vigência e decisões com autor e fundamento tornam o plano auditável."),
]
PERGUNTAS = [
    "Como medir o risco inerente de cada tipo de uso da água: captação, lançamento, barragens?",
    "Que parcela dos usuários de baixo risco deveria ser sorteada a cada ano?",
    "Como compartilhar equipes, vistorias e fases de escritório entre órgãos gestores?",
]


def encerramento():
    rec = "\n".join(
        f'      <div class="recado"><i class="fas {i}"></i><div><p class="recado-t">{t}</p><p class="recado-d">{d}</p></div></div>'
        for i, t, d in RECADOS)
    perg = "\n".join(f'        <p class="perg">{p}</p>' for p in PERGUNTAS)
    return ESCURO_HEAD.format(title=f"Encerramento — {TITULO_DECK}", base="1.22", css=ESCURO_CSS) + f"""<body>
<div class="slide">
  <div class="shape-circle"></div><div class="shape-circle2"></div>
  <div style="height:6px; background:#FFD700; width:100%;"></div>
  <div class="relative z-10 flex-1 px-24 pt-10 pb-4 grid grid-cols-12 gap-12 items-center">
    <div class="col-span-6 flex flex-col">
      <div class="flex items-center gap-3 mb-6"><div class="bg-gold" style="width:40px;height:3px;"></div>
        <p class="text-gray-400 text-lg font-montserrat font-medium tracking-widest uppercase">Em síntese</p></div>
      <p class="font-montserrat font-black text-white leading-none" style="font-size:calc(50px * var(--tz));">O risco orienta,</p>
      <p class="font-montserrat font-black gold leading-none mt-3" style="font-size:calc(50px * var(--tz));">a equipe limita,</p>
      <p class="font-montserrat font-black text-white leading-none mt-3" style="font-size:calc(50px * var(--tz));">a regra decide.</p>
      <div class="bg-gold mt-8 mb-6" style="width:100px; height:4px;"></div>
      <p class="text-gray-400 text-sm font-montserrat font-bold uppercase tracking-widest" style="margin-bottom:12px;">Para a discussão de hoje</p>
      <div class="flex flex-col gap-3">
{perg}
      </div>
    </div>
    <div class="col-span-6 flex flex-col gap-4">
{rec}
    </div>
  </div>
  <div class="relative z-10 px-24 pb-10 flex justify-between items-end border-t border-gray-700 pt-6 mx-8">
    <div><p class="font-montserrat font-bold text-white text-xl">Obrigado.</p>
      <p class="text-gray-400 text-sm mt-1">Pedro Henrique Soares · Gerente de Planejamento e Inteligência da Fiscalização (GPF) · SFC — ANTAQ · www.gov.br/antaq</p></div>
    <div class="text-right"><p class="text-gray-400 text-sm">{TITULO_DECK} · 2ª Oficina de Integração</p>
      <p class="text-gray-500 text-sm font-montserrat font-bold tracking-wider mt-1">{TOTAL} / {TOTAL}</p></div>
  </div>
  <div class="absolute bottom-24 left-1/2 transform -translate-x-1/2 opacity-5" style="z-index:0;"><img src="assets/logo-antaq-branca.png" alt="" style="height:220px;"></div>
</div>
<script src="zoom.js"></script>
<script src="anim.js"></script>
{NAV}
</body>
</html>
"""


def render(s):
    css = f':root {{ --tz-base: {s["base"]:.4g}; }}\n' + BASE_CSS + s["extra_css"]
    tag, ico = MODULOS[s["mod"]]
    return HEAD.format(title=f'{s["title"]} — {TITULO_DECK}', css=css, kicker=s["kicker"], titulo=s["titulo"],
                       tag=tag, tagico=ico, body=s["body"], rodape=RODAPE, n=s["n"], total=TOTAL,
                       head_extra=s["head_extra"], js_extra=s["js_extra"])


assert sorted(s["n"] for s in SLIDES) == list(range(2, TOTAL))
(DST / "slide-01.html").write_text(versiona(CAPA), encoding="utf-8")
print("slide-01.html (capa)")
for s in sorted(SLIDES, key=lambda s: s["n"]):
    (DST / f"slide-{s['n']:02d}.html").write_text(versiona(render(s)), encoding="utf-8")
    print(f"slide-{s['n']:02d}.html")
(DST / f"slide-{TOTAL:02d}.html").write_text(versiona(encerramento()), encoding="utf-8")
print(f"slide-{TOTAL:02d}.html (encerramento)")
