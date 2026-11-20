"""More typing test pages for YourTypingTests."""

CERT = ("Can I get a certificate?", "Yes. After the test, click Get certificate, type your name and download or print it.")
SAVED = ("Are my results saved?", "Your best scores and recent results are saved in your own browser, so you can track your progress. Nothing is uploaded.")


def add_all(add, WPM_TABLE):
    for secs, label, about in [
        (15, "15 Second", "The 15 second typing test is the shortest test here. It measures your absolute top speed, since there's no time to slow down or tire. Expect your result to be a little higher than in longer tests."),
        (120, "2 Minute", "Two minutes is a nice balance: long enough for a reliable score, short enough to repeat a few times in a practice session. Many school and training programs use 2-minute timed writings."),
        (600, "10 Minute", "The 10 minute typing test measures real stamina. It's close to how you type when writing a long email or report, and some employers and certifications use 10-minute tests. Keep a steady pace and stay relaxed."),
    ]:
        slug = f"{label.lower().replace(' ', '-')}-typing-test"
        add(slug, "⏱️", f"{label} Typing Test", f"{label} Typing Test – Free {label} WPM Test",
            f"Take a free {label.lower()} typing test. See your words per minute, accuracy and speed chart, and get a free certificate.",
            f"{label} <span>Typing Test</span>", f"Type as many words as you can in {label.lower()}s." if secs < 60 else f"Type as many words as you can in {label.lower()}s.",
            "test", {"dur": secs, "lockDur": True},
            f"<h2>About the {label.lower()} typing test</h2><p>{about}</p><h2>How does your score compare?</h2>{WPM_TABLE}"
            "<h2>Tips</h2><ul><li>Look at the next word, not your fingers.</li><li>Fix mistakes right away with Backspace: wrong words don't count toward WPM.</li><li>Relax your shoulders and keep your wrists level.</li></ul>",
            [(f"What's a good {label.lower()} typing score?", "About 40 WPM is average, 60 WPM is good for most jobs and 80 WPM or more is fast."), CERT, SAVED],
            ui={"dur": False})

    add("typing-test-with-punctuation", "❗", "Punctuation Typing Test", "Typing Test with Punctuation – Free WPM Test with Commas & Periods",
        "Free typing test with punctuation. Practice commas, periods, question marks and capitals while measuring your WPM and accuracy.",
        "Typing Test with <span>Punctuation</span>", "Real typing includes commas, periods and capital letters. Test yourself with them included.",
        "test", {"dur": 60, "mode": "words", "punc": True, "lockMode": True},
        """<h2>Why practice punctuation?</h2><p>Most typing tests use plain lowercase words, but real writing is full of capitals, commas, periods, question marks and apostrophes. Reaching for Shift and the punctuation keys slows most people down by 10–20%, so practicing them makes your everyday typing faster.</p>
<h2>Punctuation key tips</h2><ul><li>Use the <b>opposite</b> hand's Shift key: left Shift for keys typed with the right hand, and right Shift for the left hand.</li><li>Your right pinky handles the semicolon, apostrophe, slash and question mark; your right ring finger handles the period; your right middle finger the comma.</li><li>Keep the rest of your fingers on the home row while your pinky stretches.</li></ul>""",
        [("Why is my WPM lower with punctuation?", "Shift and punctuation keys need extra finger movement. A drop of 5–15 WPM compared with plain words is normal."), CERT, SAVED], ui={"mode": False})

    add("advanced-typing-test", "🔥", "Advanced Typing Test", "Advanced Typing Test – Hard Typing Test with Numbers & Punctuation",
        "Challenge yourself with a harder typing test: mixed punctuation, capitals and numbers. Measure your real-world WPM and accuracy.",
        "Advanced <span>Typing Test</span>", "A harder test with punctuation, capitals and numbers mixed in. Ready for the challenge?",
        "test", {"dur": 60, "mode": "words", "punc": True, "nums": True, "lockMode": True},
        """<h2>A tougher typing test</h2><p>This test mixes common words with punctuation, capital letters and numbers, so you have to use the whole keyboard, including the number row. It's a better match for real work like writing reports, invoices and emails than a plain word test.</p>
<h2>How to master the number row</h2><p>Each number key is typed by the same finger that types the letter below it: 1 and 2 with the left pinky and ring finger, 5 and 6 with the index fingers, 0 with the right pinky. Reach up without moving your whole hand, then return to the home row.</p>""",
        [("What's a good score on this test?", "Scores are usually 10–25% lower than on a plain word test. 45+ WPM with over 95% accuracy is excellent."), CERT, SAVED], ui={"mode": False})

    add("data-entry-typing-test", "🗂️", "Data Entry Test", "Data Entry Typing Test – Free Practice Test (Numbers & Accuracy)",
        "Free data entry typing test. Practice typing numbers quickly and accurately, the skills tested for data entry jobs. Measure your speed and accuracy.",
        "Data Entry <span>Typing Test</span>", "Practice the number speed and accuracy that data entry jobs test for.",
        "test", {"dur": 180, "mode": "numbers", "lockMode": True, "lockDur": True},
        """<h2>What data entry tests measure</h2><p>Data entry jobs test how fast and accurately you type numbers and text. Employers often measure <b>keystrokes per hour (KPH)</b> for numbers: 8,000–10,000 KPH is a common minimum, and experienced clerks reach 12,000+. For text, 35–45 WPM is a typical requirement. Accuracy matters more than raw speed: 98% or higher is often expected.</p>
<h2>Converting WPM to keystrokes per hour</h2><p>One "word" is 5 keystrokes, so KPH ≈ WPM × 5 × 60. For example, 35 WPM ≈ 10,500 KPH.</p>
<h2>Tips</h2><ul><li>Use the number pad (10-key) if your keyboard has one: it's much faster for numbers.</li><li>Rest your right hand on 4-5-6, with your middle finger on the 5 (it has a bump).</li><li>Slow down if your accuracy drops below 98%.</li></ul>""",
        [("How long is a typical data entry test?", "Usually 3–5 minutes. This practice test runs for 3 minutes."),
         ("Do employers accept online results?", "Some employers accept a certificate as proof of practice, but most run their own test. Use this to prepare."), SAVED], ui={"mode": False, "dur": False})

    add("typing-test-for-jobs", "💼", "Typing Test for Jobs", "Typing Test for Jobs – Practice Employment Typing Test (5 Min)",
        "Prepare for employment typing tests. Take a 5-minute typing test with real sentences, see your WPM and accuracy, and get a certificate for your resume.",
        "Typing Test <span>for Jobs</span>", "A 5-minute test with real sentences, like the tests employers use.",
        "test", {"dur": 300, "mode": "sentences", "lockMode": True, "lockDur": True},
        """<h2>What typing speed do jobs require?</h2><table><thead><tr><th>Job</th><th>Typical requirement</th></tr></thead><tbody>
<tr><td>Customer service / call center</td><td>30–45 WPM</td></tr><tr><td>Administrative assistant / receptionist</td><td>40–60 WPM</td></tr>
<tr><td>Data entry clerk</td><td>40+ WPM, 98% accuracy</td></tr><tr><td>Legal or medical secretary</td><td>60–75 WPM</td></tr>
<tr><td>Transcriptionist</td><td>65–80+ WPM</td></tr></tbody></table>
<h2>How employment typing tests work</h2><p>Most employers use a 1–5 minute test with sentences or paragraphs, and report net WPM (speed after subtracting errors) plus accuracy. Some subtract a word for each mistake, so accuracy matters as much as speed.</p>
<h2>Should I put my typing speed on my resume?</h2><p>Yes, if it's relevant to the job and above about 50 WPM. Write it like "Typing: 65 WPM, 98% accuracy".</p>""",
        [("How can I improve before a job test?", "Practice 10–15 minutes daily for a couple of weeks, focusing on accuracy first. Our typing lessons help if you still look at the keyboard."), CERT], ui={"mode": False, "dur": False})

    add("typing-test-for-beginners", "🌱", "Beginner Typing Test", "Typing Test for Beginners – Easy Free Typing Speed Test",
        "An easy typing test for beginners with short, common words. Find your starting WPM, then improve with free typing lessons.",
        "Typing Test <span>for Beginners</span>", "Short, simple words to find your starting speed. No pressure!",
        "test", {"dur": 60, "mode": "kids", "lockMode": True},
        """<h2>Just getting started?</h2><p>This test uses short, easy words so you can focus on finding the keys. Don't worry about your score: most beginners type 10–25 WPM. What matters is that you improve each week.</p>
<h2>Your first steps to faster typing</h2><ol><li>Learn the home row: left fingers on A S D F, right fingers on J K L ;.</li><li>Take the free <a href="typing-lessons">typing lessons</a> to learn each row of the keyboard.</li><li>Practice a little every day: 10 minutes daily beats an hour once a week.</li><li>Take this test once a week to see your progress.</li></ol>""",
        [("How long until I can type 40 WPM?", "With daily practice, many beginners go from hunt-and-peck to 30–40 WPM in one to three months."), CERT, SAVED], ui={"mode": False})

    add("wpm-test", "🚀", "WPM Test", "WPM Test – Check Your Words Per Minute Free",
        "Free WPM test. Find out how many words per minute you type, with accuracy, raw speed and a chart of your speed during the test.",
        "WPM <span>Test</span>", "Find your words per minute in 60 seconds.", "test", {"dur": 60},
        """<h2>What does WPM mean?</h2><p>WPM stands for <b>words per minute</b>, the standard measure of typing speed. To make tests fair, a "word" is counted as any 5 characters, including spaces. So typing 250 correct characters in one minute is 50 WPM.</p>
<h2>Net WPM vs gross WPM</h2><p><b>Gross (raw) WPM</b> counts everything you typed. <b>Net WPM</b> only counts correct words, so mistakes lower it. This test shows both, plus your accuracy.</p>
<h2>WPM vs CPM</h2><p>Some tests show characters per minute (CPM). To convert, divide CPM by 5: 300 CPM = 60 WPM.</p>""",
        [("What's the world record WPM?", "Top competitive typists have recorded bursts over 200 WPM on short tests. For long passages, sustained speeds of 150+ WPM have been verified."), CERT, SAVED])

    add("typing-certificate", "📜", "Typing Certificate", "Free Typing Certificate – Take a Test & Download Your Certificate",
        "Get a free typing certificate. Take a typing test, then download a certificate with your name, WPM and accuracy. Great for students and job seekers.",
        "Free Typing <span>Certificate</span>", "Take the test, then click Get certificate to download yours.", "test", {"dur": 60},
        """<h2>How to get your typing certificate</h2><ol><li>Choose a test length. One minute is the most common.</li><li>Take the test. Try to keep accuracy above 90%.</li><li>Click <b>Get certificate</b>, type your name and download or print it.</li></ol>
<h2>Who uses typing certificates?</h2><p>Teachers give them to students as rewards, job seekers include them with applications, and they're a fun way to celebrate a personal best. The certificate shows your WPM, accuracy, test length and date.</p>
<h2>Is it an official certificate?</h2><p>It's a free certificate of your result, not an accredited qualification. Some employers accept it as evidence of practice; others run their own test.</p>""",
        [("Does the certificate cost anything?", "No, it's completely free with no watermark or sign-up."), SAVED])

    add("how-to-type-faster", "💡", "How to Type Faster", "How to Type Faster – 10 Proven Tips to Increase Your WPM",
        "Learn how to type faster with 10 practical tips, from posture and touch typing to practice routines. Then test your speed for free.",
        "How to <span>Type Faster</span>", "Ten proven tips, then a quick test to measure your speed.", "test", {"dur": 60},
        """<h2>10 tips to type faster</h2><ol>
<li><b>Learn touch typing.</b> Not looking at the keyboard is the biggest speed boost there is. Start with our free <a href="typing-lessons">lessons</a>.</li>
<li><b>Use the home row.</b> Return your fingers to A S D F and J K L ; after every key.</li>
<li><b>Use the right finger for each key.</b> It feels slower at first but pays off quickly.</li>
<li><b>Accuracy first.</b> Speed comes from smooth, correct typing. Every Backspace costs time.</li>
<li><b>Read ahead.</b> Look at the next word while finishing the current one.</li>
<li><b>Sit well.</b> Feet flat, back straight, elbows at about 90°, wrists floating rather than resting.</li>
<li><b>Type in a rhythm.</b> An even beat is faster than bursts and pauses.</li>
<li><b>Practice daily.</b> 10–15 minutes a day beats long, rare sessions.</li>
<li><b>Practice your weak keys.</b> Notice which letters slow you down and drill words that use them.</li>
<li><b>Use a comfortable keyboard.</b> Keys with a clear feel and good spacing reduce mistakes.</li></ol>
<h2>How fast can you improve?</h2><p>Most people gain 5–10 WPM in the first month of regular practice. Track your progress by taking the test above once a week.</p>""",
        [("Is it worth learning touch typing as an adult?", "Yes. Your speed may drop for a week or two while you switch, but most adults end up much faster than before."), SAVED])

    # ---- more pages (Nov 20) ----
    MORE = [
        ("typing-speed-test", "⚡", "Typing Speed Test", "Typing Speed Test – Free 1 Minute WPM & Accuracy Test",
         "Free typing speed test. Find your words per minute and accuracy in one minute, see a live speed chart and get a free certificate.",
         "Typing <span>Speed Test</span>", "How fast do you type? Start typing to begin the one-minute test.", {"dur": 60}, None,
         f"""<h2>How the typing speed test works</h2><p>Type the words shown as fast and accurately as you can. When the timer ends, you'll see your words per minute (WPM), accuracy, raw speed and a chart of your speed during the test.</p>
<h2>Typing speed chart</h2>{WPM_TABLE}
<h2>Get a reliable result</h2><p>Take the test three times and use your average. Your first try is often slower while you warm up.</p>""",
         [("How is typing speed measured?", "In words per minute, where every 5 characters (including spaces) count as one word. Wrong words don't count."), CERT, SAVED]),
        ("touch-typing-test", "🙌", "Touch Typing Test", "Touch Typing Test – Test Your Speed Without Looking",
         "Free touch typing test. Check your speed and accuracy typing without looking at the keyboard, and see how touch typing compares with hunt-and-peck.",
         "Touch <span>Typing Test</span>", "Keep your eyes on the screen and your fingers on the home row.", {"dur": 60}, None,
         """<h2>What is touch typing?</h2><p>Touch typing means typing without looking at the keyboard, using all ten fingers. Each finger is responsible for its own keys, starting from the home row: <b>A S D F</b> for the left hand and <b>J K L ;</b> for the right. The bumps on F and J help you find the home row by feel.</p>
<h2>Touch typing vs hunt and peck</h2><p>Hunt-and-peck typists usually top out around 25–40 WPM. Touch typists commonly reach 60–80 WPM and are more accurate, because their eyes stay on the text.</p>
<h2>Learn touch typing</h2><p>Start with our free <a href="typing-lessons">typing lessons</a>, one row at a time. It feels slow for the first week, then speed builds quickly.</p>""",
         [("Can I cover my hands for the test?", "Yes. Some people put a cloth over their hands to stop peeking. It's a great way to practice."), CERT, SAVED]),
        ("typing-practice", "🎯", "Typing Practice", "Typing Practice – Free Online Typing Practice with Instant Feedback",
         "Free online typing practice. Type real words, get instant feedback on speed and mistakes, and track your progress every day.",
         "Typing <span>Practice</span>", "Practice daily and watch your speed go up. Pick a length and start typing.", {"dur": 120}, None,
         """<h2>A simple daily practice routine</h2><ol><li><b>Warm up (2 min):</b> a short test at a relaxed pace, focusing on accuracy.</li><li><b>Drill (5 min):</b> a <a href="typing-lessons">typing lesson</a> on the keys that slow you down.</li><li><b>Push (3 min):</b> a timed test where you try to beat yesterday's score.</li></ol>
<h2>Track your progress</h2><p>Your best scores and recent results are saved in your browser. Most people gain 5–10 WPM in the first month of 10 minutes a day.</p>""",
         [("How long should I practice each day?", "10–15 minutes of focused practice is enough. Short daily sessions beat long weekly ones."), SAVED]),
        ("sentence-typing-test", "📝", "Sentence Typing Test", "Sentence Typing Test – Type Real Sentences (Free WPM Test)",
         "Free sentence typing test. Type real sentences with capitals and punctuation and measure your WPM and accuracy, just like real-world writing.",
         "Sentence <span>Typing Test</span>", "Type full sentences with capitals and punctuation.", {"dur": 60, "mode": "sentences", "lockMode": True}, {"mode": False},
         """<h2>Why type sentences?</h2><p>Random word tests are great for raw speed, but real typing is full sentences. Sentences add capitals, commas and periods, and they're easier to read ahead, so they're a more realistic measure of how you type emails and documents.</p>
<h2>Tips</h2><ul><li>Read a few words ahead so your fingers never wait.</li><li>Use the opposite hand's Shift key for capitals.</li><li>Don't pause at the end of a sentence; keep your rhythm going.</li></ul>""",
         [("Is my WPM lower on sentences?", "A little, usually. Capitals and punctuation take extra movement. It's normal to be 5–10 WPM slower than on plain words."), CERT, SAVED]),
        ("10-key-typing-test", "🔢", "10 Key Typing Test", "10 Key Typing Test – Free Number Pad Speed Test (KPH)",
         "Free 10-key typing test. Practice typing numbers on the number pad and measure your speed and accuracy for data entry and accounting jobs.",
         "10 Key <span>Typing Test</span>", "Use your number pad and type the numbers as fast as you can.", {"dur": 180, "mode": "numbers", "lockMode": True}, {"mode": False},
         """<h2>What is a 10-key test?</h2><p>A 10-key test measures how fast and accurately you type numbers on the numeric keypad. It's common for data entry, accounting, bookkeeping, banking and medical billing jobs. Results are often shown in <b>keystrokes per hour (KPH)</b>.</p>
<h2>10-key speeds</h2><ul><li><b>Under 6,000 KPH:</b> beginner.</li><li><b>8,000–10,000 KPH:</b> a common job requirement.</li><li><b>12,000+ KPH:</b> fast and experienced.</li></ul><p>To estimate KPH from this test: WPM × 5 × 60.</p>
<h2>Finger placement</h2><p>Rest your right index finger on 4, middle on 5 (feel for the bump) and ring finger on 6. Your thumb presses 0 and your pinky handles Enter and +.</p>""",
         [("Can I take it without a number pad?", "Yes, using the number row, but it will be slower. A cheap USB number pad helps a lot if you're training for a job."), SAVED]),
        ("accuracy-typing-test", "✅", "Accuracy Typing Test", "Typing Accuracy Test – Check How Accurately You Type",
         "Free typing accuracy test. See your accuracy percentage, error count and net WPM, and learn how to make fewer mistakes when you type.",
         "Typing <span>Accuracy Test</span>", "Focus on getting every word right, then check your accuracy score.", {"dur": 60}, None,
         """<h2>What's a good typing accuracy?</h2><ul><li><b>Below 90%:</b> slow down; mistakes are costing you speed.</li><li><b>92–95%:</b> average.</li><li><b>96–98%:</b> good, and what most employers look for.</li><li><b>99%+:</b> excellent.</li></ul>
<h2>Why accuracy matters more than speed</h2><p>Every mistake costs extra keystrokes to fix, and job tests often subtract errors from your score. Typists who slow down slightly and stay accurate usually end up with a higher net WPM.</p>
<h2>How to improve accuracy</h2><ul><li>Type at about 80% of your top speed for a week.</li><li>Watch the screen, not your hands.</li><li>Notice which keys you miss most and drill them in the <a href="typing-lessons">lessons</a>.</li></ul>""",
         [("How is accuracy calculated?", "Correct characters divided by total characters typed, as a percentage."), CERT, SAVED]),
        ("typing-test-for-students", "🎓", "Typing Test for Students", "Typing Test for Students – Free WPM Test for School",
         "Free typing test for students. Check your WPM and accuracy, practice for school typing assignments and print a certificate for your teacher.",
         "Typing Test <span>for Students</span>", "Take the test, then print your certificate to show your teacher.", {"dur": 60}, None,
         """<h2>Typing speeds by grade (rough guide)</h2><ul><li><b>Grades 3–5:</b> 10–25 WPM.</li><li><b>Grades 6–8:</b> 20–35 WPM.</li><li><b>High school:</b> 30–45 WPM.</li><li><b>College:</b> 40+ WPM makes essays and notes much faster.</li></ul>
<h2>Why typing matters in school</h2><p>Most homework, tests and essays are typed now. Faster typing means less time spent on assignments and more focus on what you're writing.</p>
<h2>For teachers</h2><p>No sign-up is needed, results stay on each student's device, and the certificate is free to print. Younger students can use the <a href="typing-test-for-kids">kids typing test</a>.</p>""",
         [("Is it free for classrooms?", "Yes, it's completely free with no accounts, so it works on school Chromebooks right away."), CERT, SAVED]),
        ("typing-test-for-programmers", "💻", "Typing Test for Programmers", "Typing Test for Programmers – Numbers, Symbols & Punctuation",
         "Free typing test for programmers. Practice punctuation, numbers and capitals and measure your WPM and accuracy on a harder mix of keys.",
         "Typing Test <span>for Programmers</span>", "A harder mix with numbers and punctuation. Coders use these keys all day.", {"dur": 60, "mode": "words", "punc": True, "nums": True, "lockMode": True}, {"mode": False},
         """<h2>Why programmers should practice symbols</h2><p>Code is full of brackets, semicolons, quotes, numbers and capitals. Typing them without looking saves time and keeps you focused on the problem instead of the keyboard.</p>
<h2>Tips</h2><ul><li>Learn which finger owns each symbol: the right pinky handles ; ' / [ ] and Enter.</li><li>Use the opposite Shift key to avoid twisting your hand.</li><li>Practice the number row. Many developers reach for it with the wrong finger.</li></ul>
<h2>Does typing speed matter for coding?</h2><p>Thinking is the slow part of programming, but fast, accurate typing removes friction, especially when writing tests, docs and messages.</p>""",
         [("What WPM do programmers type?", "Many developers type 50–80 WPM on plain text. Expect lower scores on symbol-heavy tests."), CERT, SAVED]),
        ("cpm-typing-test", "🔤", "CPM Typing Test", "CPM Typing Test – Characters Per Minute Speed Test",
         "Free characters per minute (CPM) typing test. Measure your typing speed in CPM and WPM and see how they convert.",
         "CPM <span>Typing Test</span>", "Measure your speed in characters per minute. Your WPM × 5 = CPM.", {"dur": 60}, None,
         """<h2>What is CPM?</h2><p>CPM stands for <b>characters per minute</b>. It counts every letter, number, space and punctuation mark you type. Some countries and employers use CPM (or keystrokes per minute) instead of WPM.</p>
<h2>CPM to WPM</h2><p>A standard word is 5 characters, so <b>WPM = CPM ÷ 5</b>. 200 CPM = 40 WPM, 300 CPM = 60 WPM and 400 CPM = 80 WPM.</p>
<h2>What's a good CPM?</h2><p>About 200 CPM is average, 300 CPM is good for most office jobs and 400+ CPM is fast.</p>""",
         [("Where do I see my CPM?", "Multiply the WPM shown after the test by 5. Raw WPM × 5 gives your raw CPM, including mistakes."), CERT, SAVED]),
        ("home-row-keys", "🏠", "Home Row Keys", "Home Row Keys – Learn the Home Row & Test Your Typing",
         "Learn the home row keys (ASDF JKL;), where each finger goes, and why the home row is the key to touch typing. Then test your speed.",
         "Home Row <span>Keys</span>", "Put your fingers on A S D F and J K L ; then try the test.", {"dur": 60, "mode": "kids", "lockMode": True}, {"mode": False},
         """<h2>What are the home row keys?</h2><p>The home row is the middle row of letters on the keyboard. In touch typing, your fingers rest there between keystrokes:</p><ul><li><b>Left hand:</b> pinky on A, ring on S, middle on D, index on F.</li><li><b>Right hand:</b> index on J, middle on K, ring on L, pinky on ;.</li><li><b>Thumbs:</b> on the spacebar.</li></ul>
<h2>Why do F and J have bumps?</h2><p>The small ridges on F and J let you find the home row by feel, so you never have to look down.</p>
<h2>Next steps</h2><p>Once the home row feels natural, move on to the top and bottom rows in our free <a href="typing-lessons">typing lessons</a>.</p>""",
         [("Why is it called the home row?", "Because your fingers return 'home' to it after every key you press."), SAVED]),
    ]
    for slug, emo, name, title, desc, h1, sub, cfg, ui, content, faq in MORE:
        if ui is None:
            add(slug, emo, name, title, desc, h1, sub, "test", cfg, content, faq)
        else:
            add(slug, emo, name, title, desc, h1, sub, "test", cfg, content, faq, ui=ui)
