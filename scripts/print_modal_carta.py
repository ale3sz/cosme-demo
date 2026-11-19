import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'<div id="modal-carta"[\s\S]*?</div>\s*</div>\s*</div>', html)
if m:
    print(m.group(0))
