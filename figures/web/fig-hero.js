// The banner of the repository of the three papers (author 2026-10-29: the series' banner, same specification):
// Series 00's fig-banner.js (the series covers' ground, aurora, black glass and type; the title block left, the
// seven-cell honeycomb right; the same geometry and sizes), with one change: the third line of each cell is the
// range of the problems drawn from that work, instead of the formula of its cover. Data: data-hero.json and
// data-social.json, written by tools/banner.py from programme.yaml and the problem cards.
import { ACC, LIGHT, INK, HEAD, PT, hexPts, rgb } from './lib.js';
import { done } from './rs.js';

// the front cover's colours (covers/cover.css: .master-kicker, h1, .master-subtitle, .world-index, .core-title, author)
const KICK = '#6be5dc', TITLE = '#faf7ef', SUBT = '#dce8e9', CELLNAME = '#f0f5f3', CORENAME = '#7df0e6',
      AUTHOR = '#f8f6ee', IMPRINT = '#7cebe2', FORMULA = '#e3edee';
const RECIPE = { cyan: 'wCyan', blue: 'wBlue', violet: 'wViolet' };

const geometry = (D) => {
  const [W, H] = D.size_mm;
  const R = D.fill * H / (6 * Math.sqrt(3) / 2);                   // the honeycomb is 6 · √3/2 · R high
  const DX = 1.5 * R, DY = Math.sqrt(3) / 2 * R;
  // the honeycomb alone (D.honeycomb_only: the site's clickable honeycomb, tools/web_assets.py) is centred
  const C0 = D.honeycomb_only ? { x: W / 2, y: H / 2 } : { x: W - D.right - 2.5 * R, y: H / 2 };
  const POS = { centre: [0, 0], top: [0, -2 * DY], 'upper-right': [DX, -DY], 'lower-right': [DX, DY],
                bottom: [0, 2 * DY], 'lower-left': [-DX, DY], 'upper-left': [-DX, -DY] };
  const cellXY = (p) => ({ x: C0.x + POS[p][0], y: C0.y + POS[p][1] });
  const TX = D.left, TW = C0.x - 2.5 * R - D.gap - TX;             // the title block: from the left margin to the gap
  return { W, H, R, DX, DY, C0, cellXY, GAP: Math.max(.22, R * .018), TX, TW };
};

export function light(D) {
  const G = geometry(D);
  const shapes = [], backings = [];
  for (const c of D.cells) { const { x, y } = G.cellXY(c.position); backings.push({ x, y, r: G.R + .06 }); }
  for (const c of D.cells) {
    const { x, y } = G.cellXY(c.position);
    shapes.push({ kind: 'hex', x, y, r: G.R - G.GAP, recipe: c.series === '01' ? 'wCore' : RECIPE[c.colour], bw: G.R * .05,
                  acc: c.series === '01' ? ACC.blue : ACC[c.colour] });
  }
  // the ribbons of the cover, lifted so that they cross the banner behind the honeycomb
  return { focus: G.C0, lift: D.lift, stars: D.stars, backings, shapes };
}

export function hud(h, D) {
  const G = geometry(D), { R, DY, C0, cellXY, TX, TW, H } = G;
  const { el, glassEdge, inHex, line, measure } = h;
  // the colour of a line as an inline style: style.css sets "#hud text { fill: #f3f5f1 }", which overrides a fill
  // attribute (the book's figures print every word in that one colour); the banners take the cover's colours
  const text = (x, y, str, size, cls, fill, anchor, maxW, group, floor) =>
    h.text(x, y, str, size, cls, fill, anchor, maxW, group, floor, { style: `fill: ${fill}` });
  const s = R / 14.55;                            // the cells' type scales with the honeycomb (first revision: s = 1)
  // the three lines of a cell are stacked about its centre, the name (the widest line, in the cover's Black) on the
  // centre line where the cell is widest; each line's width is the cell's width at the line's farthest point
  const RE = R - G.GAP, M = 1.0 * s;
  // ---- the seven cells: SERIES 0n, the short name of the cover, the cover's formula
  for (const c of D.cells) {
    const { x, y } = cellXY(c.position);
    if (c.series === '01') {                      // the core: an edge running from teal into blue
      const hp = hexPts(x, y, RE - .12 * s), mix = (t) => {
        const a = rgb(ACC.cyan), b = rgb(ACC.blue);
        return '#' + a.map((v, k) => Math.round(255 * (v + (b[k] - v) * t)).toString(16).padStart(2, '0')).join(''); };
      const span = (px, py) => Math.min(1, Math.max(0, ((px - (x - RE)) + (py - (y - RE * .866))) / (2 * RE + 2 * RE * .866)));
      for (let k = 0; k < 6; k++) { const a = hp[k], b = hp[(k + 1) % 6];
        for (let j = 0; j < 12; j++) { const t0 = j / 12, t1 = (j + 1) / 12;
          const xa = a[0] + (b[0] - a[0]) * t0, ya = a[1] + (b[1] - a[1]) * t0, xb = a[0] + (b[0] - a[0]) * t1, yb = a[1] + (b[1] - a[1]) * t1;
          el('line', { x1: xa, y1: ya, x2: xb, y2: yb, stroke: mix(span((xa + xb) / 2, (ya + yb) / 2)), 'stroke-width': .40 * s, 'stroke-linecap': 'round' }); } }
    } else glassEdge(hexPts(x, y, RE - .1 * s), ACC[c.colour], .34 * s, 1);
    text(x, y - 6.8 * s, `SERIES ${c.series}`, 7.0 * s, 'blab', LIGHT[c.colour], 'middle', inHex(RE, 8.6 * s, M), 'series');
    text(x, y - .4 * s, c.label, 10.2 * s, 'bname', c.series === '01' ? CORENAME : CELLNAME, 'middle',
         inHex(RE, 2.5 * s, M), 'label', 7.4 * s);
    // the range of the problems drawn from this work (the cards), in the italic of the cells' roles
    text(x, y + 6.0 * s, c.range, 8.6 * s, 'it', FORMULA, 'middle', inHex(RE, 7.0 * s, M), 'range', 7.0 * s);
  }
  // the kernel's edge, drawn heavier, and the ports on the shared edges
  const ky = C0.y - DY;
  line(C0.x - R / 2 + .8 * s, ky, C0.x + R / 2 - .8 * s, ky, ACC.cyan, .8 * s, null, 1);
  for (const c of D.cells) {
    if (c.position === 'centre' || c.position === 'top') continue;
    const p = cellXY(c.position);
    el('circle', { cx: (p.x + C0.x) / 2, cy: (p.y + C0.y) / 2, r: .82 * s, fill: '#05111b', stroke: ACC[c.colour], 'stroke-width': .3 * s });
  }
  if (D.honeycomb_only) { done([]); return; }
  // ---- the title block, as on the front cover: kicker, title, subtitle, edition line, author and imprint. The title
  //      is set as large as the width allows (at most D.title_max); every other size and every interval follows it.
  const T = Math.min(D.title_max, ...D.title_lines.map(l => D.title_max * TW / measure(l, D.title_max, 'title')));
  const em = T * PT;
  // (each in proportion to the title, never below 7 pt for the lines in capitals, 9 pt for the subtitle and the name)
  const sizes = { kick: Math.max(7, .215 * T), sub: Math.max(9, .33 * T), ed: Math.max(7, .205 * T),
                  auth: Math.max(9, .34 * T), imp: Math.max(7, .215 * T) };
  let subLines = h.wrap(D.subtitle, sizes.sub, 'it', TW);
  if (subLines.length > 1) {                     // one line, smaller, rather than two
    sizes.sub = Math.max(9, sizes.sub * TW / measure(D.subtitle, sizes.sub, 'it'));
    subLines = [D.subtitle];
  }
  // baselines, from the kicker down, in ems of the title (cover: kicker, h1 line-height .98, subtitle, edition)
  const nT = D.title_lines.length;
  const steps = { title1: 1.02, title: .98, sub: .80, ed: .62, rule: .33, auth: .58 };
  const cap = sizes.kick * PT * .7;              // the kicker's capital height: the block starts at its top
  const height = cap + (steps.title1 + (nT - 1) * steps.title + steps.sub + steps.ed + steps.rule + steps.auth) * em;
  let y = H / 2 - height / 2 + cap + (D.title_shift || 0);
  text(TX, y, D.kicker, sizes.kick, 'bkick', KICK, 'start', TW, 'kicker', 7);
  y += steps.title1 * em;
  D.title_lines.forEach((l, k) => text(TX, y + k * steps.title * em, l, T, 'title', TITLE, 'start', TW + .01, 'title', 18));
  y += (nT - 1) * steps.title * em + steps.sub * em;
  text(TX, y, subLines[0], sizes.sub, 'it', SUBT, 'start', TW + .01, 'subtitle', 9);
  y += steps.ed * em;
  text(TX, y, D.edition_line, sizes.ed, 'bcap', HEAD, 'start', TW, 'edition', 7);
  y += steps.rule * em;
  line(TX, y - .1 * em, TX + Math.min(TW, 3.1 * em), y - .1 * em, 'rgb(164,222,229)', .22 * s, null, .45);
  y += steps.auth * em;
  text(TX, y, D.author, sizes.auth, 'bauth', AUTHOR, 'start', TW, 'author', 9);
  text(TX + measure(D.author, sizes.auth, 'bauth') + .42 * em, y, D.imprint, sizes.imp, 'bimp', IMPRINT, 'start', null, 'imprint', 7);
  done([]);
}
