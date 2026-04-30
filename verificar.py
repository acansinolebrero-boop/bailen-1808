import os, re

html = open('/Users/bakinbardi/Desktop/bailen-1808/bailen-completo.html').read()

# Extraer función toFileName aproximando el mapeo
esp_dir = '/Users/bakinbardi/Desktop/bailen-1808/Fichas/España'
fra_dir = '/Users/bakinbardi/Desktop/bailen-1808/Fichas/Francia'

esp_files = set(os.listdir(esp_dir))
fra_files = set(os.listdir(fra_dir))

print(f"Fichas España: {len(esp_files)}")
print(f"Fichas Francia: {len(fra_files)}")

# Extraer unidades del HTML
units_esp = re.findall(r"\['([^']+)',\d+,\d+\]", html[:html.find("fra_")] if "fra_" in html else html)

# Buscar bloques ALL
all_match = re.search(r"const ALL=\{esp:\[(.*?)\],fra:\[(.*?)\]\}", html, re.DOTALL)
if not all_match:
    print("No se encontró ALL")
    exit()

def check_side(side_text, folder, files, side):
    names = re.findall(r"\['([^']+)',\d+,\d+\]", side_text)
    missing = []
    for name in names:
        # Buscar en mapeo espAbbr/fraAbbr del HTML
        found = any(name in f or name.replace(' ','_') in f for f in files)
        if not found:
            missing.append(name)
    return missing

esp_text, fra_text = all_match.group(1), all_match.group(2)
print("\n--- Verificando España ---")
for name in re.findall(r"\['([^']+)',\d+,\d+\]", esp_text):
    found = any(f.lower().replace('.png','') for f in esp_files if name.split(' ')[0].lower() in f.lower())
    if not found:
        print(f"  ⚠️  Sin vincular: {name}")

print("\n--- Verificando Francia ---")
for name in re.findall(r"\['([^']+)',\d+,\d+\]", fra_text):
    found = any(name.split(' ')[0].lower() in f.lower() for f in fra_files)
    if not found:
        print(f"  ⚠️  Sin vincular: {name}")

print("\nListo.")
