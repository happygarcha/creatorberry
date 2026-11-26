// Kolkata underwater metro · Line-Art Cutaway film (Hindi). Model in metres (vertical scale x5, labelled), traced live from normal/depth edges (three line weights);
// one accent colour (#0a84ff) only for water. Page contract: window.render(t), window.DUR, window.EV, window.TEXTS, window.READY.
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
const SANS = '"Plex Sans", "Noto Deva", sans-serif', MONO = '"Plex Mono", "Noto Deva", monospace';
const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
const L_ = Math.log;
const VO = TLJ.vo;
// ---------- Timeline (whole-film seconds; narration starts v1 0.8, v2 10.3, v3 25.4, v4 35.3, v5 47.5, v6 58.7, v7 66.9) ----------
const K = {
  title1: [0.9, 9.4],
  sweep: [3.0, 6.2], trainA: [5.4, 10.4],
  route: [10.4, 24.6], trainC: [11.4, 22.4], lblWest: [11.4, 15.2], lblEast: [18.6, 24.3], dateA: [16.7, 20.3], dateB: [20.4, 24.6],
  tunnel: [25.4, 34.6], dimLen: [25.9, 34.2], trainB: [26.4, 31.6], watch: [29.9, 34.4],
  cutA: [34.2, 35.1],
  tbm: [35.3, 47.0], lblHead: [36.5, 41.0], lblRing: [40.0, 46.4], lblWater: [44.2, 46.9], tbmRun: [35.6, 46.0],
  cutB: [46.8, 47.6],
  stn: [47.6, 58.4], dimDepth: [50.6, 57.9], floors: [54.0, 57.4], lblStn: [48.4, 54.0],
  out: [58.7, 66.6], lblBoat: [62.2, 66.2], lblMetro: [63.8, 66.6],
  hatch: [66.4, 67.0], irisC: [67.0, 67.8], card: 67.9, logo: [68.0, 68.7],
};
const LOGO = new Image(); LOGO.src = 'logo.png'; await LOGO.decode();
const T_LIKE = VO.v7 + 0.1, T_SHARE = VO.v7 + 1.0, T_SUB = VO.v7 + 1.95;
