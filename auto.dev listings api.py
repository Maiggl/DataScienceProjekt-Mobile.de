import requests
import csv
import time
import json

# ============================ KONFIGURATION ===============================
API_KEY = "sk_ad_rmkZvJcwP9FccFOyOo9A9j9a"

# Seiten-Parameter
MAX_PAGES = 10
# ==========================================================================

BASE_URL = "https://api.auto.dev/listings"
OUTPUT_FILE = 'mercedes_s_klasse_datensatz.csv'

headers = {
    'x-api-key': API_KEY
}

all_vehicles_for_csv = []
processed_vins = set()

try:
    if not API_KEY or API_KEY == "IHR_API_SCHLÜSSEL":
        raise ValueError("API-Schlüssel wurde nicht in der Konfiguration festgelegt.")

    print("--- Sammle alle Fahrzeug-Listings ---")
    for page_num in range(1, MAX_PAGES + 1):
        request_url = f"{BASE_URL}?vehicle.make=Mercedes-Benz&vehicle.model=S-Class&page={page_num}"
        print(f"Sende Anfrage für Seite {page_num}...")
        response = requests.get(request_url, headers=headers)
        response.raise_for_status()

        data = response.json()
        vehicle_listings = data.get('data', [])

        if not vehicle_listings:
            print("Keine weiteren Fahrzeuge gefunden. Paginierung beendet.")
            break

        new_vehicles_found = 0
        for vehicle_data in vehicle_listings:
            vin = vehicle_data.get('vin')
            if vin and vin not in processed_vins:
                vehicle_details = vehicle_data.get('vehicle', {}) or {}
                retail_details = vehicle_data.get('retailListing', {}) or {}

                # --- HIER WERDEN DIE DATEN DEN NEUEN SPALTEN ZUGEORDNET ---
                row_data = {
                    'year': vehicle_details.get('year'),
                    'make': vehicle_details.get('make'),
                    'model': vehicle_details.get('model'),
                    'trim': vehicle_details.get('trim'),
                    'body': vehicle_details.get('bodyStyle'),  # bodyStyle -> body
                    'transmission': vehicle_details.get('transmission'),
                    'vin': vin,
                    'state': retail_details.get('state'),
                    # 'used' (boolean) -> 'condition' (Text)
                    'condition': 'Used' if retail_details.get('used', False) else 'New',
                    'odometer': retail_details.get('miles'),  # miles -> odometer
                    'color': vehicle_details.get('exteriorColor'),  # exteriorColor -> color
                    'interior': vehicle_details.get('interiorColor')  # interiorColor -> interior
                }
                # -----------------------------------------------------------

                all_vehicles_for_csv.append(row_data)
                processed_vins.add(vin)
                new_vehicles_found += 1

        print(f"{new_vehicles_found} neue, einzigartige Fahrzeuge auf dieser Seite gefunden.")
        time.sleep(0.5)

    if not all_vehicles_for_csv:
        raise Exception("Es wurden keine Fahrzeuge für 'Mercedes-Benz S-Class' gefunden.")

    print(f"\n--- Schreibe {len(all_vehicles_for_csv)} Fahrzeuge in die CSV-Datei ---")

    # Exakte Feldnamen wie von Ihnen gewünscht
    fieldnames = ['year', 'make', 'model', 'trim', 'body', 'transmission', 'vin', 'state', 'condition', 'odometer',
                  'color', 'interior']

    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(all_vehicles_for_csv)

    print(f"Daten erfolgreich in '{OUTPUT_FILE}' gespeichert!")

except Exception as e:
    print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

