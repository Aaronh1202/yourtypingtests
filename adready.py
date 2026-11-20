"""Shared post-build step: makes a static site AdSense-ready.

- Full Privacy Policy, Terms of Use, About and Contact pages (cloned from the
  site's own privacy.html shell so they match the design).
- Legal links in every footer.
- Extra, page-specific help content (how-to, tips, FAQ) appended to tool pages.
- Placeholder emails replaced, sitemap updated.
"""
import os, re, html as _h

OWNER = "Aaron Hernandez"


def _contact():
    return os.environ.get("CONTACT_EMAIL") or "Aaronh1202@gmail.com"


def faq(items):
    """items: list of (question, answer_html) -> FAQ section html."""
    out = "<h2>Frequently asked questions</h2>"
    for q, a in items:
        out += f"<h3>{q}</h3><p>{a}</p>"
    return out


def _shell(template, slug, title, desc, body, domain):
    t = template
    t = re.sub(r"<title>.*?</title>", f"<title>{_h.escape(title)}</title>", t, count=1, flags=re.S)
    t = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + _h.escape(desc) + m.group(2), t, count=1)
    t = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + f"{domain}/{slug}" + m.group(2), t, count=1)
    t = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1) + _h.escape(title) + m.group(2), t, count=1)
    t = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1) + _h.escape(desc) + m.group(2), t, count=1)
    t = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m: m.group(1) + f"{domain}/{slug}" + m.group(2), t, count=1)
    t = re.sub(r'<script type="application/ld\+json">.*?</script>', "", t, flags=re.S)
    t = t.replace(' class="active"', "")
    h1 = title.split(" | ")[0].split(" – ")[0]
    t = re.sub(r"(<main[^>]*>).*?(</main>)",
               lambda m: m.group(1) + f'\n<h1>{h1}</h1>\n<section class="content legal">{body}</section>\n' + m.group(2),
               t, count=1, flags=re.S)
    return t


def legal_pages(site, domain, what, about_extra=""):
    c = _contact()
    mail = f'<a href="mailto:{c}">{c}</a>'
    privacy = f"""
<p><b>Last updated:</b> November 18, 2026</p>
<p>This Privacy Policy explains how {site} ("we", "us") handles information when you use {domain.replace('https://','')} (the "Site"). We built the Site so that you can use it without creating an account or giving us personal information.</p>
<h2>Information we collect</h2>
<p><b>Things you enter into the tools.</b> {what} run entirely inside your web browser. Text, files, images and settings you enter are processed on your own device and are not uploaded to our servers. Some preferences (for example your last settings, best scores or streaks) may be saved in your browser's local storage so they are still there next time. You can clear them at any time by clearing your browser data.</p>
<p><b>Usage data.</b> We use Cloudflare Web Analytics to count visits and see which pages are popular. It does not use cookies, does not track you across websites and does not collect personal information. Our hosting provider (Cloudflare) also processes standard technical data such as IP address and browser type to deliver the Site securely.</p>
<h2>Cookies and advertising</h2>
<p>The Site is free because it is supported by advertising. We use (or may use) Google AdSense to show ads. Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this website or other websites.</p>
<p>Google's use of advertising cookies enables it and its partners to serve ads to you based on your visit to this Site and/or other sites on the Internet. You may opt out of personalized advertising by visiting <a href="https://adssettings.google.com" rel="nofollow">Google Ads Settings</a>. You can also opt out of some third-party vendors' use of cookies for personalized advertising at <a href="https://www.aboutads.info/choices/" rel="nofollow">aboutads.info</a>.</p>
<p>To learn how Google uses information from sites that use its services, see <a href="https://policies.google.com/technologies/partner-sites" rel="nofollow">How Google uses information from sites or apps that use our services</a>. Where required by law (for example in the EEA, UK and Switzerland), we will ask for your consent before personalized ads cookies are used.</p>
<h2>How we use information</h2>
<p>We use the limited data above to keep the Site running, fix problems, understand which tools are useful and fund the Site through advertising. We do not sell personal information.</p>
<h2>Your choices and rights</h2>
<p>You can block or delete cookies in your browser settings, use the opt-out links above, and clear local storage at any time. Depending on where you live (for example under the GDPR or the California Consumer Privacy Act), you may have rights to access, correct or delete personal data. Because we don't collect personal data directly, there is usually nothing for us to delete, but you can contact us with any request.</p>
<h2>Children</h2>
<p>The Site is meant for a general audience and is not directed at children under 13. We do not knowingly collect personal information from children.</p>
<h2>Changes</h2>
<p>We may update this policy from time to time. The date at the top shows when it was last changed.</p>
<h2>Contact</h2>
<p>Questions about this policy? Email {mail}.</p>"""
    terms = f"""
<p><b>Last updated:</b> November 18, 2026</p>
<p>By using {site} (the "Site") you agree to these Terms of Use. If you don't agree, please don't use the Site.</p>
<h2>Use of the Site</h2>
<p>The Site provides free online tools for personal and commercial use. You may use them as much as you like, but you agree not to misuse the Site: for example by trying to break, overload or copy the Site, scraping it automatically, or using it for anything unlawful.</p>
<h2>Your content</h2>
<p>Anything you type, upload or create with the tools stays yours. Processing happens in your browser, so we don't receive or store your files. You are responsible for having the right to use any content you put into the tools.</p>
<h2>No warranty</h2>
<p>We work hard to make the tools accurate and reliable, but the Site is provided "as is" without warranties of any kind. Results are for general information only and are not professional (financial, legal, medical or technical) advice. Always double-check important results.</p>
<h2>Limitation of liability</h2>
<p>To the fullest extent allowed by law, {site} and its owner are not liable for any loss or damage arising from your use of the Site, including lost data or decisions made based on results.</p>
<h2>Advertising and links</h2>
<p>The Site shows ads and may link to other websites. We are not responsible for the content, products or privacy practices of third-party sites or advertisers.</p>
<h2>Changes</h2>
<p>We may change these terms or the Site at any time. Continuing to use the Site means you accept the current terms.</p>
<h2>Contact</h2>
<p>Questions? Email {mail}.</p>"""
    about = f"""
<p>{site} is an independent website made by {OWNER}. The idea is simple: useful tools that open instantly, work on any phone or computer, and don't make you sign up, install anything or upload your data.</p>
{about_extra}
<h2>How the tools work</h2>
<p>{what} run directly in your web browser using modern web technology. That makes them fast and private: your data stays on your device. It also means the tools keep working on slow connections once the page has loaded.</p>
<h2>Why it's free</h2>
<p>The Site is supported by advertising. Ads pay for the domain, hosting and time spent building new tools. We keep ads out of the way of the tools themselves.</p>
<h2>Feedback</h2>
<p>Found a bug, have an idea for a new tool or spotted a mistake? We read every message. Visit the <a href="contact">Contact page</a> or email <a href="mailto:{c}">{c}</a>.</p>"""
    contact = f"""
<p>We'd love to hear from you. Whether you found a bug, want a new feature or tool, have a business inquiry or a question about privacy, the best way to reach us is by email.</p>
<p style="font-size:1.25em"><b>Email:</b> {mail}</p>
<h2>What to include</h2>
<p>If you're reporting a problem, please tell us which page you were on, what you expected to happen and what happened instead, plus your device and browser (for example "iPhone, Safari" or "Windows, Chrome"). Screenshots help a lot.</p>
<h2>Response time</h2>
<p>{site} is run by {OWNER}. We usually reply within 2–3 business days.</p>
<h2>Privacy requests</h2>
<p>For questions about your data or cookies, see our <a href="privacy">Privacy Policy</a> or email us with "Privacy" in the subject line.</p>"""
    return {
        "privacy": (f"Privacy Policy | {site}", f"Privacy policy for {site}: what we collect, cookies, Google AdSense advertising and your choices.", privacy),
        "terms": (f"Terms of Use | {site}", f"Terms of use for {site}.", terms),
        "about": (f"About {site}", f"About {site}: free online tools by {OWNER} that run in your browser, no sign-up needed.", about),
        "contact": (f"Contact Us | {site}", f"Contact {site} by email for feedback, bug reports, business or privacy questions.", contact),
    }


NETWORK = [("yourstopwatch.com", "Online Stopwatch &amp; Timers"), ("yourspinwheel.com", "Spin the Wheel"),
           ("yourimagetools.com", "Image Tools"), ("yourcalculatorapp.com", "Calculators"),
           ("yourfreeonlinegames.com", "Free Online Games"), ("yourdevicetest.com", "Device Tests"),
           ("yourqrcodegenerator.com", "QR Code Generator"), ("yourtypingtests.com", "Typing Test")]
# Only link to sites that are live, so we never show broken links. Add domains here as they go live.
LIVE = {d for d, _ in NETWORK}


def _social(h, site, domain, slug):
    """Add Open Graph / Twitter tags and the share image if missing."""
    title = re.search(r"<title>(.*?)</title>", h, re.S)
    desc = re.search(r'<meta name="description" content="([^"]*)"', h)
    t = title.group(1).strip() if title else site
    d = desc.group(1) if desc else ""
    url = f"{domain}/" + ("" if slug == "index" else slug)
    tags = []
    if 'property="og:title"' not in h: tags.append(f'<meta property="og:title" content="{t}">')
    if 'property="og:description"' not in h and d: tags.append(f'<meta property="og:description" content="{d}">')
    if 'property="og:type"' not in h: tags.append('<meta property="og:type" content="website">')
    if 'property="og:url"' not in h: tags.append(f'<meta property="og:url" content="{url}">')
    if 'property="og:site_name"' not in h: tags.append(f'<meta property="og:site_name" content="{site}">')
    if 'property="og:image"' not in h:
        tags += [f'<meta property="og:image" content="{domain}/og.png">', '<meta property="og:image:width" content="1200">',
                 '<meta property="og:image:height" content="630">', f'<meta property="og:image:alt" content="{site}">']
    if 'name="twitter:card"' not in h:
        tags += ['<meta name="twitter:card" content="summary_large_image">', f'<meta name="twitter:title" content="{t}">',
                 f'<meta name="twitter:image" content="{domain}/og.png">'] + ([f'<meta name="twitter:description" content="{d}">'] if d else [])
    return h.replace("</head>", "".join(tags) + "</head>", 1) if tags else h


ADSENSE_PUB = "ca-pub-2333823498112859"
ADSENSE_TAG = ('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='
               + ADSENSE_PUB + '" crossorigin="anonymous"></script>')


LEGAL_CSS = ('<style>.legal-links{text-align:center;padding:14px 0 4px;font-size:.9em;opacity:.85}'
             '.legal-links a{margin:0 8px}.net-links{text-align:center;font-size:.8em;opacity:.7;padding:2px 12px 14px;line-height:1.9}.net-links a{margin:0 6px;white-space:nowrap}.legal h3{margin-top:1.2em;font-size:1.05em}</style>')


def run(out, site, domain, what, extra=None, default_extra="", about_extra="", skip=()):
    """out: pathlib.Path to built site. extra: dict slug -> html appended to that page."""
    extra = extra or {}
    c = _contact()
    tpl_path = out / "privacy.html"
    template = tpl_path.read_text()
    pages = legal_pages(site, domain, what, about_extra)
    for slug, (title, desc, body) in pages.items():
        f = out / f"{slug}.html"
        if slug == "about" and f.exists() and "adready-about" not in f.read_text():
            # keep the site's own About page, add the shared sections below it
            h = f.read_text()
            more = body[body.index("<h2>How the tools work"):]
            i = h.rfind("</main>")
            f.write_text(h[:i] + f'<section class="content adready-about">{more}</section>\n' + h[i:])
            continue
        f.write_text(_shell(template, slug, title, desc, body, domain))
    links = ('<div class="wrap legal-links"><a href="about">About</a>·<a href="contact">Contact</a>'
             '·<a href="terms">Terms</a>·<a href="privacy">Privacy</a></div>')
    net = '<div class="wrap net-links">More free tools: ' + " · ".join(
        f'<a href="https://{d}/">{n}</a>' for d, n in NETWORK if d not in domain and d in LIVE) + "</div>"
    import shutil, pathlib
    if pathlib.Path("og.png").exists():
        shutil.copy("og.png", out / "og.png")
    added = 0
    for f in sorted(out.glob("*.html")):
        slug = f.stem
        h = f.read_text()
        h = h.replace("hello@example.com", c)
        if slug not in pages and slug not in skip and slug not in ("how-we-calculate",):
            add = extra.get(slug, default_extra)
            if add:
                block = f'<section class="content more">{add}</section>'
                i = h.rfind("</main>")
                h = h[:i] + block + "\n" + h[i:]
                added += 1
        if "legal-links" not in h:
            h = h.replace("</footer>", links + "</footer>", 1)
        if "LEGALCSS" not in h:
            h = h.replace("</head>", LEGAL_CSS.replace("<style>", "<style>/*LEGALCSS*/") + "</head>", 1)
        if 'class="wrap net-links"' not in h:
            h = h.replace("</footer>", net + "</footer>", 1)
        h = _social(h, site, domain, slug)
        if "adsbygoogle.js" not in h:
            h = h.replace("</head>", ADSENSE_TAG + "</head>", 1)
        f.write_text(h)
    (out / "ads.txt").write_text(f"google.com, {ADSENSE_PUB.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n")
    sm = out / "sitemap.xml"
    if sm.exists():
        s = sm.read_text()
        for slug in pages:
            loc = f"<loc>{domain}/{slug}</loc>"
            if loc not in s:
                s = s.replace("</urlset>", f"<url>{loc}</url></urlset>")
        sm.write_text(s)
    print(f"adready: legal pages + content added to {added} pages")
    ai_ready(out, site, domain, what)


# ---------------- AI search readiness (ChatGPT, Perplexity, Claude, Gemini, Copilot) ----------------
AI_BOTS = ["OAI-SearchBot", "ChatGPT-User", "GPTBot", "PerplexityBot", "Perplexity-User", "Claude-SearchBot",
           "Claude-User", "ClaudeBot", "Google-Extended", "Applebot-Extended", "Bingbot", "Googlebot"]


def _txt(x):
    x = re.sub(r"<[^>]+>", " ", x)
    return re.sub(r"\s+", " ", _h.unescape(x)).strip()


def _faq_pairs(h):
    m = re.search(r"<h2[^>]*>\s*(Frequently asked questions|FAQ)[^<]*</h2>(.*?)(?=<h2|</section>|</main>)", h, re.S | re.I)
    if not m:
        return []
    body = m.group(2)
    pairs = re.findall(r"<summary>(.*?)</summary>\s*(.*?)</details>", body, re.S)
    if not pairs:
        pairs = re.findall(r"<h3[^>]*>(.*?)</h3>\s*(.*?)(?=<h3|$)", body, re.S)
    return [(_txt(q), _txt(a)) for q, a in pairs if _txt(q) and _txt(a)]


def ai_ready(out, site, domain, what):
    import json
    n_faq = 0
    pages = []
    for f in sorted(out.glob("*.html")):
        h = f.read_text()
        if '"FAQPage"' not in h:
            pairs = _faq_pairs(h)
            if pairs:
                data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}
                tag = '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>"
                h = h.replace("</head>", tag + "</head>", 1)
                f.write_text(h)
                n_faq += 1
        if 'name="robots" content="noindex' in h:
            continue
        t = re.search(r"<title>(.*?)</title>", h, re.S)
        d = re.search(r'<meta name="description" content="([^"]*)"', h)
        slug = "" if f.stem == "index" else f.stem
        pages.append((slug, _txt(t.group(1)).split(" | ")[0] if t else f.stem, _h.unescape(d.group(1)) if d else ""))
    # robots.txt: explicitly welcome search + AI answer crawlers
    rob = "User-agent: *\nAllow: /\n\n# AI search and answer engines are welcome\n"
    rob += "".join(f"User-agent: {b}\nAllow: /\n\n" for b in AI_BOTS)
    rob += f"Sitemap: {domain}/sitemap.xml\n"
    (out / "robots.txt").write_text(rob)
    # llms.txt: plain-language map of the site for AI assistants
    legal = {"about", "contact", "privacy", "terms"}
    main = [p for p in pages if p[0] not in legal]
    home = next((p for p in pages if p[0] == ""), None)
    lines = [f"# {site}", "", f"> {home[2] if home and home[2] else what}", "",
             f"Everything on {domain} is free and runs in the browser, with no sign-up or download.",
             "Pages are free to use and to link to.", "", "## Tools and pages", ""]
    for slug, title, desc in main:
        url = f"{domain}/{slug}" if slug else f"{domain}/"
        lines.append(f"- [{title}]({url})" + (f": {desc}" if desc else ""))
    lines += ["", "## About", ""] + [f"- [{t}]({domain}/{s})" for s, t, _ in pages if s in legal]
    (out / "llms.txt").write_text("\n".join(lines) + "\n")
    print(f"ai_ready: FAQ schema added to {n_faq} pages, robots.txt + llms.txt ({len(main)} pages)")
