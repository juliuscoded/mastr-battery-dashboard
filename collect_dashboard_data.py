#!/usr/bin/env python3
import os
import sys
import json
import logging
import argparse
import requests

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_all_batteries(api_key: str,
                        min_brutto_kw: int = 4999,  # Lower threshold for dashboard
                        min_speicher_kwh: int = 4999,  # Lower threshold for dashboard
                        page_size: int = 1000) -> list:
    """
    Fetch all battery storage units for the dashboard with lower thresholds
    """
    logger.info(f"Starting fetch with filters: Bruttoleistung > {min_brutto_kw-1}, Speicherkapazität > {min_speicher_kwh-1}, All Battery Technologies")
    
    BASE_URL = (
        "https://www.marktstammdatenregister.de"
        "/MaStR/Einheit/EinheitJson/GetErweiterteOeffentlicheEinheitStromerzeugung"
    )

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Accept": "application/json",
    }

    # Combine criteria into one OData filter string (all battery technologies):
    # 727: Lithium-Batterie, 728: Blei-Batterie, 729: Redox-Flow-Batterie, 
    # 730: Hochtemperaturbatterie, 731: Nickel-Cadmium- / Nickel-Metallhydridbatterie, 732: Sonstige Batterie
    # Stromspeichertechnologie = 524 ensures we only get battery storage, not pumped hydro or other storage types
    flt = (
        f"Bruttoleistung der Einheit~gt~{min_brutto_kw - 1}"
        f"~and~Nutzbare Speicherkapazität in kWh~gt~{min_speicher_kwh - 1}"
        f"~and~Stromspeichertechnologie~eq~524"
    )
    
    logger.info(f"Using filter: {flt}")

    all_units = []
    page = 1

    while True:
        try:
            logger.info(f"Fetching page {page}...")
            
            resp = requests.get(
                BASE_URL,
                headers=headers,
                params={"filter": flt, "page": page, "pageSize": page_size},
                timeout=30
            )
            resp.raise_for_status()
            body = resp.json()

            batch = body.get("Data") or []
            logger.info(f"Page {page}: Retrieved {len(batch)} units")
            all_units.extend(batch)

            # Check if there are more pages
            if len(batch) < page_size:
                logger.info(f"Last page reached (got {len(batch)} units, page size was {page_size})")
                break

            page += 1
            
        except Exception as e:
            logger.error(f"Error fetching page {page}: {e}")
            break

    # Filter for battery technologies in Python code
    battery_tech_codes = [727, 728, 729, 730, 731, 732]
    filtered_units = [unit for unit in all_units if unit.get('Batterietechnologie') in battery_tech_codes]
    
    logger.info(f"Total units retrieved: {len(all_units)}")
    logger.info(f"Battery technology units after filtering: {len(filtered_units)}")
    
    return filtered_units

def main():
    parser = argparse.ArgumentParser(description='Collect comprehensive battery data for dashboard')
    parser.add_argument('--min-power', type=int, default=10000, 
                       help='Minimum power in kW (default: 10000)')
    parser.add_argument('--min-capacity', type=int, default=10000, 
                       help='Minimum capacity in kWh (default: 100)')
    parser.add_argument('--page-size', type=int, default=1000, 
                       help='Page size for API requests (default: 1000)')
    
    args = parser.parse_args()
    
    api_key = os.getenv("MASTR_API_KEY") or "YOUR_API_KEY"
    if not api_key or api_key == "YOUR_API_KEY":
        print("❌ Please set your key in MASTR_API_KEY (or replace the placeholder).", file=sys.stderr)
        sys.exit(1)

    logger.info("Starting comprehensive MaStR battery storage data collection for dashboard...")
    batteries = fetch_all_batteries(api_key, args.min_power, args.min_capacity, args.page_size)
    
    # Ensure we save in the current working directory
    out_file = os.path.join(os.getcwd(), f"all_batterie_speicher_all_tech_>={args.min_power}kW_{args.min_capacity}kWh.json")
    
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(batteries, f, ensure_ascii=False, indent=2)

    print(f"✅ Retrieved {len(batteries)} units → {out_file}")
    print(f"📊 This data includes all battery technologies and is ready for the Streamlit dashboard!")

if __name__ == "__main__":
    main() 
