import json, os, pathlib, shutil, re
OUT = pathlib.Path("public")
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir()
for f in pathlib.Path("static").iterdir(): shutil.copy(f, OUT / f.name)
SITE, DOMAIN, AUTHOR, UPDATED = "YourTypingTests", "https://yourtypingtests.com", "Aaron Hernandez", "November 2026"
CONTACT = os.environ.get("CONTACT_EMAIL", "")
PREVIEW = os.environ.get("PREVIEW")
ICON = "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='24' fill='%23f5b301'/><text x='50' y='68' font-size='54' text-anchor='middle'>⌨️</text></svg>"
LOGO = '<a class="logo" href="./"><span class="mark">⌨️</span><span>Your<em>TypingTests</em></span></a>'

def test_ui(dur=True, mode=True, kids=False):
    durs = seg("dur", [("15", "15s"), ("30", "30s"), ("60", "1 min"), ("120", "2 min"), ("180", "3 min"), ("300", "5 min")]) if dur else ""
    modes = (seg("mode", [("words", "Words"), ("sentences", "Sentences"), ("numbers", "Numbers")]) + '<button class="tog" id="punc" type="button">Punctuation</button><button class="tog" id="nums" type="button">+ Numbers</button>') if mode else ""
    return f'''<div class="ttbar" id="ttbar">{durs}{modes}<button class="btn" id="restart" type="button">↻ Restart</button></div>
<div class="live"><span id="timer">60</span><span id="lwpm">0 WPM</span><span id="lacc">100%</span></div>
<div class="wwrap{' kids' if kids else ''}" id="wwrap"><div id="caret"></div><div class="words" id="words"></div><input id="hidden" type="text" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" aria-label="Type here"></div>
<p class="hint">Just start typing. The timer starts on your first key · <kbd>Tab</kbd> or <kbd>Esc</kbd> to restart</p>
<div class="results hidden" id="results"><div class="rtop"><div class="big"><div class="n" id="r-wpm">0</div><div class="l">WPM</div><div class="n2" id="r-acc">0%</div><div class="l">ACCURACY</div></div>
<div><canvas class="chart" id="r-chart"></canvas></div></div><p class="pb" id="r-pb"></p>
<div class="stats"><div class="stat"><span>Raw speed</span><b id="r-raw">0</b></div><div class="stat"><span>Consistency</span><b id="r-cons">0</b></div><div class="stat"><span>Words ✓ / ✗</span><b id="r-words">0</b></div><div class="stat"><span>Time</span><b id="r-time">0</b></div></div>
<div class="level" id="r-level"></div>
<div id="r-progwrap" class="hidden" style="margin-top:14px"><b>📈 Your progress</b> <span class="hint" id="r-avg"></span><canvas class="chart" id="r-prog" style="height:150px;margin-top:6px"></canvas></div>
<div class="row"><button class="btn primary" id="again" type="button">↻ Try again</button><button class="btn" id="cert" type="button">🏅 Get certificate</button><button class="btn" id="share" type="button">📤 Share result</button></div></div>
<div class="modal hidden" id="certm"><div class="box"><div style="display:flex;justify-content:space-between;align-items:center"><b>🏅 Your typing certificate</b><button class="btn" id="cclose" type="button">✕</button></div>
<input id="cname" placeholder="Type your name for the certificate" maxlength="40" style="margin-top:10px"><canvas id="ccanvas"></canvas><button class="btn primary" id="cdl" type="button">⬇ Download certificate (PNG)</button></div></div>'''

def seg(id, opts): return f'<div class="seg" id="{id}">' + "".join(f'<button type="button" data-v="{v}">{t}</button>' for v, t in opts) + "</div>"
TEST_JS = '<script src="words.js"></script><script src="typing.js"></script><script src="app.js"></script>'

P = {}
def add(slug, emoji, name, title, desc, h1, sub, kind, cfg, content, faq, ui=None):
    P[slug] = dict(emoji=emoji, name=name, title=title, desc=desc, h1=h1, sub=sub, kind=kind, cfg=cfg, content=content, faq=faq, ui=ui or {})

WPM_TABLE = """<table><thead><tr><th>Speed</th><th>Level</th><th>What it means</th></tr></thead><tbody>
<tr><td>Under 20 WPM</td><td>Beginner</td><td>Usually hunt-and-peck typing. Lessons will help a lot.</td></tr>
<tr><td>20–35 WPM</td><td>Developing</td><td>You know the keyboard but still look down sometimes.</td></tr>
<tr><td>35–50 WPM</td><td>Average</td><td>Where most adults land. Fine for everyday typing.</td></tr>
<tr><td>50–70 WPM</td><td>Above average</td><td>Comfortable touch typing. Great for office work.</td></tr>
<tr><td>70–90 WPM</td><td>Fast</td><td>A strong speed for typing-heavy jobs.</td></tr>
<tr><td>90+ WPM</td><td>Very fast</td><td>Expert-level speed.</td></tr></tbody></table>"""

add("index", "⌨️", "Typing Test", "Typing Test – Free Typing Speed Test (WPM & Accuracy)",
    "Take a free typing test and check your typing speed in WPM and accuracy. 15 seconds to 5 minutes, results chart, progress tracking and a free certificate.",
    "Free <span>Typing Test</span>", "How fast can you type? Find your words per minute (WPM) and accuracy in 60 seconds.", "test", {"dur": 60},
    f"""<h2>How the typing test works</h2><p>Start typing the words on the screen. The timer starts with your first key press. Press <b>space</b> after each word to move to the next one. When time runs out, you'll see your <b>WPM</b> (words per minute), <b>accuracy</b>, a speed chart and your progress over time.</p>
<ul><li><b>WPM</b> counts only correctly typed words. One "word" is 5 characters, including spaces, the standard way typing speed is measured.</li><li><b>Raw speed</b> counts everything you typed, mistakes included.</li><li><b>Accuracy</b> is the percentage of keys you pressed correctly.</li><li><b>Consistency</b> shows how steady your speed was from second to second.</li></ul>
<h2>What is a good typing speed?</h2>{WPM_TABLE}<p>Want the full breakdown? Read <a href="average-typing-speed">what is a good typing speed</a>.</p>
<h2>Tips to type faster</h2><ol><li><b>Don't look at the keyboard.</b> Learning to touch type is the single biggest speed boost. Try our free <a href="typing-lessons">typing lessons</a>.</li><li><b>Accuracy first.</b> Fixing mistakes costs more time than typing a little slower.</li><li><b>Keep your fingers on the home row:</b> A S D F and J K L ;. Feel for the bumps on F and J.</li><li><b>Practice a few minutes daily.</b> Short, regular practice beats one long session.</li><li><b>Relax.</b> Tense hands are slow hands. Sit up straight and keep your wrists loose.</li></ol>""",
    [("How is WPM calculated?", "WPM is the number of correctly typed characters (including spaces) divided by 5, then divided by the minutes of the test. Dividing by 5 turns characters into standard 'words' so every test is measured the same way."),
     ("What is a good typing speed?", "Around 40 WPM is a common average for adults. 60 WPM or more is considered good for most office jobs, and 80+ WPM is fast."),
     ("Is this typing test free?", "Yes. Every test, lesson and certificate is completely free with no sign-up."),
     ("Can I take the typing test on my phone?", "Yes. Tap the text to bring up your keyboard. Phone keyboards are usually slower than physical keyboards, so compare phone results with other phone results."),
     ("Does it save my scores?", "Yes. Your personal bests and recent results are saved in your browser, so you can track your progress over time.")])

for secs, label, extra in [(60, "1 Minute", "The 1 minute typing test is the most popular way to measure typing speed. It's long enough to give a reliable WPM and short enough to take again and again."),
                           (180, "3 Minute", "A 3 minute typing test gives a more realistic picture of your everyday speed than a short burst, because it measures how well you keep your pace."),
                           (300, "5 Minute", "The 5 minute typing test is the classic test many employers use. It shows your true sustained speed and accuracy, the way you'd type in real work."),
                           (30, "30 Second", "The 30 second typing test is a quick burst of speed. It's great for warming up or for a fast check of your top speed.")]:
    slug = f"{label.lower().replace(' ', '-')}-typing-test"
    add(slug, "⏱️", f"{label} Typing Test", f"{label} Typing Test – Free {label} WPM Test", f"Take a free {label.lower()} typing test. Check your words per minute and accuracy, see your speed chart and get a free typing certificate.",
        f"{label} <span>Typing Test</span>", f"Type as many words as you can in {label.lower()}. Your WPM and accuracy appear the moment time runs out.", "test", {"dur": secs, "lockDur": True},
        f"""<h2>About the {label.lower()} typing test</h2><p>{extra} Your WPM counts only correctly typed words, and every mistake lowers your accuracy score.</p>
<h2>{label} typing test scores</h2>{WPM_TABLE}
<h2>How to do better</h2><ul><li>Warm up with a <a href="30-second-typing-test">30 second test</a> before longer ones.</li><li>Keep a steady rhythm instead of rushing. Speed bursts often lead to mistakes.</li><li>If you make a mistake mid-word, fix it right away with Backspace.</li><li>Build real speed with our <a href="typing-lessons">typing lessons</a>.</li></ul>""",
        [(f"What is a good score on a {label.lower()} typing test?", "Around 40 WPM is average, 60 WPM is good for most jobs, and 80 WPM or more is fast. Aim for at least 90% accuracy."),
         ("Can I get a certificate?", "Yes. After the test, click Get certificate, type your name and download it as an image."),
         ("Can I try other test lengths?", "Yes. Try the main typing test page to choose anything from 15 seconds to 5 minutes.")], ui={"dur": False})

add("typing-test-for-kids", "🧒", "Typing Test for Kids", "Typing Test for Kids – Fun Free Typing Practice for Kids",
    "A free typing test for kids with simple, fun words and big letters. Kids can check their typing speed, earn a certificate and track their progress.",
    "Typing Test <span>for Kids</span>", "Simple words, big letters and a certificate at the end. Perfect for young typists!", "test", {"dur": 60, "mode": "kids", "lockMode": True},
    """<h2>A typing test made for kids</h2><p>This version uses short, everyday words like <i>cat</i>, <i>sun</i> and <i>pizza</i>, with bigger letters that are easy to read. Kids can choose a test from 15 seconds to 5 minutes, see their speed, and print a certificate to show off their progress.</p>
<h2>What's a good typing speed for kids?</h2><p>Speeds vary a lot with age and practice. As a rough guide, many kids type around <b>5–15 WPM</b> in early elementary school, <b>15–25 WPM</b> in upper elementary and <b>25–40 WPM</b> by middle school. The most important thing is steady improvement and good habits.</p>
<h2>Tips for parents and teachers</h2><ul><li>Start with our <a href="typing-lessons">typing lessons</a> to learn the home row.</li><li>Practice for 10–15 minutes a day. Short sessions keep it fun.</li><li>Praise accuracy, not just speed.</li><li>Try the <a href="typing-game">Word Rain typing game</a> for extra fun practice.</li></ul>""",
    [("At what age should kids learn to type?", "Many kids start learning keyboarding around ages 7 to 9, when their hands are big enough to reach the keys comfortably."),
     ("Is this typing test free for schools?", "Yes. It's free for anyone, including classrooms, with no accounts needed."),
     ("Can kids get a certificate?", "Yes. After each test, click Get certificate, type a name and download or print it.")], ui={"mode": False, "kids": True})

add("number-typing-test", "🔢", "Number Typing Test", "Number Typing Test – Free Numbers & 10-Key Typing Test",
    "Practice typing numbers with a free number typing test. Check your speed on the number row or 10-key number pad for data entry jobs.",
    "Number <span>Typing Test</span>", "Test how fast and accurately you type numbers, on the number row or the number pad.", "test", {"dur": 60, "mode": "numbers", "lockMode": True},
    """<h2>Why practice typing numbers?</h2><p>Many jobs in data entry, accounting, banking and retail involve typing numbers all day. Fast, accurate number typing saves time and prevents costly mistakes. This test gives you random numbers so you can practice on the top number row or the <b>10-key number pad</b>.</p>
<h2>10-key typing tips</h2><ul><li>Rest your right hand on the number pad with your middle finger on <b>5</b>. It has a small bump.</li><li>Use your index finger for 1, 4 and 7, your middle finger for 2, 5 and 8, and your ring finger for 3, 6 and 9.</li><li>Use your thumb for <b>0</b>.</li><li>Make sure <b>Num Lock</b> is on.</li></ul>
<h2>What's a good number typing speed?</h2><p>Data entry jobs often measure number speed in <b>keystrokes per hour (KPH)</b>. Multiply your WPM by 300 for a rough KPH estimate. Many data entry roles look for about 8,000–10,000 KPH or more with high accuracy.</p>""",
    [("Can I use the number pad for this test?", "Yes. Use the number row or the number pad, whichever you want to practice."),
     ("How do I convert WPM to keystrokes per hour?", "Multiply WPM by 5 to get characters per minute, then by 60 for per hour. That's WPM × 300."),
     ("Is this good practice for data entry tests?", "Yes. Number speed and accuracy are key parts of most data entry tests.")], ui={"mode": False})

add("paragraph-typing-test", "📄", "Paragraph Typing Test", "Paragraph Typing Test – Free Typing Test with Sentences",
    "Take a free paragraph typing test with real sentences, capital letters and punctuation. Measure your true typing speed and accuracy.",
    "Paragraph <span>Typing Test</span>", "Type real sentences with capitals and punctuation, the way you type every day.", "test", {"dur": 60, "mode": "sentences", "lockMode": True},
    """<h2>Why use a paragraph typing test?</h2><p>Random word tests measure raw speed, but real typing includes <b>capital letters, commas, periods and longer words</b>. A paragraph test shows the speed you'll actually reach when writing emails, essays and reports. Expect it to be a little slower than a plain word test. That's normal!</p>
<h2>Tips for typing paragraphs</h2><ul><li>Use the <b>opposite Shift key</b> for capitals: the right Shift for left-hand letters and vice versa.</li><li>Read a word or two ahead so your fingers never wait.</li><li>Keep your rhythm through punctuation instead of stopping.</li></ul>""",
    [("Why is my paragraph speed lower than my word test speed?", "Sentences include capital letters, punctuation and longer words, which all take more time. Most people type 5–15% slower on paragraphs."),
     ("Are the paragraphs the same every time?", "No. The sentences are shuffled for each test, so you get fresh text every time."),
     ("How long is the test?", "One minute by default, and you can choose anything from 15 seconds to 5 minutes.")], ui={"mode": False})

add("typing-lessons", "🎓", "Typing Lessons", "Free Typing Lessons – Learn to Touch Type Step by Step",
    "Learn to touch type with 12 free typing lessons, from the home row to full sentences. On-screen keyboard shows which finger to use. Earn stars as you improve.",
    "Free <span>Typing Lessons</span>", "Learn to type without looking, one row at a time. The keyboard below shows the next key and which finger to use.", "lessons", {},
    """<h2>How to learn touch typing</h2><p>Touch typing means typing without looking at the keyboard, using all ten fingers. These 12 lessons teach the keyboard step by step, starting with the <b>home row</b> and adding a few new keys at a time. Each key on the on-screen keyboard is colored by the finger that should press it.</p>
<h2>The home row</h2><p>Place your left fingers on <b>A S D F</b> and your right fingers on <b>J K L ;</b>. Your thumbs rest on the space bar. Feel for the small bumps on <b>F</b> and <b>J</b>. They let you find the home row without looking. After every key, your fingers return home.</p>
<h2>Earning stars</h2><ul><li>⭐ Pass with at least 85% accuracy.</li><li>⭐⭐ Reach 92% accuracy and 20 WPM.</li><li>⭐⭐⭐ Reach 96% accuracy and 30 WPM.</li></ul><p>Your progress is saved in your browser, so you can pick up where you left off. When you finish, test yourself with the <a href="./">typing test</a>.</p>""",
    [("How long does it take to learn touch typing?", "With 15–20 minutes of practice a day, most people learn the keyboard in 2 to 4 weeks, and keep getting faster for months after that."),
     ("Should I look at the keyboard while learning?", "Try not to. Use the on-screen keyboard instead. It shows the next key and the finger to use, so you build the right habits."),
     ("Are these typing lessons free?", "Yes, all 12 lessons are free with no account needed.")])

add("typing-game", "🌧️", "Typing Game", "Typing Game – Word Rain Free Typing Game",
    "Play Word Rain, a free typing game. Type the falling words before they hit the ground. Levels get faster as you go. Great typing practice for kids and adults.",
    "Word Rain <span>Typing Game</span>", "Type the falling words before they hit the ground. How long can you last?", "game", {},
    """<h2>How to play Word Rain</h2><p>Words fall from the sky. Type a word exactly and it pops. Let a word reach the ground and you lose a life. You have 5 lives. As your score grows, you level up: words fall faster and get longer.</p>
<ul><li>You don't need to press Enter. A word pops as soon as you type it correctly.</li><li>Letters you've typed light up in yellow on matching words.</li><li>Press <b>Enter</b> to clear your typing if you make a mistake.</li></ul>
<h2>Why typing games help</h2><p>Games turn practice into fun, so you practice longer without noticing. Word Rain trains you to read ahead and react quickly, two skills that make you a faster typist in everyday life.</p>""",
    [("Is Word Rain free?", "Yes, it's completely free with no download."),
     ("Is it good for kids?", "Yes. The first levels use short, common words, so it's a great way for kids to practice."),
     ("Is my high score saved?", "Yes. Your best score is saved in your browser.")])

add("average-typing-speed", "📊", "Average Typing Speed", "Average Typing Speed – What Is a Good WPM?",
    "What is the average typing speed? See typing speed levels from beginner to expert, what WPM jobs look for, and take a free test to see where you stand.",
    "What Is a Good <span>Typing Speed?</span>", "See how your speed compares, then take the test below to find your WPM.", "test", {"dur": 60},
    f"""<h2>Average typing speed</h2><p>About <b>40 words per minute</b> is the figure most often quoted as the average typing speed for adults. Many people who type for work reach <b>50–70 WPM</b>, and expert typists go well past <b>90 WPM</b>. Accuracy matters too: aim for <b>95% or higher</b>.</p>
<h2>Typing speed levels</h2>{WPM_TABLE}
<h2>Typing speed for jobs</h2><ul><li><b>General office work:</b> about 40–50 WPM is usually enough.</li><li><b>Administrative assistants:</b> often 50–70 WPM.</li><li><b>Data entry:</b> 60+ WPM, or 8,000–10,000+ keystrokes per hour for number entry.</li><li><b>Transcription:</b> often 65–75 WPM or more with very high accuracy.</li></ul><p>Requirements vary by employer, so check the job listing.</p>
<h2>How to raise your WPM</h2><ol><li>Learn to touch type with our <a href="typing-lessons">free lessons</a>.</li><li>Practice daily with <a href="1-minute-typing-test">1 minute tests</a>.</li><li>Focus on accuracy, and speed will follow.</li><li>Keep good posture and relaxed hands.</li></ol>""",
    [("What is the average typing speed?", "About 40 WPM is the commonly cited average for adults. People who type for work often reach 50–70 WPM."),
     ("Is 60 WPM a good typing speed?", "Yes. 60 WPM is above average and meets the requirement for most office and typing jobs."),
     ("What is the fastest typing speed?", "The fastest typists can burst well over 200 WPM on short tests, but sustained speeds of 120–150 WPM are already world-class.")])

NAV = ["index", "1-minute-typing-test", "typing-lessons", "typing-game", "typing-test-for-kids", "paragraph-typing-test", "number-typing-test"]
ALL = list(P)
LESSON_UI = '''<div class="llayout"><div><p class="hint" id="lprog" style="text-align:left;margin:0 0 8px"></p><div id="lessons"></div></div>
<div class="lpanel"><h2 id="ltitle"></h2><p class="hint" id="ldesc" style="text-align:left;margin:2px 0 0"></p>
<div class="live"><span id="timer">0s</span><span id="lwpm">0 WPM</span><span id="lacc">100%</span></div>
<div class="wwrap" id="wwrap"><div id="caret"></div><div class="words" id="words"></div><input id="hidden" type="text" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" aria-label="Type here"></div>
<div id="lres" class="hidden"></div><div class="kb" id="kb"></div><div class="row"><button class="btn" id="restart" type="button">↻ Restart lesson</button></div></div></div>
<script src="words.js"></script><script src="typing.js"></script><script src="lessons.js"></script>'''
GAME_UI = '''<div class="rstats"><span>Score <b id="rscore">0</b></span><span>Level <b id="rlevel">1</b></span><span>WPM <b id="rwpm">0</b></span><span>Best <b id="rbest">0</b></span><span id="rlives">❤️❤️❤️❤️❤️</span></div>
<div class="rain" id="rain"><div class="rov" id="rov"><h2>🌧️ Word Rain</h2><p>Type the falling words before they hit the ground.</p><button class="btn primary" id="rgo" type="button">Start game</button></div></div>
<input class="rinput" id="rinput" type="text" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" placeholder="Type here…" aria-label="Type the falling words">
<script src="words.js"></script><script src="game.js"></script>'''

def page(slug, title, desc, body, faq=None, app=False):
    url = DOMAIN + "/" + ("" if slug == "index" else slug)
    nav = "".join(f'<a href="{"./" if s == "index" else s}"{" class=on" if s == slug else ""}>{P[s]["name"]}</a>' for s in NAV)
    ld = [{"@context": "https://schema.org", "@type": "WebApplication", "name": title.split(" – ")[0], "url": url, "applicationCategory": "EducationalApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "publisher": {"@type": "Person", "name": AUTHOR}}]
    if faq: ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    foot = "".join(f'<a href="{"./" if s == "index" else s}">{P[s]["name"]}</a>' for s in ALL)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:url" content="{url}">
<meta name="theme-color" content="#14161f">
<link rel="icon" href="{ICON}">
<link rel="stylesheet" href="style.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<header class="top"><div class="wrap">{LOGO}<nav class="top">{nav}</nav></div></header>
<main class="wrap">{body}</main>
<footer><div class="wrap"><div><b>{SITE}</b><br>Free typing tests, lessons and games.<br>Made by {AUTHOR} · © 2026</div><div>{foot}<br><a href="about">About</a><a href="privacy">Privacy</a></div></div></footer>
</body>
</html>"""

pages = {}
for s, d in P.items():
    if d["kind"] == "test":
        ui = test_ui(dur=d["ui"].get("dur", True), mode=d["ui"].get("mode", True), kids=d["ui"].get("kids", False)) + f"<script>window.TTCFG={json.dumps(d['cfg'])}</script>" + TEST_JS
    elif d["kind"] == "lessons": ui = LESSON_UI
    else: ui = GAME_UI
    others = '<h2>More typing tests and practice</h2><div class="tiles">' + "".join(f'<a href="{"./" if o == "index" else o}"><span>{P[o]["emoji"]}</span>{P[o]["name"]}</a>' for o in ALL if o != s) + "</div>"
    faqh = '<h2>Frequently asked questions</h2><div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in d["faq"]) + "</div>"
    body = f'''<section class="head"><h1>{d["h1"]}</h1><p>{d["sub"]}</p></section>{ui}
<article class="content">{d["content"]}{faqh}{others}<p class="hint" style="text-align:left;margin-top:30px">Updated {UPDATED} by {AUTHOR}</p></article>'''
    pages[s] = page(s, d["title"], d["desc"], body, d["faq"])

contact = f"<p>Questions or ideas? Email <a href=\"mailto:{CONTACT}\">{CONTACT}</a>.</p>" if CONTACT else ""
pages["about"] = page("about", f"About {SITE}", f"About {SITE}, free typing tests and lessons made by {AUTHOR}.",
    f'''<article class="content"><h1>About {SITE}</h1><p>Hi, I'm {AUTHOR}. I built {SITE} to be a clean, fast place to test and improve your typing, with no sign-ups, no clutter and no cost.</p>
<p>All the practice text is original, and your results stay private in your own browser.</p><h2>What you'll find here</h2><ul>{"".join(f'<li><a href="{"./" if s == "index" else s}">{P[s]["name"]}</a></li>' for s in ALL)}</ul>{contact}</article>''')
pages["privacy"] = page("privacy", f"Privacy Policy – {SITE}", f"Privacy policy for {SITE}.",
    f'''<article class="content"><h1>Privacy Policy</h1><p>Last updated: {UPDATED}</p>
<h2>Your results stay on your device</h2><p>Your typing results, personal bests, lesson progress and certificate name are saved only in your own browser's local storage. They are never sent to our servers.</p>
<h2>Advertising</h2><p>This site may show ads from Google and other partners to stay free. These partners may use cookies to show ads based on your visits to this and other websites. You can opt out of personalized ads at <a href="https://www.google.com/settings/ads" rel="nofollow">Google Ads Settings</a>.</p>
<h2>Analytics</h2><p>We may use privacy-friendly analytics to count page visits. This data is aggregated and isn't used to identify you.</p>{contact}</article>''')

for slug, html in pages.items():
    if PREVIEW:
        html = re.sub(r'href="(%s)"' % "|".join(re.escape(s) for s in pages if s != "index"), r'href="\1.html"', html).replace('href="./"', 'href="index.html"')
    (OUT / f"{slug}.html").write_text(html)
urls = "".join(f"<url><loc>{DOMAIN}/{'' if s == 'index' else s}</loc></url>" for s in pages if s != "privacy")
(OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
print("built", len(pages), "pages")
