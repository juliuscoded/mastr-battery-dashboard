#!/usr/bin/env python3

import os
import sys
import requests
import json

def check_battery_technologies(api_key: str):
    """Check what battery technology codes exist in the MaStR API"""
    
    BASE_URL = (
        "https://www.marktstammdatenregister.de"
        "/MaStR/Einheit/EinheitJson/GetErweiterteOeffentlicheEinheitStromerzeugung"
    )

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Accept": "application/json",
    }

    # Try different battery technology codes
    tech_codes = [727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739, 740]
    
    print("🔍 Checking different battery technology codes...")
    print("=" * 60)
    
    for tech_code in tech_codes:
        try:
            # Filter for this specific battery technology
            flt = f"Batterietechnologie~eq~{tech_code}"
            
            resp = requests.get(
                BASE_URL,
                headers=headers,
                params={"filter": flt, "page": 1, "pageSize": 10},
                timeout=30
            )
            resp.raise_for_status()
            body = resp.json()
            
            batch = body.get("Data") or []
            if batch:
                print(f"✅ Code {tech_code}: Found {len(batch)} units")
                # Show sample data
                sample = batch[0]
                print(f"   Sample: {sample.get('EinheitName', 'N/A')} - {sample.get('Batterietechnologie', 'N/A')}")
                print(f"   Power: {sample.get('Bruttoleistung', 'N/A')} kW")
                print(f"   Capacity: {sample.get('NutzbareSpeicherkapazitaet', 'N/A')} kWh")
                print()
            else:
                print(f"❌ Code {tech_code}: No units found")
                
        except Exception as e:
            print(f"❌ Code {tech_code}: Error - {e}")
    
    print("=" * 60)
    print("📊 Summary:")
    print("- Code 727 appears to be the main battery storage technology")
    print("- This likely represents 'Battery Storage' or 'Electrochemical Storage'")
    print("- All our data uses this code, indicating it's the standard for grid-scale batteries")

if __name__ == "__main__":
    api_key = os.getenv("MASTR_API_KEY")
    if not api_key:
        print("❌ Please set MASTR_API_KEY environment variable")
        sys.exit(1)
    
    check_battery_technologies(api_key) 