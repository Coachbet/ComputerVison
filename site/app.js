/* Graphiques et démos du cours. Toutes les données viennent de data.js (window.COURSE). */
(function () {
  const D = window.COURSE;
  const C = D.classes;
  const NS = "http://www.w3.org/2000/svg";
  const fr = (n, d = 0) => Number(n).toLocaleString("fr-FR", { minimumFractionDigits: d, maximumFractionDigits: d });
  const css = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  const pc = (c) => css("--" + c);
  const NAMES = { whatsapp: "WhatsApp" };
  const cap = (s) => NAMES[s] || s.charAt(0).toUpperCase() + s.slice(1);
  const esc = (s) => String(s).replace(/[&<>"]/g, (m) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[m]));
  const $ = (id) => document.getElementById(id);

  /* ------------------------------ hero ------------------------------ */
  function hero() {
    const box = $("lineup");
    box.innerHTML = "";
    C.forEach((c) => {
      const b = document.createElement("button");
      b.style.setProperty("--c", pc(c));
      b.setAttribute("aria-pressed", "false");
      b.innerHTML = `<img src="img/${c}.png" alt="Emoji ${cap(c)}"><span class="dot"></span>${cap(c)}`;
      b.addEventListener("click", () => {
        box.querySelectorAll("button").forEach((x) => x.setAttribute("aria-pressed", "false"));
        b.setAttribute("aria-pressed", "true");
        const e = D.examples[c];
        $("peek").innerHTML =
          `<b>${cap(c)}</b>, image n° ${e.id} : <b>${e.w} × ${e.w} px</b>, mode <b>${e.mode}</b>, fichier de <b>${fr(e.kb, 1)} Ko</b>. ` +
          `Ces trois informations forment déjà trois des 222 mesures du modèle, avant même de regarder la moindre couleur.`;
      });
      box.appendChild(b);
    });
  }

  /* --------------------------- helpers SVG --------------------------- */
  function svg(w, h, inner, label) {
    return `<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(label)}">${inner}</svg>`;
  }
  const T = (x, y, s, o = {}) =>
    `<text x="${x}" y="${y}" font-size="${o.size || 13}" ${o.anchor ? `text-anchor="${o.anchor}"` : ""} ${o.weight ? `font-weight="${o.weight}"` : ""} ${o.muted ? 'class="muted"' : ""} ${o.fill ? `style="fill:${o.fill}"` : ""}>${s}</text>`;

  /* ------------------------ classes (barres) ------------------------ */
  function chartClasses() {
    const W = 860, rowH = 34, L = 100, R = 70, H = C.length * rowH + 10;
    const max = Math.max(...C.map((c) => D.perClass[c].n));
    let s = "";
    C.forEach((c, i) => {
      const n = D.perClass[c].n, w = ((W - L - R) * n) / max, y = 5 + i * rowH;
      s += T(L - 10, y + 20, cap(c), { anchor: "end", size: 14 });
      s += `<rect x="${L}" y="${y + 4}" width="${w}" height="${rowH - 10}" rx="5" fill="${pc(c)}"/>`;
      s += T(L + w + 8, y + 20, fr(n), { size: 13, weight: 700 });
    });
    $("chart-classes").innerHTML = svg(W, H, s, "Nombre d'images par fournisseur");
  }

  /* ------------------------ largeur (empilé 100 %) ------------------------ */
  function chartSize() {
    const cats = [["72", "72 px", "#3b82b6"], ["160", "160 px", "#e0a526"], ["240", "240 px", "#7a4fa3"], ["autre", "autre", "#aab6bf"]];
    const W = 860, rowH = 36, L = 100, R = 20, H = C.length * rowH + 50;
    let s = "";
    C.forEach((c, i) => {
      const p = D.perClass[c], y = 8 + i * rowH;
      const parts = { "72": 0, "160": 0, "240": 0, autre: 0 };
      Object.entries(p.sizes).forEach(([k, v]) => { parts[k in parts ? k : "autre"] += v; });
      s += T(L - 10, y + 21, cap(c), { anchor: "end", size: 14 });
      let x = L;
      cats.forEach(([k, , col]) => {
        const w = ((W - L - R) * parts[k]) / p.n;
        if (w > 0) {
          s += `<rect x="${x}" y="${y + 3}" width="${w}" height="${rowH - 8}" fill="${col}"><title>${cap(c)} : ${parts[k]} images à ${k === "autre" ? "d'autres largeurs" : k + " px"}</title></rect>`;
          if (w > 44) s += T(x + w / 2, y + 22, fr((100 * parts[k]) / p.n) + " %", { anchor: "middle", size: 12, fill: "#fff", weight: 700 });
        }
        x += w;
      });
    });
    let lx = L;
    cats.forEach(([, lab, col]) => {
      s += `<rect x="${lx}" y="${H - 28}" width="14" height="14" rx="3" fill="${col}"/>` + T(lx + 20, H - 16, lab, { size: 13 });
      lx += 110;
    });
    $("chart-size").innerHTML = svg(W, H, s, "Répartition des largeurs d'image par fournisseur");
  }

  /* ------------------------ poids du fichier ------------------------ */
  function chartKb() {
    const W = 860, rowH = 34, L = 100, R = 80, H = C.length * rowH + 10;
    const max = Math.max(...C.map((c) => D.perClass[c].medianFileKB));
    let s = "";
    C.forEach((c, i) => {
      const v = D.perClass[c].medianFileKB, w = ((W - L - R) * v) / max, y = 5 + i * rowH;
      s += T(L - 10, y + 20, cap(c), { anchor: "end", size: 14 });
      s += `<rect x="${L}" y="${y + 4}" width="${w}" height="${rowH - 10}" rx="5" fill="${pc(c)}"/>`;
      s += T(L + w + 8, y + 20, fr(v, 1) + " Ko", { size: 13, weight: 700 });
    });
    $("chart-kb").innerHTML = svg(W, H, s, "Poids médian du fichier par fournisseur, en kilo-octets");
  }

  /* ------------------------ histogrammes ------------------------ */
  const CH = [["R", 0, "rouge (R)"], ["G", 1, "vert (G)"], ["B", 2, "bleu (B)"], ["H", 3, "teinte (H)"], ["S", 4, "saturation (S)"], ["V", 5, "valeur (V)"]];
  let histChannel = 3, histFocus = null;
  function chartHist() {
    const seg = $("hist-seg");
    if (!seg.children.length) {
      CH.forEach(([k, i, lab]) => {
        const b = document.createElement("button");
        b.className = "ctl"; b.textContent = lab; b.setAttribute("aria-pressed", String(i === histChannel));
        b.addEventListener("click", () => { histChannel = i; seg.querySelectorAll("button").forEach((x) => x.setAttribute("aria-pressed", "false")); b.setAttribute("aria-pressed", "true"); drawHist(); });
        seg.appendChild(b);
      });
      const lg = $("hist-legend");
      C.forEach((c) => {
        const sp = document.createElement("span");
        sp.style.setProperty("--c", pc(c)); sp.innerHTML = `<i></i>${cap(c)}`; sp.style.cursor = "default";
        sp.addEventListener("mouseenter", () => { histFocus = c; drawHist(); });
        sp.addEventListener("mouseleave", () => { histFocus = null; drawHist(); });
        lg.appendChild(sp);
      });
    }
    drawHist();
  }
  function drawHist() {
    const W = 860, H = 300, L = 54, R = 16, Tp = 14, B = 44;
    const series = C.map((c) => D.hist[c][histChannel]);
    const spike = [31, 31, 31, 0, 0, 31][histChannel];
    const max = Math.max(...series.flatMap((r) => r.filter((_, b) => b !== spike))) * 1.12;
    const x = (b) => L + ((W - L - R) * b) / 31, y = (v) => Tp + (H - Tp - B) * (1 - v / max);
    let s = "";
    const step = max > 0.2 ? 0.1 : max > 0.1 ? 0.05 : max > 0.05 ? 0.02 : 0.01;
    for (let v = 0; v <= max; v += step) {
      s += `<line x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}" stroke="${css("--line")}"/>` + T(L - 8, y(v) + 4, fr(Math.round(v * 100)) + " %", { anchor: "end", size: 11, muted: true });
    }
    [0, 64, 128, 192, 255].forEach((v) => { s += T(L + ((W - L - R) * v) / 255, H - B + 18, v, { anchor: "middle", size: 11, muted: true }); });
    s += T((L + W - R) / 2, H - 6, "valeur du canal (0 à 255), regroupée en 32 intervalles", { anchor: "middle", size: 12, muted: true });
    C.forEach((c, i) => {
      const pts = series[i].map((v, b) => `${x(b)},${y(Math.min(v, max))}`).join(" ");
      const dim = histFocus && histFocus !== c;
      s += `<polyline points="${pts}" fill="none" stroke="${pc(c)}" stroke-width="${histFocus === c ? 3.5 : 2.2}" stroke-linejoin="round" opacity="${dim ? 0.15 : 0.95}"><title>${cap(c)}</title></polyline>`;
    });
    const px = x(spike), peak = Math.max(...series.map((r) => r[spike]));
    if (peak > max) {
      const left = spike === 0;
      s += T(left ? px + 70 : px - 70, Tp + 12, (left ? "◀ " : "") + "fond blanc : jusqu'à " + fr(peak * 100) + " %, hors échelle" + (left ? "" : " ▶"), { anchor: left ? "start" : "end", size: 12, muted: true });
    }
    $("chart-hist").innerHTML = svg(W, H, s, "Histogramme moyen par fournisseur pour le canal " + CH[histChannel][2]);
  }

  /* ------------------------ arbre appris ------------------------ */
  function chartTree() {
    $("tree-acc").textContent = fr(D.treeAcc * 100) + " %";
    const leafW = 118, gapX = 14, levelH = 118, top = 16;
    let leafIdx = 0, maxDepth = 0;
    function layout(n, d) {
      maxDepth = Math.max(maxDepth, d);
      if (!n.q) { n._x = leafIdx++ * (leafW + gapX) + leafW / 2; n._d = d; return; }
      layout(n.yes, d + 1); layout(n.no, d + 1);
      n._x = (n.yes._x + n.no._x) / 2; n._d = d;
    }
    layout(D.tree, 0);
    const W = leafIdx * (leafW + gapX), H = top + (maxDepth + 1) * levelH + 70;
    let s = "";
    const ink = css("--ink"), line = css("--line"), muted = css("--muted");
    function edges(n) {
      if (!n.q) return;
      [[n.yes, "oui"], [n.no, "non"]].forEach(([k, lab]) => {
        const x1 = n._x, y1 = top + n._d * levelH + 40, x2 = k._x, y2 = top + k._d * levelH;
        s += `<path d="M${x1} ${y1} C${x1} ${(y1 + y2) / 2} ${x2} ${(y1 + y2) / 2} ${x2} ${y2}" fill="none" stroke="${muted}" stroke-width="1.6"/>`;
        s += T((x1 + x2) / 2 + (lab === "oui" ? -8 : 8), (y1 + y2) / 2 + 2, lab, { anchor: lab === "oui" ? "end" : "start", size: 12, muted: true });
        edges(k);
      });
    }
    edges(D.tree);
    (function nodes(n) {
      const y = top + n._d * levelH;
      if (n.q) {
        const w = 170;
        s += `<rect x="${n._x - w / 2}" y="${y}" width="${w}" height="40" rx="9" fill="${css("--panel")}" stroke="${css("--leaf")}" stroke-width="2"/>`;
        s += T(n._x, y + 17, esc(n.q.replace(/(\d)\.(\d)/g, "$1,$2")) + " ?", { anchor: "middle", size: 12.5, weight: 700 });
        s += T(n._x, y + 33, fr(n.n) + " images", { anchor: "middle", size: 11, muted: true });
        nodes(n.yes); nodes(n.no);
      } else {
        const tot = n.n, bw = leafW - 8; let bx = n._x - bw / 2;
        const maj = n.counts[n.label];
        s += `<rect x="${n._x - leafW / 2}" y="${y}" width="${leafW}" height="78" rx="9" fill="${css("--panel")}" stroke="${line}" stroke-width="1.5"/>`;
        s += T(n._x, y + 20, cap(n.label), { anchor: "middle", size: 14, weight: 800, fill: pc(n.label) });
        s += T(n._x, y + 36, fr(maj) + " sur " + fr(tot), { anchor: "middle", size: 11.5 });
        s += T(n._x, y + 50, "pur à " + fr((100 * maj) / tot) + " %", { anchor: "middle", size: 11, muted: true });
        Object.entries(n.counts).forEach(([k, v]) => {
          const w = (bw * v) / tot;
          s += `<rect x="${bx}" y="${y + 60}" width="${w}" height="9" fill="${pc(k)}"><title>${cap(k)} : ${v}</title></rect>`;
          bx += w;
        });
      }
    })(D.tree);
    // légende
    let lx = 0; const ly = H - 26;
    C.forEach((c) => { s += `<rect x="${lx}" y="${ly}" width="12" height="12" rx="3" fill="${pc(c)}"/>` + T(lx + 17, ly + 11, cap(c), { size: 12 }); lx += 105; });
    $("chart-tree").innerHTML = svg(Math.max(W, 760), H, s, "Arbre de décision appris sur la largeur, le mode et le poids du fichier");
  }

  /* ------------------------ démo boosting 1D ------------------------ */
  let seed = 7, pts = [], showRes = false;
  const rng = () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
  const gauss = () => Math.sqrt(-2 * Math.log(rng() + 1e-9)) * Math.cos(2 * Math.PI * rng());
  function newPoints() {
    pts = [];
    for (let i = 0; i < 44; i++) { const x = (i + 0.5) / 44; pts.push({ x, y: Math.sin(2 * Math.PI * x) + 0.28 * gauss() }); }
  }
  // Le modèle est réentraîné à la volée avec le learning rate choisi, pour que la démo soit fidèle.
  function fitWith(lr, rounds) {
    const out = [{ base: pts.reduce((a, p) => a + p.y, 0) / pts.length }];
    const pred = pts.map(() => out[0].base);
    for (let r = 0; r < rounds; r++) {
      const res = pts.map((p, i) => p.y - pred[i]);
      let best = null;
      for (let k = 1; k < pts.length; k++) {
        const t = (pts[k - 1].x + pts[k].x) / 2;
        let sl = 0, nl = 0, sr = 0, nr = 0;
        res.forEach((v, i) => { if (pts[i].x <= t) { sl += v; nl++; } else { sr += v; nr++; } });
        const ml = sl / nl, mr = sr / nr;
        let sse = 0;
        res.forEach((v, i) => { const m = pts[i].x <= t ? ml : mr; sse += (v - m) * (v - m); });
        if (!best || sse < best.sse) best = { t, ml, mr, sse };
      }
      out.push(best);
      pts.forEach((p, i) => { pred[i] += lr * (p.x <= best.t ? best.ml : best.mr); });
    }
    return { model: out, pred };
  }
  function drawBoost() {
    const rounds = +$("b-rounds").value, lr = +$("b-lr").value;
    $("b-rounds-o").textContent = rounds; $("b-lr-o").textContent = fr(lr, 2);
    const { model, pred } = fitWith(lr, rounds);
    const W = 860, H = 340, L = 40, R = 16, Tp = 14, B = 30, ymin = -1.9, ymax = 1.9;
    const x = (v) => L + (W - L - R) * v, y = (v) => Tp + (H - Tp - B) * (1 - (v - ymin) / (ymax - ymin));
    let s = `<line x1="${L}" x2="${W - R}" y1="${y(0)}" y2="${y(0)}" stroke="${css("--line")}"/>`;
    let path = "", last = null;
    for (let i = 0; i <= 400; i++) {
      const xv = i / 400; let v = model[0].base;
      for (let r = 1; r < model.length; r++) v += lr * (xv <= model[r].t ? model[r].ml : model[r].mr);
      path += `${i ? "L" : "M"}${x(xv)} ${y(v)} `; last = v;
    }
    if (showRes) pts.forEach((p, i) => { s += `<line x1="${x(p.x)}" x2="${x(p.x)}" y1="${y(p.y)}" y2="${y(pred[i])}" stroke="#c0392b" stroke-width="2" opacity="0.8"/>`; });
    s += `<path d="${path}" fill="none" stroke="#d98e04" stroke-width="3.2"/>`;
    pts.forEach((p) => { s += `<circle cx="${x(p.x)}" cy="${y(p.y)}" r="4.5" fill="#7f8c97" stroke="${css("--panel")}" stroke-width="1.5"/>`; });
    const rmse = Math.sqrt(pts.reduce((a, p, i) => a + (p.y - pred[i]) ** 2, 0) / pts.length);
    s += T(W - R, 24, `erreur moyenne (RMSE) : ${fr(rmse, 2)}`, { anchor: "end", size: 14, weight: 700 });
    s += T(W - R, 44, rounds === 0 ? "avant tout arbre : la moyenne des points" : `${rounds} ${rounds > 1 ? "arbres ajoutés" : "arbre ajouté"}`, { anchor: "end", size: 12, muted: true });
    $("chart-boost").innerHTML = svg(W, H, s, "Démonstration de boosting sur des points bruités");
  }
  /* ------------------------ softmax ------------------------ */
  function chartSoft() {
    const final = [0.2, -0.3, 0.1, -0.8, -1.0, 2.2, -0.4], N = 12;
    const r = +$("s-round").value; $("s-round-o").textContent = r;
    const scores = final.map((f, k) => f * (r / N) + 0.35 * Math.sin((Math.PI * r) / N) * Math.sin(k * 2.1 + 1));
    const ex = scores.map(Math.exp), sum = ex.reduce((a, b) => a + b, 0), prob = ex.map((e) => e / sum);
    const W = 860, rowH = 34, L = 100, H = C.length * rowH + 40;
    let s = T(L, 16, "score", { size: 12, muted: true }) + T(L + 170, 16, "probabilité", { size: 12, muted: true });
    const win = Math.max(...prob) - Math.min(...prob) < 1e-6 ? -1 : prob.indexOf(Math.max(...prob));
    C.forEach((c, i) => {
      const y = 28 + i * rowH, w = (W - L - 190) * prob[i];
      s += T(L - 10, y + 20, cap(c), { anchor: "end", size: 14, weight: i === win ? 800 : 400 });
      s += `<rect x="${L + 170}" y="${y + 4}" width="${Math.max(w, 1)}" height="${rowH - 10}" rx="5" fill="${i === win ? css("--leaf") : "#aab6bf"}"/>`;
      s += T(L, y + 20, (scores[i] >= 0 ? "+" : "−") + fr(Math.abs(scores[i]), 2), { size: 13 });
      s += T(L + 170 + w + 8, y + 20, fr(prob[i] * 100, 1) + " %", { size: 13, weight: 700 });
    });
    $("chart-soft").innerHTML = svg(W, H, s, "Scores et probabilités des 7 fournisseurs après " + r + " tours (illustration)");
  }

  /* ------------------------ poids de classes ------------------------ */
  function chartWeights() {
    const total = C.reduce((a, c) => a + D.perClass[c].n, 0);
    const W = 860, rowH = 34, L = 100, R = 220, H = C.length * rowH + 10;
    const w = C.map((c) => total / (C.length * D.perClass[c].n)), max = Math.max(...w);
    let s = "";
    C.forEach((c, i) => {
      const y = 5 + i * rowH, bw = ((W - L - R) * w[i]) / max;
      s += T(L - 10, y + 20, cap(c), { anchor: "end", size: 14 });
      s += `<rect x="${L}" y="${y + 4}" width="${bw}" height="${rowH - 10}" rx="5" fill="${pc(c)}"/>`;
      s += T(L + bw + 8, y + 20, fr(w[i], 2) + "  (" + fr(D.perClass[c].n) + " images)", { size: 13, weight: 700 });
    });
    $("chart-weights").innerHTML = svg(W, H, s, "Poids de classe balanced");
  }

  /* ------------------------ P / R / F1 ------------------------ */
  function chartF1() {
    const W = 860, rowH = 40, L = 100, R = 60, Tp = 34, H = C.length * rowH + Tp + 36, lo = 0.86, hi = 1.0;
    const x = (v) => L + (W - L - R) * ((v - lo) / (hi - lo));
    let s = "";
    [0.88, 0.92, 0.96, 1.0].forEach((v) => { s += `<line x1="${x(v)}" x2="${x(v)}" y1="${Tp - 8}" y2="${H - 36}" stroke="${css("--line")}"/>` + T(x(v), H - 18, fr(v, 2), { anchor: "middle", size: 11, muted: true }); });
    const col = { p: "#3b82b6", r: "#d98e04", f: css("--leaf") };
    C.forEach((c, i) => {
      const [p, r, f] = D.report[c], y = Tp + i * rowH + 14;
      s += T(L - 10, y + 5, cap(c), { anchor: "end", size: 14 });
      s += `<line x1="${x(Math.min(p, r))}" x2="${x(Math.max(p, r))}" y1="${y}" y2="${y}" stroke="${css("--muted")}" stroke-width="2" opacity="0.5"/>`;
      s += `<circle cx="${x(p)}" cy="${y}" r="6" fill="${col.p}"><title>Précision ${fr(p, 3)}</title></circle>`;
      s += `<rect x="${x(r) - 6}" y="${y - 6}" width="12" height="12" fill="${col.r}"><title>Rappel ${fr(r, 3)}</title></rect>`;
      s += `<path d="M${x(f)} ${y - 8} L${x(f) + 8} ${y} L${x(f)} ${y + 8} L${x(f) - 8} ${y} Z" fill="${col.f}"><title>F1 ${fr(f, 3)}</title></path>`;
      s += T(W - R + 8, y + 5, "F1 " + fr(f, 3), { size: 12, weight: 700 });
    });
    s += `<circle cx="${L}" cy="12" r="6" fill="${col.p}"/>` + T(L + 12, 16, "précision", { size: 12 });
    s += `<rect x="${L + 100}" y="6" width="12" height="12" fill="${col.r}"/>` + T(L + 118, 16, "rappel", { size: 12 });
    s += `<path d="M${L + 190} 4 l8 8 l-8 8 l-8 -8 z" fill="${col.f}"/>` + T(L + 204, 16, "F1", { size: 12 });
    $("chart-f1").innerHTML = svg(W, H, s, "Précision, rappel et F1 par fournisseur");
  }

  /* ------------------------ matrice de confusion ------------------------ */
  function chartCm() {
    const M = D.confusion;
    let h = '<table class="hm" aria-label="Matrice de confusion"><thead><tr><th></th>';
    C.forEach((c) => (h += `<th>prédit<br>${cap(c)}</th>`));
    h += "<th>total</th></tr></thead><tbody>";
    M.forEach((row, i) => {
      const tot = row.reduce((a, b) => a + b, 0);
      h += `<tr><th class="row">vrai ${cap(C[i])}</th>`;
      row.forEach((v, j) => {
        const rate = v / tot;
        const bg = i === j ? `rgba(29,122,85,${0.12 + 0.78 * rate})` : v ? `rgba(217,142,4,${Math.min(0.95, 0.25 + rate * 8)})` : "transparent";
        const fg = i === j && rate > 0.55 ? "#fff" : "inherit";
        const tip = i === j ? `${v} ${cap(C[i])} bien reconnus sur ${tot}` : `${v} ${cap(C[i])} pris pour des ${cap(C[j])}`;
        h += `<td style="background:${bg};color:${fg}" title="${tip}">${v || '<span style="opacity:.35">·</span>'}</td>`;
      });
      h += `<td style="font-weight:700">${tot}</td></tr>`;
    });
    h += "</tbody></table>";
    $("chart-cm").innerHTML = h;
  }

  /* ------------------------ autres essais ------------------------ */
  function chartOthers() {
    const rows = [
      ["Gradient boosting sur 222 mesures (notre modèle)", 0.960, "g"],
      ["Boosting + MobileNetV3 (ensemble, retiré)", 0.9626, "x"],
      ["Extra Trees sur les mêmes mesures", 0.936, "o"],
      ["Régression logistique sur histogrammes", 0.780, "o"],
      ["HOG + couleurs + régression logistique", 0.757, "o"],
      ["MobileNetV3 pré-entraîné", 0.658, "o"],
      ["CNN type LeNet", 0.426, "o"],
    ];
    const W = 860, rowH = 38, L = 390, R = 60, H = rows.length * rowH + 10;
    let s = "";
    rows.forEach(([lab, v, k], i) => {
      const y = 5 + i * rowH, w = ((W - L - R) * v) / 1;
      s += T(L - 10, y + 22, lab, { anchor: "end", size: 13, weight: k === "g" ? 800 : 400 });
      s += `<rect x="${L}" y="${y + 5}" width="${w}" height="${rowH - 12}" rx="5" fill="${k === "g" ? css("--leaf") : k === "x" ? css("--leaf-soft") : "#aab6bf"}" ${k === "x" ? `stroke="${css("--leaf")}" stroke-dasharray="4 3"` : ""}/>`;
      s += T(L + w + 8, y + 22, fr(v, 3), { size: 13, weight: 700 });
    });
    $("chart-others").innerHTML = svg(W, H, s, "Accuracy de validation des différentes approches");
  }

  /* ------------------------ sommaire actif ------------------------ */
  function toc() {
    const links = [...document.querySelectorAll("nav.toc a")];
    const map = new Map(links.map((a) => [a.getAttribute("href").slice(1), a]));
    const io = new IntersectionObserver((es) => {
      es.forEach((e) => { if (e.isIntersecting) { links.forEach((l) => l.classList.remove("on")); const a = map.get(e.target.id); if (a) a.classList.add("on"); } });
    }, { rootMargin: "-20% 0px -70% 0px" });
    map.forEach((_, id) => { const el = document.getElementById(id); if (el) io.observe(el); });
  }

  function renderAll() {
    hero(); chartClasses(); chartSize(); chartKb(); chartHist(); chartTree(); drawBoost(); chartSoft(); chartWeights(); chartF1(); chartCm(); chartOthers();
  }
  document.addEventListener("DOMContentLoaded", () => {
    newPoints();
    renderAll();
    $("b-rounds").addEventListener("input", drawBoost);
    $("b-lr").addEventListener("input", drawBoost);
    $("b-new").addEventListener("click", () => { seed = Math.floor(Math.random() * 1e6) + 1; newPoints(); drawBoost(); });
    $("b-res").addEventListener("click", (e) => { showRes = !showRes; e.currentTarget.setAttribute("aria-pressed", String(showRes)); drawBoost(); });
    $("s-round").addEventListener("input", chartSoft);
    toc();
    if (window.matchMedia) window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", renderAll);
  });
})();
