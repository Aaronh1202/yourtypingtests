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
