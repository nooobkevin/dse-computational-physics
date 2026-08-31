#!/usr/bin/env bash
#
# make_handouts.sh — build print-ready A4 HTML handouts from every unit's
# lesson_handout.md.
#
# For each units/*/lesson_handout.md this produces units/*/lesson_handout.html,
# a self-contained A4 page (inline CSS with @page A4 margins, a CJK font stack,
# and table styling; no external assets).
#
# Renderer selection:
#   * pandoc  — used when `command -v pandoc` succeeds (preferred; handles
#               tables and LaTeX-style math well).
#   * python3 — tiny fallback that wraps the markdown in a styled HTML template
#               (keeps code blocks and tables passable).
#
# PDF is OUT OF SCOPE: the generated HTML is the print-to-PDF deliverable.
# Open the HTML in a browser and "Print to PDF" (A4) to get the handout.
# No Docker is required.
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Shared inline CSS: A4 @page, CJK font stack, table styling.
read -r -d '' CSS <<'CSS' || true
@page { size: A4; margin: 14mm 14mm 16mm 14mm; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body {
  font-family: "PingFang HK", "PingFang TC", "Microsoft JhengHei",
               "Noto Sans CJK TC", "Noto Sans TC", "Heiti TC",
               "Hiragino Sans GB", "Source Han Sans TC", sans-serif;
  font-size: 10.5pt; line-height: 1.45; color: #1a1a1a; margin: 0;
}
h1 { font-size: 16pt; margin: 0 0 2pt 0; color: #0b3d66; }
h2 { font-size: 12pt; margin: 10pt 0 3pt 0; color: #0b3d66;
     border-bottom: 1.5px solid #0b3d66; padding-bottom: 1pt; }
h3 { font-size: 11pt; margin: 7pt 0 2pt 0; color: #14507a; }
p  { margin: 3pt 0; }
ul, ol { margin: 3pt 0 3pt 0; padding-left: 16pt; }
li { margin: 1pt 0; }
table { border-collapse: collapse; width: 100%; margin: 4pt 0; font-size: 9.5pt; }
th, td { border: 1px solid #b9c6d2; padding: 2pt 5pt; text-align: left; vertical-align: top; }
th { background: #e8eef4; color: #0b3d66; }
tr:nth-child(even) td { background: #f6f9fb; }
code { font-family: "SF Mono", Menlo, Consolas, "Courier New", monospace;
       font-size: 9pt; background: #f0f2f5; padding: 0 2pt; border-radius: 2pt; }
pre { background: #f0f2f5; border: 1px solid #d5dbe2; border-radius: 3pt;
      padding: 5pt 7pt; overflow-x: auto; font-size: 9pt; }
pre code { background: none; padding: 0; }
CSS

# Write the CSS to a temp file for pandoc's -c / --embed-resources.
CSS_FILE="$(mktemp)"
trap 'rm -f "$CSS_FILE"' EXIT
printf '%s\n' "$CSS" > "$CSS_FILE"

count=0
renderer=""

if command -v pandoc >/dev/null 2>&1; then
  renderer="pandoc"
  for md in units/*/lesson_handout.md; do
    [ -e "$md" ] || continue
    out="${md%.md}.html"
    pandoc -s --embed-resources -c "$CSS_FILE" \
      --metadata title="DSE Computational Physics — Lesson Handout" \
      -o "$out" "$md"
    count=$((count + 1))
  done
else
  renderer="python3 fallback"
  for md in units/*/lesson_handout.md; do
    [ -e "$md" ] || continue
    out="${md%.md}.html"
    CSS="$CSS" python3 - "$md" "$out" <<'PY'
import html, re, sys

css = __import__("os").environ["CSS"]
src, dst = sys.argv[1], sys.argv[2]
lines = open(src, encoding="utf-8").read().splitlines()

def esc(s):
    return html.escape(s, quote=False)

out = []
i = 0
in_code = False
code_buf = []
in_table = False
table_rows = []

def flush_table():
    global table_rows
    if not table_rows:
        return
    out.append("<table>")
    for r, cells in enumerate(table_rows):
        tag = "th" if r == 0 else "td"
        out.append("<tr>" + "".join(f"<{tag}>{c}</{tag}>" for c in cells) + "</tr>")
    out.append("</table>")
    table_rows = []

while i < len(lines):
    line = lines[i]
    if line.startswith("```"):
        if in_code:
            out.append("<pre><code>" + esc("\n".join(code_buf)) + "</code></pre>")
            code_buf = []
            in_code = False
        else:
            flush_table()
            in_code = True
        i += 1
        continue
    if in_code:
        code_buf.append(line)
        i += 1
        continue
    if line.strip() == "":
        flush_table()
        out.append("")
        i += 1
        continue
    if line.lstrip().startswith("|") and line.rstrip().endswith("|"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if re.fullmatch(r":?-{2,}:?", cells[0].strip()) and len(cells) > 1:
            i += 1
            continue  # separator row
        table_rows.append(cells)
        i += 1
        continue
    flush_table()
    m = re.match(r"^(#{1,6})\s+(.*)$", line)
    if m:
        lvl = len(m.group(1))
        out.append(f"<h{lvl}>{esc(m.group(2))}</h{lvl}>")
    elif re.match(r"^\s*[-*]\s+", line):
        out.append("<ul><li>" + esc(re.sub(r"^\s*[-*]\s+", "", line)) + "</li></ul>")
    elif re.match(r"^\s*\d+\.\s+", line):
        out.append("<ol><li>" + esc(re.sub(r"^\s*\d+\.\s+", "", line)) + "</li></ol>")
    else:
        out.append("<p>" + esc(line) + "</p>")
    i += 1
flush_table()
if in_code:
    out.append("<pre><code>" + esc("\n".join(code_buf)) + "</code></pre>")

body = "\n".join(out)
page = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<title>DSE Computational Physics — Lesson Handout</title>
<style>{css}</style>
</head>
<body>
{body}
</body>
</html>
"""
open(dst, "w", encoding="utf-8").write(page)
PY
    count=$((count + 1))
  done
fi

echo "Renderer: $renderer"
echo "Generated $count handout HTML file(s):"
for f in units/*/lesson_handout.html; do
  [ -e "$f" ] && echo "  - $f"
done