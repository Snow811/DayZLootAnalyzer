import os
import json
from datetime import datetime

def save_report_json(report_data, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"loot_report_{timestamp}.json"
    file_path = os.path.join(output_folder, filename)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=4)

    return file_path
