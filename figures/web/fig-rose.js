// Paper II, "rose": the 57 problems in the seven-cell honeycomb of the works (Series 00, Figure 1: D4). In each work's
// cell its problems as small cells of glass, grouped by kind (mathematical, machine, formalization) and numbered;
// the dots under a number give the level (one entry, two research, three programme). A small cell links to its card.
import { ACC, LIGHT, INK, SEC, HEAD, SOFT, hexPts, rgb } from './lib.js';
import { footer, done, chipShape, chipHud, KIND, LEVEL_DOTS } from './rs.js';

const geometry = (D) => {
  const [W, H] = D.size_mm;
  const R = 24.0, DX = 1.5 * R, DY = Math.sqrt(3) / 2 * R, r = 2.75;
  const C0 = { x: W / 2, y: 13.0 + 3 * DY };
  const POS = { centre: [0, 0], top: [0, -2 * DY], 'upper-right': [DX, -DY], 'lower-right': [DX, DY],
                bottom: [0, 2 * DY], 'lower-left': [-DX, DY], 'upper-left': [-DX, -DY] };
  const cellXY = (p) => ({ x: C0.x + POS[p][0], y: C0.y + POS[p][1] });
  const chips = (c) => {                          // the small cells of one work: rows of six, interlocking
    const { x, y } = cellXY(c.position), n = c.problems.length, s = Math.sqrt(3) / 2 * r;
    if (n <= 6) return c.problems.map((p, k) => ({ p, x: x + (k - (n - 1) / 2) * 1.5 * r, y: y + 4.4 + (k % 2 ? s : 0) - s / 2 }));
    return c.problems.map((p, k) => { const row = Math.floor(k / 6), col = k % 6;
      return { p, x: x + (col - 2.5) * 1.5 * r, y: y - 1.0 + row * 2 * s + (col % 2 ? s : 0) }; });
  };
  return { W, H, R, DX, DY, r, C0, cellXY, chips, GAP: .35 };
};

export function light(D) {
  const G = geometry(D), shapes = [], backings = [];
  for (const c of D.cells) { const { x, y } = G.cellXY(c.position); backings.push({ x, y, r: G.R + .06 }); }
  for (const c of D.cells) {
    const { x, y } = G.cellXY(c.position);
    const recipe = c.series === '01' ? 'core' : c.colour;
    shapes.push({ kind: 'hex', x, y, r: G.R - G.GAP, recipe, bw: 1.0, acc: c.series === '01' ? ACC.blue : ACC[c.colour] });
    // the glass beneath a small cell is its work's (the core's gradient glass has no single tint: its teal)
    for (const q of G.chips(c)) shapes.push(chipShape(q.x, q.y, G.r - .28, q.p.kind, recipe === 'core' ? 'cyan' : recipe));
  }
  // the legend's sample cells
  const ly = G.C0.y + 3 * G.DY + 6.6;
  ['math', 'machine', 'formal'].forEach((k, i) => shapes.push(chipShape(10.6 + i * 33.0, ly - .9, 1.9, k)));
  return { focus: G.C0, lift: -30.0, stars: [[10, 40, .24], [122, 38, .22], [8, 120, .2], [124, 124, .2], [30, 150, .18]], backings, shapes };
}

export function hud(h, D) {
  const G = geometry(D), { W, R, DY, C0, cellXY, r } = G;
  const { text, el, glassEdge, inHex, wrap } = h;
  const links = [];
  h.titleStrip(D.number, D.title, D.right);
  const RE = R - G.GAP, M = 1.9;
  for (const c of D.cells) {
    const { x, y } = cellXY(c.position);
    if (c.series === '01') {
      const hp = hexPts(x, y, RE - .12), mix = (t) => { const a = rgb(ACC.cyan), b = rgb(ACC.blue);
        return '#' + a.map((v, k) => Math.round(255 * (v + (b[k] - v) * t)).toString(16).padStart(2, '0')).join(''); };
      const span = (px, py) => Math.min(1, Math.max(0, ((px - (x - RE)) + (py - (y - RE * .866))) / (2 * RE + 2 * RE * .866)));
      for (let k = 0; k < 6; k++) { const a = hp[k], b = hp[(k + 1) % 6];
        for (let j = 0; j < 12; j++) { const t0 = j / 12, t1 = (j + 1) / 12;
          const xa = a[0] + (b[0] - a[0]) * t0, ya = a[1] + (b[1] - a[1]) * t0, xb = a[0] + (b[0] - a[0]) * t1, yb = a[1] + (b[1] - a[1]) * t1;
          el('line', { x1: xa, y1: ya, x2: xb, y2: yb, stroke: mix(span((xa + xb) / 2, (ya + yb) / 2)), 'stroke-width': .38, 'stroke-linecap': 'round' }); } }
    } else glassEdge(hexPts(x, y, RE - .1), ACC[c.colour], .3, .9);
    text(x, y - 18.4, `SERIES ${c.series}`, 6.5, 'lab', LIGHT[c.colour], 'middle', inHex(RE, 20.1, M), 'series');
    text(x, y - 14.2, c.name[0], 7.2, 'name', INK, 'middle', inHex(RE, 16.0, M), 'names', 6.6);
    text(x, y - 11.0, c.name[1], 7.2, 'name', INK, 'middle', inHex(RE, 12.8, M), 'names', 6.6);
    text(x, y - 7.2, c.role, 6.8, 'it', SEC, 'middle', inHex(RE, 9.0, M), 'roles', 6.5);
    for (const q of G.chips(c)) chipHud(h, q.x, q.y, r - .28, q.p, links);
    const many = c.problems.length > 6;
    text(x, y + (many ? 17.4 : 13.2), c.range.replace('PROBLEMS', 'Problems'), 6.5, 'txt', SEC, 'middle',
         inHex(RE, many ? 17.9 : 13.7, M), 'range');
  }
  // the two parts, in the free corners beside cell 02
  const [p1, p2] = D.parts;
  const a = p1.split(' · '), b = p2.split(' · ');
  text(7.5, 18.0, `${a[0]} · ${a[1]}`, 6.5, 'cap', LIGHT.cyan, 'start');
  text(7.5, 21.2, a[2].replace('PROBLEMS', 'Problems'), 6.5, 'txt', SEC, 'start');
  text(W - 7.5, 18.0, `${b[0]} · ${b[1].split(' ').slice(0, 2).join(' ')}`, 6.5, 'cap', LIGHT.blue, 'end');
  text(W - 7.5, 21.2, b[1].split(' ').slice(2).join(' '), 6.5, 'cap', LIGHT.blue, 'end');
  text(W - 7.5, 24.4, b[2].replace('PROBLEMS', 'Problems'), 6.5, 'txt', SEC, 'end');
  // legend: kinds (the glass of the sample cells: light layer) and levels (dots)
  const ly = C0.y + 3 * DY + 6.6;
  D.kinds.forEach(([k, s], i) => { const x = 10.6 + i * 33.0;
    glassEdge(hexPts(x, ly - .9, 1.84), ACC[KIND[k]], .2, .95);
    text(x + 3.4, ly, s, 6.5, 'cap', LIGHT[KIND[k]], 'start'); });
  D.levels.forEach(([lv, s], i) => { const x = 10.6 + i * 33.0, n = LEVEL_DOTS[lv];
    for (let k = 0; k < n; k++) el('circle', { cx: (x + (k - (n - 1) / 2) * .62).toFixed(3), cy: (ly + 4.2 - .9).toFixed(3), r: .19, fill: SOFT });
    text(x + 3.4, ly + 4.2, s, 6.5, 'cap', SOFT, 'start'); });
  footer(h, D);
  done(links);
}
