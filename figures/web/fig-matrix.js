// Paper II, "matrix": the problems by thesis and by work (Appendix A). One row per thesis, one column per work; in each
// cell the problems of that thesis and work as small cells of glass, numbered, tinted by kind; totals by row and column.
// A small cell links to its card, a row's label to its thesis in the companion paper's numbering (not a link: the
// theses are in paper I).
import { ACC, LIGHT, INK, SEC, HEAD, SOFT, hexPts } from './lib.js';
import { footer, done, chipShape, chipHud, KIND } from './rs.js';

const WORKS = ['S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07'];
const GROUP = (n) => n <= 3 ? 'cyan' : n <= 7 ? 'blue' : 'gold';
const r = 2.0, PX = 4.4, PY = 4.0;
const geometry = (D) => {
  const [W, H] = D.size_mm;
  const cap = { S01: 3, S02: 3 }, X0 = 7.5, LABEL = 30.0;
  let x = X0 + LABEL;
  const cols = WORKS.map(w => { const c = cap[w] || 2, width = c * PX + 1.4; const col = { w, x0: x, x1: x + width, cap: c }; x += width; return col; });
  const TOT = { x0: x, x1: x + 8.5 };
  const TOP = 22.0;
  let y = TOP;
  const rows = D.rows.map(row => {
    const lines = Math.max(1, ...cols.map(c => Math.ceil(row.cells[c.w].length / c.cap)));
    const h = Math.max(7.6, lines * PY + 1.8);
    const R = { row, top: y, bot: y + h }; y += h; return R; });
  return { W, H, X0, LABEL, cols, TOT, TOP, rows, BOT: y };
};
const chipsOf = (G, R, c) => R.row.cells[c.w].map((p, k) => {
  const line = Math.floor(k / c.cap), col = k % c.cap, n = Math.min(c.cap, R.row.cells[c.w].length - line * c.cap);
  return { p, x: (c.x0 + c.x1) / 2 + (col - (n - 1) / 2) * PX, y: R.top + 2.9 + line * PY }; });

export function light(D) {
  const G = geometry(D), shapes = [];
  shapes.push({ kind: 'rect', x: (G.X0 + G.TOT.x1) / 2, y: (G.TOP - 6.4 + G.BOT + 6.6) / 2, w: G.TOT.x1 - G.X0 + 2.0,
                h: G.BOT - G.TOP + 13.0, recipe: 'panel', bw: .6 });
  for (const R of G.rows) for (const c of G.cols) for (const q of chipsOf(G, R, c)) shapes.push(chipShape(q.x, q.y, r - .1, q.p.kind, 'panel'));
  const ly = G.BOT + 12.2;
  ['math', 'machine', 'formal'].forEach((k, i) => shapes.push(chipShape(10.6 + i * 33.0, ly - .9, 1.9, k)));
  return { focus: { x: 70, y: 70 }, lift: -26.0, stars: [[126, 30, .18], [128, 100, .16]], shapes };
}

export function hud(h, D) {
  const G = geometry(D), { W, X0, cols, TOT, TOP, rows, BOT } = G;
  const { text, el, glassEdge, line, wrap } = h;
  const links = [];
  h.titleStrip(D.number, D.title, D.right);
  el('rect', { x: X0 - 1.0, y: TOP - 6.4, width: TOT.x1 - X0 + 2.0, height: BOT - TOP + 13.0, fill: 'none',
               stroke: 'rgb(164,222,229)', 'stroke-opacity': .3, 'stroke-width': .24 });
  text(X0 + .6, TOP - 2.6, 'THESIS', 6.5, 'cap', HEAD, 'start');
  for (const c of cols) text((c.x0 + c.x1) / 2, TOP - 2.6, c.w, 6.5, 'cap', HEAD, 'middle');
  text((TOT.x0 + TOT.x1) / 2, TOP - 2.6, 'ALL', 6.5, 'cap', HEAD, 'middle');
  line(X0, TOP - .6, TOT.x1, TOP - .6, 'rgb(164,222,229)', .22, null, .6);
  for (const R of rows) {
    const n = R.row.num, acc = GROUP(n);
    text(X0 + .6, R.top + 4.0, String(n), 7.4, 'code', LIGHT[acc], 'start');
    wrap(R.row.title, 6.5, 'txt', G.LABEL - 7.0).forEach((l, j) => text(X0 + 5.4, R.top + 3.4 + j * 2.75, l, 6.5, 'txt', INK, 'start', G.LABEL - 6.0, 'tl'));
    for (const c of cols) for (const q of chipsOf(G, R, c)) chipHud(h, q.x, q.y, r - .1, q.p, links, false);
    text((TOT.x0 + TOT.x1) / 2, R.top + 4.0, String(R.row.n), 6.8, 'sb', SOFT, 'middle');
    line(X0, R.bot, TOT.x1, R.bot, 'rgb(164,222,229)', .14, null, .35);
  }
  for (const c of [...cols, TOT]) line(c.x0, TOP - 5.4, c.x0, BOT + 5.6, 'rgb(164,222,229)', .14, null, .3);
  for (const c of cols) text((c.x0 + c.x1) / 2, BOT + 4.4, String(D.cols[c.w]), 6.8, 'sb', SOFT, 'middle');
  text(X0 + .6, BOT + 4.4, 'ALL', 6.5, 'cap', HEAD, 'start');
  text((TOT.x0 + TOT.x1) / 2, BOT + 4.4, String(D.total), 7.0, 'code', INK, 'middle');
  // legend: the kinds
  const ly = BOT + 12.2;
  D.kinds.forEach(([k, s], i) => { const x = 10.6 + i * 33.0;
    glassEdge(hexPts(x, ly - .9, 1.84), ACC[KIND[k]], .2, .95);
    text(x + 3.4, ly, s, 6.5, 'cap', LIGHT[KIND[k]], 'start'); });
  footer(h, D);
  done(links);
}
