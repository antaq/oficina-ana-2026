// Exporta o deck Oficina ANA 2026 para PDF vetorial, uma página por slide.
// Adaptado de ApresentacaoSFC/exportar-desempenho-2025/exportar-pdf.js.
// Uso: node exportar-pdf.js <pasta-do-deck> <arquivo-pdf>
const path = require('path');
const fs = require('fs');
const { execFileSync, spawn } = require('child_process');
const puppeteer = require('puppeteer-core');

const DECK = path.resolve(process.argv[2]);
const SAIDA = path.resolve(process.argv[3]);
const TMP = path.join(__dirname, 'tmp');
const TOTAL = 15;
const PORTA = 8792;
fs.rmSync(TMP, { recursive: true, force: true });
fs.mkdirSync(TMP, { recursive: true });

(async () => {
  // Servidor local: os scripts são chamados com ?v=<hash>, o que pede http, não file://.
  const srv = spawn('python3', ['-m', 'http.server', String(PORTA), '--bind', '127.0.0.1'], { cwd: DECK, stdio: 'ignore' });
  await new Promise(r => setTimeout(r, 1200));
  const nav = await puppeteer.launch({ executablePath: '/usr/bin/google-chrome', headless: true,
    args: ['--no-sandbox', '--font-render-hinting=none'] });
  try {
    const page = await nav.newPage();
    await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 2 });
    // "Reduzir movimento": anim.js e graficos.js desenham direto no estado final.
    const cdp = await page.createCDPSession();
    await cdp.send('Emulation.setEmulatedMedia', { media: 'screen',
      features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] });

    for (let n = 1; n <= TOTAL; n++) {
      const nn = String(n).padStart(2, '0');
      await page.goto(`http://127.0.0.1:${PORTA}/slide-${nn}.html`, { waitUntil: 'networkidle0', timeout: 60000 });
      await page.evaluate(() => document.fonts.ready);
      await new Promise(r => setTimeout(r, 2500));
      const d = await page.evaluate(() => {
        const h = document.documentElement;
        const ocultos = [...document.querySelectorAll('body *')].filter(e => e.offsetParent && e.innerText && e.innerText.trim()
          && parseFloat(getComputedStyle(e).opacity) < 0.99).length;
        const faltaIcone = [...document.querySelectorAll('i.fas, i.fa-solid')].filter(i => getComputedStyle(i, '::before').content === 'none').length;
        return { reduz: matchMedia('(prefers-reduced-motion: reduce)').matches, titulo: document.title.split(' — ')[0],
                 sw: h.scrollWidth, sh: h.scrollHeight, ocultos, faltaIcone,
                 graficos: document.querySelectorAll('.graf svg').length + '/' + document.querySelectorAll('.graf').length };
      });
      if (!d.reduz) throw new Error('reduzir movimento não valeu no slide ' + nn);
      await page.pdf({ path: path.join(TMP, `slide-${nn}.pdf`), width: '1920px', height: '1080px', printBackground: true,
        margin: { top: 0, right: 0, bottom: 0, left: 0 }, pageRanges: '1' });
      console.log(nn, d.titulo, `| ${d.sw}x${d.sh} | gráficos ${d.graficos} | ocultos ${d.ocultos} | ícones sem glifo ${d.faltaIcone}`);
    }
  } finally {
    await nav.close();
    srv.kill();
  }
  const pdfs = Array.from({ length: TOTAL }, (_, i) => path.join(TMP, `slide-${String(i + 1).padStart(2, '0')}.pdf`));
  execFileSync('pdfunite', [...pdfs, SAIDA]);
  console.log('ok', SAIDA);
})().catch(e => { console.error(e); process.exit(1); });
