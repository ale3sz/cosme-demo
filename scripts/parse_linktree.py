import urllib.request
import json
import re

url = 'https://linktr.ee/COSMEALBERDI'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
    
    match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
    if match:
        data = json.loads(match.group(1))
        page_props = data.get('props', {}).get('pageProps', {})
        print("Profile title:", page_props.get('pageTitle') or page_props.get('name'))
        print("Bio:", page_props.get('description'))
        links = page_props.get('links', [])
        print(f"Total links found: {len(links)}")
        for l in links:
            print(f"- Title: {l.get('title')}")
            print(f"  URL: {l.get('url')}")
            print(f"  Type: {l.get('type')}")
    else:
        print("NEXT_DATA not found. Searching for links directly in html...")
        # look for json inside body or script
        matches = re.findall(r'"title":"([^"]+)","url":"([^"]+)"', html)
        for t, u in matches:
            print(f"- {t} -> {u}")
except Exception as e:
    print("Error:", e)
