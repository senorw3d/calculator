/**
 * HIGH-PERFORMANCE MAIN APP CONTROLLER (TRADING DESK STANDARD)
 * Integrates FinancialMath engine, dataset with real BYMA ONs, multi-dimensional grouping filters,
 * Chart.js Yield Curve, Arbitrage Scanner, Portfolio Manager, and UI controls.
 */

import { FinancialMath } from './financial-math.js?v=1.0.1';
import { BONDS_DATASET, RATINGS_LIST, SECTORS_LIST, RATING_EQUIVALENCE_TABLE } from './data.js?v=1.0.1';
import { MarketApiConnector } from './api.js?v=1.0.1';
import { BymaCustodyApi } from './byma-api.js?v=1.0.1';

class TradingDeskApp {
  constructor() {
    this.bonds = JSON.parse(JSON.stringify(BONDS_DATASET));
    this.calculatedBonds = [];
    this.settlementMode = 'T+1';

    // Main Control Bar Multi-Grouping State
    this.selectedGroup = 'USD MEP';
    this.selectedRating = 'Todos';
    this.searchQuery = '';

    this.favorites = this.loadFavorites();
    this.activeView = 'view-table';
    this.rafPending = false;

    // Dedicated Curve View Filters State
    this.curveIssuer = 'Todos';
    this.curveRating = 'Todos';
    this.curveSector = 'Todos';
    this.curveMaturity = 'Todos';

    this.apiConnector = new MarketApiConnector();
    this.bymaApi = new BymaCustodyApi('homologacion');
    this.selectedBondForModal = null;

    this.init();
  }

  loadFavorites() {
    try {
      const saved = localStorage.getItem('argen_bonds_watchlist');
      const parsed = saved ? JSON.parse(saved) : null;
      if (Array.isArray(parsed)) return parsed;
      return ['bond_ym34d', 'bond_ymcid', 'bond_tlcmd', 'bond_ircpd'];
    } catch (e) {
      return ['bond_ym34d', 'bond_ymcid', 'bond_tlcmd', 'bond_ircpd'];
    }
  }

  saveFavorites() {
    try {
      localStorage.setItem('argen_bonds_watchlist', JSON.stringify(this.favorites));
    } catch (e) {
      console.error("Failed to save favorites", e);
    }
  }

  init() {
    const savedTheme = localStorage.getItem('argen_bonds_theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    this.recalculateAllBonds();
    this.renderRatingTabs();
    this.setupEventListeners();
    this.updateMarketStatusBadge();
    this.renderRatingEquivalenceTable();
    this.requestDashboardUpdate();
    this.startLiveTicksSimulation();
  }

  requestDashboardUpdate() {
    if (this.rafPending) return;
    this.rafPending = true;
    requestAnimationFrame(() => {
      this.updateDashboard();
      this.rafPending = false;
    });
  }

  updateMarketStatusBadge() {
    const badgeText = document.getElementById('live-status-text');
    if (!badgeText) return;

    if (this.apiConnector.isMarketOpen()) {
      badgeText.textContent = 'BYMA / MAE LIVE • OPEN';
    } else {
      badgeText.textContent = 'BYMA / MAE READY • MARKET CLOSED';
    }
  }

  generateCashFlows(bond) {
    if (!bond.maturity) return bond.cashFlows || [];
    
    const matParts = bond.maturity.split('-');
    if (matParts.length !== 3) return bond.cashFlows || [];
    const matYear = parseInt(matParts[0]);
    const matMonth = parseInt(matParts[1]);
    const matDay = parseInt(matParts[2]);
    
    const freq = bond.frequency || 2;
    const intervalMonths = 12 / freq;

    let startYear = 2025;
    let startMonth = matMonth;

    const flowDates = [];
    let curY = startYear;
    let curM = startMonth;

    while (curY > 2025 || (curY === 2025 && curM > 1)) {
      curM -= intervalMonths;
      if (curM <= 0) {
        curM += 12;
        curY -= 1;
      }
    }

    while (curY < matYear || (curY === matYear && curM <= matMonth)) {
      const formattedDate = `${curY}-${String(curM).padStart(2, '0')}-${String(matDay).padStart(2, '0')}`;
      if (!flowDates.includes(formattedDate)) {
        flowDates.push(formattedDate);
      }
      curM += intervalMonths;
      if (curM > 12) {
        curM -= 12;
        curY += 1;
      }
    }

    if (!flowDates.includes(bond.maturity)) {
      flowDates.push(bond.maturity);
    }
    flowDates.sort();

    const n = flowDates.length;
    let residual = 100.0;
    const couponRate = bond.couponRate || 8.0;
    const periodCouponPct = couponRate / freq;
    
    const isAmortizable = bond.structureType === 'Amortizable';
    const amortYears = [matYear - 2, matYear - 1, matYear];

    const result = [];
    for (let i = 0; i < n; i++) {
      const dateStr = flowDates[i];
      const parts = dateStr.split('-');
      const y = parseInt(parts[0]);
      const m = parseInt(parts[1]);
      const isLast = (i === n - 1);
      
      let amort = 0;
      if (isAmortizable && m === matMonth && amortYears.includes(y)) {
        if (y === matYear) {
          amort = residual;
        } else {
          amort = 33.33;
        }
      } else if (!isAmortizable && isLast) {
        amort = 100.0;
      }

      if (isLast) {
        amort = residual;
      }

      const cpnAmount = Number(((residual * periodCouponPct) / 100.0).toFixed(3));
      const totalAmount = Number((amort + cpnAmount).toFixed(3));
      const nextResidual = Math.max(0, Number((residual - amort).toFixed(2)));

      result.push({
        date: dateStr,
        amortization: amort,
        coupon: Number(periodCouponPct.toFixed(3)),
        amount: totalAmount,
        residual: nextResidual
      });

      residual = nextResidual;
    }

    return result;
  }

  recalculateAllBonds() {
    const settlementDate = FinancialMath.getSettlementDate(this.settlementMode);

    this.calculatedBonds = this.bonds.map(bond => {
      const cashFlows = this.generateCashFlows(bond);

      const accruedInterest = FinancialMath.calculateAccruedInterest(
        bond.couponRate,
        bond.lastCouponDate || '2026-01-01',
        settlementDate,
        '30/360',
        100
      );

      const dirtyPrice = bond.cleanPrice + accruedInterest;
      const technicalValue = FinancialMath.calculateTechnicalValue(100, accruedInterest);
      const parity = FinancialMath.calculateParity(dirtyPrice, technicalValue);

      const tir = FinancialMath.calculateTIR(
        dirtyPrice,
        cashFlows,
        settlementDate,
        bond.frequency
      );

      const { macaulayDuration, modifiedDuration, convexity, dv01 } = FinancialMath.calculateRiskMetrics(
        dirtyPrice,
        cashFlows,
        tir,
        settlementDate,
        bond.frequency
      );

      return {
        ...bond,
        cashFlows,
        settlementDate,
        accruedInterest: Number(accruedInterest.toFixed(2)),
        dirtyPrice: Number(dirtyPrice.toFixed(2)),
        technicalValue: Number(technicalValue.toFixed(2)),
        parity: Number(parity.toFixed(1)),
        tir: Number(tir.toFixed(2)),
        duration: modifiedDuration,
        macaulayDuration,
        convexity,
        dv01
      };
    });
  }

  renderRatingTabs() {
    const container = document.getElementById('rating-tabs-container');
    if (!container) return;

    let uniqueRatings = [...new Set(BONDS_DATASET.map(b => b.rating))].sort();
    uniqueRatings.unshift('Todos'); // Add a "Todos" option at the beginning

    const fragment = document.createDocumentFragment();
    uniqueRatings.forEach(r => {
      const btn = document.createElement('button');
      btn.className = `rating-btn ${r === this.selectedRating ? 'active' : ''}`;
      btn.dataset.rating = r;
      btn.textContent = r;
      btn.addEventListener('click', (e) => {
        this.selectedRating = e.target.dataset.rating;
        this.renderRatingTabs();
        this.requestDashboardUpdate();
      });
      fragment.appendChild(btn);
    });

    container.innerHTML = '';
    container.appendChild(fragment);
  }

  renderRatingEquivalenceTable() {
    const tbody = document.getElementById('rating-equivalence-tbody');
    if (!tbody) return;

    tbody.innerHTML = RATING_EQUIVALENCE_TABLE.map(row => `
      <tr>
        <td style="font-weight: 700; color: var(--accent-lime);">${row.grade}</td>
        <td class="num-tabular text-cyan">${row.fix}</td>
        <td class="num-tabular">${row.moodys}</td>
        <td class="num-tabular">${row.sp}</td>
        <td class="num-tabular text-yellow">${row.globalEquivalent}</td>
      </tr>
    `).join('');
  }

  setupEventListeners() {
    // Navigation Tabs




    // Main Control Bar Multi-Grouping Filters
    document.getElementById('search-input')?.addEventListener('input', (e) => {
      this.searchQuery = e.target.value.toLowerCase().trim();
      this.requestDashboardUpdate();
    });

    // Main Navigation Tabs (Grouping & Favorites)
    const navTabs = document.querySelectorAll('#main-tabs .nav-btn');
    navTabs.forEach(btn => {
      btn.addEventListener('click', (e) => {
        navTabs.forEach(t => t.classList.remove('active'));
        e.target.classList.add('active');
        this.selectedGroup = e.target.dataset.group;
        this.requestDashboardUpdate();
      });
    });



    // Theme Toggle
    document.getElementById('theme-toggle')?.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('argen_bonds_theme', next);
      this.requestDashboardUpdate();
    });

    // Rating Guide Modal Triggers
    document.getElementById('btn-rating-guide')?.addEventListener('click', () => {
      document.getElementById('rating-guide-modal')?.classList.add('active');
    });

    document.getElementById('rating-guide-modal-close')?.addEventListener('click', () => {
      document.getElementById('rating-guide-modal')?.classList.remove('active');
    });

    // API Config Modal Triggers
    document.getElementById('btn-api-config')?.addEventListener('click', () => {
      document.getElementById('api-modal')?.classList.add('active');
    });

    document.getElementById('api-modal-close')?.addEventListener('click', () => {
      document.getElementById('api-modal')?.classList.remove('active');
    });

    // BYMA Custody API - List Asset Classes
    document.getElementById('btn-fetch-asset-classes')?.addEventListener('click', async () => {
      const token = document.getElementById('api-key-input')?.value?.trim();
      const env = document.getElementById('byma-env-select')?.value || 'homologacion';
      const statusDiv = document.getElementById('byma-api-status');

      if (!token) {
        if (statusDiv) {
          statusDiv.style.display = 'block';
          statusDiv.style.color = 'var(--accent-red, #ff4d4d)';
          statusDiv.textContent = '❌ Por favor ingresa el OAuth 2.0 Bearer Token para conectar a BYMA.';
        }
        return;
      }

      if (statusDiv) {
        statusDiv.style.display = 'block';
        statusDiv.style.color = 'var(--accent-cyan)';
        statusDiv.textContent = `⏳ Consultando asset-classes en BYMA (${env})... (polling UUID si corresponde)`;
      }

      try {
        this.bymaApi.setEnvironment(env);
        const classes = await this.bymaApi.getAssetClasses(token);
        if (statusDiv) {
          statusDiv.style.color = 'var(--accent-lime)';
          statusDiv.textContent = `✅ Éxito! Se obtuvieron ${classes.length} clases de activos desde BYMA (${env}).`;
        }
        console.log('[BYMA API Asset Classes]', classes);
      } catch (err) {
        if (statusDiv) {
          statusDiv.style.color = 'var(--accent-red, #ff4d4d)';
          statusDiv.textContent = `❌ Error consultando BYMA API: ${err.message}`;
        }
      }
    });

    // BYMA Custody API - Save & Sync Instruments
    document.getElementById('btn-save-api')?.addEventListener('click', async () => {
      const token = document.getElementById('api-key-input')?.value?.trim();
      const env = document.getElementById('byma-env-select')?.value || 'homologacion';
      const assetClass = document.getElementById('byma-asset-class')?.value || 'ACCIONES';
      const cvsaId = document.getElementById('byma-cvsa-id')?.value || '';
      const statusDiv = document.getElementById('byma-api-status');

      if (!token) {
        if (statusDiv) {
          statusDiv.style.display = 'block';
          statusDiv.style.color = 'var(--accent-red, #ff4d4d)';
          statusDiv.textContent = '❌ Se requiere un Bearer Token válido para sincronizar con BYMA.';
        }
        return;
      }

      if (statusDiv) {
        statusDiv.style.display = 'block';
        statusDiv.style.color = 'var(--accent-cyan)';
        statusDiv.textContent = `⏳ Sincronizando instrumentos estandarizados desde BYMA ${env}...`;
      }

      try {
        this.bymaApi.setEnvironment(env);
        const instruments = await this.bymaApi.getStandardInstruments(assetClass, cvsaId, token);

        if (Array.isArray(instruments) && instruments.length > 0) {
          const newBonds = instruments.map(item => this.bymaApi.transformToBondSchema(item));
          
          // Merge new BYMA instruments into existing bonds
          newBonds.forEach(nb => {
            const idx = this.bonds.findIndex(b => b.ticker === nb.ticker || b.id === nb.id);
            if (idx >= 0) {
              this.bonds[idx] = { ...this.bonds[idx], ...nb };
            } else {
              this.bonds.push(nb);
            }
          });

          this.recalculateAllBonds();
          this.requestDashboardUpdate();

          if (statusDiv) {
            statusDiv.style.color = 'var(--accent-lime)';
            statusDiv.textContent = `✅ Conectado y Sincronizado! Se procesaron ${instruments.length} instrumentos desde BYMA.`;
          }
          setTimeout(() => {
            document.getElementById('api-modal')?.classList.remove('active');
          }, 1500);
        } else {
          if (statusDiv) {
            statusDiv.style.color = 'var(--accent-yellow)';
            statusDiv.textContent = `⚠️ La API de BYMA respondió correctamente pero no devolvió registros para la búsqueda.`;
          }
        }
      } catch (err) {
        if (statusDiv) {
          statusDiv.style.color = 'var(--accent-red, #ff4d4d)';
          statusDiv.textContent = `❌ Error al sincronizar con BYMA: ${err.message}`;
        }
      }
    });

    // Bond Detail Modal Close
    document.getElementById('modal-close-btn')?.addEventListener('click', () => {
      document.getElementById('bond-modal')?.classList.remove('active');
    });
    // Modal Real-Time Calculator Listeners
    const calcCleanInput = document.getElementById('calc-clean-price');
    const calcTirInput = document.getElementById('calc-result-tir');
    const fxRateInput = document.getElementById('calc-fx-rate');

    this.modalCurrency = 'MEP'; // Default 'MEP', 'CCL', 'ARS'

    document.querySelectorAll('.btn-calc-curr').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.btn-calc-curr').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.modalCurrency = btn.dataset.curr;
        this.refreshModalCurrencyView();
      });
    });

    fxRateInput?.addEventListener('input', () => {
      if (this.modalCurrency === 'ARS') {
        this.refreshModalCurrencyView();
      }
    });

    calcCleanInput?.addEventListener('input', (e) => {
      const newCleanPrice = parseFloat(e.target.value);
      if (!isNaN(newCleanPrice) && this.selectedBondForModal) {
        this.updateModalCalculatorFromCleanPrice(newCleanPrice);
      }
    });

    calcTirInput?.addEventListener('input', (e) => {
      const targetTIR = parseFloat(e.target.value);
      if (!isNaN(targetTIR) && this.selectedBondForModal) {
        this.updateModalCalculatorFromTIR(targetTIR);
      }
    });

    // CSV Exporter
    document.getElementById('btn-export-csv')?.addEventListener('click', () => {
      if (this.selectedBondForModal) {
        this.exportCashFlowsToCSV(this.selectedBondForModal);
      }
    });
  }

  getFilteredBonds() {
    return this.calculatedBonds.filter(b => {
      const matchSearch = !this.searchQuery ||
        b.ticker.toLowerCase().includes(this.searchQuery) ||
        b.isin.toLowerCase().includes(this.searchQuery) ||
        b.issuer.toLowerCase().includes(this.searchQuery);

      let matchGroup = true;
      if (this.selectedGroup === 'Favoritos') {
        matchGroup = Array.isArray(this.favorites) && this.favorites.includes(b.id);
      } else if (this.selectedGroup !== 'Todos') {
        matchGroup = b.instrumentGroup === this.selectedGroup;
      }
      const matchRating = this.selectedRating === 'Todos' || b.rating === this.selectedRating;

      return matchSearch && matchGroup && matchRating;
    });
  }

  updateDashboard() {
    const filteredBonds = this.getFilteredBonds();
    this.renderBondsTable(filteredBonds);
  }

  renderBondsTable(bondsList) {
    const tbody = document.getElementById('bonds-table-body');
    if (!tbody) return;

    if (bondsList.length === 0) {
      tbody.innerHTML = `<tr><td colspan="12" style="text-align: center; color: var(--text-dim); padding: 2rem;">No se encontraron especies con los filtros seleccionados</td></tr>`;
      return;
    }

    tbody.innerHTML = bondsList.map(b => {
      const isFav = this.favorites.includes(b.id);
      return `
        <tr id="row-${b.id}" data-id="${b.id}">
          <td style="text-align: center;">
            <button class="fav-btn ${isFav ? 'active' : ''}" onclick="event.stopPropagation(); window.app.toggleFavorite('${b.id}')">
              ${isFav ? '★' : '☆'}
            </button>
          </td>
          <td>
            <div style="font-weight: 700; color: var(--accent-lime);">${b.ticker}</div>
            <div style="font-size: 0.7rem; color: var(--text-dim);">${b.isin}</div>
          </td>
          <td>
            <div style="font-weight: 600;">${b.shortIssuer}</div>
            <div style="font-size: 0.7rem; color: var(--text-muted);">${b.sector}</div>
          </td>
          <td>
            <span class="badge badge-sector">${b.instrumentGroup}</span>
          </td>
          <td>
            <span class="badge badge-law">${b.structureType}</span>
          </td>
          <td style="text-align: center; font-weight: 700; color: ${b.isCallable ? 'var(--accent-cyan)' : 'var(--text-muted)'};">
            ${b.isCallable ? 'Sí' : 'No'}
          </td>
          <td>
            <span class="badge badge-rating">${b.rating}</span>
            <div style="font-size: 0.65rem; color: var(--text-dim); margin-top: 2px;">${b.ratingAgency || 'FIX'}</div>
          </td>
          <td>
            <span class="badge ${b.law === 'Nueva York' ? 'badge-law' : 'badge-sector'}">${b.law}</span>
          </td>
          <td class="num-tabular">${this.formatDate(b.maturity)}</td>
          <td class="num-tabular text-lime" style="font-weight: 700;">${b.tir.toFixed(2)}%</td>
          <td class="num-tabular">${b.duration.toFixed(2)} yrs</td>
          <td class="num-tabular text-cyan" style="font-weight: 700; font-size: 1.05em;">${b.parity.toFixed(1)}%</td>
          <td class="num-tabular" style="font-weight: 700; font-size: 1.05em;">
            <div>$${b.cleanPrice.toFixed(2)}</div>
            <div style="font-size: 0.7rem; color: var(--text-muted); font-weight: 400;">$${b.dirtyPrice.toFixed(2)} dirty</div>
          </td>
        </tr>
      `;
    }).join('');

    tbody.querySelectorAll('tr[data-id]').forEach(tr => {
      tr.addEventListener('click', () => {
        const id = tr.dataset.id;
        const bond = this.calculatedBonds.find(b => b.id === id);
        if (bond) this.openModal(bond);
      });
    });
  }

  formatDate(dateStr) {
    if (!dateStr) return '';
    const parts = dateStr.split('T')[0].split('-');
    if (parts.length === 3) {
      return `${parts[2]}/${parts[1]}/${parts[0]}`;
    }
    return dateStr;
  }

  toggleFavorite(bondId) {
    if (this.favorites.includes(bondId)) {
      this.favorites = this.favorites.filter(id => id !== bondId);
    } else {
      this.favorites.push(bondId);
    }
    this.saveFavorites();
    this.requestDashboardUpdate();
  }

  getFxRate() {
    const fxInput = document.getElementById('calc-fx-rate');
    return (fxInput && parseFloat(fxInput.value) > 0) ? parseFloat(fxInput.value) : 1280.0;
  }

  openModal(bond) {
    this.selectedBondForModal = bond;

    document.getElementById('modal-bond-ticker').textContent = `${bond.ticker} - ${bond.issuer}`;
    document.getElementById('modal-bond-isin').textContent = `ISIN: ${bond.isin} • Ley ${bond.law} • Especie: ${bond.instrumentGroup} • Estructura: ${bond.structureType}${bond.isCallable ? ' (Callable)' : ''} • Rating: ${bond.rating} (${bond.ratingAgency})`;

    this.refreshModalCurrencyView();

    document.getElementById('bond-modal')?.classList.add('active');
  }

  refreshModalCurrencyView() {
    const bond = this.selectedBondForModal;
    if (!bond) return;

    const curr = this.modalCurrency || 'MEP';
    const fxRate = this.getFxRate();
    const mult = (curr === 'ARS') ? fxRate : 1.0;
    const currSymbol = (curr === 'ARS') ? 'ARS $' : '$';

    document.getElementById('lbl-clean-price').textContent = `Precio Limpio (${curr})`;
    document.getElementById('lbl-accrued-interest').textContent = `Interés Corrido (${curr})`;
    document.getElementById('lbl-dirty-price').textContent = `Precio Sucio (${curr})`;

    const cleanVal = bond.cleanPrice * mult;
    const dirtyVal = bond.dirtyPrice * mult;
    const accruedVal = bond.accruedInterest * mult;

    document.getElementById('calc-clean-price').value = cleanVal.toFixed(2);
    document.getElementById('calc-accrued-interest').value = `${currSymbol}${accruedVal.toFixed(2)}`;
    document.getElementById('calc-dirty-price').value = `${currSymbol}${dirtyVal.toFixed(2)}`;
    document.getElementById('calc-result-tir').value = bond.tir.toFixed(2);
    document.getElementById('calc-result-parity').value = `${bond.parity.toFixed(1)}%`;
    document.getElementById('calc-result-duration').value = `${bond.duration.toFixed(2)} yrs`;

    const tbody = document.getElementById('modal-cashflows-body');
    if (tbody) {
      tbody.innerHTML = bond.cashFlows.map(cf => `
        <tr>
          <td class="num-tabular">${this.formatDate(cf.date)}</td>
          <td class="num-tabular">${cf.amortization > 0 ? cf.amortization + '%' : '-'}</td>
          <td class="num-tabular">${cf.coupon.toFixed(3)}%</td>
          <td class="num-tabular text-lime" style="font-weight: 700;">${currSymbol}${(cf.amount * mult).toFixed(2)}</td>
          <td class="num-tabular text-muted">${cf.residual}%</td>
        </tr>
      `).join('');
    }
  }

  updateModalCalculatorFromCleanPrice(inputCleanPrice) {
    const bond = this.selectedBondForModal;
    if (!bond) return;

    const curr = this.modalCurrency || 'MEP';
    const fxRate = this.getFxRate();
    const usdCleanPrice = (curr === 'ARS') ? (inputCleanPrice / fxRate) : inputCleanPrice;

    const dirtyPriceUSD = usdCleanPrice + bond.accruedInterest;
    const parity = FinancialMath.calculateParity(dirtyPriceUSD, bond.technicalValue);
    const tir = FinancialMath.calculateTIR(dirtyPriceUSD, bond.cashFlows, bond.settlementDate, bond.frequency);
    const { modifiedDuration } = FinancialMath.calculateRiskMetrics(dirtyPriceUSD, bond.cashFlows, tir, bond.settlementDate, bond.frequency);

    const mult = (curr === 'ARS') ? fxRate : 1.0;
    const currSymbol = (curr === 'ARS') ? 'ARS $' : '$';

    document.getElementById('calc-dirty-price').value = `${currSymbol}${(dirtyPriceUSD * mult).toFixed(2)}`;
    document.getElementById('calc-result-parity').value = `${parity.toFixed(1)}%`;
    document.getElementById('calc-result-tir').value = tir.toFixed(2);
    document.getElementById('calc-result-duration').value = `${modifiedDuration.toFixed(2)} yrs`;
  }

  updateModalCalculatorFromTIR(targetTIR) {
    const bond = this.selectedBondForModal;
    if (!bond) return;

    const curr = this.modalCurrency || 'MEP';
    const fxRate = this.getFxRate();
    const mult = (curr === 'ARS') ? fxRate : 1.0;
    const currSymbol = (curr === 'ARS') ? 'ARS $' : '$';

    const { cleanPrice, dirtyPrice } = FinancialMath.calculatePriceFromTIR(targetTIR, bond.cashFlows, bond.settlementDate, bond.accruedInterest, bond.frequency);
    const parity = FinancialMath.calculateParity(dirtyPrice, bond.technicalValue);
    const { modifiedDuration } = FinancialMath.calculateRiskMetrics(dirtyPrice, bond.cashFlows, targetTIR, bond.settlementDate, bond.frequency);

    document.getElementById('calc-clean-price').value = (cleanPrice * mult).toFixed(2);
    document.getElementById('calc-dirty-price').value = `${currSymbol}${(dirtyPrice * mult).toFixed(2)}`;
    document.getElementById('calc-result-parity').value = `${parity.toFixed(1)}%`;
    document.getElementById('calc-result-duration').value = `${modifiedDuration.toFixed(2)} yrs`;
  }

  exportCashFlowsToCSV(bond) {
    let csv = `Fecha Pago,Amortizacion (%),Cupon Renta (%),Flujo Total ($),Capital Residual (%)\n`;
    bond.cashFlows.forEach(cf => {
      csv += `${this.formatDate(cf.date)},${cf.amortization},${cf.coupon},${cf.amount},${cf.residual}\n`;
    });

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `Flujo_Fondos_${bond.ticker}_${bond.settlementDate}.csv`;
    link.click();
  }

  startLiveTicksSimulation() {
    setInterval(() => {
      const randomIndex = Math.floor(Math.random() * this.bonds.length);
      const targetBond = this.bonds[randomIndex];
      const delta = (Math.random() - 0.5) * 0.25;

      targetBond.cleanPrice = Math.max(10, Number((targetBond.cleanPrice + delta).toFixed(2)));

      this.recalculateAllBonds();

      const updatedRow = document.getElementById(`row-${targetBond.id}`);
      if (updatedRow) {
        updatedRow.classList.add('price-flash');
        setTimeout(() => updatedRow.classList.remove('price-flash'), 800);
      }

      this.requestDashboardUpdate();
    }, 4000);
  }
}

window.addEventListener('DOMContentLoaded', () => {
  window.app = new TradingDeskApp();
});
