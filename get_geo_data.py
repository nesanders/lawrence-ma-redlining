import requests
import json
import os

def fetch_and_process_redlining(output_filename="lawrence_redlining.geojson"):
    print("Fetching Mapping Inequality Redlining Data (this may take a moment)...")
    url = "https://dsl.richmond.edu/panorama/redlining/static/mappinginequality.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        print("Data fetched. Filtering for Lawrence, MA...")
        
        lawrence_features = []
        
        # The structure is typically a FeatureCollection
        features = data.get('features', [])
        
        for feature in features:
            props = feature.get('properties', {})
            # Check for city and state keys (normalization to lower case for safety)
            city = props.get('city', '').lower()
            state = props.get('state', '').lower()
            
            if city == 'lawrence' and state == 'ma':
                lawrence_features.append(feature)
        
        if not lawrence_features:
            print("Warning: No features found for Lawrence, MA. Check city/state spelling in source.")
            return

        filtered_geojson = {
            "type": "FeatureCollection",
            "features": lawrence_features
        }
        
        with open(output_filename, 'w') as f:
            json.dump(filtered_geojson, f)
            
        print(f"Success! Saved {len(lawrence_features)} features to '{output_filename}'.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_process_redlining() 
