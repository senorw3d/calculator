/**
 * YIELD CURVE SCATTER CHART & POLYNOMIAL FITTING ENGINE WITH HIGH CONTRAST THEMING
 * Renders Modified Duration (x-axis) vs TIR % (y-axis) with Chart.js
 * Draws Ticker Labels directly next to each point on the chart canvas with theme-aware contrast.
 */

export class YieldCurveChart {
  constructor(canvasId) {
    this.canvasId = canvasId;
    this.chart = null;
  }

  fitQuadraticCurve(points) {
    if (points.length < 3) return null;

    let n = points.length;
    let sumX = 0, sumY = 0, sumX2 = 0, sumX3 = 0, sumX4 = 0;
    let sumXY = 0, sumX2Y = 0;

    for (let p of points) {
      let x = p.x;
      let y = p.y;
      sumX += x;
      sumY += y;
      sumX2 += x * x;
      sumX3 += x * x * x;
      sumX4 += x * x * x * x;
      sumXY += x * y;
      sumX2Y += x * x * y;
    }

    const det = (matrix) => {
      return matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) -
             matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]) +
             matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]);
    };

    const A = [
      [n, sumX, sumX2],
      [sumX, sumX2, sumX3],
      [sumX2, sumX3, sumX4]
    ];

    const D = det(A);
    if (Math.abs(D) < 1e-9) return null;

    const Ac = [
      [sumY, sumX, sumX2],
      [sumXY, sumX2, sumX3],
      [sumX2Y, sumX3, sumX4]
    ];

    const Ab = [
      [n, sumY, sumX2],
      [sumX, sumXY, sumX3],
      [sumX2, sumX2Y, sumX4]
    ];

    const Aa = [
      [n, sumX, sumY],
      [sumX, sumX2, sumY],
      [sumX2, sumX3, sumX2Y]
    ];

    const c = det(Ac) / D;
    const b = det(Ab) / D;
    const a = det(Aa) / D;

    return (x) => a * x * x + b * x + c;
  }

  render(bonds, onSelectBond) {
    const canvas = document.getElementById(this.canvasId);
    if (!canvas) return;

    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const isLight = currentTheme === 'light';

    // Theme Colors
    const axisTextColor = isLight ? '#071126' : '#ffee00';
    const tickTextColor = isLight ? '#0f172a' : '#cbd5e1';
    const gridLineColor = isLight ? 'rgba(15, 23, 42, 0.12)' : 'rgba(255, 238, 0, 0.15)';
    const fittedLineColor = isLight ? '#b45309' : '#ffee00';
    const pointLabelColor = isLight ? '#071126' : '#ffee00';
    const pointOutlineColor = isLight ? '#ffffff' : '#071126';

    const points = bonds
      .filter(b => b.duration > 0 && b.tir > 0 && b.tir < 100)
      .map(b => ({
        x: b.duration,
        y: b.tir,
        ticker: b.ticker,
        issuer: b.shortIssuer,
        rating: b.rating,
        parity: b.parity,
        bondObj: b
      }));

    const minX = Math.min(...points.map(p => p.x), 0.5);
    const maxX = Math.max(...points.map(p => p.x), 5);
    const curveFunc = this.fitQuadraticCurve(points);

    const fittedLinePoints = [];
    if (curveFunc) {
      const step = (maxX - minX) / 30;
      for (let x = minX; x <= maxX + 0.1; x += step) {
        fittedLinePoints.push({ x: Number(x.toFixed(2)), y: Number(curveFunc(x).toFixed(2)) });
      }
    }

    if (this.chart) {
      this.chart.destroy();
    }

    // High-Contrast Theme-Aware Canvas Plugin for Ticker Labels
    const pointLabelsPlugin = {
      id: 'pointLabelsPlugin',
      afterDatasetsDraw(chart) {
        const ctx = chart.ctx;
        ctx.save();
        ctx.font = 'bold 11px "JetBrains Mono", monospace';
        ctx.fillStyle = pointLabelColor;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'bottom';

        const meta = chart.getDatasetMeta(0);
        if (meta && meta.data) {
          meta.data.forEach((element, index) => {
            const dataPoint = chart.data.datasets[0].data[index];
            if (dataPoint && dataPoint.ticker) {
              ctx.strokeStyle = pointOutlineColor;
              ctx.lineWidth = 3;
              ctx.strokeText(dataPoint.ticker, element.x, element.y - 7);
              ctx.fillText(dataPoint.ticker, element.x, element.y - 7);
            }
          });
        }
        ctx.restore();
      }
    };

    const ctx = canvas.getContext('2d');
    this.chart = new Chart(ctx, {
      type: 'scatter',
      data: {
        datasets: [
          {
            label: 'Obligaciones Negociables & Bonos',
            data: points,
            backgroundColor: (ctx) => {
              const raw = ctx.raw;
              if (!raw) return fittedLineColor;
              if (raw.rating && raw.rating.includes('AAA')) return isLight ? '#d97706' : '#ffee00';
              if (raw.rating && raw.rating.includes('AA')) return isLight ? '#0284c7' : '#38bdf8';
              return '#ea580c';
            },
            borderColor: pointOutlineColor,
            borderWidth: 1.5,
            pointRadius: 8,
            pointHoverRadius: 12
          },
          {
            label: 'Curva Teórica Ajustada (Fitted Curve)',
            data: fittedLinePoints,
            type: 'line',
            borderColor: fittedLineColor,
            borderWidth: 3,
            borderDash: [4, 4],
            fill: false,
            pointRadius: 0,
            tension: 0.4
          }
        ]
      },
      plugins: [pointLabelsPlugin],
      options: {
        responsive: true,
        maintainAspectRatio: false,
        onClick: (event, elements) => {
          if (elements.length > 0 && elements[0].datasetIndex === 0) {
            const index = elements[0].index;
            const selectedPoint = points[index];
            if (selectedPoint && onSelectBond) {
              onSelectBond(selectedPoint.bondObj);
            }
          }
        },
        plugins: {
          legend: {
            labels: {
              color: axisTextColor,
              font: { family: 'Inter, sans-serif', size: 12, weight: 'bold' }
            }
          },
          tooltip: {
            backgroundColor: isLight ? '#071126' : '#0d1d3d',
            titleColor: '#ffee00',
            bodyColor: '#ffffff',
            borderColor: isLight ? '#b45309' : '#ffee00',
            borderWidth: 1.5,
            titleFont: { family: 'Merriweather, serif', weight: 'bold' },
            bodyFont: { family: 'JetBrains Mono, monospace' },
            callbacks: {
              title: (items) => {
                const p = items[0].raw;
                return p.ticker ? `${p.ticker} - ${p.issuer}` : 'Curva Ajustada';
              },
              label: (item) => {
                const p = item.raw;
                if (!p.ticker) return `TIR Estimada: ${p.y}%`;
                return [
                  `Duration Modificada: ${p.x} años`,
                  `TIR (YTM): ${p.y.toFixed(2)}%`,
                  `Paridad: ${p.parity.toFixed(1)}%`,
                  `Rating: ${p.rating}`
                ];
              }
            }
          }
        },
        scales: {
          x: {
            title: {
              display: true,
              text: 'Modified Duration (Años)',
              color: axisTextColor,
              font: { family: 'Inter, sans-serif', weight: 'bold' }
            },
            grid: { color: gridLineColor },
            ticks: { color: tickTextColor, font: { family: 'JetBrains Mono, monospace', weight: 'bold' } }
          },
          y: {
            title: {
              display: true,
              text: 'TIR / YTM Anual (%)',
              color: axisTextColor,
              font: { family: 'Inter, sans-serif', weight: 'bold' }
            },
            grid: { color: gridLineColor },
            ticks: { color: tickTextColor, font: { family: 'JetBrains Mono, monospace', weight: 'bold' } }
          }
        }
      }
    });
  }
}
