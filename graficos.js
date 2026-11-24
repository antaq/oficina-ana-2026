/*
 * Gráficos do deck Fiscalização Responsiva na ANTAQ (ECharts 5, renderizador SVG).
 * Copiado do deck Desempenho Aquaviário 2025; as cores por papel valem para os grupos de risco.
 *
 * O SVG fica nítido quando o visualizador escala o iframe de 1920x1080 com transform;
 * o canvas borraria. Cores por papel, iguais em todos os slides: a área Porto é sempre
 * azul, Marítima laranja e Interior verde-água (paleta validada para daltonismo, com
 * rótulos diretos porque o verde-água fica abaixo de 3:1 sobre o branco).
 *
 * Cada gráfico começa a desenhar só depois que o card que o contém pousa (anim.js),
 * para não competir com a entrada das cartas.
 */
window.G = (function () {
  var C = {
    porto: '#0066CC', maritima: '#eb6834', interior: '#1baf7a',
    paf: '#0066CC', ext: '#eb6834', tup: '#eb6834', po: '#0066CC',
    grA: '#1baf7a', grB: '#0066CC', grC: '#DC2626', antes: '#94A3B8',
    marca: '#003366', ouro: '#FFD700',
    tinta: '#0F172A', tinta2: '#475569', apagado: '#64748B',
    grade: '#E2E8F0', base: '#CBD5E1', fundo: '#ffffff'
  };
  var FT = 'Montserrat, sans-serif', FC = "'Open Sans', sans-serif";
  var reduz = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function num(v, d) {
    if (v === null || v === undefined || isNaN(v)) return '—';
    return Number(v).toLocaleString('pt-BR', { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 });
  }
  function pct(v, d) { return num(v, d === undefined ? 1 : d) + '%'; }
  function mi(v, d) { return num(v / 1e6, d === undefined ? 1 : d) + ' mi t'; }

  function eixoCat(cats, extra) {
    return Object.assign({
      type: 'category', data: cats, axisTick: { show: false },
      axisLine: { lineStyle: { color: C.base } },
      axisLabel: { color: C.tinta2, fontFamily: FT, fontSize: 18, fontWeight: 600, margin: 14 }
    }, extra || {});
  }
  function eixoVal(extra) {
    return Object.assign({
      type: 'value', splitNumber: 4,
      axisLine: { show: false }, axisTick: { show: false },
      splitLine: { lineStyle: { color: C.grade, width: 1 } },
      axisLabel: { color: C.apagado, fontFamily: FC, fontSize: 16, formatter: function (v) { return num(v); } }
    }, extra || {});
  }
  function dica(extra) {
    return Object.assign({
      backgroundColor: '#ffffff', borderColor: '#E2E8F0', borderWidth: 1, padding: [10, 14],
      textStyle: { color: C.tinta, fontFamily: FC, fontSize: 16 },
      extraCssText: 'box-shadow:0 8px 24px rgba(15,23,42,.14); border-radius:10px;'
    }, extra || {});
  }
  function legenda(extra) {
    return Object.assign({
      top: 0, left: 0, icon: 'roundRect', itemWidth: 22, itemHeight: 10, itemGap: 26,
      textStyle: { color: C.tinta2, fontFamily: FT, fontSize: 17, fontWeight: 600 }
    }, extra || {});
  }

  /* Atraso até o card que contém o gráfico terminar de pousar. */
  function atraso(el) {
    if (reduz) return 0;
    var card = el.closest('.anim-carta');
    var d = card ? parseFloat(card.style.getPropertyValue('--d')) || 0 : 0;
    return (d + 0.45) * 1000;
  }

  function desenha(id, opcao) {
    var el = document.getElementById(id);
    if (!el || !window.echarts) return null;
    var ch = echarts.init(el, null, { renderer: 'svg' });
    var base = { animation: !reduz, animationDuration: 1100, animationEasing: 'cubicOut',
                 textStyle: { fontFamily: FC } };
    setTimeout(function () { ch.setOption(Object.assign(base, opcao)); }, atraso(el));
    window.addEventListener('resize', function () { ch.resize(); });
    return ch;
  }

  return { C: C, FT: FT, FC: FC, num: num, pct: pct, mi: mi, reduz: reduz, atraso: atraso,
           eixoCat: eixoCat, eixoVal: eixoVal, dica: dica, legenda: legenda, desenha: desenha };
})();
