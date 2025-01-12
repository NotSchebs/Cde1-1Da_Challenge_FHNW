import configparser

class ConfigProfileManager:
    def __init__(self, ini_file, profile_file):
        """
        Initialisiert die ConfigProfileManager-Klasse mit den angegebenen Dateipfaden.

        :param ini_file: Pfad zur INI-Datei
        :param profile_file: Pfad zur Profil-TXT-Datei
        """
        self.ini_file = ini_file
        self.profile_file = profile_file
        self.config = configparser.ConfigParser()

    def load_profile_from_txt(self):
        """
        Lädt Profile aus einer TXT-Datei und bereitet die Daten für die INI-Datei auf.

        :return: Aufbereitete Profil-Daten als Zeichenkette
        """
        with open(self.profile_file, 'r') as file:
            lines = file.readlines()
        # Entferne Leerzeilen und bereinige Daten
        lines = [line.strip() for line in lines if line.strip()]
        # Kombiniere die Werte mit Semikolon für die Konfigurationsdatei
        return "; ".join(lines)

    def update_ini_profile(self):
        """
        Liest die INI-Datei, aktualisiert den 'profile'-Eintrag im 'simulation'-Abschnitt
        und speichert die Änderungen.
        """
        # Konfigurationsdatei einlesen
        self.config.read(self.ini_file)
        profile_data = self.load_profile_from_txt()

        # Aktualisiere den Wert für "profile" im Abschnitt "simulation"
        if 'simulation' not in self.config:
            self.config['simulation'] = {}
        self.config['simulation']['profile'] = profile_data

        # Änderungen speichern
        with open(self.ini_file, 'w') as configfile:
            self.config.write(configfile)

# Beispielverwendung:
# manager = ConfigProfileManager('config-switch.ini', 'profile.txt')
# manager.update_ini_profile()

