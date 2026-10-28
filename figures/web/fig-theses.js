// Paper I, "theses": the twelve theses in their three groups (representation, operation, method), each group a strip
// of flat-top cells; in each cell the number of the thesis, its name, and the number of problems of the companion
// paper at which it can be tested. A cell links to its thesis in the paper.
import { ACC, LIGHT, INK, SEC, hexPts } from './lib.js';
import { footer, done } from './rs.js';

const RECIPE = { cyan: 'cyan', blue: 'blue', gold: 'chipG' };
const geometry = (D) => {
  const [W, H] = D.size_mm;
  const R = 13.5, DX = 1.5 * R, DY = Math.sqrt(3) / 2 * R, BAND = 43.6, TOP = 16.6;
  const bands = D.groups.map((g, b) => {
    const n = g.items.length, width = 2 * R + (n - 1) * DX, x0 = W / 2 - width / 2 + R;
    const label = TOP + b * BAND, top = label + 2.6;
    return { label, top, x0, x1: x0 + (n - 1) * DX, left: W / 2 - width / 2, right: W / 2 + width / 2,
             cells: g.items.map((t, k) => ({ x: x0 + k * DX, y: top + DY + (k % 2 ? DY : 0), t })) };
  });
  return { W, H, R, DX, DY, GAP: .35, bands };
};

export function light(D) {
  const G = geometry(D), shapes = [], backings = [];
  G.bands.forEach((b, i) => b.cells.forEach(c => backings.push({ x: c.x, y: c.y, r: G.R + .06 })));
  G.bands.forEach((b, i) => b.cells.forEach(c => shapes.push({ kind: 'hex', x: c.x, y: c.y, r: G.R - G.GAP,
    recipe: RECIPE[D.groups[i].colour], bw: .8, acc: ACC[D.groups[i].colour] })));
  return { focus: { x: G.W / 2, y: G.H * .52 }, lift: -40.0,
           stars: [[8, 30, .24], [124, 26, .22], [6, 92, .2], [126, 110, .2], [14, 136, .18], [118, 70, .18]], backings, shapes };
}

export function hud(h, D) {
  const G = geometry(D), { R } = G;
  const { text, glassEdge, inHex, wrap } = h;
  const links = [];
  h.titleStrip(D.number, D.title, D.right);
  const RE = R - G.GAP, M = 1.4;
  G.bands.forEach((b, i) => {
    const g = D.groups[i], acc = g.colour;
    text(b.left + 1.0, b.label, `${g.name} · ${g.range}`, 6.5, 'cap', LIGHT[acc], 'start');
    const n = g.items.reduce((s, t) => s + t.problems.length, 0);
    text(b.right - 1.0, b.label, `${n} problems`, 6.5, 'txt', SEC, 'end');
    for (const c of b.cells) {
      glassEdge(hexPts(c.x, c.y, RE - .1), ACC[acc], .3, .9);
      text(c.x, c.y - 6.9, String(c.t.num), 10.0, 'code', LIGHT[acc], 'middle', inHex(RE, 9.4, M), 'num');
      const ls = wrap(c.t.title, 7.0, 'name', 21.0);       // three lines at most; the fit narrows a line to its height in the cell
      const y0 = c.y + 1.15 - (ls.length - 1) * 1.65;
      ls.forEach((l, j) => { const y = y0 + j * 3.3;
        text(c.x, y, l, 7.0, 'name', INK, 'middle', inHex(RE, Math.max(Math.abs(y - 1.9 - c.y), Math.abs(y + .6 - c.y)), M), 'tname', 6.5); });
      const k = c.t.problems.length;
      text(c.x, c.y + 8.4, `${k} ${k === 1 ? 'problem' : 'problems'}`, 6.5, 'txt', SEC, 'middle', inHex(RE, 8.9, M), 'tcount');
      links.push({ x: c.x - RE * .8, y: c.y - RE * .8, w: RE * 1.6, h: RE * 1.6, to: `thesis-${c.t.num}` });
    }
  });
  footer(h, D);
  done(links);
}
