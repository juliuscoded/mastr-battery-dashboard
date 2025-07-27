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
                        min_brutto_kw: int = 100,  # Changed from 3000 to 100 kW
                        min_speicher_kwh: int = 100,  # Changed from 3000 to 100 kWh
                        page_size: int = 1000) -> list:
    """
    Fetch all public Stromerzeugungseinheiten with:
      • Bruttoleistung der Einheit > (min_brutto_kw - 1)
      • Nutzbare Speicherkapazität in kWh > (min_speicher_kwh - 1)
      • Batterietechnologie == "Batterie"

    Loops until Ergebniscode != "OkWeitereDatenVorhanden".
    """
    logger.info(f"Starting fetch with filters: Bruttoleistung > {min_brutto_kw-1}, Speicherkapazität > {min_speicher_kwh-1}, Batterietechnologie = 727")
    
    # ← **Production** endpoint (must use marktstammdatenregister.de, not the .api.bund.dev host!)
    BASE_URL = (
        "https://www.marktstammdatenregister.de"
        "/MaStR/Einheit/EinheitJson/GetErweiterteOeffentlicheEinheitStromerzeugung"
    )

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Accept": "application/json",
    }

    # Combine your three criteria into one OData filter string:
    flt = (
        f"Bruttoleistung der Einheit~gt~{min_brutto_kw - 1}"
        f"~and~Nutzbare Speicherkapazität in kWh~gt~{min_speicher_kwh - 1}"
        f"~and~Batterietechnologie~eq~727"
        f"~and~Betriebs-Status~eq~35"
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

    logger.info(f"Total units retrieved: {len(all_units)}")
    return all_units

def main():
    parser = argparse.ArgumentParser(description='Fetch battery storage units from MaStR API')
    parser.add_argument('--min-power', type=int, default=100000, 
                       help='Minimum power in kW (default: 100)')
    parser.add_argument('--min-capacity', type=int, default=1000000, 
                       help='Minimum capacity in kWh (default: 100)')
    parser.add_argument('--page-size', type=int, default=1000, 
                       help='Page size for API requests (default: 1000)')
    
    args = parser.parse_args()
    
    api_key = os.getenv("MASTR_API_KEY") or "YOUR_API_KEY"
    if not api_key or api_key == "YOUR_API_KEY":
        print("❌ Please set your key in MASTR_API_KEY (or replace the placeholder).", file=sys.stderr)
        sys.exit(1)

    logger.info("Starting MaStR battery storage query...")
    batteries = fetch_all_batteries(api_key, args.min_power, args.min_capacity, args.page_size)
    out_file = f"all_batterie_speicher_>={args.min_power}kW_{args.min_capacity}kWh.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(batteries, f, ensure_ascii=False, indent=2)

    print(f"✅ Retrieved {len(batteries)} units → {out_file}")

if __name__ == "__main__":
    main()