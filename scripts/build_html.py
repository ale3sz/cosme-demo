# -*- coding: utf-8 -*-
import os
import re
import sys
import time

def resolve_includes(content, depth=0):
    if depth > 5:
        print("Advertencia: Límite de recursión de includes alcanzado (posible ciclo).")
        return content

    pattern = re.compile(r'<!--\s*@include:([^\s>]+)\s*-->')

    def replace_include(match):
        rel_path = match.group(1).strip()
        if os.path.exists(rel_path):
            with open(rel_path, 'r', encoding='utf-8') as f_inc:
                inc_text = f_inc.read().strip()
                # Resolver inclusiones recursivas anidadas
                return resolve_includes(inc_text, depth + 1)
        else:
            print(f"Advertencia: Archivo incluido no encontrado: {rel_path}")
            return f"<!-- Error: {rel_path} no encontrado -->"

    return pattern.sub(replace_include, content)

def build():
    template_path = 'index.template.html'
    output_path = 'index.html'

    if not os.path.exists(template_path):
        print(f"Error: {template_path} no encontrado.")
        return False

    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    compiled = resolve_includes(content)

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        f.write(compiled)

    lines = len(compiled.splitlines())
    print(f"[{time.strftime('%H:%M:%S')}] ✓ index.html compilado con éxito ({lines} líneas).")
    return True

def watch():
    print("Iniciando watcher de componentes (Ctrl+C para salir)...")
    build()
    
    watched_dirs = ['components']
    watched_files = ['index.template.html']
    
    last_mtimes = {}

    def get_mtimes():
        mtimes = {}
        for f in watched_files:
            if os.path.exists(f):
                mtimes[f] = os.path.getmtime(f)
        for d in watched_dirs:
            if os.path.exists(d):
                for root, _, files in os.walk(d):
                    for file in files:
                        full_path = os.path.join(root, file)
                        mtimes[full_path] = os.path.getmtime(full_path)
        return mtimes

    last_mtimes = get_mtimes()

    try:
        while True:
            time.sleep(0.5)
            current_mtimes = get_mtimes()
            if current_mtimes != last_mtimes:
                last_mtimes = current_mtimes
                print("Cambio detectado en componentes...")
                build()
    except KeyboardInterrupt:
        print("\nWatcher detenido.")

if __name__ == '__main__':
    if '--watch' in sys.argv:
        watch()
    else:
        build()
