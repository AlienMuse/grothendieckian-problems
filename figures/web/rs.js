// Shared by the figures of the two papers (tools/figures.py). The design is Series 00's lib.js, unchanged; this module
// adds only what a paper figure needs besides it: the footer line, the problem and thesis chips, the record of every
// drawn line (checked against the PDF text) and the link areas (placed over the figure in LaTeX).
import { ACC, LIGHT, INK, SEC, HEAD, hexPts } from './lib.js';

// the kinds of problem: one accent each, and the glass that carries it. Blue, cyan and gold: of the four accents of the
// series, the three that stay apart under simulated protanopia, deuteranopia and tritanopia (ΔE*ab ≥ 25; blue and
// violet fall to 4 under protanopia: tools/figures.py)
export const KIND = { math: 'blue', machine: 'cyan', formal: 'gold' };
export const CHIP = { cyan: 'chipC', blue: 'chipB', violet: 'chipV', gold: 'chipG' };
export const LEVEL_DOTS = { entry: 1, research: 2, programme: 3 };

export function footer(h, D) {
  h.el('path', { d: `M7.5 ${(h.H - 6.0).toFixed(2)} H${h.W - 7.5}`, stroke: 'rgb(164,222,229)', 'stroke-opacity': .22,
                 'stroke-width': .18, fill: 'none' });
  h.text(h.W - 7.5, h.H - 2.6, D.footer, 6.5, 'txt', SEC, 'end');
}

// a problem chip: a small hexagon of glass (light layer) with the number and its level as one to three dots (HUD)
export function chipShape(x, y, r, kind, under = null) {
  const acc = KIND[kind];
  return { kind: 'hex', x, y, r, recipe: CHIP[acc], under, bw: .35, acc: ACC[acc] };
}
export function chipHud(h, x, y, r, p, links, dots = true) {
  const acc = KIND[p.kind];
  h.glassEdge(hexPts(x, y, r - .06), ACC[acc], .2, .95);
  h.text(x, y + (dots ? .55 : .85), String(p.num), 6.5, 'sb', INK, 'middle');
  if (dots) {
    const n = LEVEL_DOTS[p.level], s = .62;
    for (let k = 0; k < n; k++) h.el('circle', { cx: (x + (k - (n - 1) / 2) * s).toFixed(3), cy: (y + 1.55).toFixed(3), r: .17,
                                                 fill: LIGHT[acc] });
  }
  links.push({ x: x - r, y: y - r * .866, w: 2 * r, h: 2 * r * .866, to: `problem-${p.num}` });
}

export function done(links) {
  const svg = document.getElementById('hud');
  const texts = [...svg.querySelectorAll('text')];
  document.body.dataset.lines = JSON.stringify(texts.map(t => t.textContent));
  document.body.dataset.links = JSON.stringify(links);
  // collisions: two lines of text whose boxes overlap by more than 0.15 mm in both directions (a line that runs into
  // another; 2026-10-28, the title strip of the overview's Figure 1). Boxes are measured on the glyphs as set.
  const boxes = texts.map(t => { const b = t.getBBox(); return { s: t.textContent, x0: b.x, y0: b.y + b.height * .18,
                                                                  x1: b.x + b.width, y1: b.y + b.height * .82 }; });
  const hits = [];
  for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
    const a = boxes[i], b = boxes[j];
    const ox = Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0), oy = Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0);
    if (ox > .15 && oy > .15) hits.push(`“${a.s.slice(0, 40)}” × “${b.s.slice(0, 40)}”`);
  }
  document.body.dataset.overlap = JSON.stringify(hits);
}
export { ACC, LIGHT, INK, SEC, HEAD };
