(() => {
  const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
  const CFG = Object.assign({ dur: 60, mode: "words" }, window.TTCFG || {});
  const saved = TT.store.get("opts", {});
  if (!CFG.lockDur && saved.dur) CFG.dur = saved.dur;
  if (!CFG.lockMode) { if (saved.mode) CFG.mode = saved.mode; CFG.punc = !!saved.punc; CFG.nums = !!saved.nums; }
  function seg(id, val, cb) {
    const box = $(id); if (!box) return;
    $$(id + " button").forEach(b => b.classList.toggle("on", b.dataset.v == val));
    box.addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return; $$(id + " button").forEach(x => x.classList.toggle("on", x === b)); cb(b.dataset.v); b.blur(); });
  }
  const persist = () => TT.store.set("opts", { dur: TT.cfg.dur, mode: TT.cfg.mode, punc: TT.cfg.punc, nums: TT.cfg.nums });
  seg("#dur", CFG.dur, v => { TT.set("dur", +v); persist(); });
  seg("#mode", CFG.mode, v => { TT.set("mode", v); persist(); syncToggles(); });
  const syncToggles = () => { $$(".tog").forEach(t => t.classList.toggle("hidden", TT.cfg.mode !== "words")); };
  [["#punc", "punc"], ["#nums", "nums"]].forEach(([id, k]) => { const b = $(id); if (!b) return; b.classList.toggle("on", !!CFG[k]); b.onclick = () => { const v = !TT.cfg[k]; b.classList.toggle("on", v); TT.set(k, v); persist(); b.blur(); }; });
  TT.init(CFG); syncToggles();
  $("#restart").onclick = () => TT.restart(); $("#again").onclick = () => TT.restart();
  $("#share").onclick = async () => {
    const R = window.__lastResult; if (!R) return;
    const txt = `I just typed ${R.wpm} WPM with ${R.acc}% accuracy on a ${R.dur}-second typing test! ⌨️ Try it: ${location.origin}${location.pathname}`;
    try { if (navigator.share) await navigator.share({ text: txt }); else { await navigator.clipboard.writeText(txt); flash("#share", "✓ Copied!"); } } catch (e) {}
  };
  function flash(s, t) { const b = $(s), o = b.textContent; b.textContent = t; setTimeout(() => b.textContent = o, 1500); }

  // ---------- certificate ----------
  const modal = $("#certm");
  $("#cert").onclick = () => { if (!window.__lastResult) return; $("#cname").value = TT.store.get("name", ""); modal.classList.remove("hidden"); drawCert(); $("#cname").focus(); };
  $("#cclose").onclick = () => modal.classList.add("hidden");
  modal.addEventListener("click", e => { if (e.target === modal) modal.classList.add("hidden"); });
  $("#cname").oninput = () => { TT.store.set("name", $("#cname").value); drawCert(); };
  $("#cdl").onclick = () => { const a = document.createElement("a"); a.href = $("#ccanvas").toDataURL("image/png"); a.download = "typing-certificate.png"; a.click(); };
  function drawCert() {
    const R = window.__lastResult, c = $("#ccanvas"), x = c.getContext("2d"), W = 1400, H = 990; c.width = W; c.height = H;
    const g = x.createLinearGradient(0, 0, W, H); g.addColorStop(0, "#fffaf0"); g.addColorStop(1, "#fff3d6"); x.fillStyle = g; x.fillRect(0, 0, W, H);
    x.strokeStyle = "#e0a800"; x.lineWidth = 14; x.strokeRect(36, 36, W - 72, H - 72); x.strokeStyle = "#1f2433"; x.lineWidth = 3; x.strokeRect(66, 66, W - 132, H - 132);
    x.textAlign = "center"; x.fillStyle = "#1f2433";
    x.font = "700 34px Georgia, serif"; x.fillText("YourTypingTests.com", W / 2, 150);
    x.font = "700 78px Georgia, serif"; x.fillText("Certificate of Typing Speed", W / 2, 260);
    x.font = "italic 32px Georgia, serif"; x.fillStyle = "#555"; x.fillText("This certifies that", W / 2, 345);
    const name = ($("#cname").value || "Your Name").slice(0, 40);
    x.fillStyle = "#1f2433"; x.font = "700 70px Georgia, serif"; x.fillText(name, W / 2, 440);
    x.strokeStyle = "#e0a800"; x.lineWidth = 3; x.beginPath(); x.moveTo(W / 2 - 360, 465); x.lineTo(W / 2 + 360, 465); x.stroke();
    x.font = "32px Georgia, serif"; x.fillStyle = "#555"; x.fillText(`completed a ${R.dur}-second typing test with a speed of`, W / 2, 530);
    x.font = "900 150px Georgia, serif"; x.fillStyle = "#c98a00"; x.fillText(`${R.wpm} WPM`, W / 2, 690);
    x.font = "700 40px Georgia, serif"; x.fillStyle = "#1f2433"; x.fillText(`Accuracy: ${R.acc}%`, W / 2, 770);
    x.font = "28px Georgia, serif"; x.fillStyle = "#555";
    x.fillText(new Date(R.date).toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" }), W / 2 - 330, 880);
    x.fillText("yourtypingtests.com", W / 2 + 330, 880);
    x.beginPath(); x.arc(W / 2, 865, 52, 0, 7); x.fillStyle = "#e0a800"; x.fill(); x.font = "50px serif"; x.fillText("⌨️", W / 2, 884);
  }
})();
