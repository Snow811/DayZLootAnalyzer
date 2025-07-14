import os
import sys
from analyzer.types_parser import parse_types_folder
from analyzer.proto_parser import parse_proto_folder
from analyzer.mapgrouppos_parser import parse_mapgrouppos_folder
from analyzer.cross_reference import analyze_loot_economy
from analyzer.report_generator import save_report_json

def get_base_dir():
    if getattr(sys, 'frozen', False):
        # Running as compiled .exe
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

def ensure_folders(base_dir):
    folders = [
        os.path.join(base_dir, 'input', 'types'),
        os.path.join(base_dir, 'input', 'proto'),
        os.path.join(base_dir, 'input', 'mapgrouppos'),
        os.path.join(base_dir, 'output')
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

def main():
    base_dir = get_base_dir()
    ensure_folders(base_dir)

    types_path = os.path.join(base_dir, 'input', 'types')
    proto_path = os.path.join(base_dir, 'input', 'proto')
    mapgrouppos_path = os.path.join(base_dir, 'input', 'mapgrouppos')
    output_path = os.path.join(base_dir, 'output')

    print("🔍 Parsing types.xml files...")
    types_data = parse_types_folder(types_path)
    print(f"📦 Loaded {len(types_data)} items from types.xml.")

    print("🔍 Parsing proto.xml...")
    proto_data = parse_proto_folder(proto_path)
    print(f"📦 Loaded {len(proto_data)} containers from proto.xml.")

    print("🔍 Parsing mapgrouppos.xml...")
    map_positions = parse_mapgrouppos_folder(mapgrouppos_path)
    print(f"📦 Loaded {len(map_positions)} placements from mapgrouppos.xml.")

    print("📊 Analyzing loot economy...")
    report = analyze_loot_economy(types_data, proto_data, map_positions)

    print("📊 Final usage zones:")
    for usage, data in report['bias_by_usage'].items():
        print(f"   → {usage}: {data['nominal']} nominal, {data['spawn_slots']} slots, saturation {data['saturation']}")

    print("💾 Saving report...")
    report_file = save_report_json(report, output_path)

    print(f"✅ Done! Report saved to: {report_file}")

if __name__ == '__main__':
    main()
