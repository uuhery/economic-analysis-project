from typing import List


def improved_greedy_schedule(tasks: List[dict]) -> List[dict]:
    """
    支持 earliest_start, deadline, priority 排序调度。
    优先调度高优先级任务，避免早期时间段被低优先级任务占据。
    """
    # 时间轴记录被占用的时间段（简化为线性时间表）
    timeline = []
    schedule = []

    # 按 priority 降序，deadline 升序排列（越早越紧急）
    tasks_sorted = sorted(tasks, key=lambda t: (-t.get('priority', 1), t['deadline']))

    for task in tasks_sorted:
        duration = task['duration']
        earliest = task.get('earliest_start', 0)
        deadline = task['deadline']
        feasible = False

        # 从 earliest 到 deadline - duration 依次尝试可用时间槽
        for start in range(earliest, deadline - duration + 1):
            if all(t not in timeline for t in range(start, start + duration)):
                for t in range(start, start + duration):
                    timeline.append(t)
                schedule.append({
                    'name': task['name'],
                    'start': start,
                    'end': start + duration,
                    'resource_usage': duration
                })
                feasible = True
                break

        if not feasible:
            schedule.append({
                'name': task['name'],
                'start': None,
                'end': None,
                'skipped': True,
                'reason': 'No feasible slot in window'
            })

    return schedule

def improved_resource_smoothing(tasks: List[dict], total_resources: int, total_time: int) -> List[dict]:
    """
    考虑任务延迟灵活度，根据每个任务的workload进行时间段分布
    """
    result = []
    resource_slots = [0 for _ in range(total_time)]

    for task in tasks:
        workload = task['workload']
        flexibility = task.get('flexibility', 0)
        assigned = False

        for start in range(0, total_time - flexibility):
            end = start + flexibility + 1
            window = list(range(start, min(end, total_time)))

            for window_size in range(1, len(window) + 1):
                slot_comb = window[:window_size]
                if all(resource_slots[s] + (workload / len(slot_comb)) <= (total_resources / total_time) * 1.2 for s in slot_comb):
                    for s in slot_comb:
                        resource_slots[s] += workload / len(slot_comb)
                    result.append({
                        'name': task['name'],
                        'slots': slot_comb,
                        'allocated_per_slot': round(workload / len(slot_comb), 2)
                    })
                    assigned = True
                    break
            if assigned:
                break

        if not assigned:
            result.append({
                'name': task['name'],
                'slots': [],
                'allocated_per_slot': 0,
                'skipped': True
            })

    return result
