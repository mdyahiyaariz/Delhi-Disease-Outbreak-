// ─── STATE ────────────────────────────────────────────────────────
let currentLayer = 'hex';
let currentDisease = 'all';
let hexSize = 600; // fixed meters — zoom-independent
let heatRadius = 28;
let heatBlur = 18;

let hexLayers = [];
let heatLayer = null;
let dotLayers = [];

// ─── MAP SETUP ────────────────────────────────────────────────────
const map = L.map('map', {
  center: [28.625, 77.215],
  zoom: 13,
  zoomControl: true,
  attributionControl: true,
});

// OpenStreetMap dark-ish tile (CartoDB Dark Matter — free, no key)
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>',
  subdomains: 'abcd',
  maxZoom: 19,
}).addTo(map);
