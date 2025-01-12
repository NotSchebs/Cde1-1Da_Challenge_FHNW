import configparser

class ConfigProfileManager:
    def __init__(self, ini_file, profile_file,input_company, input_container):
        """
        Initialisiert die ConfigProfileManager-Klasse mit den angegebenen Dateipfaden.

        :param ini_file: Pfad zur INI-Datei
        :param profile_file: Pfad zur Profil-TXT-Datei
        :param input_company: Eingabewert für die Firma
        :param input_container: Eingabewert für den Container
        """
        self.ini_file = ini_file
        self.profile_file = profile_file
        self.input_company = input_company
        self.input_container = input_container
        self.config = configparser.ConfigParser()

    def load_profile_from_txt(self):
        """
        Lädt Profile aus einer TXT-Datei im erwarteten Format (eine Zeile) und entfernt überflüssige Leerzeichen.
        Erwartetes Format: 0.0, 18, 88; 0.1, 18, 85; ...
        """
        with open(self.profile_file, 'r') as file:
            content = file.read()

        # Entferne überflüssige Leerzeichen (am Anfang und Ende der Datei)
        cleaned_content = content.strip()

        # Überprüfen, ob das Format korrekt ist
        if not cleaned_content or ";" not in cleaned_content:
            print("Fehler: Die Datei enthält keine gültigen Profildaten.")
            return ""

        # Entferne überflüssige Leerzeichen um jedes Segment
        entries = cleaned_content.split(";")
        formatted_entries = ["; ".join(entry.strip() for entry in entries)]

        # Rückgabe als sauber formatierter String
        return "; ".join(formatted_entries)

    def update_ini_profile(self):
        """
        Aktualisiert den 'profile'-Eintrag in der INI-Datei ohne zusätzliche Leerzeichen.
        """
        print(f"Lese INI-Datei: {self.ini_file}")
        self.config.read(self.ini_file)

        # Lade Profil-Daten aus der TXT-Datei
        profile_data = self.load_profile_from_txt()
        print(f"Geladene Profile-Daten: {profile_data}")

        if not profile_data:
            print("Fehler: Die Profile-Daten sind leer. Bitte prüfen Sie die Datei profile.txt.")
            return

        # Abschnitt 'simulation' erstellen, falls er nicht existiert
        if 'simulation' not in self.config:
            print("Abschnitt 'simulation' nicht gefunden, wird erstellt.")
            self.config['simulation'] = {}

        # Profil-Daten aktualisieren und sicherstellen, dass keine überflüssigen Leerzeichen vorhanden sind
        self.config['simulation']['profile'] = profile_data.strip()
        print(f"Profile-Daten in INI-Datei aktualisiert: {profile_data.strip()}")

        # Änderungen in der INI-Datei speichern
        try:
            with open(self.ini_file, 'w') as configfile:
                self.config.write(configfile)
            print(f"INI-Datei erfolgreich gespeichert: {self.ini_file}")
        except Exception as e:
            print(f"Fehler beim Speichern der INI-Datei: {e}")

    def update_ini_company(self):
        """
        Aktualisiert den 'company'-Eintrag im Abschnitt 'DEFAULT'.
        """
        self.config.read(self.ini_file)
        self.config['DEFAULT']['company'] = self.input_company

        with open(self.ini_file, 'w') as configfile:
            self.config.write(configfile)

    def update_ini_container(self):
        """
        Aktualisiert den 'container'-Eintrag im Abschnitt 'DEFAULT'.
        """
        self.config.read(self.ini_file)
        self.config['DEFAULT']['container'] = self.input_container

        with open(self.ini_file, 'w') as configfile:
            self.config.write(configfile)