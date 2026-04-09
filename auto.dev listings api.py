import requests
import csv
import time
import json

# ============================ KONFIGURATION ===============================
API_KEY = "sk_ad_rmkZvJcwP9FccFOyOo9A9j9a"

# Seiten-Parameter
MAX_PAGES = 100
# ==========================================================================

API_URL = "https://api.auto.dev/listings"
OUTPUT_FILE = 'mercedes_s_klasse_final.csv'

headers = {
    'x-api-key': API_KEY
}

all_vehicles = []
processed_vins = set()

try:
    if API_KEY == "IHR_API_SCHLÜSSEL" or not API_KEY:
        raise ValueError("API-Schlüssel wurde nicht in der Konfiguration festgelegt.")

    # Schleife für die Paginierung
    for page_num in range(1, MAX_PAGES + 1):
        # KORRIGIERTE PARAMETER: Exakte Schreibweise laut Dokumentationsbeispiel
        params = {
            'vehicle.make': 'Mercedes-Benz',  # Korrekte Großschreibung
            'vehicle.model': 'S-Class',  # Korrekte Großschreibung
            'page': page_num
        }

        print(f"Sende landesweite Anfrage für Seite {page_num}...")
        response = requests.get(API_URL, params=params, headers=headers)
        response.raise_for_status()

        data = response.json()
        vehicle_listings = data.get('results', [])

        if not vehicle_listings:
            print("Keine weiteren Fahrzeuge gefunden. Paginierung beendet.")
            break

        new_vehicles_found = 0
        for vehicle in vehicle_listings:
            vin = vehicle.get('vin')
            if vin and vin not in processed_vins:
                all_vehicles.append(vehicle)
                processed_vins.add(vin)
                new_vehicles_found += 1

        print(f"{new_vehicles_found} neue, einzigartige Fahrzeuge auf dieser Seite gefunden.")
        time.sleep(0.5)

    if not all_vehicles:
        print(
            "Es wurden keine Fahrzeuge für 'Mercedes-Benz S-Class' gefunden. Möglicherweise gibt es aktuell keine Listings unter diesem genauen Namen.")
    else:
        print(f"\nSuche abgeschlossen. Insgesamt {len(all_vehicles)} einzigartige Fahrzeuge gefunden.")
        print(f"Schreibe Daten in '{OUTPUT_FILE}'...")

        fieldnames = [
            'vin', 'make', 'model', 'year', 'trim',
            'price', 'mileage', 'city', 'state', 'zip', 'ausstattung'
        ]
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            for vehicle in all_vehicles:
                equipment_list = vehicle.get('features', [])
                vehicle['ausstattung'] = ", ".join(map(str, equipment_list))
                writer.writerow(vehicle)
        print(f"Daten erfolgreich in '{OUTPUT_FILE}' gespeichert!")

except ValueError as e:
    print(f"Fehler in der Konfiguration: {e}")
except requests.exceptions.HTTPError as e:
    print(f"HTTP-Fehler bei der API-Anfrage: {e.response.status_code} {e.response.reason} für URL: {e.request.url}")
    try:
        error_details = e.response.json()
        print("--- API Fehlerdetails ---\n" + json.dumps(error_details, indent=2) + "\n-------------------------")
    except json.JSONDecodeError:
        print("Zusätzliche Fehlerdetails konnten nicht im JSON-Format gelesen werden.")
except requests.exceptions.RequestException as e:
    print(f"Netzwerkfehler bei der API-Anfrage: {e}")
except Exception as e:
    print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

