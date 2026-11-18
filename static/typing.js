// Typing test engine for YourTypingTests
const TT = (() => {
  const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
  const store = { get(k, d) { try { const v = localStorage.getItem("ytt_" + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } }, set(k, v) { try { localStorage.setItem("ytt_" + k, JSON.stringify(v)); } catch (e) {} } };
  const rnd = n => Math.floor(Math.random() * n), pick = a => a[rnd(a.length)];
  let C = {}, words = [], typed = [], wi = 0, started = false, done = false, t0 = 0, tick = null, keys = 0, goodKeys = 0, samples = [], errSec = [], lastKeys = 0, lastGood = 0, onDone = null, elapsedFixed = 0;
  const el = {};

  // ---------- text generation ----------
  function gen(n) {
    const out = [], m = C.mode;
    if (m === "sentences") { while (out.length < n) G_shuffle(WORDS.sentences.slice()).forEach(s => out.push(...s.split(" "))); return out.slice(0, Math.max(n, out.length)); }
    for (let i = 0; i < n; i++) {
      if (m === "numbers") { const len = 1 + rnd(5); let w = String(1 + rnd(9)); for (let k = 1; k < len; k++) w += rnd(10); out.push(w); continue; }
      const list = m === "kids" ? WORDS.kids : WORDS.common;
      let w; do { w = pick(list); } while (w === out[out.length - 1]);
      if (C.nums && Math.random() < .12) w = String(rnd(1000));
      if (C.punc) {
        if (i === 0 || /[.?!]$/.test(out[out.length - 1] || "")) w = w[0].toUpperCase() + w.slice(1);
        const r = Math.random();
        if (r < .08) w += "."; else if (r < .14) w += ","; else if (r < .16) w += "?"; else if (r < .17) w += "!"; else if (r < .19) w = '"' + w + '"'; else if (r < .2) w += ";";
      }
      out.push(w);
    }
    return out;
  }
  function G_shuffle(a) { for (let i = a.length - 1; i > 0; i--) { const j = rnd(i + 1); [a[i], a[j]] = [a[j], a[i]]; } return a; }

  // ---------- rendering ----------
  function wordHTML(w, i) { return `<div class="word" data-i="${i}">` + [...w].map(ch => `<span>${ch === "<" ? "&lt;" : ch}</span>`).join("") + "</div>"; }
  function renderAll() { el.words.innerHTML = words.map(wordHTML).join(""); el.words.style.transform = "translateY(0)"; paintWord(0); moveCaret(); }
  function paintWord(i) {
    const node = el.words.children[i]; if (!node) return;
    const w = words[i], t = typed[i] || "";
    node.querySelectorAll(".extra").forEach(x => x.remove());
    [...node.children].forEach((s, k) => { s.className = k < t.length ? (t[k] === w[k] ? "ok" : "bad") : ""; });
    if (t.length > w.length) t.slice(w.length).split("").forEach(ch => { const s = document.createElement("span"); s.className = "extra"; s.textContent = ch; node.appendChild(s); });
    node.classList.toggle("err", i < wi && t !== w);
  }
  function moveCaret() {
    const node = el.words.children[wi]; if (!node) return;
    const t = typed[wi] || "", letters = node.children;
    let x, y = node.offsetTop, h = node.offsetHeight;
    if (t.length < letters.length) x = node.offsetLeft + letters[t.length].offsetLeft;
    else { const last = letters[letters.length - 1]; x = node.offsetLeft + (last ? last.offsetLeft + last.offsetWidth : 0); }
    // scroll lines
    const lh = h * 1.0, gap = parseFloat(getComputedStyle(node).marginBottom) || 0, line = lh + gap;
    let shift = 0; if (y > line * 1.2) shift = y - line;
    el.words.style.transform = `translateY(${-shift}px)`;
    el.caret.style.transform = `translate(${x}px, ${y - shift}px)`;
    el.caret.style.height = h + "px";
    if (C.keyboard) highlightKey();
  }
  function highlightKey() {
    const w = words[wi] || "", t = typed[wi] || "", next = t.length < w.length ? w[t.length] : " ";
    $$(".kb .key").forEach(k => k.classList.remove("next"));
    const k = next === " " ? $(".kb .key[data-k=' ']") : $(`.kb .key[data-k="${CSS.escape(next.toLowerCase())}"]`) || $(`.kb .key[data-s="${CSS.escape(next)}"]`);
    if (k) k.classList.add("next");
    const sh = /[A-Z~!@#$%^&*()_+{}|:"<>?]/.test(next); $$(".kb .key[data-k='shift']").forEach(x => x.classList.toggle("next", sh));
  }

  // ---------- input ----------
  function onInput() {
    if (done) { el.input.value = ""; return; }
    let v = el.input.value;
    if (!started) { if (!v.trim()) { el.input.value = ""; return; } begin(); }
    const prev = typed[wi] || "";
    if (v.includes(" ")) {
      const cur = v.split(" ")[0];
      if (!cur && !prev) { el.input.value = ""; return; }
      typed[wi] = cur; countKeys(prev, cur);
      keys++; if (cur === words[wi]) goodKeys++; // the space
      paintWord(wi); wi++; el.input.value = "";
      if (wi >= words.length) { if (C.fixed) return finish(); words.push(...gen(60)); el.words.insertAdjacentHTML("beforeend", words.slice(wi).map((w, k) => wordHTML(w, wi + k)).join("")); }
      if (!C.fixed && words.length - wi < 40) { const add = gen(60), base = words.length; words.push(...add); el.words.insertAdjacentHTML("beforeend", add.map((w, k) => wordHTML(w, base + k)).join("")); }
      moveCaret(); live(); return;
    }
    if (v.length > (words[wi] || "").length + 12) v = el.input.value = v.slice(0, words[wi].length + 12);
    countKeys(prev, v); typed[wi] = v; paintWord(wi); moveCaret(); live();
    if (C.fixed && wi === words.length - 1 && v === words[wi]) { finish(); }
  }
  function countKeys(prev, cur) {
    if (cur.length > prev.length && cur.startsWith(prev)) {
      const w = words[wi] || "";
      for (let k = prev.length; k < cur.length; k++) { keys++; if (cur[k] === w[k]) goodKeys++; else errSec[Math.floor(elapsed())] = (errSec[Math.floor(elapsed())] || 0) + 1; }
    }
  }
  function onKey(e) {
    if (e.key === "Tab" || e.key === "Escape") { e.preventDefault(); restart(); return; }
    if (e.key === "Backspace" && el.input.value === "" && wi > 0 && !done) {
      if (typed[wi - 1] !== words[wi - 1] || e.ctrlKey || e.altKey) { e.preventDefault(); wi--; el.input.value = typed[wi]; typed[wi + 1] = ""; paintWord(wi + 1); paintWord(wi); moveCaret(); }
    }
  }

  // ---------- timing / stats ----------
  const elapsed = () => started ? (performance.now() - t0) / 1000 : 0;
  function begin() {
    started = true; t0 = performance.now(); el.wrap.classList.add("running");
    tick = setInterval(() => {
      const e = elapsed(), s = Math.floor(e);
      if (samples.length < s) { samples.push({ wpm: netWpm(e), raw: (keys - lastKeys) / 5 * 60, err: errSec[samples.length] || 0 }); lastKeys = keys; }
      if (!C.fixed) { const left = Math.max(0, C.dur - e); el.timer.textContent = Math.ceil(left); if (left <= 0) finish(); }
      else el.timer.textContent = Math.floor(e) + "s";
      live();
    }, 100);
  }
  function correctChars() {
    let c = 0;
    for (let i = 0; i < wi; i++) if (typed[i] === words[i]) c += words[i].length + 1;
    const cur = typed[wi] || "", w = words[wi] || ""; if (cur && w.startsWith(cur)) c += cur.length;
    return c;
  }
  function netWpm(e) { e = e || elapsed(); return e > 0 ? Math.max(0, correctChars() / 5 / (e / 60)) : 0; }
  function live() {
    if (!started) return;
    el.lwpm.textContent = Math.round(netWpm()) + " WPM";
    el.lacc.textContent = (keys ? Math.round(goodKeys / keys * 100) : 100) + "%";
  }
  function finish() {
    if (done) return; done = true; clearInterval(tick); el.wrap.classList.remove("running");
    const e = C.fixed ? elapsed() : C.dur;
    if (!samples.length || samples.length < Math.floor(e)) samples.push({ wpm: netWpm(e), raw: (keys - lastKeys) / 5 * 60 / Math.max(.2, e - samples.length), err: errSec[samples.length] || 0 });
    const wpm = Math.round(netWpm(e)), raw = Math.round(keys / 5 / (e / 60)), acc = keys ? Math.round(goodKeys / keys * 1000) / 10 : 0;
    const raws = samples.map(s => s.raw), mean = raws.reduce((a, b) => a + b, 0) / (raws.length || 1), sd = Math.sqrt(raws.reduce((a, b) => a + (b - mean) ** 2, 0) / (raws.length || 1));
    const consistency = mean ? Math.max(0, Math.round(100 - sd / mean * 100)) : 0;
    let cw = 0, ww = 0; for (let i = 0; i < wi; i++) typed[i] === words[i] ? cw++ : ww++;
    const R = { wpm, raw, acc, consistency, cw, ww, keys, goodKeys, dur: Math.round(e), mode: C.mode, date: Date.now() };
    if (onDone) { onDone(R); return; }
    showResults(R);
  }
  function showResults(R) {
    const key = `best_${R.mode}_${C.dur}`, best = store.get(key, 0), pb = R.wpm > best && R.acc >= 75;
    if (pb) store.set(key, R.wpm);
    const hist = store.get("history", []); hist.push({ w: R.wpm, a: R.acc, d: R.date, t: C.dur, m: R.mode }); store.set("history", hist.slice(-100));
    el.res.classList.remove("hidden"); el.wrap.classList.add("hidden"); $("#ttbar").classList.add("dim");
    const top = $("#ttbar").getBoundingClientRect().top + scrollY - 80; if (scrollY > top + 40 || scrollY < top - 200) scrollTo({ top, behavior: "smooth" });
    $("#r-wpm").textContent = R.wpm; $("#r-acc").textContent = R.acc + "%"; $("#r-raw").textContent = R.raw; $("#r-cons").textContent = R.consistency + "%";
    $("#r-words").innerHTML = `<b class="ok">${R.cw}</b> / <b class="bad">${R.ww}</b>`; $("#r-time").textContent = R.dur + "s";
    $("#r-pb").innerHTML = pb ? "🏆 New personal best!" : best ? `Your best: <b>${best} WPM</b>` : "";
    $("#r-level").innerHTML = level(R.wpm);
    chart($("#r-chart"), samples); progress();
    window.__lastResult = R;
  }
  function level(w) {
    const L = [[0, "🐢 Getting started", "Keep practicing. Try our typing lessons to build good habits."], [20, "🙂 Beginner", "You're on your way. Focus on accuracy first, and speed will follow."],
      [35, "👍 Average", "This is about where most people type. Daily practice will push you higher."], [50, "🚀 Above average", "You're faster than most people. Nice!"],
      [70, "⚡ Fast", "Great speed, the kind many typing-heavy jobs look for."], [90, "🔥 Very fast", "Excellent! You type faster than the vast majority of people."], [120, "👑 Elite", "Incredible speed. You're in expert territory."]];
    let r = L[0]; L.forEach(x => { if (w >= x[0]) r = x; });
    return `<b>${r[1]}</b> · ${r[2]}`;
  }
  function chart(cv, S) {
    const dpr = Math.min(2, devicePixelRatio || 1), W = cv.clientWidth || 600, H = cv.clientHeight || 200; cv.width = W * dpr; cv.height = H * dpr;
    const x = cv.getContext("2d"); x.scale(dpr, dpr); x.clearRect(0, 0, W, H);
    if (!S.length) return;
    const max = Math.max(20, ...S.map(s => Math.max(s.wpm, s.raw))) * 1.15, pl = 34, pb = 22, w = W - pl - 8, h = H - pb - 8;
    const css = getComputedStyle(document.body), mute = css.getPropertyValue("--mute"), acc = css.getPropertyValue("--acc"), line = css.getPropertyValue("--line");
    x.font = "11px system-ui"; x.fillStyle = mute; x.strokeStyle = line; x.lineWidth = 1;
    for (let g = 0; g <= 4; g++) { const yy = 8 + h - h * g / 4; x.beginPath(); x.moveTo(pl, yy); x.lineTo(pl + w, yy); x.stroke(); x.fillText(Math.round(max * g / 4), 4, yy + 4); }
    const px = i => pl + (S.length === 1 ? w / 2 : w * i / (S.length - 1)), py = v => 8 + h - h * Math.min(v, max) / max;
    x.fillText("seconds", pl + w - 44, H - 4);
    const path = (k, col, wd, dash) => { x.beginPath(); S.forEach((s, i) => i ? x.lineTo(px(i), py(s[k])) : x.moveTo(px(i), py(s[k]))); x.strokeStyle = col; x.lineWidth = wd; x.setLineDash(dash || []); x.stroke(); x.setLineDash([]); };
    path("raw", mute, 1.5, [4, 4]); path("wpm", acc, 3);
    S.forEach((s, i) => { if (s.err) { x.fillStyle = "#ff5c5c"; x.beginPath(); x.arc(px(i), py(s.raw), 3, 0, 7); x.fill(); } });
  }
  function progress() {
    const cv = $("#r-prog"); if (!cv) return;
    const H = store.get("history", []).slice(-20); $("#r-progwrap").classList.toggle("hidden", H.length < 2);
    if (H.length < 2) return;
    chart(cv, H.map(h => ({ wpm: h.w, raw: h.w, err: 0 })));
    const avg = Math.round(H.reduce((a, b) => a + b.w, 0) / H.length); $("#r-avg").textContent = `Average of your last ${H.length} tests: ${avg} WPM`;
  }

  // ---------- control ----------
  function restart(newText = true) {
    clearInterval(tick); started = done = false; wi = 0; typed = []; keys = goodKeys = 0; samples = []; errSec = []; lastKeys = lastGood = 0;
    if (newText) words = C.fixed ? C.words.slice() : gen(C.mode === "sentences" ? 120 : 120);
    el.timer.textContent = C.fixed ? "0s" : C.dur; el.lwpm.textContent = "0 WPM"; el.lacc.textContent = "100%";
    el.res && el.res.classList.add("hidden"); el.wrap.classList.remove("hidden", "running"); $("#ttbar") && $("#ttbar").classList.remove("dim");
    el.input.value = ""; renderAll(); focus();
  }
  function focus() { el.input.focus({ preventScroll: true }); el.wrap.classList.remove("blurred"); }
  function init(cfg) {
    C = Object.assign({ dur: 60, mode: "words", punc: false, nums: false }, cfg || {});
    Object.assign(el, { wrap: $("#wwrap"), words: $("#words"), caret: $("#caret"), input: $("#hidden"), timer: $("#timer"), lwpm: $("#lwpm"), lacc: $("#lacc"), res: $("#results") });
    onDone = C.onDone || null;
    el.input.addEventListener("input", onInput); el.input.addEventListener("keydown", onKey);
    el.input.addEventListener("blur", () => setTimeout(() => { if (document.activeElement !== el.input && !done) el.wrap.classList.add("blurred"); }, 120));
    el.wrap.addEventListener("click", focus);
    document.addEventListener("keydown", e => {
      if (e.target === el.input || e.target.closest("input,textarea,select,button")) return;
      if (e.key === "Tab" || e.key === "Escape") { e.preventDefault(); restart(); return; }
      if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !el.wrap.classList.contains("hidden")) focus();
    });
    addEventListener("resize", () => moveCaret());
    restart();
  }
  function set(k, v) { C[k] = v; restart(); }
  return { init, restart, set, load(cfg) { Object.assign(C, cfg); onDone = cfg.onDone || onDone; restart(); }, store, chart, get cfg() { return C; } };
})();
