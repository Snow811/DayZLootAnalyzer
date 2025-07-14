import os
import xml.etree.ElementTree as ET

def parse_types_folder(folder_path):
    loot_items = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            file_path = os.path.join(folder_path, filename)
            try:
                loot_items.extend(parse_types_file(file_path))
            except ET.ParseError as e:
                print(f"❌ XML Parse Error in file: {filename}")
                print(f"   → {str(e)}")
            except Exception as e:
                print(f"❌ Unexpected error in file: {filename}")
                print(f"   → {str(e)}")
    return loot_items

def parse_types_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    items = []

    for type_elem in root.findall('type'):
        item = {
            'name': type_elem.get('name'),
            'nominal': int(get_text(type_elem, 'nominal', default='0')),
            'category': get_attr(type_elem.find('category'), 'name'),
            'usage': [u.get('name') for u in type_elem.findall('usage')],
            'value': [v.get('name') for v in type_elem.findall('value')],
            'tag': [t.get('name').lower().strip() for t in type_elem.findall('tag') if t.get('name')]
        }
        items.append(item)

    return items

def get_text(parent, tag, default=None):
    elem = parent.find(tag)
    return elem.text if elem is not None else default

def get_attr(elem, attr, default=None):
    return elem.get(attr) if elem is not None else default
