import os
import requests
from dotenv import load_dotenv

# Toto načíta všetky premenné z tvojho .env súboru do pamäte
load_dotenv()

# Získame kľúč. Ak v .env nie je, vráti None.
ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")


def check_ip_abuse(ip):
    """Skontroluje IP adresu voči AbuseIPDB a vráti skóre hrozby (0-100)."""

    # Skontrolujeme, či kľúč existuje, či nie je prázdny, alebo či nezostal starý text
    if not ABUSEIPDB_API_KEY or ABUSEIPDB_API_KEY == "TVOJ_API_KLUC_SEM":
        print(f"  [!] Preskakujem kontrolu hrozieb: API kľúč nie je nastavený.")
        return 0

    url = 'https://api.abuseipdb.com/api/v2/check'
    querystring = {'ipAddress': ip, 'maxAgeInDays': '90'}
    headers = {
        'Accept': 'application/json',
        'Key': ABUSEIPDB_API_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)

        # Pridal som sem aj kontrolu chýb (napr. ak by bol kľúč neplatný, API vráti kód 401)
        if response.status_code != 200:
            print(f"  [!] Chyba API (kód {response.status_code}): Pravdepodobne zlý kľúč v .env")
            return 0

        data = response.json()
        return data['data']['abuseConfidenceScore']
    except Exception as e:
        print(f"  [!] Chyba pripojenia k AbuseIPDB: {e}")
        return 0