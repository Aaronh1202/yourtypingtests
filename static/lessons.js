(() => {
  const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
  const HOME = "asdfjkl;";
  const LESSONS = [
    { t: "Home row", d: "A S D F and J K L ;", keys: "asdfjkl;" },
    { t: "Home row + G and H", d: "Stretch your index fingers", keys: "asdfghjkl;" },
    { t: "E and I", d: "Your first top-row keys", keys: "asdfghjkl;ei" },
    { t: "R, T, U and Y", d: "Index fingers reach up", keys: "asdfghjkl;eirtuy" },
    { t: "W, O, Q and P", d: "The whole top row", keys: "asdfghjkl;eirtuywoqp" },
    { t: "C, V, N and M", d: "Bottom row, index and middle", keys: "asdfghjkl;eirtuywoqpcvnm" },
    { t: "X, Z, B, comma, period", d: "Every letter on the keyboard", keys: "abcdefghijklmnopqrstuvwxyz,." },
    { t: "Capital letters", d: "Use the opposite Shift key", special: "caps" },
    { t: "Numbers", d: "The number row", special: "numbers" },
    { t: "Punctuation", d: "Quotes, questions and more", special: "punct" },
    { t: "Common words", d: "The words you type most", special: "common" },
    { t: "Full sentences", d: "Put it all together", special: "sentences" }
  ];
  const ALLW = [...new Set(WORDS.common.concat(WORDS.kids))];
  const rnd = n => Math.floor(Math.random() * n), pick = a => a[rnd(a.length)];
  function lessonWords(L) {
    const out = [];
    if (L.special === "caps") { for (let i = 0; i < 22; i++) { const w = pick(WORDS.common); out.push(Math.random() < .6 ? w[0].toUpperCase() + w.slice(1) : w.toUpperCase().slice(0, 4)); } return out; }
    if (L.special === "numbers") { for (let i = 0; i < 24; i++) { let w = ""; const n = 1 + rnd(4); for (let k = 0; k < n; k++) w += rnd(10); out.push(w); } return out; }
    if (L.special === "punct") { const p = ["?", "!", ",", ".", ";", ":", "'s", "-"]; for (let i = 0; i < 20; i++) { let w = pick(WORDS.common); const s = pick(p); w = s === "-" ? w + "-" + pick(WORDS.common) : w + s; if (Math.random() < .2) w = '"' + w + '"'; out.push(w); } return out; }
    if (L.special === "common") { for (let i = 0; i < 30; i++) out.push(WORDS.common[rnd(120)]); return out; }
    if (L.special === "sentences") { const s = WORDS.sentences.slice().sort(() => Math.random() - .5).slice(0, 3); s.forEach(x => out.push(...x.split(" "))); return out; }
    const keys = L.keys, real = ALLW.filter(w => [...w].every(c => keys.includes(c)));
    const fresh = keys.split("").filter(c => !LESSONS[0].keys.includes(c) || L === LESSONS[0]);
    for (let i = 0; i < 24; i++) {
      if (real.length >= 6 && Math.random() < .55) { out.push(pick(real)); continue; }
      const len = 2 + rnd(4); let w = "";
      for (let k = 0; k < len; k++) w += Math.random() < .5 && fresh.length ? pick(fresh) : keys[rnd(keys.length)];
      out.push(w.replace(/;(?=.)/g, "a"));
    }
    return out;
  }
  // keyboard
  const ROWS = [["`~", "1!", "2@", "3#", "4$", "5%", "6^", "7&", "8*", "9(", "0)", "-_", "=+", "⌫"], ["Tab", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[{", "]}", "\\|"], ["Caps", "a", "s", "d", "f", "g", "h", "j", "k", "l", ";:", "'\"", "Enter"], ["shift", "z", "x", "c", "v", "b", "n", "m", ",<", ".>", "/?", "shift"], [" "]];
  const FINGER = { "`": 1, 1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 6: 5, 7: 5, 8: 6, 9: 7, 0: 8, "-": 8, "=": 8, q: 1, w: 2, e: 3, r: 4, t: 4, y: 5, u: 5, i: 6, o: 7, p: 8, "[": 8, "]": 8, "\\": 8, a: 1, s: 2, d: 3, f: 4, g: 4, h: 5, j: 5, k: 6, l: 7, ";": 8, "'": 8, z: 1, x: 2, c: 3, v: 4, b: 4, n: 5, m: 5, ",": 6, ".": 7, "/": 8, " ": 9 };
  $("#kb").innerHTML = ROWS.map(r => '<div class="krow">' + r.map(k => {
    const base = k.length === 2 ? k[0] : k, sh = k.length === 2 ? k[1] : "";
    const wide = ["Tab", "Caps", "Enter", "shift", "⌫", " "].includes(k) ? " wide w-" + (k === " " ? "space" : k.toLowerCase().replace("⌫", "bs")) : "";
    const label = k === " " ? "space" : k === "shift" ? "Shift" : k.length === 2 ? `<small>${sh}</small>${base}` : base.toUpperCase();
    const f = FINGER[base] || 0;
    return `<span class="key f${f}${wide}" data-k="${base === "shift" ? "shift" : base}" data-s="${sh}">${label}</span>`;
  }).join("") + "</div>").join("");

  let cur = 0;
  const prog = TT.store.get("lessons", {});
  function list() {
    $("#lessons").innerHTML = LESSONS.map((L, i) => { const s = prog[i] || 0; return `<button class="lesson${i === cur ? " on" : ""}" data-i="${i}"><span class="ln">${i + 1}</span><span><b>${L.t}</b><small>${L.d}</small></span><span class="stars">${"★".repeat(s)}${"☆".repeat(3 - s)}</span></button>`; }).join("");
    const doneN = Object.values(prog).filter(s => s > 0).length; $("#lprog").textContent = `${doneN} of ${LESSONS.length} lessons passed`;
  }
  function start(i) {
    cur = i; list(); $("#ltitle").textContent = `Lesson ${i + 1}: ${LESSONS[i].t}`; $("#ldesc").textContent = LESSONS[i].d;
    $("#lres").classList.add("hidden");
    TT.load({ fixed: true, words: lessonWords(LESSONS[i]), keyboard: true, mode: "lesson" });
  }
  function done(R) {
    const stars = R.acc >= 96 && R.wpm >= 30 ? 3 : R.acc >= 92 && R.wpm >= 20 ? 2 : R.acc >= 85 ? 1 : 0;
    if (stars > (prog[cur] || 0)) { prog[cur] = stars; TT.store.set("lessons", prog); }
    const r = $("#lres"); r.classList.remove("hidden");
    r.innerHTML = `<div class="bigstars">${"★".repeat(stars)}${"☆".repeat(3 - stars)}</div><p><b>${R.wpm} WPM</b> · <b>${R.acc}%</b> accuracy</p><p>${stars === 3 ? "Perfect! On to the next lesson." : stars ? "Nice work! Aim for 96% accuracy and 30 WPM for 3 stars." : "Slow down and focus on hitting the right keys. Get 85% accuracy to pass."}</p><div class="row"><button class="btn" id="lretry">↻ Try again</button>${cur < LESSONS.length - 1 ? '<button class="btn primary" id="lnext">Next lesson →</button>' : ""}</div>`;
    $("#lretry").onclick = () => start(cur); const n = $("#lnext"); if (n) n.onclick = () => start(cur + 1);
    list();
  }
  $("#lessons").addEventListener("click", e => { const b = e.target.closest(".lesson"); if (b) start(+b.dataset.i); });
  $("#restart").onclick = () => start(cur);
  const first = LESSONS.findIndex((_, i) => !(prog[i] > 0));
  cur = first < 0 ? 0 : first;
  TT.init({ fixed: true, words: lessonWords(LESSONS[cur]), keyboard: true, mode: "lesson", onDone: done });
  $("#ltitle").textContent = `Lesson ${cur + 1}: ${LESSONS[cur].t}`; $("#ldesc").textContent = LESSONS[cur].d; list();
})();
