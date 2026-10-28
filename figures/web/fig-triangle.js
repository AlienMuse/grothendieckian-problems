// Paper I, "triangle": the worked example of Section 5 (S01 Vol. III §61.18, p. 9227). Three charts with local
// sections; the three pairwise comparisons pass, the triangular law fails; the record of the failure and what it
// excludes; where Theses 1, 2, 5, 6 and 10 act. Every phrase is the paper's (45-together.md) or the source's.
import { ACC, LIGHT, INK, SEC, HEAD, hexPts } from './lib.js';
import { footer, done } from './rs.js';

const geometry = (D) => {
  const [W, H] = D.size_mm;
  const r = 9.0;
  const U = [{ x: 21.0, y: 44.0 }, { x: 54.0, y: 27.0 }, { x: 54.0, y: 61.0 }];
  const U4 = { x: 21.0, y: 73.4 };
  const PANEL = { x0: 76.0, x1: W - 7.5, top: 13.6, bot: 81.2 };
  const ACTS = { top: 89.4, bot: 106.6, x0: 7.5, x1: W - 7.5, gap: 1.6 };
  return { W, H, r, U, U4, PANEL, ACTS };
};

export function light(D) {
  const G = geometry(D), shapes = [];
  G.U.forEach(u => shapes.push({ kind: 'hex', x: u.x, y: u.y, r: G.r, recipe: 'chipC', bw: .6, acc: ACC.cyan }));
  shapes.push({ kind: 'hex', x: G.U4.x, y: G.U4.y, r: G.r * .62, recipe: 'open', bw: .4, acc: ACC.cyan });
  const c = { x: (G.U[0].x + G.U[1].x + G.U[2].x) / 3, y: (G.U[0].y + G.U[1].y + G.U[2].y) / 3 };
  shapes.push({ kind: 'hex', x: c.x + .4, y: c.y - 1.2, r: 3.0, recipe: 'chipG', bw: .4, acc: ACC.gold });
  const P = G.PANEL;
  shapes.push({ kind: 'rect', x: (P.x0 + P.x1) / 2, y: (P.top + P.bot) / 2, w: P.x1 - P.x0, h: P.bot - P.top, recipe: 'chipG', bw: .6, acc: ACC.gold });
  const A = G.ACTS, n = D.acts.length, w = (A.x1 - A.x0 - (n - 1) * A.gap) / n;
  for (let k = 0; k < n; k++) shapes.push({ kind: 'rect', x: A.x0 + k * (w + A.gap) + w / 2, y: (A.top + A.bot) / 2, w, h: A.bot - A.top,
                                            recipe: 'panel', bw: .5, acc: ACC.cyan });
  return { focus: { x: 40, y: 44 }, lift: -50.0, stars: [[8, 20, .2], [66, 14, .18], [70, 80, .18]], shapes };
}

export function hud(h, D) {
  const G = geometry(D), { W, r, U, U4, PANEL: P, ACTS: A } = G;
  const { text, el, glassEdge, rectPts, line, port, wrap } = h;
  const links = [];
  h.titleStrip(D.number, D.title, D.right);
  text(7.5, 16.6, D.heads[0], 6.5, 'cap', HEAD, 'start');
  // the three comparisons: each passes (a port on its edge; its transition and a check mark outside the triangle)
  const c = { x: (U[0].x + U[1].x + U[2].x) / 3, y: (U[0].y + U[1].y + U[2].y) / 3 };
  const tl = [['t_{12}', 0, 1], ['t_{23}', 1, 2], ['t_{13}', 0, 2]];
  for (const [lab, a, b] of tl) {
    const p = U[a], q = U[b], L = Math.hypot(q.x - p.x, q.y - p.y), ux = (q.x - p.x) / L, uy = (q.y - p.y) / L;
    line(p.x + ux * (r * .9), p.y + uy * (r * .9), q.x - ux * (r * .9), q.y - uy * (r * .9), LIGHT.cyan, .32);
    const mx = (p.x + q.x) / 2, my = (p.y + q.y) / 2;
    port(mx, my, ACC.cyan);
    let nx = -uy, ny = ux;
    if ((mx - c.x) * nx + (my - c.y) * ny < 0) { nx = -nx; ny = -ny; }     // the outward normal
    text(mx + nx * 4.4 - ux * 2.6, my + ny * 4.4 - uy * 2.6 + 1.2, lab, 8.2, 'math', LIGHT.cyan, 'middle');
    text(mx + nx * 4.4 + ux * 3.4, my + ny * 4.4 + uy * 3.4 + 1.0, '✓', 7.0, 'math', LIGHT.cyan, 'middle');
  }
  U.forEach((u, k) => {
    glassEdge(hexPts(u.x, u.y, r - .08), ACC.cyan, .3, .95);
    text(u.x, u.y - 1.2, `U_{${k + 1}}`, 10.0, 'math', INK, 'middle');
    text(u.x, u.y + 4.2, `s_{${k + 1}}`, 8.0, 'math', SEC, 'middle');
  });
  glassEdge(hexPts(c.x + .4, c.y - 1.2, 2.94), ACC.gold, .26, .95);
  text(c.x + .4, c.y - .1, '≠', 8.0, 'math', LIGHT.gold, 'middle');
  text(c.x + 1.6, c.y + 5.6, 't_{23} ∘ t_{12} ≠ t_{13}', 7.8, 'math', LIGHT.gold, 'middle');
  text(7.5, 63.6, `“${D.pass}”`, 7.0, 'it', SEC, 'start');
  // the fourth chart, excluded
  glassEdge(hexPts(U4.x, U4.y, r * .62 - .06), ACC.cyan, .2, .45, '.6 .5');
  text(U4.x, U4.y + 1.1, 'U_{4}', 8.0, 'math', SEC, 'middle');
  text(30.0, 72.6, D.heads[2], 6.5, 'cap', HEAD, 'start');
  text(30.0, 75.8, D.excluded, 7.0, 'it', SEC, 'start');
  // the record
  glassEdge(rectPts(P.x0, P.top, P.x1, P.bot), ACC.gold, .28, .85);
  const pw = P.x1 - P.x0 - 6.0;
  text(P.x0 + 3.0, P.top + 4.8, D.heads[1], 6.5, 'cap', LIGHT.gold, 'start', pw);
  D.keeps.forEach((s, k) => {
    const y = P.top + 10.4 + k * 3.35;
    glassEdge(hexPts(P.x0 + 4.2, y - .85, .72), ACC.gold, .2, .95);
    text(P.x0 + 6.4, y, s, 7.0, 'txt', INK, 'start', pw - 3.4, 'keep');
  });
  let qy = P.top + 10.4 + D.keeps.length * 3.35 + 2.6;
  for (const l of wrap(`“${D.quote}”`, 6.6, 'it', pw)) { text(P.x0 + 3.0, qy, l, 6.6, 'it', SEC, 'start', pw, 'pq'); qy += 2.75; }
  // where the theses act
  text(7.5, A.top - 2.6, D.heads[3], 6.5, 'cap', HEAD, 'start');
  const n = D.acts.length, w = (A.x1 - A.x0 - (n - 1) * A.gap) / n;
  D.acts.forEach((a, k) => {
    const x0 = A.x0 + k * (w + A.gap), tw = w - 3.6;
    glassEdge(rectPts(x0, A.top, x0 + w, A.bot), ACC.cyan, .24, .7);
    text(x0 + 1.8, A.top + 4.2, `THESIS ${a.num}`, 6.5, 'lab', LIGHT.cyan, 'start', tw, 'alab');
    wrap(a.text, 6.6, 'it', tw).forEach((l, j) => text(x0 + 1.8, A.top + 7.9 + j * 2.65, l, 6.6, 'it', INK, 'start', tw, 'atext'));
    links.push({ x: x0, y: A.top, w, h: A.bot - A.top, to: `thesis-${a.num}` });
  });
  footer(h, D);
  done(links);
}
