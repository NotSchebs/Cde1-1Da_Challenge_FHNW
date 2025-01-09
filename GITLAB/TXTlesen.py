# TXT-Datei lesen
variablen = {}
with open('variablen.txt', 'r') as file:
    for line in file:
        # Leerzeilen und Kommentare ignorieren
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        # Zeile in Schlüssel und Wert aufteilen
        key, value = line.split('=', 1)
        variablen[key] = value

# Variablen anzeigen
print(variablen)

# Zugriff auf spezifische Variablen
route = variablen.get('route', None)
print(f"Route: {route}")

# Beispiel: Konvertiere 'httpadresse' in einen Integer, falls möglich
httpadresse = variablen.get('httpadresse', None)
if httpadresse and httpadresse.isdigit():
    httpadresse = int(httpadresse)
print(f"HTTP-Adresse: {httpadresse}")
