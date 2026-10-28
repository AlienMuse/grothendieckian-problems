// Paper I, "works": the seven works as the seven-cell honeycomb of Series 00, Figure 1 (D4: flat-top cells; 01 at the
// centre, 02 above it on a shared edge, 03–07 clockwise from the upper right), without the core's decomposition (D5:
// that panel stays in the book). Each cell: series, name, role, the formula of its cover's centre cell, its pages.
import { ACC, LIGHT, INK, SEC, HEAD, SOFT, hexPts, rgb } from './lib.js';
import { footer, done } from './rs.js';

const geometry = (D) => {
  const [W, H] = D.size_mm;
  const R = 19.0, DX = 1.5 * R, DY = Math.sqrt(3) / 2 * R;
  const C0 = { x: W / 2, y: 13.2 + 3 * DY };
  const POS = { centre: [0, 0], top: [0, -2 * DY], 'upper-right': [DX, -DY], 'lower-right': [DX, DY],
                bottom: [0, 2 * DY], 'lower-left': [-DX, DY], 'upper-left': [-DX, -DY] };
  return { W, H, R, DX, DY, C0, GAP: .35, cellXY: (p) => ({ x: C0.x + POS[p][0], y: C0.y + POS[p][1] }) };
};

export function light(D) {
  const G = geometry(D), shapes = [], backings = [];
  for (const c of D.cells) { const { x, y } = G.cellXY(c.position); backings.push({ x, y, r: G.R + .06 }); }
  for (const c of D.cells) {
    const { x, y } = G.cellXY(c.position);
    shapes.push({ kind: 'hex', x, y, r: G.R - G.GAP, recipe: c.series === '01' ? 'core' : c.colour, bw: .95,
                  acc: c.series === '01' ? ACC.blue : ACC[c.colour] });
  }
  return { focus: G.C0, lift: -52.0, stars: [[8, 22, .26], [122, 20, .24], [10, 98, .2], [124, 92, .22], [30, 6, .18], [104, 5, .18]],
           backings, shapes };
}

export function hud(h, D) {
  const G = geometry(D), { W, H, R, DY, C0, cellXY } = G;
  const { text, el, glassEdge, inHex, arrow, line, port } = h;
  const links = [];
  h.titleStrip(D.number, D.title, D.right);
  const RE = R - G.GAP, M = 1.9;
  for (const c of D.cells) {
    const { x } = cellXY(c.position);
    // the text of cell 02 stands 1.6 mm higher: the plate of the kernel's edge covers the foot of the cell
    const y = cellXY(c.position).y - (c.series === '02' ? 1.6 : 0), yc = cellXY(c.position).y;
    if (c.series === '01') {                      // the core: an edge running from teal into blue (as Series 00, Fig. 1)
      const hp = hexPts(x, yc, RE - .12), mix = (t) => { const a = rgb(ACC.cyan), b = rgb(ACC.blue);
        return '#' + a.map((v, k) => Math.round(255 * (v + (b[k] - v) * t)).toString(16).padStart(2, '0')).join(''); };
      const span = (px, py) => Math.min(1, Math.max(0, ((px - (x - RE)) + (py - (yc - RE * .866))) / (2 * RE + 2 * RE * .866)));
      for (let k = 0; k < 6; k++) { const a = hp[k], b = hp[(k + 1) % 6];
        for (let j = 0; j < 12; j++) { const t0 = j / 12, t1 = (j + 1) / 12;
          const xa = a[0] + (b[0] - a[0]) * t0, ya = a[1] + (b[1] - a[1]) * t0, xb = a[0] + (b[0] - a[0]) * t1, yb = a[1] + (b[1] - a[1]) * t1;
          el('line', { x1: xa, y1: ya, x2: xb, y2: yb, stroke: mix(span((xa + xb) / 2, (ya + yb) / 2)), 'stroke-width': .38, 'stroke-linecap': 'round' }); } }
    } else glassEdge(hexPts(x, yc, RE - .1), ACC[c.colour], .3, .9);
    text(x, y - 9.9, `SERIES ${c.series}`, 6.5, 'lab', LIGHT[c.colour], 'middle', inHex(RE, 11.6, M), 'series');
    text(x, y - 5.0, c.name[0], 7.6, 'name', INK, 'middle', inHex(RE, 7.0, M), 'names', 6.9);
    text(x, y - 1.6, c.name[1], 7.6, 'name', INK, 'middle', inHex(RE, 3.6, M), 'names', 6.9);
    text(x, y + 2.7, c.role, 7.4, 'it', SEC, 'middle', inHex(RE, 4.5, M), 'roles', 6.8);
    // the formula on one line, or on two, broken before its relation sign, when one line would need less than 8.4 pt
    const f = c.formula;
    const one = text(x, y + 8.4, f, 9.0, 'math', '#e6eeee', 'middle', inHex(RE, 9.8, M), null, 8.4);
    const fits = h.width(one) * 8.4 / 9.0 <= one.maxW;
    const br = Math.max(f.indexOf(' ≤ '), f.indexOf(' ≅ '));
    let py = y + 12.9;
    if (!fits && br > 0) {
      h.drop(one);
      text(x, y + 7.1, f.slice(0, br), 8.4, 'math', '#e6eeee', 'middle', inHex(RE, 8.9, M), 'formula2', 7.8);
      text(x, y + 10.4, f.slice(br + 1), 8.4, 'math', '#e6eeee', 'middle', inHex(RE, 11.0, M), 'formula2', 7.8);
      py = y + (c.series === '02' ? 13.6 : 14.0);
    } else { one.group = 'formula1'; }
    text(x, py, c.size.replace(/^\d+ volumes · /, ''), 6.5, 'txt', SEC, 'middle', inHex(RE, py - yc + .5, M), 'pages');
  }
  // the kernel's edge, heavier, its label on a plate of glass across it (Series 00, Figure 1)
  const ky = C0.y - DY;
  line(C0.x - R / 2 + 1.0, ky, C0.x + R / 2 - 1.0, ky, ACC.cyan, .75, null, .95);
  el('rect', { x: C0.x - 13.4, y: ky - 2.95, width: 26.8, height: 5.9, rx: .7, fill: 'rgb(4,15,22)', 'fill-opacity': .95, stroke: ACC.cyan, 'stroke-width': .26 });
  const se = D.shared_edge.split(' OVER ');
  text(C0.x, ky - .4, se[0], 6.5, 'cap', LIGHT.cyan, 'middle', 25.2, 'plate');
  text(C0.x, ky + 2.15, 'OVER ' + se[1], 6.5, 'cap', LIGHT.cyan, 'middle', 25.2, 'plate');
  arrow(C0.x, ky + 3.55, Math.PI / 2, LIGHT.violet, .6);
  // ports on the shared edges and the three flows across them
  const edgeAt = (a, b) => { const pa = cellXY(a), pb = cellXY(b); return { mx: (pa.x + pb.x) / 2, my: (pa.y + pb.y) / 2,
    nx: (pb.x - pa.x) / (2 * DY), ny: (pb.y - pa.y) / (2 * DY) }; };
  const flow = (e, sgn, off, c, dash = null, a = .95, b = .95) => {
    const tx = -e.ny, ty = e.nx;
    const x1 = e.mx - sgn * e.nx * a + tx * off, y1 = e.my - sgn * e.ny * a + ty * off;
    const x2 = e.mx + sgn * e.nx * b + tx * off, y2 = e.my + sgn * e.ny * b + ty * off;
    line(x1, y1, x2, y2, c, .3, dash);
    arrow(x2 + sgn * e.nx * .35, y2 + sgn * e.ny * .35, Math.atan2(sgn * e.ny, sgn * e.nx), c, .6);
  };
  for (const c of D.cells) {
    if (c.position === 'centre' || c.series === '02') continue;
    const e = edgeAt('centre', c.position);
    flow(e, 1, 1.75, LIGHT.cyan); flow(e, -1, -1.75, LIGHT.gold); port(e.mx, e.my, ACC[c.colour]);
  }
  for (const s of ['upper-right', 'upper-left']) { const e = edgeAt('top', s);
    flow(e, 1, 1.75, LIGHT.violet, '.55 .4'); flow(e, 1, -1.75, LIGHT.violet, '.55 .4'); port(e.mx, e.my, ACC.violet); }
  // legend: the three flows and the port, in two rows under the honeycomb
  const ly = C0.y + 3 * DY + 5.6;
  const item = (x, y, c, dash, s) => { line(x, y - .9, x + 4.8, y - .9, c, .34, dash); arrow(x + 5.4, y - .9, 0, c, .75);
    text(x + 7.6, y, s, 6.5, 'txt', SOFT, 'start'); };
  item(9.0, ly, LIGHT.cyan, null, D.legend[0]);
  item(9.0, ly + 4.2, LIGHT.violet, '1 .7', D.legend[1]);
  item(W / 2 + 2.0, ly, LIGHT.gold, null, D.legend[2]);
  el('circle', { cx: W / 2 + 4.4, cy: ly + 4.2 - .9, r: .85, fill: '#05111b', stroke: LIGHT.cyan, 'stroke-width': .28 });
  text(W / 2 + 9.6, ly + 4.2, D.legend[3], 6.5, 'txt', SOFT, 'start');
  footer(h, D);
  done(links);
}
