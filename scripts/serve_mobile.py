import subprocess
import re
import time
import sys
import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
import socket

PORT = 8080

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

if not is_port_in_use(PORT):
    print(f"Iniciando servidor local HTTP en puerto {PORT}...")
    class SilentHandler(SimpleHTTPRequestHandler):
        def log_message(self, *args): pass
    
    server = HTTPServer(('127.0.0.1', PORT), SilentHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    time.sleep(1)
    print("Servidor HTTP listo.")

cf_bin = os.path.abspath('scripts/cloudflared.exe')
if not os.path.exists(cf_bin):
    print("Error: cloudflared.exe no encontrado en", cf_bin)
    sys.exit(1)

print("Iniciando tunel Cloudflare sobre http://127.0.0.1:8080...")
proc = subprocess.Popen(
    [cf_bin, 'tunnel', '--url', f'http://127.0.0.1:{PORT}'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1
)

public_url = None
start_time = time.time()

while time.time() - start_time < 25:
    line = proc.stderr.readline()
    if not line:
        continue
    sys.stdout.write(line)
    sys.stdout.flush()
    match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
    if match:
        public_url = match.group(0)
        break

if not public_url:
    print("No se pudo obtener URL de Cloudflare a tiempo.")
    proc.terminate()
    sys.exit(1)

print("\n" + "=" * 65)
print("🚀 ENLACE PÚBLICO ACTIVO PARA VER EN EL CELULAR:")
print(f"👉 {public_url}")
print("=" * 65 + "\n")

with open('mobile_preview_url.txt', 'w', encoding='utf-8') as f:
    f.write(public_url)

try:
    while True:
        line = proc.stderr.readline()
        if not line and proc.poll() is not None:
            break
        time.sleep(1)
except KeyboardInterrupt:
    proc.terminate()
