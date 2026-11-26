// AC water: DON'T DRINK IT · Line-Art Cutaway film (60 s). Model in millimetres, traced live from normal/depth edges (three line weights);
// one accent colour (#0a84ff) only for the water path. Page contract: window.render(t), window.DUR, window.EV, window.TEXTS, window.READY.
import * as THREE from 'three';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { clamp, lerp, seg, eio, eo, ei, ss, back, track, mulberry } from '/core/lib.js';

THREE.ColorManagement.enabled = false;
const Q = new URLSearchParams(location.search);
const TLJ = await (await fetch('timeline.json')).json();
const FILM = TLJ.end;
const FROM = +(Q.get('from') ?? 0), TO = +(Q.get('to') ?? FILM);
const SUBS = Q.get('subs') !== '0';
const PX = 1920, PY = 1080, SS = +(Q.get('ss') || 2), JIT = +(Q.get('jit') || 8);
const PAPER = '#f6f5f0', INK = '#141414', GRAPH = '#5a5955', FAINT = '#8a8984', ACC = '#0a84ff', ACC_GL = 0x0a84ff;
const SANS = '"Plex Sans", sans-serif', MONO = '"Plex Mono", monospace';
const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
const L_ = Math.log;

// ---------- Timeline (whole-film seconds; narration: v1 0.8, v2 5.4, v3 14.5, v4 22.8, v5 34.4, v6 39.3, v7 50.4) ----------
const K = {
  title1: [0.9, 4.7],
  sweep: [5.6, 8.9], pathRun: [8.4, 13.4], lblCoil: [7.2, 12.6], lblPan: [9.4, 12.8], lblPipe: [10.6, 13.6],
  moist: [14.6, 21.5], gauge: [14.8, 19.4], dryNote: [15.4, 21.8],
  roomIn: [22.4, 24.6], co2: [24.6, 31.4], sleep: [29.3, 33.2], latch: 31.4, fresh: [31.7, 33.9],
  roomOut: [33.7, 34.9],
  catch: [34.4, 39.0], lift: 34.7, liftStep: 0.45, liftDur: 1.1, dive: [36.0, 38.6], clipOn: 36.0, cut: 38.7, iris: [38.9, 39.7],
  mag: [39.6, 48.6], germs: [40.2, 45.0], metals: [45.5, 48.4], flood: [39.4, 41.4],
  close: [48.5, 50.3], carry: [50.3, 53.2], plant: [51.0, 52.0], title2: [50.4, 53.2],
  trace: [53.0, 55.0], block: [54.2, 59.9],
  hatch: [59.2, 59.8], irisC: [59.9, 60.7], card: 60.0, logo: [60.15, 60.9],
};
const VO = TLJ.vo;
const LOGO = new Image(); LOGO.src = 'logo.png'; await LOGO.decode();
const W8 = [[-0.6, 0.1], [0.24, 0.48], [0.48, 0.64], [0.64, 0.92]].map(([a]) => VO.v8 + Math.max(0, a));   // like, share, and, subscribe word starts
const T_LIKE = W8[0], T_SHARE = W8[1], T_SUB = W8[3];
