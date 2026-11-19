import urllib.request
import re

url = 'https://drive.google.com/drive/folders/1nQJKftaSDtPjgDU_UEiqetQnh72M2eEz'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# Match filename and nearby 33-char drive id
for filename in ['CARTA COSME ALBERDI', 'DESAYUNOS Y MERIENDAS']:
    idx = html.find(filename)
    if idx != -1:
        snippet = html[max(0, idx - 500): min(len(html), idx + 500)]
        print(f"=== SNIPPET FOR {filename} ===")
        # search for 28-40 char alphanumeric IDs (Google Drive file IDs)
        ids = re.findall(r'[a-zA-Z0-9_-]{28,35}', snippet)
        print("Possible IDs:", set(ids))
        print("Raw text snippet:\n", snippet[:300])
