// ─── HEATMAP ──────────────────────────────────────────────────────
function drawHeat(pts) {
  const useWeight = document.getElementById('chk-weight').checked;
  const data = [];
  pts.forEach(p => {
    const hw = useWeight ? 0.7 : 0.5;
    const ww = useWeight ? 0.3 : 0.5;
    data.push([p.home.lat, p.home.lng, hw * p.conf]);
    data.push([p.work.lat, p.work.lng, ww * p.conf]);
  });
  heatLayer = L.heatLayer(data, {
    radius: heatRadius,
    blur: heatBlur,
    maxZoom: 16,
    gradient: { 0.0:'transparent', 0.2:'#1a3a8a', 0.4:'#2B7FD4', 0.6:'#16A37A', 0.8:'#E85D30', 1.0:'#E8253A' },
  }).addTo(map);
}
