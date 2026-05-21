import json
import csv
from datetime import datetime
from pathlib import Path

def export_to_json(results, filename=None):
    if filename is None:
        filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    filepath = Path("exports") / filename
    filepath.parent.mkdir(exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"✅ JSON exported to: {filepath}")
    return filepath

def export_to_csv(results, filename=None):
    if filename is None:
        filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    filepath = Path("exports") / filename
    filepath.parent.mkdir(exist_ok=True)
    
    if results:
        # Get all unique keys from all dicts
        all_keys = set()
        for r in results:
            all_keys.update(r.keys())
        fieldnames = sorted(list(all_keys))
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
    
    print(f"✅ CSV exported to: {filepath}")
    return filepath

if __name__ == "__main__":
    # Example usage
    sample_results = [
        {"task": "Long BTC 10x", "agent": "FuturesSpecialist", "entry": 79834, "sl": 78237, "tp": 81829},
        {"task": "Check portfolio risk", "agent": "RiskManager", "drawdown": 4.76, "status": "BREACH"},
    ]
    
    export_to_json(sample_results)
    export_to_csv(sample_results)
