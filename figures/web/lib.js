// The figures of The Grothendieckian Programme: one light layer (Three.js) and one vector HUD (SVG) per figure, one
// geometry. Coordinates: millimetres on the printed page, x to the right, y downwards, origin at the top-left corner.
// The WebGL camera is orthographic and looks straight down the z axis, so a point (x, y) of the light layer and of
// the HUD coincide exactly.
// Design (D6, second revision by the author, 2026-10-26; every figure of the book, 2026-10-26): the ground and the
// aurora of the series covers — the 145° gradient of the Series 01 volume covers, and the ribbons of this book's cover
// rendered as the Series 01 volume covers render theirs (Gaussian stroke profiles, curtain filaments) — with every
// cell, panel and bar of a figure made of black glass: the aurora seen through it blurred and darkened, the covers'
// sheen, a bevel lit from the upper left, hairline edges. The aurora is the only light in a figure: no bloom, no glow.
// Type, as on the covers: Segoe UI for labels and names, Pagella italic for roles and phrases, Pagella Math for
// formulas; no line is ever condensed.
import * as THREE from 'three';

export const ACC = { cyan: '#58ded4', blue: '#82a4ff', violet: '#cf8df6', gold: '#dfc174' };
// each accent mixed 78 % with #eaf2f2, as the covers colour their labels
export const LIGHT = { cyan: '#78e2db', blue: '#99b5fc', violet: '#d5a3f5', gold: '#e1cc90' };
export const INK = '#f3f5f1', SEC = '#aebfc7', HEAD = '#b8cbd2', SOFT = '#d3dee3';
export const PT = 0.352778;                       // mm per point

export const hexPts = (cx, cy, r) => Array.from({ length: 6 }, (_, k) => {
  const a = Math.PI / 3 * k; return [cx + r * Math.cos(a), cy + r * Math.sin(a)];
});
// half-width of a flat-top hexagon of circumradius r at vertical offset dy from its centre
export const hexHalfWidth = (r, dy) => Math.max(0, r - Math.abs(dy) / Math.sqrt(3));
export const rgb = (h) => [1, 3, 5].map(k => parseInt(h.slice(k, k + 2), 16) / 255);

// the glass of every shape: tint and opacity of its body (the covers: a cell rgba(5,16,27,.88) × .82, the hero cell a
// gradient #17333d → #14243b → #241b3d, the stage rgba(3,11,19,.69)); the bar recipes are the same glass, tinted
// with the accent of the work it measures
export const GLASS = {
  panel: { tint: '#030b13', alpha: .69, radial: .065, gloss: .7 },
  core: { grad: ['#17333d', '#14243b', '#241b3d'], alpha: .92 },
  cyan: { tint: '#0b2127', alpha: .90 },
  blue: { tint: '#07121f', alpha: .90 },
  violet: { tint: '#100c20', alpha: .90 },
  chipC: { tint: '#0d232a', alpha: .86 },
  chipB: { tint: '#08131f', alpha: .84 },
  chipV: { tint: '#110d21', alpha: .84 },
  chipG: { tint: '#1a160c', alpha: .86 },
  open: { tint: '#06111a', alpha: .34, gloss: .45 },
  plane: { tint: '#0a1820', alpha: .82 },
  barC: { tint: '#1f5f5d', alpha: .86 },
  barB: { tint: '#2a3d72', alpha: .86 },
  barV: { tint: '#4a2f66', alpha: .86 },
  // the banners (fig-banner.js): the cells of the front cover's honeycomb — its world gradients (cyan #143942 →
  // #0a1a25, blue #182e55 → #0a1728, violet #38235a → #151528) and its core plate (#2f5d70 → #253558 → #261d43),
  // as black glass
  wCyan: { grad: ['#143942', '#0f2a33', '#0a1a25'], alpha: .90 },
  wBlue: { grad: ['#182e55', '#11213f', '#0a1728'], alpha: .90 },
  wViolet: { grad: ['#38235a', '#251c40', '#151528'], alpha: .90 },
  wCore: { grad: ['#2f5d70', '#253558', '#261d43'], alpha: .92 },
};
// the aurora's gain against its SVG original: the Series 01 covers calibrate theirs to .87–.96
const AURORA_GAIN = .87;

// the aurora: the ribbons of this book's cover (covers/front-A.html, 816 × 1145 units), scaled to the width of the
// figure and lifted behind its subject; blur radii and opacities of the Series 01 volume covers (σ 24 and 10 units;
// .5, .36)
const SPECTRUM_A = { x1: 0, y1: 0, x2: 1, y2: 0, stops: [[0, '#20f4e5', 1], [.3, '#23cbd5', 1], [.58, '#347dff', 1], [.8, '#8b50f5', 1], [1, '#f052cf', 1]] };
const SPECTRUM_B = { x1: 1, y1: 0, x2: 0, y2: 1, stops: [[0, '#52f4dd', 1], [.43, '#397df4', 1], [.72, '#8b56e9', 1], [1, '#e657bd', 1]] };
const GOLD = { x1: 0, y1: 1, x2: 1, y2: 0, stops: [[0, '#75602f', .22], [.28, '#b8954d', 1], [.54, '#dfc174', 1], [.78, '#a98342', 1], [1, '#65502a', .18]] };
const RIBBONS = [
  // broad: σ 24 units, group opacity .5
  ['M-136 738C44 544 210 558 337 658S595 840 944 562', SPECTRUM_A, 82, 24, .50, 0],
  ['M-112 860C90 626 267 690 410 772S677 852 932 682', SPECTRUM_B, 62, 24, .50, 0],
  ['M-94 586C99 449 259 464 393 542S665 654 921 456', SPECTRUM_A, 44, 24, .50, 0],
  ['M-122 1021C101 830 282 868 438 954S694 1034 938 846', GOLD, 38, 24, .50, 0],
  // defined: σ 10 units, group opacity .36
  ['M-104 720C76 535 215 560 344 654S620 802 914 565', SPECTRUM_A, 30, 10, .36, 1],
  ['M-94 844C102 635 269 689 414 769S670 838 908 690', SPECTRUM_B, 22, 10, .36, 1],
  ['M-70 575C120 453 270 480 401 551S665 630 892 468', SPECTRUM_A, 16, 10, .36, 1],
  ['M-96 1008C118 844 287 877 442 955S688 1015 908 857', GOLD, 11, 10, .36, 1],
];
// the halo of the Series 01 volume covers (rx 300, ry 275 units; stops .32 / .2 / .1 / .045)
const HALO_STOPS = [[0, '#dffcff', .32], [.2, '#58ded4', .2], [.52, '#82a4ff', .1], [.78, '#b353d6', .045], [1, '#071019', 0]];
// the stars of Figure 1 (mm on 150 × 200); other figures take those that fall on their page, or their own
export const STARS_150x200 = [[8, 34, .30], [21, 47, .22], [138, 30, .28], [131, 44, .2], [12, 80, .24], [142, 86, .3], [6, 101, .2],
  [144, 108, .22], [98, 6, .2], [54, 5, .18], [141, 64, .2], [16, 63, .18]];

// "M x y C x1 y1 x2 y2 x y S x2 y2 x y" (cover units) → points along the path in figure mm
function samplePath(d, K, lift) {
  const tok = d.match(/[MCS]|-?\d*\.?\d+/g);
  const T = (x, y) => [x * K, y * K + lift];
  let i = 0, cur = null, lastCtrl = null;
  const segs = [];
  while (i < tok.length) {
    const c = tok[i++];
    const num = () => parseFloat(tok[i++]);
    if (c === 'M') { cur = [num(), num()]; }
    else if (c === 'C') { const p1 = [num(), num()], p2 = [num(), num()], p = [num(), num()]; segs.push([cur, p1, p2, p]); lastCtrl = p2; cur = p; }
    else if (c === 'S') { const p1 = [2 * cur[0] - lastCtrl[0], 2 * cur[1] - lastCtrl[1]], p2 = [num(), num()], p = [num(), num()];
      segs.push([cur, p1, p2, p]); lastCtrl = p2; cur = p; }
  }
  const pts = [];
  for (const [a, b, c2, e] of segs) for (let k = pts.length ? 1 : 0; k <= 160; k++) {
    const t = k / 160, u = 1 - t;
    pts.push(T(u * u * u * a[0] + 3 * u * u * t * b[0] + 3 * u * t * t * c2[0] + t * t * t * e[0],
               u * u * u * a[1] + 3 * u * u * t * b[1] + 3 * u * t * t * c2[1] + t * t * t * e[1]));
  }
  return pts;
}

// ================================================================ light layer ====================================
// S = { W, H, focus: {x, y} (the halo and the radial light of the ground), lift (mm the ribbons are raised),
//       stars: [[x, y, r]], backings: [{x, y, r}] (dark hexagons under a honeycomb: its seams),
//       shapes: [{kind: 'hex' | 'rect', x, y, r | w, h, recipe, under, bw, acc}] (black glass, in drawing order) }
export function renderLight(canvas, dpr, S) {
  const { W, H } = S, F = S.focus, K = W / 816, LIFT = S.lift ?? -40;
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(dpr);
  renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
  // shader values are written as they are: sRGB arithmetic, as CSS and SVG composite and as the Series 01 cover
  // renderer writes its aurora
  renderer.outputColorSpace = THREE.LinearSRGBColorSpace;
  renderer.toneMapping = THREE.NoToneMapping;
  renderer.autoClear = false;
  const buf = renderer.getDrawingBufferSize(new THREE.Vector2());
  const cam = new THREE.OrthographicCamera(0, W, 0, -H, -50, 50);    // x right, y up = −(page y)
  const P = (x, y, z = 0) => new THREE.Vector3(x, -y, z);
  const aur = new THREE.Scene(), comp = new THREE.Scene(), glass = new THREE.Scene();
  const VS = `varying vec2 vp; void main(){ vec4 w = modelMatrix * vec4(position, 1.); vp = vec2(w.x, -w.y);
    gl_Position = projectionMatrix * viewMatrix * w; }`;
  const COMMON = `
    float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
    float noise(vec2 p){ vec2 i = floor(p), f = fract(p); vec2 u = f*f*(3.0-2.0*f);
      return mix(mix(hash(i), hash(i+vec2(1,0)), u.x), mix(hash(i+vec2(0,1)), hash(i+vec2(1,1)), u.x), u.y); }
    float fbm(vec2 p){ float v = 0.0, a = 0.5; for (int k = 0; k < 5; k++){ v += a*noise(p); p *= 2.03; a *= 0.5; } return v; }
    float erf_(float x){ float s = sign(x); x = abs(x); float t = 1.0/(1.0+0.3275911*x);
      float y = 1.0 - (((((1.061405429*t - 1.453152027)*t) + 1.421413741)*t - 0.284496736)*t + 0.254829592)*t*exp(-x*x);
      return s*y; }
    float dither(){ return (hash(gl_FragCoord.xy * 1.37 + 11.3) - .5) / 255.; }
    uniform float stopO[8]; uniform vec4 stopC[8]; uniform int nStops;
    vec4 grad(float t){ t = clamp(t, 0.0, 1.0); vec4 c = stopC[0];
      for (int k = 1; k < 8; k++){ if (k >= nStops) break;
        if (t >= stopO[k-1]) c = mix(stopC[k-1], stopC[k], clamp((t - stopO[k-1]) / max(stopO[k] - stopO[k-1], 1e-5), 0.0, 1.0)); }
      return c; }`;
  const stopsU = (stops) => {
    const o = new Array(8).fill(1), c = new Array(8).fill(0).map(() => new THREE.Vector4(0, 0, 0, 0));
    stops.forEach(([off, hex, a], k) => { o[k] = off; c[k] = new THREE.Vector4(...rgb(hex), a); });
    return { stopO: { value: o }, stopC: { value: c }, nStops: { value: stops.length } };
  };
  const quad = (scene, frag, x, y, w, h, uniforms = {}, blending = THREE.NormalBlending) => {
    const m = new THREE.ShaderMaterial({ uniforms, transparent: blending !== THREE.NoBlending, depthTest: false, depthWrite: false,
      blending, vertexShader: VS, fragmentShader: frag });
    const mesh = new THREE.Mesh(new THREE.PlaneGeometry(w, h), m);
    mesh.position.copy(P(x, y)); scene.add(mesh); return mesh;
  };

  // ---------- 1. the aurora, on black (the Series 01 cover renderer draws its effects layer so, and lays it over the
  //               cover with mix-blend-mode: screen): the halo, the ribbons, a few stars ------------------------------
  const hrx = 300 * K, hry = 275 * K;
  quad(aur, COMMON + `varying vec2 vp; uniform vec4 e;
    void main(){ float r = length((vp - e.xy) / e.zw); if (r > 1.) discard; vec4 g = grad(r); gl_FragColor = vec4(g.rgb, g.a); }`,
    F.x, F.y, 2 * hrx, 2 * hry, { e: { value: new THREE.Vector4(F.x, F.y, hrx, hry) }, ...stopsU(HALO_STOPS) },
    THREE.AdditiveBlending);
  RIBBONS.forEach(([d, paint, width, sigmaU, opac, defined], n) => {
    const pts = samplePath(d, K, LIFT), halfW = width * K / 2, sigma = sigmaU * K;
    const half = halfW + 3.2 * sigma;
    const pos = [], att = [], idx = [];
    let acc = 0, minx = 1e9, miny = 1e9, maxx = -1e9, maxy = -1e9;
    pts.forEach(([x, y]) => { minx = Math.min(minx, x); maxx = Math.max(maxx, x); miny = Math.min(miny, y); maxy = Math.max(maxy, y); });
    for (let i = 0; i < pts.length; i++) {
      const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)];
      let tx = b[0] - a[0], ty = b[1] - a[1]; const l = Math.hypot(tx, ty) || 1; tx /= l; ty /= l;
      if (i > 0) acc += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
      for (const s of [-1, 1]) { pos.push(pts[i][0] - ty * half * s, -(pts[i][1] + tx * half * s), 0); att.push(s * half, acc); }
      if (i < pts.length - 1) { const k = 2 * i; idx.push(k, k + 1, k + 2, k + 1, k + 3, k + 2); }
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute('across', new THREE.Float32BufferAttribute(att, 2));
    g.setIndex(idx);
    const u = { halfW: { value: halfW }, sigma: { value: sigma }, opac: { value: opac },
                bb: { value: new THREE.Vector4(minx, miny, maxx - minx, maxy - miny) },
                gv: { value: new THREE.Vector4(paint.x1, paint.y1, paint.x2, paint.y2) },
                seed: { value: 17.0 + 13.7 * n }, defined: { value: defined }, ...stopsU(paint.stops) };
    const m = new THREE.ShaderMaterial({ uniforms: u, transparent: true, depthTest: false, depthWrite: false, side: THREE.DoubleSide,
      blending: THREE.AdditiveBlending,
      vertexShader: `attribute vec2 across; varying vec2 vA; varying vec2 vP;
        void main(){ vA = across; vP = vec2(position.x, -position.y); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
      // the filament noise runs in cover units, so that the curtains have the covers' grain
      fragmentShader: COMMON + `
        uniform float halfW, sigma, opac, seed, defined; uniform vec4 bb, gv; varying vec2 vA; varying vec2 vP;
        void main(){
          float d = vA.x, s = sigma * 1.41421356;
          float prof = 0.5 * (erf_((d + halfW) / s) - erf_((d - halfW) / s));
          vec2 q = (vP - bb.xy) / bb.zw; vec2 dir = gv.zw - gv.xy;
          float t = dot(q - gv.xy, dir) / max(dot(dir, dir), 1e-6);
          vec4 c = grad(t);
          float along = vA.y / ${K.toFixed(6)}, x = d / max(halfW, 0.2);
          float rays = fbm(vec2(along * 0.11 + seed, x * 0.9));
          float fine = noise(vec2(along * 0.9 + seed * 3.0, x * 2.5));
          float tex = mix(1.0, 0.84 + 0.26 * rays + 0.06 * (fine - 0.5), 0.5 + 0.25 * defined);
          float core = defined * exp(-pow(d / max(halfW * 0.42, 0.12), 2.0)) * 0.12;
          float a = c.a * opac * clamp(prof * tex + core * prof, 0.0, 1.0);
          gl_FragColor = vec4(c.rgb + dither() * step(0.002, a), a);
        }` });
    aur.add(new THREE.Mesh(g, m));
  });
  for (const [x, y, r] of S.stars || []) quad(aur, `varying vec2 vp; uniform vec3 c;
      void main(){ float d = length(vp - c.xy) / c.z; float a = .55 * (smoothstep(1.15, .85, d) + .22 * exp(-d * d * .35));
        gl_FragColor = vec4(vec3(.83, .92, 1.), a); }`, x, y, r * 8, r * 8, { c: { value: new THREE.Vector3(x, y, r) } },
      THREE.AdditiveBlending);
  // ---------- 2. the ground: linear-gradient(145deg, #040a10, #07131e 42 %, #10142a 73 %, #070b15), the faint radial
  //               light of the Series 01 volume covers on the subject, and the aurora over it in screen --------------
  const groundQuad = (() => {
    const a = 145 * Math.PI / 180, dir = [Math.sin(a), -Math.cos(a)];
    const L = Math.abs(W * dir[0]) + Math.abs(H * dir[1]);
    const far = Math.max(...[[0, 0], [W, 0], [0, H], [W, H]].map(([x, y]) => Math.hypot(x - F.x, y - F.y)));
    return quad(comp, COMMON + `varying vec2 vp; uniform sampler2D aurTex; uniform float gain;
      void main(){
        float t = dot(vp - vec2(${(W / 2).toFixed(3)}, ${(H / 2).toFixed(3)}), vec2(${dir[0].toFixed(6)}, ${dir[1].toFixed(6)})) / ${L.toFixed(3)} + .5;
        vec3 g = grad(t).rgb;
        float r = length(vp - vec2(${F.x.toFixed(3)}, ${F.y.toFixed(3)})) / ${(far * .32).toFixed(3)};
        g = mix(g, vec3(61., 210., 204.) / 255., .075 * clamp(1. - r, 0., 1.));
        vec3 a = clamp(texture2D(aurTex, vec2(vp.x / ${W.toFixed(1)}, 1. - vp.y / ${H.toFixed(1)})).rgb * gain, 0., 1.);
        gl_FragColor = vec4(1. - (1. - g) * (1. - a) + dither(), 1.);
      }`, W / 2, H / 2, W, H, { aurTex: { value: null }, gain: { value: AURORA_GAIN },
        ...stopsU([[0, '#040a10', 1], [.42, '#07131e', 1], [.73, '#10142a', 1], [1, '#070b15', 1]]) }, THREE.NoBlending);
  })();

  // ---------- 3. what the glass sees: the ground, rendered small and blurred (σ 2 mm) ----------------------------
  const target = (w, h) => new THREE.WebGLRenderTarget(w, h, { minFilter: THREE.LinearFilter, magFilter: THREE.LinearFilter, depthBuffer: false });
  const lowW = Math.round(W * 3), lowH = Math.round(H * 3);       // 3 px per mm, whatever the output resolution
  const aurLow = target(lowW, lowH), rtA = target(lowW, lowH), rtB = target(lowW, lowH);
  const draw = (scene, rt, camera = cam) => { renderer.setRenderTarget(rt); renderer.setClearColor(0x000000, 1); renderer.clear(); renderer.render(scene, camera); };
  draw(aur, aurLow);
  groundQuad.material.uniforms.aurTex.value = aurLow.texture;
  draw(comp, rtA);
  const fsCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const blurPass = (src, dst, dx, dy) => {
    const s = new THREE.Scene();
    s.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), new THREE.ShaderMaterial({ depthTest: false, depthWrite: false,
      uniforms: { src: { value: src.texture }, stp: { value: new THREE.Vector2(dx / lowW, dy / lowH) } },
      vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0., 1.); }`,
      fragmentShader: `uniform sampler2D src; uniform vec2 stp; varying vec2 vUv;
        void main(){ vec4 a = vec4(0.); float ws = 0.;
          for (int i = -18; i <= 18; i++){ float w = exp(-float(i * i) / 72.); a += texture2D(src, vUv + stp * float(i)) * w; ws += w; }
          gl_FragColor = a / ws; }` })));
    draw(s, dst, fsCam);
  };
  blurPass(rtA, rtB, 1, 0); blurPass(rtB, rtA, 0, 1);
  const seen = rtA.texture;

  // ---------- 4. black glass --------------------------------------------------------------------------------------
  // A slab of dark glass with a rounded edge of width bw, seen from straight above:
  //   transmission  the blurred ground (through the glass beneath, for shapes on a panel), displaced where the edge
  //                 bends it, darkened by the tint; the slab is thicker at the edge, so it passes less there
  //   reflection    Schlick fresnel of a sky with a dark zenith and the aurora's colours at its horizon (cyan above,
  //                 blue to the right, violet below, gold to the left): the face reflects almost nothing, the edge
  //                 reflects the colours of the aurora
  //   key light     upper left: a soft glint on the edges that face it
  //   face          the covers' glass sheen (white .16 → .05 → 0 → #9fe9ff .035 along x .85, y 1 of the box)
  //   thickness     a faint line of light where the face meets the edge
  const glassMat = (shape) => {
    const G = GLASS[shape.recipe], U = shape.under ? GLASS[shape.under] : null;
    const t = G.grad ? G.grad.map(rgb) : [rgb(G.tint), rgb(G.tint), rgb(G.tint)];
    const rect = shape.kind === 'rect';
    return new THREE.ShaderMaterial({ depthTest: false, depthWrite: false, transparent: false,
      uniforms: { seen: { value: seen }, buf: { value: buf }, page: { value: new THREE.Vector2(W, H) },
        t0: { value: new THREE.Vector3(...t[0]) }, t1: { value: new THREE.Vector3(...t[1]) }, t2: { value: new THREE.Vector3(...t[2]) },
        useGrad: { value: G.grad ? 1 : 0 }, alpha: { value: G.alpha },
        tu: { value: new THREE.Vector3(...(U ? rgb(U.tint) : [0, 0, 0])) }, au: { value: U ? U.alpha : 0 },
        c: { value: new THREE.Vector2(shape.x, shape.y) },
        shp: { value: new THREE.Vector3(rect ? shape.w / 2 : shape.r, rect ? shape.h / 2 : 0, rect ? 1 : 0) },
        radial: { value: G.radial || 0 }, bw: { value: shape.bw ?? .6 }, gloss: { value: G.gloss ?? 1 },
        acc: { value: new THREE.Vector3(...rgb(shape.acc || '#a4dee5')) } },
      vertexShader: VS,
      fragmentShader: COMMON + `
        uniform sampler2D seen; uniform vec2 buf, page, c; uniform vec3 t0, t1, t2, tu, shp, acc;
        uniform float useGrad, alpha, au, radial, bw, gloss; varying vec2 vp;
        void main(){
          vec2 p = vp - c;
          vec2 hb = shp.z > .5 ? shp.xy : vec2(shp.x, shp.x * .8660254);
          vec2 q = (p + hb) / (2. * hb);                                   // 0..1 over the bounding box
          float e = 1e9; vec2 n = vec2(0.);                                // distance to the nearest edge, its normal
          if (shp.z > .5) { vec2 dd = hb - abs(p);
            if (dd.x < dd.y) { e = dd.x; n = vec2(sign(p.x), 0.); } else { e = dd.y; n = vec2(0., sign(p.y)); } }
          else { float a = shp.x * .8660254;
            for (int k = 0; k < 6; k++){ float th = radians(30. + 60. * float(k)); vec2 nk = vec2(cos(th), sin(th));
              float dk = a - dot(p, nk); if (dk < e) { e = dk; n = nk; } } }
          float u = clamp(1. - e / bw, 0., 1.);
          float tilt = u * u * (3. - 2. * u);
          vec3 N = normalize(vec3(n * tilt * 2.6, 1.));                    // page axes: x right, y down, z to the eye
          // transmission
          vec2 uv = gl_FragCoord.xy / buf + vec2(n.x, -n.y) * tilt * .9 / page;
          vec3 b = mix(texture2D(seen, uv).rgb, tu, au);
          vec3 tint = t0;
          if (useGrad > .5) { float g = clamp((q.x + q.y) * .5, 0., 1.); tint = g < .54 ? mix(t0, t1, g / .54) : mix(t1, t2, (g - .54) / .46); }
          vec3 col = mix(b, tint, clamp(alpha + (1. - alpha) * .45 * tilt, 0., 1.));
          if (radial > 0.) { float r = length(p) / (length(hb) * .35); col = mix(col, vec3(120., 236., 228.) / 255., radial * clamp(1. - r, 0., 1.)); }
          col *= mix(1.07, .86, q.y);
          // reflection of the sky
          vec3 Rf = vec3(2. * N.z * N.xy, 2. * N.z * N.z - 1.);
          vec2 h = length(Rf.xy) > 1e-4 ? normalize(Rf.xy) : vec2(0.);
          vec3 hz = vec3(.35, .87, .83) * max(-h.y, 0.) + vec3(.81, .55, .96) * .75 * max(h.y, 0.)
                  + vec3(.51, .64, 1.) * .8 * max(h.x, 0.) + vec3(.87, .76, .45) * .45 * max(-h.x, 0.);
          vec3 env = mix(hz, vec3(.02, .035, .05), smoothstep(0., .95, Rf.z));
          float F = .04 + .96 * pow(1. - N.z, 5.);
          col += env * F * 1.15 * gloss;
          // key light
          vec3 Hh = normalize(normalize(vec3(-.5, -.8, .55)) + vec3(0., 0., 1.));
          col += vec3(.94, .98, 1.) * pow(max(dot(N, Hh), 0.), 40.) * .5 * gloss * step(.001, tilt);
          // depth: seen from above, a slab of glass is dark just inside its lit rim
          col *= 1. - .24 * exp(-e / (bw * 1.4)) * (1. - exp(-e / .10));
          // rim light: a bright line along the upper edges, and along the lower ones a faint line of the accent colour,
          // the light that crosses the slab
          float up = max(-n.y, 0.), dn = max(n.y, 0.);
          float rim = exp(-pow((e - .30) / .11, 2.));
          col += vec3(.93, .97, 1.) * rim * (.32 * pow(up, 1.3) + .05) * gloss;
          col += acc * rim * .14 * pow(dn, 1.2) * gloss;
          // face: the covers' sheen, and the reflection of a softbox at the upper left with a soft but definite edge,
          // a fainter second panel beside it
          vec2 dv = vec2(.85, 1.); float s = clamp(dot(q, dv) / dot(dv, dv), 0., 1.);
          float sa = s < .28 ? mix(.16, .05, s / .28) : s < .55 ? mix(.05, 0., (s - .28) / .27) : mix(0., .035, (s - .55) / .45);
          col = mix(col, s < .55 ? vec3(1.) : vec3(159., 233., 255.) / 255., sa * .45 * gloss * (1. - tilt));
          float box = 1. - smoothstep(.37, .43, s);
          col = mix(col, vec3(1.), (.045 + .045 * (1. - s / .43)) * box * gloss * (1. - tilt));
          float box2 = smoothstep(.47, .50, s) * (1. - smoothstep(.56, .61, s));
          col = mix(col, vec3(.80, .93, 1.), .02 * box2 * gloss * (1. - tilt));
          // thickness: a faint line of light where the face meets the edge
          col += vec3(.75, .9, 1.) * exp(-pow((e - bw) / .07, 2.)) * .035 * gloss;
          gl_FragColor = vec4(col + dither(), 1.);
        }` });
  };
  for (const b of S.backings || []) {
    const m = new THREE.Mesh(new THREE.CircleGeometry(b.r, 6), new THREE.MeshBasicMaterial({ color: 0x020509 }));
    m.position.copy(P(b.x, b.y)); glass.add(m);
  }
  for (const s of S.shapes || []) {
    const geo = s.kind === 'rect' ? new THREE.PlaneGeometry(s.w, s.h) : new THREE.CircleGeometry(s.r, 6);
    const m = new THREE.Mesh(geo, glassMat(s));
    m.position.copy(P(s.x, s.y)); glass.add(m);
  }

  // ---------- 5. the page: the aurora at full resolution, the ground over which it lies, the glass ---------------
  const aurFull = target(buf.x, buf.y);
  draw(aur, aurFull);
  groundQuad.material.uniforms.aurTex.value = aurFull.texture;
  renderer.setRenderTarget(null); renderer.setClearColor(0x040a10, 1); renderer.clear();
  renderer.render(comp, cam);
  renderer.render(glass, cam);
}

// ================================================================ vector HUD =====================================
// The HUD draws every word and every line of a figure. Every line of text is set at its size, or smaller to fit its
// width (never below its floor, never below 6.5 pt); lines of one group are set at one size, the size of the
// tightest line of the group; nothing is condensed. A line that does not fit at its floor is reported and stops the
// build (tools/figures_web.py). No SVG gradient is used: Chrome's PDF writer rasterises SVG gradients at 72 ppi.
export function makeHud(svg, W, H) {
  const NS = 'http://www.w3.org/2000/svg';
  svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
  const problems = [], lines = [];
  const el = (tag, attrs, parent = svg) => { const e = document.createElementNS(NS, tag); for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v); parent.appendChild(e); return e; };
  const poly = (pts, close = true) => 'M' + pts.map(p => p.map(n => n.toFixed(3)).join(',')).join('L') + (close ? 'Z' : '');
  // an edge of glass: the accent hairline (the bevel and the rim are drawn by the light layer)
  const glassEdge = (pts, colour, width, opacity = .9, dash = null) =>
    el('path', { d: poly(pts), fill: 'none', stroke: colour, 'stroke-width': width, 'stroke-opacity': opacity,
                 'stroke-linejoin': 'round', ...(dash ? { 'stroke-dasharray': dash } : {}) });
  const rectPts = (x0, y0, x1, y1) => [[x0, y0], [x1, y0], [x1, y1], [x0, y1]];
  const sub = (t, s, pt) => {                     // "X_{E}" → X with a subscript, never below 6.5 pt, dropped .22 em
    const drop = (pt * PT * .22).toFixed(4);
    let back = false;
    for (const p of s.split(/(_\{[^}]*\})/)) { if (!p) continue;
      if (p.startsWith('_{')) { const ts = el('tspan', { dy: drop, 'font-size': (Math.max(6.5, pt * .72) * PT).toFixed(4) }, t); ts.textContent = p.slice(2, -1); back = true; }
      else { if (back) { const ts = el('tspan', { dy: '-' + drop }, t); ts.textContent = p; back = false; } else t.appendChild(document.createTextNode(p)); } }
  };
  const set = (L, pt) => { L.pt = pt; L.t.setAttribute('font-size', (pt * PT).toFixed(4));
    if (L.s.includes('_{')) { while (L.t.firstChild) L.t.removeChild(L.t.firstChild); sub(L.t, L.s, pt); } };
  const text = (x, y, s, size, cls, fill, anchor = 'middle', maxW = null, group = null, floor = 6.5, extra = {}) => {
    const t = el('text', { x: x.toFixed(3), y: y.toFixed(3), class: cls, fill, 'text-anchor': anchor, ...extra });
    if (!s.includes('_{')) t.textContent = s;
    const L = { t, s, size, maxW, group, floor: Math.max(6.5, floor) };
    set(L, size); lines.push(L); return L;
  };
  const drop = (L) => { lines.splice(lines.indexOf(L), 1); L.t.remove(); };
  const width = (L) => L.t.getComputedTextLength();
  const fitAll = () => {
    // 0.05 pt steps (as every figure of the book was set: their sizes are unchanged), then, for a line that is still
    // too wide after 2 pt (a large title), steps proportional to the excess
    const need = (L) => { if (!L.maxW) return L.size; let pt = L.size;
      for (let k = 0; k < 40 && L.t.getComputedTextLength() > L.maxW && pt > L.floor; k++) { pt = Math.max(L.floor, pt - .05); set(L, pt); }
      for (let k = 0; k < 60 && L.t.getComputedTextLength() > L.maxW && pt > L.floor; k++) {
        pt = Math.max(L.floor, Math.min(pt - .05, pt * L.maxW / L.t.getComputedTextLength())); set(L, pt); }
      return pt; };
    const groups = {};
    for (const L of lines) { const pt = need(L); if (L.group) (groups[L.group] ||= []).push(pt); }
    const gsize = Object.fromEntries(Object.entries(groups).map(([g, v]) => [g, Math.min(...v)]));
    for (const L of lines) {
      if (L.group) set(L, gsize[L.group]);
      const len = L.t.getComputedTextLength();
      if (L.maxW && len > L.maxW + .01) problems.push(`${L.s}: ${len.toFixed(2)} mm > ${L.maxW.toFixed(2)} mm at ${L.pt.toFixed(2)} pt`);
    }
    return gsize;
  };
  const inHex = (r, dy, margin) => 2 * (hexHalfWidth(r, dy) - margin);
  // the width of a string set in a class at a size (mm), and a greedy wrap by those widths: a line breaks between
  // words, and never at a joiner (" · " stays at the end of the line before it)
  const measure = (s, size, cls) => { const t = el('text', { x: 0, y: -50, class: cls, 'font-size': (size * PT).toFixed(4) });
    t.textContent = s; const w = t.getComputedTextLength(); t.remove(); return w; };
  const wrap = (s, size, cls, maxW) => {
    const words = s.split(' '), out = [];
    let cur = '';
    for (const w of words) {
      const next = cur ? `${cur} ${w}` : w;
      if (cur && measure(next, size, cls) > maxW && w !== '·') { out.push(cur); cur = w; } else cur = next;
    }
    if (cur) out.push(cur);
    return out;
  };
  const arrow = (x, y, ang, c, s = .9) => {      // a small filled arrowhead pointing along ang
    const p = [[s, 0], [-s * .7, s * .62], [-s * .7, -s * .62]].map(([u, v]) => [x + u * Math.cos(ang) - v * Math.sin(ang), y + u * Math.sin(ang) + v * Math.cos(ang)]);
    el('path', { d: poly(p), fill: c });
  };
  const line = (x1, y1, x2, y2, c, w = .3, dash = null, op = 1) => el('line', { x1, y1, x2, y2, stroke: c, 'stroke-width': w,
    'stroke-opacity': op, 'stroke-linecap': 'round', ...(dash ? { 'stroke-dasharray': dash } : {}) });
  const port = (x, y, c) => el('circle', { cx: x, cy: y, r: .8, fill: '#05111b', stroke: c, 'stroke-width': .28 });
  // an arrow along a quadratic curve from p to q, bowed by `bow` mm (positive: to the left of p → q)
  const curve = (p, q, bow, c, w = .34, dash = null, head = .7) => {
    const mx = (p[0] + q[0]) / 2, my = (p[1] + q[1]) / 2, dx = q[0] - p[0], dy = q[1] - p[1], L = Math.hypot(dx, dy) || 1;
    const cx = mx + dy / L * bow * 2, cy = my - dx / L * bow * 2;
    el('path', { d: `M${p[0].toFixed(3)} ${p[1].toFixed(3)} Q${cx.toFixed(3)} ${cy.toFixed(3)} ${q[0].toFixed(3)} ${q[1].toFixed(3)}`,
                 fill: 'none', stroke: c, 'stroke-width': w, 'stroke-linecap': 'round', ...(dash ? { 'stroke-dasharray': dash } : {}) });
    if (head) arrow(q[0], q[1], Math.atan2(q[1] - cy, q[0] - cx), c, head);
  };
  // the title strip of every figure: "FIGURE n", the title, a line on the right, a hairline beneath
  const titleStrip = (num, title, right, titleX = null) => {
    const a = text(7.5, 8.0, `FIGURE ${num}`, 7.0, 'lab', LIGHT.cyan, 'start');
    text(titleX ?? 7.5 + width(a) + 6.0, 8.0, title, 7.0, 'lab', INK, 'start');
    if (right) text(W - 7.5, 8.0, right, 6.5, 'cap', HEAD, 'end');
    el('path', { d: `M7.5 10.4 H${W - 7.5}`, stroke: 'rgb(164,222,229)', 'stroke-opacity': .32, 'stroke-width': .2, fill: 'none' });
  };
  const finish = () => {
    const sizes = fitAll();
    document.body.dataset.fit = JSON.stringify(problems);
    document.body.dataset.sizes = JSON.stringify(Object.fromEntries(Object.entries(sizes).map(([k, v]) => [k, +v.toFixed(2)])));
    document.body.dataset.minpt = String(Math.min(...lines.map(L => L.pt)));
  };
  return { W, H, el, poly, glassEdge, rectPts, text, drop, width, measure, wrap, fitAll, inHex, arrow, line, port, curve, titleStrip, finish };
}

// ================================================================ assembly =======================================
// fig = { light(D) → S, hud(h, D) }; the page carries a canvas#gl, an img#glimg (the light layer, for print) and an
// svg#hud. ?layer=gl draws the light layer alone (rendered to a 600 ppi lossless PNG); ?layer=print lays the HUD over
// that PNG (printed to the book's PDF); ?layer=live draws both, live.
export async function run(fig, dataUrl) {
  const LAYER = new URLSearchParams(location.search).get('layer') || 'live';
  const D = await (await fetch(dataUrl, { cache: 'no-store' })).json();
  const [W, H] = D.size_mm;
  const canvas = document.getElementById('gl'), img = document.getElementById('glimg'), svg = document.getElementById('hud');
  // every face is loaded before any text is measured (document.fonts.ready alone resolves before lazy faces load)
  await Promise.all(['400 10px "WM Sans"', '600 10px "WM Sans"', '700 10px "WM Sans"', '900 10px "WM Sans"', '400 10px Pagella',
    'italic 400 10px Pagella', '700 10px Pagella', '400 10px PagellaMath', '400 10px STIXMath'].map(f => document.fonts.load(f, 'AΦ𝔛ℤ⇏≅→₆')));
  await document.fonts.ready;
  const hud = () => { const h = makeHud(svg, W, H); fig.hud(h, D); h.finish(); };
  // print: the light layer is the static <img> (the page's load waits for it); gl and live draw it in WebGL instead
  if (LAYER === 'gl') { svg.style.display = 'none'; img.remove(); renderLight(canvas, window.devicePixelRatio || 1, { W, H, ...fig.light(D) }); }
  else if (LAYER === 'print') { canvas.style.display = 'none'; hud(); }
  else { img.remove(); renderLight(canvas, window.devicePixelRatio || 1, { W, H, ...fig.light(D) }); hud(); }
  document.title = 'ready';
  document.body.dataset.ready = '1';
}
