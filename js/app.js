// ─── CLEAR / RENDER ───────────────────────────────────────────────
function clearAll() {
  hexLayers.forEach(l => map.removeLayer(l)); hexLayers = [];
  dotLayers.forEach(l => map.removeLayer(l)); dotLayers = [];
  if (heatLayer) { map.removeLayer(heatLayer); heatLayer = null; }
}

function render() {
  clearAll();
  const pts = currentDisease === 'all'
    ? PATIENTS
    : PATIENTS.filter(p => p.disease === currentDisease);
  if (currentLayer === 'hex'  || currentLayer === 'all') drawHex(pts);
  if (currentLayer === 'heat' || currentLayer === 'all') drawHeat(pts);
  if (currentLayer === 'dots' || currentLayer === 'all') drawDots(pts);
}

// ─── UI WIRING ────────────────────────────────────────────────────
function setLayer(l, btn) {
  currentLayer = l;
  document.querySelectorAll('.pill').forEach(b => b.classList.remove('on'));
  btn.classList.add('on');
  render();
}
function setDisease(d, btn) {
  currentDisease = d;
  document.querySelectorAll('.dis-btn').forEach(b => b.classList.remove('on'));
  btn.classList.add('on');
  render();
}
function setHexSize(v) {
  hexSize = v;
  document.getElementById('lv-hex').textContent = v + 'm';
  if (currentLayer==='hex'||currentLayer==='all') render();
}
function setHeatRadius(v) {
  heatRadius = v; document.getElementById('lv-hr').textContent = v;
  if (heatLayer) heatLayer.setOptions({ radius: v });
}
function setHeatBlur(v) {
  heatBlur = v; document.getElementById('lv-hb').textContent = v;
  if (heatLayer) heatLayer.setOptions({ blur: v });
}

// hex grid is zoom-independent — no zoomend re-render needed

// ─── INIT STATS & ALERTS ─────────────────────────────────────────
function initUI() {
  const byD = {Dengue:0,Cholera:0,Typhoid:0};
  PATIENTS.forEach(p => byD[p.disease]++);
  const anoms = PATIENTS.filter(p => p.isAnom);
  const clusterIds = [...new Set(PATIENTS.filter(p=>p.cid>=0).map(p=>p.cid))];

  document.getElementById('h-total').textContent    = PATIENTS.length;
  document.getElementById('h-clusters').textContent = clusterIds.length;
  document.getElementById('h-alerts').textContent   = anoms.length;
  document.getElementById('c-all').textContent      = PATIENTS.length;
  document.getElementById('c-dengue').textContent   = byD.Dengue;
  document.getElementById('c-cholera').textContent  = byD.Cholera;
  document.getElementById('c-typhoid').textContent  = byD.Typhoid;

  // Build alert list grouped by cluster+disease
  const grp = {};
  anoms.forEach(p => {
    const k = `${p.cid}_${p.disease}`;
    if (!grp[k]) grp[k] = { disease:p.disease, cid:p.cid, n:0, lat:0, lng:0, weeks:new Set() };
    grp[k].n++;
    grp[k].lat += p.home.lat;
    grp[k].lng += p.home.lng;
    grp[k].weeks.add(p.week);
  });
  const alertEl = document.getElementById('alert-list');
  alertEl.innerHTML = '';
  Object.values(grp).sort((a,b)=>b.n-a.n).forEach(g => {
    g.lat /= g.n; g.lng /= g.n;
    const div = document.createElement('div');
    div.className = 'alert-item';
    div.innerHTML = `
      <div class="al-title">${g.disease} · Cluster ${g.cid}</div>
      <div class="al-meta">${g.n} cases · ${g.weeks.size} anomaly weeks</div>
    `;
    div.onclick = () => map.flyTo([g.lat, g.lng], 15, { duration: 1.2 });
    alertEl.appendChild(div);
  });
}

initUI();
render();
