import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

canillas_match = re.search(r'<!-- =+[\r\n\s]+3B\. PIZARRA DE CANILLAS[\s\S]*?<section id="canillas"[\s\S]*?</section>', html)
taps_inner = re.search(r'(<div class="taps-board">[\s\S]*?</div>\s*</div>)\s*</div>\s*</section>', canillas_match.group(0))
if not taps_inner:
    # Try finding the exact closing
    start = canillas_match.group(0).find('<div class="taps-board">')
    end = canillas_match.group(0).rfind('</div>\n      </div>\n    </section>')
    board = canillas_match.group(0)[start:end].strip()
    opens = board.count('<div')
    closes = board.count('</div>')
    print('Start to end:', opens, closes)
else:
    board = taps_inner.group(1).strip()
    print('Regex match:', board.count('<div'), board.count('</div>'))
