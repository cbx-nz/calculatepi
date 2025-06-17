def make_html_from_pi(pi_text_path, output_html_path="pi.html"):
    with open(pi_text_path, "r") as f:
        lines = f.readlines()

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pi Digits Viewer</title>
    <style>
        body {
            background: #0d0d0d;
            color: #00ff88;
            font-family: monospace;
            padding: 20px;
        }
        h1, h2 {
            color: #00ffaa;
        }
        #viewer {
            max-height: 600px;
            overflow-y: auto;
            border: 1px solid #00ffaa;
            padding: 10px;
            background: #111;
            margin-top: 10px;
        }
        .line {
            display: flex;
        }
        .linenum {
            width: 80px;
            color: #888;
        }
        .digits {
            white-space: pre-wrap;
            word-break: break-word;
            flex: 1;
        }
        #search {
            margin-bottom: 10px;
            padding: 5px;
            width: 300px;
            font-family: monospace;
            background: #1a1a1a;
            color: #00ff88;
            border: 1px solid #00ffaa;
        }
        mark {
            background: #ff0;
            color: black;
        }
    </style>
</head>
<body>
    <h1>Digits of π</h1>
    <input type="text" id="search" placeholder="Search digits (e.g. 14159)">
    <div id="trivia">
        <h2>π Trivia</h2>
        <ul>
            <li>π is an irrational number: it never ends and never repeats.</li>
            <li>The world record for digits memorized is over 70,000.</li>
            <li>π appears in circles, waves, quantum physics, statistics, and probability.</li>
            <li>π has been calculated to over 100 trillion digits with modern supercomputers.</li>
        </ul>
    </div>
    <div id="viewer">
"""

    for i, line in enumerate(lines):
        linenum = i * 1000 + 1
        html += f'        <div class="line"><div class="linenum">{linenum:,}</div><div class="digits">{line.strip()}</div></div>\n'

    html += """    </div>

    <script>
        const searchBox = document.getElementById('search');
        searchBox.addEventListener('input', () => {
            const term = searchBox.value;
            const digits = document.querySelectorAll('.digits');
            digits.forEach(el => {
                const raw = el.textContent;
                if (!term) {
                    el.innerHTML = raw;
                } else {
                    const regex = new RegExp(term, 'gi');
                    el.innerHTML = raw.replace(regex, match => `<mark>${match}</mark>`);
                }
            });
        });
    </script>
</body>
</html>"""

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ pi.html generated with {len(lines)} lines and search-enabled display.")


# Run this function directly if script is executed
if __name__ == "__main__":
    make_html_from_pi("pi_output.txt", "pi.html")