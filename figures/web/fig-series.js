// Overview paper, "series": the series and its records. Above, the eight works in the order of their release — date,
// a cell with the series number (the colour of its cell in the honeycomb), name and role, size, concept DOI and the
// GitHub repository; every work also has a signed list of checksums, the licence CC BY-NC-ND 4.0 and a place in the
// Zenodo community. Below, the three papers released together and the repository of the problems through which
// solutions and corrections are submitted. Data: programme.yaml (facts), the release record of Series 00.
import { ACC, LIGHT, INK, SEC, HEAD, hexPts } from './lib.js';
import { footer, done } from './rs.js';

const RECIPE = { cyan: 'chipC', blue: 'chipB', violet: 'chipV' };
const geometry = (D) => {
  const [W, H] = D.size_mm;
  const TOP = 21.4, ROW = 7.0;
  const rows = D.rows.map((r, k) => ({ r, y: TOP + k * ROW }));
  const COL = { date: 7.5, cell: 27.0, name: 31.4, size: 72.0, doi: 90.0 };
  const BOT = TOP + D.rows.length * ROW;
  const P = { top: BOT + 12.0, h: 6.6, x0: 7.5, w: 54.0, gap: 1.4 };
  const REPO = { x0: 70.0, x1: W - 7.5, top: P.top, bot: P.top + 3 * P.h + 2 * P.gap };
  return { W, H, TOP, ROW, rows, COL, BOT, P, REPO };
};

export function light(D) {
  const G = geometry(D), shapes = [];
  for (const { r, y } of G.rows) shapes.push({ kind: 'hex', x: G.COL.cell, y: y + .6, r: 2.5, recipe: RECIPE[D.colour[r.series]], bw: .35,
                                               acc: ACC[D.colour[r.series]] });
  const P = G.P;
  D.papers.forEach((p, k) => shapes.push({ kind: 'rect', x: P.x0 + P.w / 2, y: P.top + k * (P.h + P.gap) + P.h / 2, w: P.w, h: P.h,
                                           recipe: 'chipB', bw: .45, acc: ACC.blue }));
  const R = G.REPO;
  shapes.push({ kind: 'rect', x: (R.x0 + R.x1) / 2, y: (R.top + R.bot) / 2, w: R.x1 - R.x0, h: R.bot - R.top, recipe: 'chipG', bw: .55, acc: ACC.gold });
  return { focus: { x: 66, y: 50 }, lift: -50.0, stars: [[124, 14, .18], [6, 96, .16], [66, 92, .16]], shapes };
}

export function hud(h, D) {
  const G = geometry(D), { W, TOP, ROW, rows, COL, BOT, P, REPO } = G;
  const { text, el, glassEdge, rectPts, line, arrow, wrap } = h;
  h.titleStrip(D.number, D.title, D.right);
  const hy = TOP - 4.6;
  [[COL.date, D.heads[0]], [COL.cell - 2.5, D.heads[1]], [COL.size, D.heads[2]], [COL.doi, D.heads[3]]]
    .forEach(([x, s]) => text(x, hy, s, 6.5, 'cap', HEAD, 'start'));
  line(7.5, hy + 1.4, W - 7.5, hy + 1.4, 'rgb(164,222,229)', .2, null, .5);
  const fmt = (d) => { const [y, m, dd] = d.split('-'); return `${+dd} ${['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][+m]} ${y}`; };
  for (const { r, y } of rows) {
    const acc = D.colour[r.series];
    text(COL.date, y + 1.2, fmt(r.date), 6.8, 'sb', SOFT, 'start');
    glassEdge(hexPts(COL.cell, y + .6, 2.44), ACC[acc], .22, .95);
    text(COL.cell, y + 1.55, r.series, 6.5, 'code', LIGHT[acc], 'middle');
    text(COL.name, y + .1, r.name, 6.8, 'name', INK, 'start', COL.size - COL.name - 1.5, 'rname', 6.5);
    text(COL.name, y + 2.9, r.role, 6.5, 'it', SEC, 'start', COL.size - COL.name - 1.5, 'rrole');
    const [vol, pg] = r.size.split(' · ');
    text(COL.size, y + .1, vol, 6.5, 'txt', INK, 'start', COL.doi - COL.size - 1.5, 'rsize');
    text(COL.size, y + 2.9, pg, 6.5, 'txt', SEC, 'start', COL.doi - COL.size - 1.5, 'rsize');
    text(COL.doi, y + .1, r.doi, 6.5, 'txt', LIGHT.cyan, 'start', W - 7.5 - COL.doi, 'rdoi');
    text(COL.doi, y + 2.9, r.repo.split('/')[1], 6.5, 'txt', SEC, 'start', W - 7.5 - COL.doi, 'rrepo');
    line(7.5, y + 4.6, W - 7.5, y + 4.6, 'rgb(164,222,229)', .12, null, .28);
  }
  wrap(`Each work also has ${D.every[0]}, the licence CC ${D.every[1]}, and a place in the ${D.every[2]} The Grothendieckian Programme.`, 6.5, 'it', W - 15)
    .forEach((l, j) => text(7.5, BOT + 2.0 + j * 2.6, l, 6.5, 'it', SEC, 'start', W - 14.5, 'every'));
  // ---- the three papers and the repository of the problems ---------------------------------------------------------
  text(P.x0, P.top - 2.6, D.heads[4], 6.5, 'cap', HEAD, 'start');
  text(REPO.x0, P.top - 2.6, D.heads[5], 6.5, 'cap', HEAD, 'start');
  D.papers.forEach(([n, t], k) => {
    const y0 = P.top + k * (P.h + P.gap);
    glassEdge(rectPts(P.x0, y0, P.x0 + P.w, y0 + P.h), ACC.blue, .24, .85);
    text(P.x0 + 2.0, y0 + P.h / 2 + 1.1, n, 7.0, 'code', LIGHT.blue, 'start');
    text(P.x0 + 5.6, y0 + P.h / 2 + 1.1, t, 6.8, 'it', INK, 'start', P.w - 7.0, 'ptitle');
    line(P.x0 + P.w + .6, y0 + P.h / 2, REPO.x0 - 1.4, (REPO.top + REPO.bot) / 2, LIGHT.blue, .26, null, .8);
  });
  arrow(REPO.x0 - .9, (REPO.top + REPO.bot) / 2, 0, LIGHT.blue, .6);
  glassEdge(rectPts(REPO.x0, REPO.top, REPO.x1, REPO.bot), ACC.gold, .28, .9);
  const rw = REPO.x1 - REPO.x0 - 4.4;
  text(REPO.x0 + 2.2, REPO.top + 4.6, D.repo, 6.8, 'sb', LIGHT.gold, 'start', rw);
  let y = REPO.top + 8.4;
  for (const s of D.repo_lines) for (const l of wrap(s, 6.6, 'it', rw)) { text(REPO.x0 + 2.2, y, l, 6.6, 'it', INK, 'start', rw + .5, 'rl'); y += 2.7; }
  footer(h, D);
  done([]);
}
const SOFT = '#d3dee3';
