import os
import xml.etree.ElementTree as ET

def parse_proto_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            file_path = os.path.join(folder_path, filename)
            return parse_proto_file(file_path)
    return []

def parse_proto_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    loot_containers = []

    for group in root.findall('group'):
        group_name = group.get('name')
        group_lootmax = int(group.get('lootmax', 0))
        usages = [u.get('name') for u in group.findall('usage')]

        for container in group.findall('container'):
            container_name = container.get('name')
            container_lootmax = int(container.get('lootmax', 0))
            categories = [c.get('name') for c in container.findall('category')]
            tags = [t.get('name') for t in container.findall('tag')]
            points = container.findall('point')

            loot_containers.append({
                'group': group_name,
                'group_lootmax': group_lootmax,
                'container': container_name,
                'container_lootmax': container_lootmax,
                'usages': usages,
                'categories': categories,
                'tags': tags,
                'point_count': len(points),
                'points': [
                    {
                        'position': p.get('pos'),
                        'range': float(p.get('range', 0)),
                        'height': float(p.get('height', 0)),
                        'flags': int(p.get('flags', 0))
                    } for p in points
                ]
            })

    return loot_containers
