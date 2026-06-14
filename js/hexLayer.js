// ─── HEX BINNING — zoom-independent (size in real-world METERS) ──
// Grid indices are computed purely from geography, never from screen pixels.
// hexSize is the hex radius in meters. Changing zoom never affects bin assignment.

const EARTH = 40075016.686;
const M_PER_DEG = EARTH / 360;
const REF_LAT   = 28.62;
const M_PER_LNG = M_PER_DEG * Math.cos(REF_LAT * Math.PI / 180);

function latLngToHex(lat, lng, radiusM) {
  const dx = radiusM * Math.sqrt(3);
  const dy = radiusM * 1.5;
  const px = lng * M_PER_LNG;
  const py = lat * M_PER_DEG;
  const col = Math.round(px / dx);
  const row = Math.round(py / dy);
  return { col, row };
}

function hexCenter(col, row, radiusM) {
  const dx = radiusM * Math.sqrt(3);
  const dy = radiusM * 1.5;
  const px = col * dx + (((row % 2) + 2) % 2 === 0 ? 0 : dx / 2);
  const py = row * dy;
  return {
    lat: py / M_PER_DEG,
    lng: px / M_PER_LNG,
  };
}

function hexRing(cLat, cLng, radiusM) {
  const mPerLat = M_PER_DEG;
  const mPerLng = M_PER_DEG * Math.cos(cLat * Math.PI / 180);
  return Array.from({ length: 6 }, (_, i) => {
    const ang = Math.PI / 180 * (60 * i - 30);
    return [
      cLat + (radiusM * Math.sin(ang)) / mPerLat,
      cLng + (radiusM * Math.cos(ang)) / mPerLng,
    ];
  });
}

function hexToColor(hex, alpha) {
  const r = parseInt(hex.slice(1,3),16);
  const g = parseInt(hex.slice(3,5),16);
  const b = parseInt(hex.slice(5,7),16);
  return `rgba(${r},${g},${b},${alpha})`;
}

function drawHex(pts) {
  const showAnom = document.getElementById('chk-anom').checked;
  const useWeight = document.getElementById('chk-weight').checked;
  const bins = new Map();
  const radiusM = hexSize; // hexSize IS the real-world meter radius — zoom independent

  pts.forEach(p => {
    ['home','work'].forEach(loc => {
      const w = useWeight ? (loc==='home' ? 0.7 : 0.3) : 0.5;
      const { col, row } = latLngToHex(p[loc].lat, p[loc].lng, radiusM);
      const key = `${col}_${row}`;
      if (!bins.has(key)) bins.set(key, { col, row, pts: [] });
      bins.get(key).pts.push({ ...p, w, loc });
    });
  });

  const maxN = Math.max(...[...bins.values()].map(b => b.pts.length), 1);

  bins.forEach(bin => {
    const n = bin.pts.length;
    const hasAnom = showAnom && bin.pts.some(p => p.isAnom);
    const wSum = bin.pts.reduce((s,p) => s+p.w, 0);
    const dCount = {};
    bin.pts.forEach(p => { dCount[p.disease] = (dCount[p.disease]||0)+1; });
    const topD = Object.entries(dCount).sort((a,b)=>b[1]-a[1])[0][0];
    const center = hexCenter(bin.col, bin.row, radiusM);
    const verts  = hexRing(center.lat, center.lng, radiusM * 0.88);
    const opacity = 0.25 + 0.65*(n/maxN);
    const fillColor = hasAnom ? '#E8253A' : COLORS[topD];

    const poly = L.polygon(verts, {
      fillColor,
      fillOpacity: opacity,
      color: hasAnom ? '#ffffff' : '#0B0E14',
      weight: hasAnom ? 2 : 0.8,
      opacity: hasAnom ? 0.9 : 0.5,
    }).addTo(map);

    const tt = document.getElementById('tt');
    poly.on('mouseover', function(e) {
      const rows = Object.entries(dCount).map(([d,c]) =>
        `<div class="tt-row"><span>${d}</span><span>${c}</span></div>`).join('');
      tt.innerHTML = `
        <div class="tt-title">${topD} cluster</div>
        ${rows}
        <div class="tt-row"><span>Total</span><span>${n}</span></div>
        <div class="tt-row"><span>Weighted</span><span>${wSum.toFixed(1)}</span></div>
        ${hasAnom ? '<div class="tt-anom">⚠ OUTBREAK ANOMALY</div>' : ''}
      `;
      tt.style.display = 'block';
      this.setStyle({ weight: hasAnom ? 3 : 2, fillOpacity: Math.min(opacity+0.15, 0.95) });
    });
    poly.on('mousemove', function(e) {
      tt.style.left = (e.originalEvent.clientX + 14) + 'px';
      tt.style.top  = (e.originalEvent.clientY - 20) + 'px';
    });
    poly.on('mouseout', function() {
      tt.style.display = 'none';
      this.setStyle({ weight: hasAnom ? 2 : 0.8, fillOpacity: opacity });
    });
    poly.on('click', function() {
      const rows = Object.entries(dCount).map(([d,c]) =>
        `<div class="pop-row"><span>${d}</span><span>${c}</span></div>`).join('');
      this.bindPopup(`
        <div class="pop-title">${topD} — ${n} cases</div>
        ${rows}
        <div class="pop-row"><span>Weighted load</span><span>${wSum.toFixed(1)}</span></div>
        <div class="pop-row"><span>Anomaly</span><span>${hasAnom ? 'YES ⚠' : 'No'}</span></div>
        ${hasAnom ? '<div class="pop-anom">⚠ OUTBREAK ANOMALY FLAGGED</div>' : ''}
      `).openPopup();
    });

    hexLayers.push(poly);
  });
}
