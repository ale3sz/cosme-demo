with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start = None
for i, l in enumerate(lines):
    if 'id="canillas"' in l:
        start = i
        break

if start is not None:
    print("Found canillas at line:", start + 1)
    for j in range(start, min(len(lines), start + 250)):
        if 'beer-tap-card' in lines[j] or 'TAP #' in lines[j]:
            print(f"{j+1}: {lines[j].strip()[:80]}")
