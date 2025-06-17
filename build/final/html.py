import os

# Read raw pi digits from file (assuming all on one line or many lines)
with open("pi_output.txt", "r") as f:
    digits = f.read().replace("\n", "").strip()

# Sanitize: remove leading 3. if included, and preserve it separately
if digits.startswith("3."):
    digits = digits[2:]
elif digits.startswith("3"):
    digits = digits[1:]

# Split into lines of 1000 characters
lines = [digits[i:i+1000] for i in range(0, len(digits), 1000)]

# Build HTML content
html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Pi Digits Viewer</title>
  <style>
    body {{ font-family: monospace; background: #fdfdfd; color: #222; margin: 2em; }}
    #searchBox {{ padding: 0.5em; font-size: 1em; width: 50%; margin-bottom: 1em; }}
    #digits {{ overflow-y: scroll; max-height: 70vh; white-space: pre; border: 1px solid #ccc; padding: 1em; background: #fff; }}
    .line {{ line-height: 1.6; }}
    .line-number {{ color: #999; display: inline-block; width: 5em; }}
    h1 {{ margin-bottom: 0.2em; }}
  </style>
</head>
<body>
  <h1>π Viewer</h1>
  <p>First {} digits of Pi (excluding the '3.').</p>
  <p><b>3.</b> is shown before the digits below.</p>

  <input type="text" id="searchBox" placeholder="Search digits..." oninput="searchDigits()">
  <div id="digits">
    <div><b>3.</b></div>
""".format(len(digits))

# Append digits line by line
for idx, line in enumerate(lines, start=1):
    html += f'    <div class="line"><span class="line-number">{idx:5}</span> {line}</div>\n'

# Pi trivia and JS
html += """
  </div>
  <h2>π Trivia</h2>
  <ul>
    <li>π is irrational: its digits never end or repeat.</li>
    <li>The first 10 digits of π are 3.141592653.</li>
    <li>In 2025, π was calculated to over 300 trillion digits by Linus Media Group.</li>
  </ul>

  <script>
    function searchDigits() {
      const term = document.getElementById("searchBox").value;
      const lines = document.querySelectorAll(".line");
      lines.forEach(line => {
        if (term === "" || line.textContent.includes(term)) {
          line.style.display = "block";
        } else {
          line.style.display = "none";
        }
      });
    }
  </script>
</body>
</html>
"""

# Save HTML
with open("pi.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ pi.html generated successfully.")