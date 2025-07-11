from collections import defaultdict

def analyze_loot_economy(types_data, proto_data, map_positions):
    # Count how many times each building group is placed
    group_counts = defaultdict(int)
    for entry in map_positions:
        group_counts[entry['name']] += 1

    # Build spawn capacity map by usage
    spawn_capacity = defaultdict(lambda: {'slots': 0, 'groups': 0})

    # Track group-level spawn slots
    for container in proto_data:
        group_name = container['group']
        group_lootmax = container['group_lootmax']
        usages = container['usages']

        placement_count = group_counts.get(group_name, 0)
        total_group_slots = group_lootmax * placement_count

        # Assign total group slots to each usage
        for usage in usages:
            spawn_capacity[usage]['slots'] += total_group_slots
            spawn_capacity[usage]['groups'] += placement_count

    # Aggregate nominal loot by usage
    loot_by_usage = defaultdict(lambda: {'nominal': 0})
    for item in types_data:
        nominal = item['nominal']
        for usage in item['usage']:
            loot_by_usage[usage]['nominal'] += nominal

    # Build final report
    report = {
        'total_nominal': sum(item['nominal'] for item in types_data),
        'total_spawn_points': sum(v['slots'] for v in spawn_capacity.values()),
        'bias_by_usage': {}
    }

    for usage, spawn in spawn_capacity.items():
        nominal = loot_by_usage[usage]['nominal']
        saturation = round(nominal / spawn['slots'], 2) if spawn['slots'] > 0 else 0
        report['bias_by_usage'][usage] = {
            'nominal': nominal,
            'spawn_slots': spawn['slots'],
            'groups': spawn['groups'],
            'saturation': saturation
        }

    # Flag under/over represented usage zones
    report['flags'] = {
        'underrepresented': [u for u, d in report['bias_by_usage'].items() if d['saturation'] < 0.5],
        'overrepresented': [u for u, d in report['bias_by_usage'].items() if d['saturation'] > 2.0]
    }

    return report
