import requests
import json
import sys

def fetch_lawrence_redlining(output_filename="lawrence_redlining.geojson"):
    print(f"--- 1. Processing Redlining Data ---")
    url = "https://dsl.richmond.edu/panorama/redlining/static/mappinginequality.json"
    
    try:
        print(f"Downloading data from {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        print("Filtering for Lawrence, MA...")
        lawrence_features = []
        features = data.get('features', [])
        
        for feature in features:
            props = feature.get('properties', {})
            city = props.get('city', '').lower()
            state = props.get('state', '').lower()
            if city == 'lawrence' and state == 'ma':
                lawrence_features.append(feature)
        
        if not lawrence_features:
            print("Warning: No features found for Lawrence, MA.")
            return

        geojson_out = { "type": "FeatureCollection", "features": lawrence_features }
        
        with open(output_filename, 'w') as f:
            json.dump(geojson_out, f)
            
        print(f"Success! Saved {len(lawrence_features)} features to '{output_filename}'.")
        
    except Exception as e:
        print(f"Error fetching Redlining data: {e}")

def check_arcgis_service(name, url):
    print(f"\n--- Checking {name} Service ---")
    # append ?f=json to check metadata
    meta_url = f"{url}?f=json"
    try:
        r = requests.get(meta_url, timeout=5)
        if r.status_code == 200:
            print(f"✅ {name} is reachable.")
        else:
            print(f"⚠️ {name} returned status {r.status_code}. It might be private or moved.")
    except Exception as e:
        print(f"❌ Could not reach {name}: {e}")

if __name__ == "__main__":
    # 1. Download Local Data
    fetch_lawrence_redlining()
    
    # 2. Check Remote Services (These are used directly in HTML, not downloaded)
    canopy_url = "https://tiles.arcgis.com/tiles/StPsG80YRtvnlCJ8/arcgis/rest/services/TC_LMAmetro/MapServer"
    temp_url = "https://tiles.arcgis.com/tiles/StPsG80YRtvnlCJ8/arcgis/rest/services/LST_LMAmetro/MapServer"
    
    check_arcgis_service("Tree Canopy", canopy_url)
    check_arcgis_service("Surface Temperature", temp_url)
