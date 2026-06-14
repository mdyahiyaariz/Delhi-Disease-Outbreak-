// ─── DOTS ─────────────────────────────────────────────────────────
function drawDots(pts) {
  const showAnom = document.getElementById('chk-anom').checked;
  pts.forEach(p => {
    const isA = showAnom && p.isAnom;
    const col = isA ? '#E8253A' : COLORS[p.disease];
    const m = L.circleMarker([p.home.lat, p.home.lng], {
      radius: isA ? 7 : 5,
      fillColor: col,
      fillOpacity: 0.85,
      color: '#0B0E14',
      weight: 1.2,
    }).addTo(map);
    m.on('click', () => {
      m.bindPopup(`
        <div class="pop-title">${p.id} · ${p.disease}</div>
        <div class="pop-row"><span>Date</span><span>${p.date}</span></div>
        <div class="pop-row"><span>Confidence</span><span>${(p.conf*100).toFixed(0)}%</span></div>
        <div class="pop-row"><span>Week</span><span>${p.week}</span></div>
        <div class="pop-row"><span>Cluster</span><span>${p.cid < 0 ? 'noise' : p.cid}</span></div>
        ${isA ? '<div class="pop-anom">⚠ ANOMALY FLAGGED</div>' : ''}
      `).openPopup();
    });
    dotLayers.push(m);
  });
}
