// Overview paper, "method": recursive mathematical discovery as the Series Note of the five research subjects states
// it — four cells of one honeycomb closing into a ring (propose → test → abstract → ask again), as in Series 00,
// Figure 2; beside it, the tests fixed in advance and what is kept of what fails; below, the status labels with which
// each work reports its results. Every phrase is programme.yaml (figures.cycle), the overview's text or the page of
// the sealed PDF named in tools/figures.py.
import { ACC, LIGHT, INK, SEC, HEAD, hexPts } from './lib.js';
import { footer, done } from './rs.js';

const geometry = (D) => {
  const [W, H] = D.size_mm;
  const R = 13.6, DX = 1.5 * R, DY = Math.sqrt(3) / 2 * R;
  const O = { x: 37.0, y: 47.0 };
  const cells = [{ x: O.x, y: O.y - DY }, { x: O.x + DX, y: O.y }, { x: O.x, y: O.y + DY }, { x: O.x - DX, y: O.y }];
  const tones = [['core', 'cyan', ACC.cyan], ['blue', 'blue', ACC.blue], ['violet', 'violet', ACC.violet], ['blue', 'blue', ACC.blue]];
  return { W, H, R, DX, DY, O, cells, tones, GAP: .35,
           TESTS: { x0: 73.0, x1: W - 7.5, top: 14.0, bot: 56.0 }, KEPT: { x0: 73.0, x1: W - 7.5, top: 59.2, bot: 96.6 },
           LAB: { x0: 7.5, x1: W - 7.5, top: 100.6, bot: H - 9.0 } };
};

export function light(D) {
  const G = geometry(D), shapes = [], backings = [];
  G.cells.forEach(c => backings.push({ x: c.x, y: c.y, r: G.R + .06 }));
  G.cells.forEach((c, k) => shapes.push({ kind: 'hex', x: c.x, y: c.y, r: G.R - G.GAP, recipe: G.tones[k][0], bw: .9, acc: G.tones[k][2] }));
  const T = G.TESTS, K = G.KEPT, L = G.LAB;
  shapes.push({ kind: 'rect', x: (T.x0 + T.x1) / 2, y: (T.top + T.bot) / 2, w: T.x1 - T.x0, h: T.bot - T.top, recipe: 'panel', bw: .6 });
  shapes.push({ kind: 'rect', x: (K.x0 + K.x1) / 2, y: (K.top + K.bot) / 2, w: K.x1 - K.x0, h: K.bot - K.top, recipe: 'chipG', bw: .6, acc: ACC.gold });
  shapes.push({ kind: 'rect', x: (L.x0 + L.x1) / 2, y: (L.top + L.bot) / 2, w: L.x1 - L.x0, h: L.bot - L.top, recipe: 'panel', bw: .6 });
  return { focus: G.O, lift: -64.0, stars: [[6, 20, .22], [70, 6, .18], [126, 86, .18], [4.5, 84, .2]], backings, shapes };
}

export function hud(h, D) {
  const G = geometry(D), { W, R, GAP, cells, tones, TESTS: T, KEPT: K, LAB: L } = G;
  const { text, el, glassEdge, line, arrow, port, curve, rectPts, inHex, wrap } = h;
  h.titleStrip(D.number, D.title, D.right);
  // ---- the ring ----------------------------------------------------------------------------------------------------
  const RE = R - GAP, M = 1.6;
  D.steps.forEach((s, k) => {
    const c = cells[k], acc = tones[k][1];
    glassEdge(hexPts(c.x, c.y, RE - .1), ACC[acc], k === 0 ? .36 : .3, .92);
    text(c.x, c.y - 7.9, `STEP ${k + 1}`, 6.5, 'lab', LIGHT[acc], 'middle', inHex(RE, 10.2, M), 'step');
    text(c.x, c.y - 3.6, s.code, 8.2, 'name', INK, 'middle', inHex(RE, 6.4, M), 'scode', 7.2);
    s.lines.forEach((l, j) => { const y = c.y + .2 + j * 2.9;
      text(c.x, y, l, 6.6, 'it', SEC, 'middle', inHex(RE, Math.max(Math.abs(y - 2.0 - c.y), Math.abs(y + .7 - c.y)), 1.2), 'sline', 6.5); });
  });
  for (let k = 0; k < 4; k++) {
    const a = cells[k], b = cells[(k + 1) % 4];
    const mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2, Lh = Math.hypot(b.x - a.x, b.y - a.y), nx = (b.x - a.x) / Lh, ny = (b.y - a.y) / Lh;
    line(mx - nx * 1.4, my - ny * 1.4, mx + nx * 1.6, my + ny * 1.6, LIGHT.cyan, .32);
    arrow(mx + nx * 1.95, my + ny * 1.95, Math.atan2(ny, nx), LIGHT.cyan, .62);
    port(mx, my, ACC.cyan);
  }
  text(G.O.x, cells[2].y + G.DY + 4.6, D.source, 6.5, 'cap', HEAD, 'middle');
  // ---- tested against what is known ------------------------------------------------------------------------------
  const tw = T.x1 - T.x0 - 5.0;
  el('rect', { x: T.x0, y: T.top, width: T.x1 - T.x0, height: T.bot - T.top, fill: 'none', stroke: 'rgb(164,222,229)', 'stroke-opacity': .32, 'stroke-width': .25 });
  text(T.x0 + 2.5, T.top + 4.6, D.heads[0], 6.5, 'cap', LIGHT.cyan, 'start', tw);
  let y = T.top + 9.2;
  for (const g of D.tests) {
    text(T.x0 + 2.5, y, g.head, 6.5, 'lab', LIGHT.blue, 'start', tw, 'ghead');
    for (const l of wrap(g.text, 6.8, 'it', tw)) { y += 2.8; text(T.x0 + 2.5, y, l, 6.8, 'it', SEC, 'start', tw, 'gline'); }
    y += 4.2;
  }
  curve([T.x0 - .8, T.top + 22.0], [cells[1].x + .62 * RE, cells[1].y - .62 * RE], -2.0, LIGHT.blue, .3, null, .62);
  // ---- what does not survive is kept -----------------------------------------------------------------------------
  const kw = K.x1 - K.x0 - 5.0;
  glassEdge(rectPts(K.x0, K.top, K.x1, K.bot), ACC.gold, .28, .85);
  text(K.x0 + 2.5, K.top + 4.6, D.heads[1], 6.5, 'cap', LIGHT.gold, 'start', kw);
  let ky = K.top + 9.0;
  for (const [who, s] of D.kept) {
    text(K.x0 + 2.5, ky, who, 6.5, 'lab', LIGHT.gold, 'start', 21.0, 'kwho');
    const ls = wrap(s, 6.6, 'it', kw - 22.5);
    ls.forEach((l, j) => text(K.x0 + 25.0, ky + j * 2.6, l, 6.6, 'it', INK, 'start', kw - 22.0, 'ktext'));
    ky += 2.6 * ls.length + 1.6;
  }
  curve([cells[1].x + .62 * RE, cells[1].y + .62 * RE], [K.x0 - .8, K.top + 9.0], 1.4, LIGHT.gold, .3, null, .62);
  // ---- the status of every statement -----------------------------------------------------------------------------
  glassEdge(rectPts(L.x0, L.top, L.x1, L.bot), ACC.cyan, .24, .6);
  text(L.x0 + 2.5, L.top + 4.6, D.heads[2], 6.5, 'cap', LIGHT.cyan, 'start');
  text(L.x1 - 2.5, L.top + 4.6, `“${D.rule}”`, 6.8, 'it', SEC, 'end', L.x1 - L.x0 - 52.0);
  D.labels.forEach(([who, s], k) => {
    const yy = L.top + 9.6 + k * 3.25;
    text(L.x0 + 2.5, yy, who, 6.5, 'lab', LIGHT.blue, 'start', 24.0, 'lwho');
    text(L.x0 + 28.0, yy, s, 6.5, 'cap', INK, 'start', L.x1 - L.x0 - 31.0, 'ltext');
  });
  footer(h, D);
  done([]);
}
