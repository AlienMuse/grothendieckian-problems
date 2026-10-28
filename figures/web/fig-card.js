// Paper II, "card": what a card contains (Section 1.2), with the card of Problem 49 as the example. On the left the
// card as printed — its heading and the first words of each of its ten fields; on the right what each field records,
// in the words of Section 1.2. Below, the three things published with every card.
import { ACC, LIGHT, INK, SEC, HEAD } from './lib.js';
import { footer, done } from './rs.js';

const geometry = (D) => {
  const [W, H] = D.size_mm;
  const CARD = { x0: 7.5, x1: 71.0, top: 13.8, bot: 113.2 }, NOTE = { x0: 77.0, x1: W - 7.5 };
  const rows = D.rows.map((r, k) => ({ y: CARD.top + 15.6 + k * 8.7 }));
  return { W, H, CARD, NOTE, rows, FOOT: { top: 116.8, bot: 137.0 } };
};

export function light(D) {
  const G = geometry(D), C = G.CARD, F = G.FOOT;
  const shapes = [{ kind: 'rect', x: (C.x0 + C.x1) / 2, y: (C.top + C.bot) / 2, w: C.x1 - C.x0, h: C.bot - C.top, recipe: 'panel', bw: .7 }];
  const n = 3, w = (G.W - 15 - 2 * 1.6) / n;
  for (let k = 0; k < n; k++) shapes.push({ kind: 'rect', x: 7.5 + k * (w + 1.6) + w / 2, y: (F.top + F.bot) / 2, w, h: F.bot - F.top,
                                            recipe: 'chipG', bw: .5, acc: ACC.gold });
  return { focus: { x: 40, y: 60 }, lift: -40.0, stars: [[124, 20, .18], [76, 112, .16], [126, 100, .18]], shapes };
}

export function hud(h, D) {
  const G = geometry(D), { W, CARD: C, NOTE: N, rows, FOOT: F } = G;
  const { text, el, glassEdge, rectPts, line, wrap, measure } = h;
  h.titleStrip(D.number, D.title, D.right);
  glassEdge(rectPts(C.x0, C.top, C.x1, C.bot), ACC.cyan, .26, .7);
  // the card's heading: number and title, kind and level
  text(C.x0 + 3.0, C.top + 5.4, `Problem ${D.heading.num}`, 7.4, 'name', INK, 'start');
  text(C.x0 + 3.0 + measure(`Problem ${D.heading.num}`, 7.4, 'name') + 2.0, C.top + 5.4, D.heading.title, 7.2, 'it', INK, 'start');
  text(C.x1 - 3.0, C.top + 9.0, D.heading.tags, 6.5, 'cap', LIGHT.cyan, 'end');
  line(C.x0 + 3.0, C.top + 11.0, C.x1 - 3.0, C.top + 11.0, 'rgb(164,222,229)', .18, null, .45);
  const cw = C.x1 - C.x0 - 6.0;
  D.rows.forEach((r, k) => {
    const y = rows[k].y, bar = r.label === 'Statement' || r.label === 'Solved when';
    if (bar) line(C.x0 + 1.6, y - 2.6, C.x0 + 1.6, y + 3.6, LIGHT.cyan, .5);
    const lab = r.label.replace(' (28 October 2026)', '').toUpperCase();
    text(C.x0 + 3.0, y, lab, 6.5, 'cap', LIGHT.cyan, 'start', cw, 'flab');
    // the first words of the field, as far as they fit one line, then an ellipsis
    const words = r.text.split(' ');
    let s = '';
    for (const w of words) { const next = s ? `${s} ${w}` : w; if (measure(next + ' …', 6.6, 'it') > cw) break; s = next; }
    text(C.x0 + 3.0, y + 3.2, s.length < r.text.length ? `${s} …` : s, 6.6, 'it', SEC, 'start', cw, 'fx');
    // what the field records
    const ls = wrap(r.what, 6.8, 'txt', N.x1 - N.x0);
    ls.forEach((l, j) => text(N.x0, y + j * 2.9 + (ls.length === 1 ? 1.5 : 0), l, 6.8, 'txt', INK, 'start', N.x1 - N.x0 + .5, 'what'));
    line(C.x1 + .8, y + .5, N.x0 - 1.4, y + .5, 'rgb(164,222,229)', .2, '.5 .5', .7);
  });
  // what is published with every card
  const n = 3, w = (W - 15 - 2 * 1.6) / n;
  const notes = [['QUOTATIONS', D.checks[0]], ['LITERATURE CHECK', D.checks[1]], ['LEAN', D.lean]];
  notes.forEach(([head, s], k) => {
    const x0 = 7.5 + k * (w + 1.6);
    glassEdge(rectPts(x0, F.top, x0 + w, F.bot), ACC.gold, .24, .8);
    text(x0 + 2.0, F.top + 4.0, head, 6.5, 'cap', LIGHT.gold, 'start', w - 4.0);
    wrap(s, 6.5, 'it', w - 4.0).forEach((l, j) => text(x0 + 2.0, F.top + 7.2 + j * 2.6, l, 6.5, 'it', INK, 'start', w - 3.5, 'note'));
  });
  footer(h, D);
  done([{ x: C.x0, y: C.top, w: C.x1 - C.x0, h: C.bot - C.top, to: 'problem-49' }]);
}
