(() => {
  const $ = s => document.querySelector(s);
  const box = $("#rain"), inp = $("#rinput"), ov = $("#rov");
  const store = { get(k, d) { try { const v = localStorage.getItem("ytt_" + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } }, set(k, v) { try { localStorage.setItem("ytt_" + k, JSON.stringify(v)); } catch (e) {} } };
  let drops = [], score = 0, lives = 5, level = 1, typedChars = 0, running = false, last = 0, spawnT = 0, t0 = 0, best = store.get("rain_best", 0), list = WORDS.common.filter(w => w.length >= 3);
  $("#rbest").textContent = best;
  function spawn() {
    const pool = level < 3 ? list.filter(w => w.length <= 5) : level < 6 ? list : list.concat(list.filter(w => w.length > 6));
    let w; do { w = pool[Math.floor(Math.random() * pool.length)]; } while (drops.some(d => d.w === w));
    const e = document.createElement("div"); e.className = "drop"; e.textContent = w; box.appendChild(e);
    const maxX = box.clientWidth - e.offsetWidth - 8;
    const d = { w, e, x: 8 + Math.random() * Math.max(0, maxX), y: -30, v: 28 + level * 7 + Math.random() * 12 };
    e.style.left = d.x + "px"; drops.push(d);
  }
  function loop(t) {
    if (!running) return;
    const dt = Math.min(.05, (t - last) / 1000); last = t;
    spawnT -= dt; if (spawnT <= 0) { spawn(); spawnT = Math.max(.65, 2.2 - level * .16); }
    const H = box.clientHeight, cur = inp.value.trim().toLowerCase();
    for (const d of [...drops]) {
      d.y += d.v * dt; d.e.style.transform = `translateY(${d.y}px)`;
      d.e.classList.toggle("hit", !!cur && d.w.startsWith(cur));
      d.e.innerHTML = cur && d.w.startsWith(cur) ? `<b>${d.w.slice(0, cur.length)}</b>${d.w.slice(cur.length)}` : d.w;
      if (d.y > H - 30) { miss(d); }
    }
    const mins = (performance.now() - t0) / 60000; $("#rwpm").textContent = mins > .05 ? Math.round(typedChars / 5 / mins) : 0;
    requestAnimationFrame(loop);
  }
  function miss(d) {
    d.e.classList.add("lost"); setTimeout(() => d.e.remove(), 250); drops = drops.filter(x => x !== d);
    lives--; $("#rlives").textContent = "❤️".repeat(Math.max(0, lives)) + "🖤".repeat(5 - Math.max(0, lives));
    box.classList.add("shake"); setTimeout(() => box.classList.remove("shake"), 300);
    if (lives <= 0) over();
  }
  function check() {
    const v = inp.value.trim().toLowerCase(); if (!v) return;
    const d = drops.filter(x => x.w === v).sort((a, b) => b.y - a.y)[0];
    if (d) {
      score += d.w.length * 10 * level; typedChars += d.w.length + 1; inp.value = "";
      d.e.classList.add("pop"); drops = drops.filter(x => x !== d); setTimeout(() => d.e.remove(), 250);
      $("#rscore").textContent = score;
      const nl = 1 + Math.floor(score / (250 + level * 60)); if (nl > level) { level = nl; $("#rlevel").textContent = level; box.classList.add("lvl"); setTimeout(() => box.classList.remove("lvl"), 600); }
    }
  }
  function start() {
    drops.forEach(d => d.e.remove()); drops = []; score = 0; lives = 5; level = 1; typedChars = 0; spawnT = 0;
    $("#rscore").textContent = 0; $("#rlevel").textContent = 1; $("#rlives").textContent = "❤️❤️❤️❤️❤️";
    ov.classList.add("hidden"); running = true; inp.value = ""; inp.focus(); t0 = last = performance.now(); requestAnimationFrame(loop);
  }
  function over() {
    running = false; const pb = score > best; if (pb) { best = score; store.set("rain_best", best); $("#rbest").textContent = best; }
    ov.innerHTML = `<h2>Game over</h2><p>Score: <b>${score}</b> · Level ${level} · ${$("#rwpm").textContent} WPM${pb ? "<br>🏆 New high score!" : ""}</p><button class="btn primary" id="rgo">Play again</button>`;
    ov.classList.remove("hidden"); $("#rgo").onclick = start;
  }
  inp.addEventListener("input", check);
  inp.addEventListener("keydown", e => { if (e.key === "Enter") { e.preventDefault(); if (!running) start(); else { inp.value = ""; } } });
  $("#rgo").onclick = start;
})();
