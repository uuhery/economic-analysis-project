def greedy_schedule(tasks):
    """
    tasks: list of dicts with 'name', 'duration', 'deadline'
    """
    tasks_sorted = sorted(tasks, key=lambda t: t['deadline'])
    schedule = []
    current_time = 0

    for task in tasks_sorted:
        start = current_time
        end = start + task['duration']
        if end <= task['deadline']:
            schedule.append({
                'name': task['name'],
                'start': start,
                'end': end
            })
            current_time = end
        else:
            schedule.append({
                'name': task['name'],
                'start': None,
                'end': None,
                'skipped': True
            })

    return schedule

def resource_smoothing(tasks, total_resources, total_time):
    """
    tasks: list of {'name', 'workload'}
    evenly spread workload over time periods
    """
    schedule = []
    time_slots = total_time
    avg_per_slot = total_resources / time_slots

    for task in tasks:
        allocation = min(task['workload'], avg_per_slot)
        slots = int(task['workload'] / allocation)
        schedule.append({
            'name': task['name'],
            'slots': slots,
            'allocated_per_slot': round(allocation, 2)
        })

    return schedule