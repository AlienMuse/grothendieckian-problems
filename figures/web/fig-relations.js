// Paper I, "relations": how the theses fit together — only the relations that Section 5 states, each labelled with
// its words: Theses 1 and 2 say what an artefact is; Thesis 6 depends on both; Thesis 7 locates the last passage
// outside the producing system; Theses 4 and 5 are the reasoning step the others constrain; Theses 8–12 the method the
// architecture is meant to support; Thesis 3 would be idle without Thesis 11; Thesis 9 makes the ledger of Thesis 12
// checkable; Thesis 8 is held to the conditions of S01 Vol. III §5.1. Each node links to its thesis.
import { ACC, LIGHT, INK, SEC, HEAD, hexPts } from './lib.js';
import { footer, done } from './rs.js';

const RECIPE = { cyan: 'chipC', blue: 'chipB', gold: 'chipG' };
const R = 6.2;
const geometry = (D) => {
  const [W, H] = D.size_mm;
  const P = { 1: [16, 31], 2: [40, 31], 6: [74, 31], 7: [112, 31], 4: [16, 78], 5: [40, 78], 3: [92, 78],
              8: [17, 117], 9: [42, 117], 10: [67, 117], 11: [92, 117], 12: [117, 117] };
  const panels = [{ top: 17.6, bot: 57.0, head: 15.6 }, { top: 65.0, bot: 95.0, head: 63.0 }, { top: 103.2, bot: 149.0, head: 101.2 }];
  return { W, H, P, panels };
};

export function light(D) {
  const G = geometry(D), shapes = [];
  for (const p of G.panels) shapes.push({ kind: 'rect', x: G.W / 2, y: (p.top + p.bot) / 2, w: G.W - 15, h: p.bot - p.top, recipe: 'panel', bw: .6 });
  for (const n of D.nodes) { const [x, y] = G.P[n.num];
    shapes.push({ kind: 'hex', x, y, r: R - .2, recipe: RECIPE[n.group], under: 'panel', bw: .5, acc: ACC[n.group] }); }
  return { focus: { x: G.W / 2, y: 64 }, lift: -46.0, stars: [[6, 62, .2], [126, 60, .2], [70, 99, .16]], shapes };
}

export function hud(h, D) {
  const G = geometry(D), { W, P, panels } = G;
  const { text, el, glassEdge, line, arrow, curve, wrap } = h;
  const E = D.edges, links = [];
  h.titleStrip(D.number, D.title, D.right);
  const heads = [['THE ARTEFACT AND THE PASSAGES OF ITS STATUS · THESES 1, 2, 6, 7', null],
                 ['THE REASONING STEP · THESES 4, 5', 'THE CARRIER · THESIS 3'], ['THE METHOD OF DISCOVERY · THESES 8–12', null]];
  panels.forEach((p, k) => {
    el('rect', { x: 7.5, y: p.top, width: W - 15, height: p.bot - p.top, fill: 'none', stroke: 'rgb(164,222,229)', 'stroke-opacity': .3, 'stroke-width': .24 });
    text(7.5, p.head, heads[k][0], 6.5, 'cap', HEAD, 'start');
    if (heads[k][1]) text(W - 7.5, p.head, heads[k][1], 6.5, 'cap', HEAD, 'end');
  });
  const it = (x, y, s, w, c = SEC, anchor = 'middle', size = 6.6) => {
    const ls = wrap(s, size, 'it', w);
    ls.forEach((l, j) => text(x, y + j * 2.7, l, size, 'it', c, anchor, w + .5, 'elabel'));
    return ls.length;
  };
  for (const n of D.nodes) {
    const [x, y] = P[n.num], acc = n.group;
    glassEdge(hexPts(x, y, R - .26), ACC[acc], .28, .95);
    text(x, y + 1.25, String(n.num), 8.6, 'code', LIGHT[acc], 'middle');
    if (n.num === 3) {                             // Thesis 3: its name beside it, so that the arrow from 11 meets it
      wrap(n.title, 6.5, 'txt', 24.0).forEach((l, j) => text(x + R + 2.2, y - .6 + j * 2.75, l, 6.5, 'txt', INK, 'start', 25.0, 'nname'));
    } else {
      wrap(n.title, 6.5, 'txt', 19.5).forEach((l, j) => text(x, y + R + 3.4 + j * 2.75, l, 6.5, 'txt', INK, 'middle', 21.0, 'nname'));
    }
    links.push({ x: x - R, y: y - R * .87, w: 2 * R, h: 2 * R * .87, to: `thesis-${n.num}` });
  }
  // 1 + 2: what an artefact is (a bracket under the pair)
  const by = 48.0;
  line(6.0, by - 1.4, 6.0, by, LIGHT.cyan, .26); line(6.0, by, 50.0, by, LIGHT.cyan, .26); line(50.0, by - 1.4, 50.0, by, LIGHT.cyan, .26);
  it(28, by + 3.6, E.artefact, 42);
  // 1, 2 → 6, and 6 → 7
  line(47.2, 31, 66.4, 31, LIGHT.cyan, .32); arrow(67.0, 31, 0, LIGHT.cyan, .65);
  it(56.8, 24.4, E.depends, 17);
  line(81.2, 31, 104.4, 31, LIGHT.gold, .32); arrow(105.0, 31, 0, LIGHT.gold, .65);
  it(92.8, 20.8, E.outside, 22);
  // the others constrain the reasoning step (4, 5)
  line(70, 57.6, 70, 64.2, LIGHT.blue, .3); arrow(70, 64.7, Math.PI / 2, LIGHT.blue, .6);   // between the two headings
  it(10.0, 69.4, E.step, 70, SEC, 'start', 6.8);
  // 11 → 3: Thesis 3 would be idle without Thesis 11
  line(P[11][0], P[11][1] - R * .87 - .6, P[3][0], P[3][1] + R * .87 + 1.4, LIGHT.gold, .3);
  arrow(P[3][0], P[3][1] + R * .87 + .9, -Math.PI / 2, LIGHT.gold, .6);
  it(P[3][0] + 3.0, 98.0, `Thesis 3 ${E.idle}`, 28, SEC, 'start');
  // the method: what the architecture is meant to support
  it(10.0, 107.6, E.method, 75, SEC, 'start', 6.8);
  // 9 → 12: the ledger is checkable entry by entry (an arc under the names)
  const ay = P[9][1] + R + 11.0;
  curve([P[9][0] + 4.0, ay], [P[12][0], ay], -3.0, LIGHT.gold, .3, null, .62);
  it((P[9][0] + P[12][0]) / 2, ay + 7.2, `Thesis 9 ${E.ledger}`, 70);
  // 8: held to the conditions of S01 Vol. III §5.1
  it(P[8][0] - 6.0, P[8][1] + R + 7.6, `Thesis 8 is ${E.conditions} of ${D.s01}`, 28, LIGHT.gold, 'start', 6.5);
  footer(h, D);
  done(links);
}
