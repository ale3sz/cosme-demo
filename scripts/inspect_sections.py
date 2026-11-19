import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check section order
print("Original section positions:")
for match in re.finditer(r'<section\s+[^>]*id=["\']([^"\']+)["\']', html):
    print(f"- {match.group(1)} at pos {match.start()}")
