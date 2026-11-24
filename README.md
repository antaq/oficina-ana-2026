# Fiscalização Responsiva na ANTAQ — 2ª Oficina ANA (25/11/2026)

Deck em HTML de 15 slides para a 2ª Oficina de Integração sobre Fiscalização do Uso de Recursos Hídricos (ANA, Brasília). O público são os fiscalizadores dos órgãos gestores estaduais e da ANA.

## Como ver

```bash
python3 -m http.server 8000   # rodar nesta pasta
# abrir http://localhost:8000/index.html
```

- **Navegação:** setas ←/→, Home e End.
- **Zoom:** botões +/− na barra.

## Como alterar

Edite `build_slides.py` e rode `python3 build_slides.py` para regenerar os `slide-NN.html`. Não edite os slides gerados direto, porque a próxima geração sobrescreve a mudança.

Para mudar a escala de um slide, ajuste o dicionário `BASES`. Os gráficos (ECharts em SVG) ficam em `graficos.js`, no objeto `window.G`.

## Estrutura

| Módulo | Slides |
|---|---|
| Capa | 01 |
| 1 · Origem | 02 Por que mudar · 03 Teoria responsiva · 04 Trajetória 2017–2026 · 05 O que a prática ensinou |
| 2 · IPR 2.0 | 06 Duas fases · 07 Da faixa à solução fiscal |
| 3 · PAF 2027 | 08 Do ranking ao plano · 09 Sorteio auditável · 10 Capacidade · 11 Equalização · 12 Orçamento fechado de horas |
| 4 · Lições | 13 Governança · 14 Desafios e alternativas |
| Encerramento | 15 |

## Fontes

- **Apresentações anteriores** desta pasta (`../*.pptx`).
- **NT nº 35/2026/GPF/SFC:** IPR 2.0 e grupo de risco do PAF 2027.
- **NT nº 36/2026:** ações temáticas, operacionais e de rito próprio, e a reserva de horas para extraordinárias.
- **Especificação técnica do IPR 2.0**, no projeto IPR-PAF.

## Ressalvas

- **Proposta, não decisão:** os números do PAF 2027 estão em deliberação na Diretoria Colegiada, e é assim que o deck os apresenta.
- **Ocupação por unidade:** os slides 10 e 11 mostram a ocupação da força de trabalho de cada unidade regional. Avalie antes de distribuir o arquivo fora da ANTAQ.
