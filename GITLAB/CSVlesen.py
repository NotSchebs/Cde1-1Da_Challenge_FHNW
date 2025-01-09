import csv

# Beispiel: CSV-Datei mit Variablen (z. B. variablen.csv)
# Inhalt der Datei:
# name,wert
# variable1,10
# variable2,20
# variable3,30

# Datei öffnen und lesen
with open('variablen.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    variablen = {row['name']: row['wert'] for row in csv_reader}

# Variablen anzeigen
#print(variablen)

# Zugriff auf spezifische Variablen

var = variablen['route']
print(var)  # Gibt 'demo1' aus