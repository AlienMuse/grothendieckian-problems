// Paper II, "selection": how the problems were chosen (Section 1.1, 1.3). The items each work states as open,
// conditional, conjectural or owed, extracted by script from the sealed PDFs (candidates/pool.json); the four rules;
// the literature check and its changes (src/changes.yaml, src/litcheck-queries.yaml); the 57 problems.
import { ACC, LIGHT, INK, SEC, HEAD } from './lib.js';
import { footer, done } from './rs.js';

const geometry = (D) => {
  const [W, H] = D.size_mm;
  return { W, H, A: { x0: 7.5, x1: 63.0, top: 19.4, bot: 62.0 }, B: { x0: 69.0, x1: W - 7.5, top: 19.4, bot: 62.0 },
           C: { x0: 7.5, x1: 31.0, top: 70.4, bot: 98.4 }, Dk: { x0: 37.0, x1: 97.0, top: 70.4, bot: 98.4 },
           E: { x0: 103.0, x1: W - 7.5, top: 70.4, bot: 98.4 } };
};
const box = (b, recipe, acc) => ({ kind: 'rect', x: (b.x0 + b.x1) / 2, y: (b.top + b.bot) / 2, w: b.x1 - b.x0, h: b.bot - b.top,
                                   recipe, bw: .6, acc });

export function light(D) {
  const G = geometry(D), shapes = [box(G.A, 'panel', ACC.cyan), box(G.B, 'panel', ACC.cyan), box(G.C, 'chipB', ACC.blue),
                                    box(G.Dk, 'panel', ACC.gold), box(G.E, 'chipC', ACC.cyan)];
  const max = Math.max(...D.works.map(w => w.n));
  D.works.forEach((w, k) => { const len = 30.0 * w.n / max, y = G.A.top + 9.0 + k * 4.35;
    shapes.push({ kind: 'rect', x: G.A.x0 + 11.0 + len / 2, y: y - .95, w: len, h: 2.5, recipe: 'barC', under: 'panel', bw: .3, acc: ACC.cyan }); });
  return { focus: { x: 40, y: 40 }, lift: -58.0, stars: [[66, 66, .18], [124, 14, .18], [6, 100, .16]], shapes };
}

export function hud(h, D) {
  const G = geometry(D), { W, A, B, C, Dk, E } = G;
  const { text, el, glassEdge, rectPts, line, arrow, wrap } = h;
  h.titleStrip(D.number, D.title, D.right);
  text(7.5, 16.6, D.heads[0], 6.5, 'cap', HEAD, 'start');
  // A: extracted items by work
  glassEdge(rectPts(A.x0, A.top, A.x1, A.bot), ACC.cyan, .26, .7);
  const max = Math.max(...D.works.map(w => w.n));
  D.works.forEach((w, k) => { const len = 30.0 * w.n / max, y = A.top + 9.0 + k * 4.35;
    text(A.x0 + 2.4, y, w.work, 6.5, 'sb', SEC, 'start');
    text(A.x0 + 11.0 + len + 1.6, y, w.n.toLocaleString('en-GB'), 6.5, 'sb', INK, 'start'); });
  text(A.x0 + 2.4, A.top + 5.0, 'EXTRACTED FROM THE SEALED PDFS', 6.5, 'cap', LIGHT.cyan, 'start', A.x1 - A.x0 - 4.8);
  text(A.x1 - 2.4, A.bot - 2.6, `${D.total.toLocaleString('en-GB')} ITEMS`, 7.4, 'code', INK, 'end');
  // B: the four rules
  glassEdge(rectPts(B.x0, B.top, B.x1, B.bot), ACC.cyan, .26, .7);
  text(B.x0 + 2.4, B.top + 5.0, D.heads[1], 6.5, 'cap', LIGHT.cyan, 'start');
  let y = B.top + 6.2;
  D.rules.forEach((r, k) => {
    const ls = wrap(r, 7.0, 'txt', B.x1 - B.x0 - 10.0);
    y += 4.4;
    text(B.x0 + 3.0, y, String(k + 1), 7.4, 'code', LIGHT.cyan, 'start');
    ls.forEach((l, j) => text(B.x0 + 7.4, y + j * 3.0, l, 7.0, 'txt', INK, 'start', B.x1 - B.x0 - 10.0, 'rule'));
    y += (ls.length - 1) * 3.0 + 1.2;
  });
  line(A.x1 + .6, (A.top + A.bot) / 2, B.x0 - 1.4, (A.top + A.bot) / 2, LIGHT.cyan, .32); arrow(B.x0 - .9, (A.top + A.bot) / 2, 0, LIGHT.cyan, .65);
  // C: the 57 selected
  const mid = (C.top + C.bot) / 2;
  line((B.x0 + B.x1) / 2, B.bot + .6, (B.x0 + B.x1) / 2, 66.0, LIGHT.cyan, .32);
  line((B.x0 + B.x1) / 2, 66.0, (C.x0 + C.x1) / 2, 66.0, LIGHT.cyan, .32);
  line((C.x0 + C.x1) / 2, 66.0, (C.x0 + C.x1) / 2, C.top - 1.4, LIGHT.cyan, .32); arrow((C.x0 + C.x1) / 2, C.top - .9, Math.PI / 2, LIGHT.cyan, .65);
  glassEdge(rectPts(C.x0, C.top, C.x1, C.bot), ACC.blue, .28, .9);
  text((C.x0 + C.x1) / 2, mid - 1.6, String(D.final.n), 14.0, 'code', INK, 'middle');
  text((C.x0 + C.x1) / 2, mid + 4.6, 'SELECTED', 6.5, 'cap', LIGHT.blue, 'middle');
  // D: the literature check
  glassEdge(rectPts(Dk.x0, Dk.top, Dk.x1, Dk.bot), ACC.gold, .28, .85);
  const dw = Dk.x1 - Dk.x0 - 4.8;
  text(Dk.x0 + 2.4, Dk.top + 4.8, D.heads[2], 6.5, 'cap', LIGHT.gold, 'start', dw);
  let ly = Dk.top + 6.4;
  for (const s of [`${D.queries} search strings, two or more per problem, against ${D.searched[0]}`,
                   `code search: ${D.searched[1]}`])
    for (const l of wrap(s, 6.8, 'txt', dw)) { ly += 2.9; text(Dk.x0 + 2.4, ly, l, 6.8, 'txt', INK, 'start', dw, 'lc'); }
  text(Dk.x0 + 2.4, Dk.bot - 2.8, `${D.replaced.length} replaced · ${D.narrowed.length} narrowed`, 7.0, 'sb', LIGHT.gold, 'start', dw);
  text(Dk.x1 - 2.4, Dk.bot - 2.8, 'APPENDIX B', 6.5, 'cap', HEAD, 'end');
  line(C.x1 + .6, mid, Dk.x0 - 1.4, mid, LIGHT.cyan, .32); arrow(Dk.x0 - .9, mid, 0, LIGHT.cyan, .65);
  // E: the problems
  glassEdge(rectPts(E.x0, E.top, E.x1, E.bot), ACC.cyan, .3, .95);
  const ex = (E.x0 + E.x1) / 2;
  text(ex, E.top + 4.8, D.heads[3], 6.5, 'cap', LIGHT.cyan, 'middle', E.x1 - E.x0 - 3.0);
  text(ex, mid + .6, String(D.final.n), 14.0, 'code', INK, 'middle');
  text(ex, mid + 6.0, `Part I: ${D.final.p1}`, 6.5, 'txt', SEC, 'middle');
  text(ex, mid + 8.8, `Part II: ${D.final.p2}`, 6.5, 'txt', SEC, 'middle');
  line(Dk.x1 + .6, mid, E.x0 - 1.4, mid, LIGHT.cyan, .32); arrow(E.x0 - .9, mid, 0, LIGHT.cyan, .65);
  footer(h, D);
  done([]);
}
