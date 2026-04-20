# DataScienceProjekt-Mobile.de

Datensatz US https://www.kaggle.com/datasets/syedanwarafridi/vehicle-sales-data


sk_ad_ZF_y6274NrUEe4T97RjrYTaX


## Pipeline / Import Commands

### Voraussetzungen
- `.env` im Projektroot mit:
  - `SUPABASE_URL=...`
  - `SUPABASE_SERVICE_ROLE_KEY=...`

### (Optional) venv aktivieren (Windows PowerShell)
```powershell
.\.venv\Scripts\Activate.ps1
```

---

## Pipeline Wrapper (`pipeline.py`)

### Clean (nur Cleaning ausführen)
US:
```bash
python pipeline.py clean --market US
```

DE:
```bash
python pipeline.py clean --market DE
```

### Import (nur Import eines bereits bereinigten CSV)
US:
```bash
python pipeline.py import --market US --cleaned "cleaned_ford_f_series_mit_ownerCount.csv" --dataset-id 10
```

DE:
```bash
python pipeline.py import --market DE --cleaned "cleaned_mobile_de_erweitert_Aklasse.csv" --dataset-id 7
```

### Run (Cleaning + Import)
US:
```bash
python pipeline.py run --market US --cleaned "cleaned_ford_f_series_mit_ownerCount.csv" --dataset-id 10
```

DE:
```bash
python pipeline.py run --market DE --cleaned "cleaned_mobile_de_erweitert_Aklasse.csv" --dataset-id 7
```

---

## Direkt-Import ohne Pipeline (falls du nur importieren willst)

US:
```bash
python import_us_csv.py --csv "cleaned_ford_f_series_mit_ownerCount.csv" --dataset-id 10
```

DE:
```bash
python import_de_csv.py --csv "cleaned_mobile_de_erweitert_Aklasse.csv" --dataset-id 7
```
