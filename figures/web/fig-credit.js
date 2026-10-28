// Paper II, "credit": participation and credit (Section 1.4). What can be submitted, where, how it is checked, and
// where a solution and a correction are recorded; no prize. Every phrase is the paper's.
import { ACC, LIGHT, INK, SEC, HEAD } from './lib.js';
import { footer, done } from './rs.js';

const geometry = (D) => {
  const [W, H] = D.size_mm;
  const K = { x0: 7.5, x1: 55.0, top: 19.4 }, PH = 5.4, PG = .7;
  const kinds = D.kinds.map((s, k) => ({ x0: K.x0, x1: K.x1, top: K.top + k * (PH + PG), bot: K.top + k * (PH + PG) + PH }));
  const WHERE = { x0: 61.0, x1: 92.0, top: 19.4, bot: kinds[4].bot }, HOW = { x0: 98.0, x1: W - 7.5, top: 19.4, bot: kinds[4].bot };
  const RT = kinds[4].bot + 9.6, RB = RT + 17.0;
  const CORR = { x0: 7.5, x1: 40.0, top: RT, bot: RB };
  const rw = (W - 7.5 - 46.0 - 2 * 1.6) / 3;
  const recs = [0, 1, 2].map(k => ({ x0: 46.0 + k * (rw + 1.6), x1: 46.0 + k * (rw + 1.6) + rw, top: RT, bot: RB }));
  return { W, H, kinds, WHERE, HOW, CORR, recs };
};
const box = (b, recipe, acc) => ({ kind: 'rect', x: (b.x0 + b.x1) / 2, y: (b.top + b.bot) / 2, w: b.x1 - b.x0, h: b.bot - b.top,
                                   recipe, bw: .5, acc });

export function light(D) {
  const G = geometry(D);
  const shapes = G.kinds.map((b, k) => box(b, k === 4 ? 'chipG' : 'chipC', k === 4 ? ACC.gold : ACC.cyan));
  shapes.push(box(G.WHERE, 'panel', ACC.cyan), box(G.HOW, 'panel', ACC.cyan), box(G.CORR, 'chipG', ACC.gold));
  G.recs.forEach(b => shapes.push(box(b, 'chipB', ACC.blue)));
  return { focus: { x: 66, y: 40 }, lift: -62.0, stars: [[44, 14, .16], [126, 52, .16]], shapes };
}

export function hud(h, D) {
  const G = geometry(D), { W, kinds, WHERE, HOW, CORR, recs } = G;
  const { text, glassEdge, rectPts, line, arrow, wrap } = h;
  h.titleStrip(D.number, D.title, D.right);
  text(7.5, 16.6, D.heads[0], 6.5, 'cap', HEAD, 'start');
  text(WHERE.x0, 16.6, D.heads[1], 6.5, 'cap', HEAD, 'start');
  text(HOW.x0, 16.6, D.heads[2], 6.5, 'cap', HEAD, 'start');
  kinds.forEach((b, k) => {
    glassEdge(rectPts(b.x0, b.top, b.x1, b.bot), k === 4 ? ACC.gold : ACC.cyan, .24, .85);
    text(b.x0 + 2.0, b.top + 3.6, D.kinds[k], 6.6, 'txt', INK, 'start', b.x1 - b.x0 - 3.5, 'kind');
  });
  const para = (b, lines, top) => { let y = top;
    for (const [s, size, cls, col] of lines) for (const l of wrap(s, size, cls, b.x1 - b.x0 - 4.4)) {
      text(b.x0 + 2.2, y, l, size, cls, col, 'start', b.x1 - b.x0 - 4.0, cls + size); y += size * .42; } return y; };
  glassEdge(rectPts(WHERE.x0, WHERE.top, WHERE.x1, WHERE.bot), ACC.cyan, .24, .7);
  text(WHERE.x0 + 2.2, WHERE.top + 6.0, 'Issue n', 9.0, 'code', INK, 'start');
  para(WHERE, [[`${D.thread}. Everything ${D.via}.`, 6.8, 'it', SEC]], WHERE.top + 10.8);
  glassEdge(rectPts(HOW.x0, HOW.top, HOW.x1, HOW.bot), ACC.cyan, .24, .7);
  text(HOW.x0 + 2.2, HOW.top + 6.0, 'Solved when', 9.0, 'code', INK, 'start');
  para(HOW, [[`the criterion of its card, so that a solution can be ${D.check}.`, 6.8, 'it', SEC]], HOW.top + 10.8);
  const my = (WHERE.top + WHERE.bot) / 2;
  line(kinds[0].x1 + .6, my, WHERE.x0 - 1.4, my, LIGHT.cyan, .32); arrow(WHERE.x0 - .9, my, 0, LIGHT.cyan, .65);
  line(WHERE.x1 + .6, my, HOW.x0 - 1.4, my, LIGHT.cyan, .32); arrow(HOW.x0 - .9, my, 0, LIGHT.cyan, .65);
  // records
  text(recs[0].x0, recs[0].top - 2.6, D.heads[3], 6.5, 'cap', HEAD, 'start');
  text(CORR.x0, CORR.top - 2.6, D.heads[4], 6.5, 'cap', HEAD, 'start');
  const hx = (HOW.x0 + HOW.x1) / 2;
  line(hx, HOW.bot + .6, hx, recs[2].top - 4.6, LIGHT.blue, .32); arrow(hx, recs[2].top - 4.1, Math.PI / 2, LIGHT.blue, .6);
  recs.forEach((b, k) => {
    glassEdge(rectPts(b.x0, b.top, b.x1, b.bot), ACC.blue, .26, .85);
    para(b, [[D.records[k], 6.6, 'it', INK]], b.top + 4.0);
  });
  glassEdge(rectPts(CORR.x0, CORR.top, CORR.x1, CORR.bot), ACC.gold, .26, .85);
  para(CORR, [[D.errata.charAt(0).toUpperCase() + D.errata.slice(1), 6.6, 'it', INK]], CORR.top + 4.0);
  const cx = (CORR.x0 + CORR.x1) / 2;
  line(cx, kinds[4].bot + .6, cx, CORR.top - 4.6, LIGHT.gold, .32); arrow(cx, CORR.top - 4.1, Math.PI / 2, LIGHT.gold, .6);
  footer(h, D);
  done([]);
}
