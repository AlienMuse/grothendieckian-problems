// Paper I, "chain": Theses 6 and 7. Above, the chain of non-implications of S01 Vol. III Ch. 3 (p. 8004), each passage
// with the input it requires and the way it fails (the argument of Thesis 6); below, the separation of proposing from
// authorising (Thesis 7: S01, Architectural Prospectus, p. 7966) and the four cases in which it fails (S01 Vol. V,
// Proposition 1.3, pp. 11913–11914).
import { ACC, LIGHT, INK, SEC, HEAD } from './lib.js';
import { footer, done } from './rs.js';

const geometry = (D) => {
  const [W, H] = D.size_mm;
  const X0 = 7.5, X1 = W - 7.5, BW = 22.5, GAP = (X1 - X0 - 4 * BW) / 3;
  const boxes = [0, 1, 2, 3].map(k => ({ x0: X0 + k * (BW + GAP), x1: X0 + k * (BW + GAP) + BW, top: 20.4, bot: 31.4 }));
  const CW = (X1 - X0 - 2 * 3.0) / 3;
  const cols = [0, 1, 2].map(k => ({ x0: X0 + k * (CW + 3.0), x1: X0 + k * (CW + 3.0) + CW, top: 41.2, bot: 93.8 }));
  const quotes = [{ x0: X0, x1: X0 + 70.5, top: 103.4, bot: 111.8 }, { x0: X0 + 73.5, x1: X1, top: 103.4, bot: 111.8 }];
  const GW = (X1 - X0 - 3.0) / 2;
  const grid = [0, 1, 2, 3].map(k => ({ x0: X0 + (k % 2) * (GW + 3.0), x1: X0 + (k % 2) * (GW + 3.0) + GW,
                                        top: 118.8 + Math.floor(k / 2) * 10.2, bot: 127.6 + Math.floor(k / 2) * 10.2 }));
  return { W, H, X0, X1, BW, GAP, boxes, cols, quotes, grid };
};
const rect = (b, recipe, acc, under = null) => ({ kind: 'rect', x: (b.x0 + b.x1) / 2, y: (b.top + b.bot) / 2, w: b.x1 - b.x0,
                                                  h: b.bot - b.top, recipe, under, bw: .55, acc });

export function light(D) {
  const G = geometry(D), shapes = [];
  G.boxes.forEach((b, k) => shapes.push(rect(b, k === 3 ? 'chipG' : 'chipB', k === 3 ? ACC.gold : ACC.blue)));
  G.cols.forEach(b => shapes.push(rect(b, 'panel', ACC.cyan)));
  shapes.push(rect(G.quotes[0], 'chipB', ACC.blue), rect(G.quotes[1], 'chipG', ACC.gold));
  G.grid.forEach(b => shapes.push(rect(b, 'panel', ACC.gold)));
  return { focus: { x: G.W / 2, y: 46 }, lift: -46.0, stars: [[10, 38, .2], [124, 36, .2], [64, 88, .18], [6, 128, .18]], shapes };
}

export function hud(h, D) {
  const G = geometry(D), { W, X0, X1 } = G;
  const { text, el, glassEdge, rectPts, line, arrow, wrap } = h;  // h.measure: widths of the column titles
  h.titleStrip(D.number, D.title, D.right);
  // ---- Thesis 6 ---------------------------------------------------------------------------------------------------
  text(X0, 16.6, D.heads[0], 6.5, 'cap', LIGHT.cyan, 'start');
  text(X1, 16.6, D.src[0], 6.5, 'cap', HEAD, 'end');
  G.boxes.forEach((b, k) => {
    glassEdge(rectPts(b.x0, b.top, b.x1, b.bot), k === 3 ? ACC.gold : ACC.blue, .28, .9);
    const ls = D.stages[k].split(' ');
    const lines = ls.length > 1 ? [ls[0], ls.slice(1).join(' ')] : ls;
    const y0 = (b.top + b.bot) / 2 + 1.25 - (lines.length - 1) * 1.6;
    lines.forEach((l, j) => text((b.x0 + b.x1) / 2, y0 + j * 3.2, l, 7.4, 'name', INK, 'middle', b.x1 - b.x0 - 3.0, 'stage'));
  });
  for (let k = 0; k < 3; k++) {                    // ⇏ between the boxes
    const gx = (G.boxes[k].x1 + G.boxes[k + 1].x0) / 2;
    text(gx, 27.6, '⇏', 11.0, 'math', LIGHT.cyan, 'middle');
  }
  text(W / 2, 37.4, D.rule, 7.2, 'it', SEC, 'middle', X1 - X0);
  G.cols.forEach((c, k) => {
    el('rect', { x: c.x0, y: c.top, width: c.x1 - c.x0, height: c.bot - c.top, fill: 'none', stroke: 'rgb(164,222,229)',
                 'stroke-opacity': .32, 'stroke-width': .25 });
    const tw = c.x1 - c.x0 - 5.0;
    let y = c.top + 4.8;
    const st = (i) => D.stages[i].split(' ').slice(-1)[0];
    // the sign in the regular mathematics face: Chrome would embolden it synthetically, as a Type 3 font
    const w1 = h.measure(st(k), 7.2, 'sb'), wa = h.measure('⇏', 7.6, 'math');
    text(c.x0 + 2.5, y, st(k), 7.2, 'sb', LIGHT.cyan, 'start');
    text(c.x0 + 2.5 + w1 + 1.9, y + .2, '⇏', 7.6, 'math', LIGHT.cyan, 'start');
    text(c.x0 + 2.5 + w1 + 3.8 + wa, y, st(k + 1), 7.2, 'sb', LIGHT.cyan, 'start');
    line(c.x0 + 2.5, y + 1.6, c.x1 - 2.5, y + 1.6, 'rgb(164,222,229)', .16, null, .45);
    y += 6.4;
    text(c.x0 + 2.5, y, D.heads[1], 6.5, 'cap', LIGHT.gold, 'start', tw, 'chead');
    y += 1.4;
    for (const n of D.needs[k]) for (const l of wrap(n, 7.0, 'txt', tw)) { y += 3.0; text(c.x0 + 2.5, y, l, 7.0, 'txt', INK, 'start', tw, 'need'); }
    y += 5.0;
    text(c.x0 + 2.5, y, D.heads[2], 6.5, 'cap', HEAD, 'start', tw, 'chead');
    y += 1.4;
    for (const f of D.fails[k]) { for (const l of wrap(f, 7.0, 'it', tw)) { y += 2.9; text(c.x0 + 2.5, y, l, 7.0, 'it', SEC, 'start', tw, 'fail'); } y += 1.3; }
  });
  // ---- Thesis 7 ---------------------------------------------------------------------------------------------------
  text(X0, 99.8, D.heads[3], 6.5, 'cap', LIGHT.cyan, 'start');
  text(X1, 99.8, D.src[1], 6.5, 'cap', HEAD, 'end');
  D.who.forEach((q, k) => {
    const b = G.quotes[k], tw = b.x1 - b.x0 - 5.0;
    glassEdge(rectPts(b.x0, b.top, b.x1, b.bot), k ? ACC.gold : ACC.blue, .26, .9);
    const ls = wrap(`“${q}”`, 7.0, 'it', tw);
    const y0 = (b.top + b.bot) / 2 + 1.2 - (ls.length - 1) * 1.45;
    ls.forEach((l, j) => text(b.x0 + 2.5, y0 + j * 2.9, l, 7.0, 'it', INK, 'start', tw, 'who'));
  });
  text(X0, 116.0, D.heads[4], 6.5, 'cap', LIGHT.gold, 'start');
  text(X1, 116.0, D.src[2], 6.5, 'cap', HEAD, 'end');
  G.grid.forEach((b, k) => {
    const tw = b.x1 - b.x0 - 5.0;
    glassEdge(rectPts(b.x0, b.top, b.x1, b.bot), ACC.gold, .24, .75);
    const ls = wrap(D.broken[k], 7.0, 'it', tw);
    const y0 = (b.top + b.bot) / 2 + 1.2 - (ls.length - 1) * 1.45;
    ls.forEach((l, j) => text(b.x0 + 2.5, y0 + j * 2.9, l, 7.0, 'it', SEC, 'start', tw, 'broken'));
  });
  text(W / 2, G.grid[3].bot + 4.4, `In each case “${D.verdict}.”`, 7.0, 'it', LIGHT.gold, 'middle', X1 - X0);
  footer(h, D);
  done([]);
}
