import os
import xml.etree.ElementTree as ET
from collections import defaultdict

def parse_mapgrouppos_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            file_path = os.path.join(folder_path, filename)
            return parse_mapgrouppos_file(file_path)
    return []

def parse_mapgrouppos_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    placements = []

    for group in root.findall('group'):
        placements.append({
            'name': group.get('name'),
            'pos': group.get('pos'),
            'rotation': group.get('rpy'),
            'angle': float(group.get('a', 0))
        })

    return placements

def count_group_placements(placements):
    count_by_group = defaultdict(int)
    for entry in placements:
        count_by_group[entry['name']] += 1
    return dict(count_by_group)
