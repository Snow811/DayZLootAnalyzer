from collections import defaultdict

def analyze_loot_economy(types_data, proto_data, map_positions):
    # Normalize and count how many times each building group is placed
    group_counts = defaultdict(int)
    for entry in map_positions:
        normalized_name = entry['name'].lower().strip()
        group_counts[normalized_name] += 1

    # Build spawn capacity map by usage (or tag fallback)
    spawn_capacity = defaultdict(lambda: {'slots': 0, 'groups': 0})

    for container in proto_data:
        group_name = container['group'].lower().strip()
        group_lootmax = container['group_lootmax']
        usages = [u.lower().strip() for u in container['usages'] if u]

        # Fallback to tags if usages are missing
        if not usages:
            usages = [t.lower().strip() for t in container['tags'] if t]

        placement_count = group_counts.get(group_name, 0)
        total_group_slots = group_lootmax * placement_count

        for usage in usages:
            spawn_capacity[usage]['slots'] += total_group_slots
            spawn_capacity[usage]['groups'] += placement_count

    # Aggregate nominal loot by usage
    loot_by_usage = defaultdict(lambda: {'nominal': 0})
    for item in types_data:
        nominal = item['nominal']
        usages = [u for u in item['usage'] if u]

        # Fallback to tags if usage is missing or empty
        if not usages:
            usages = item['tag']

        for usage in usages:
            normalized_usage = usage.lower().strip() if usage else None
            if normalized_usage:
                loot_by_usage[normalized_usage]['nominal'] += nominal

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

    report['flags'] = {
        'underrepresented': [u for u, d in report['bias_by_usage'].items() if d['saturation'] < 0.5],
        'overrepresented': [u for u, d in report['bias_by_usage'].items() if d['saturation'] > 2.0]
    }

    return report
