def run_scan(requests, start, direction='right'):
    """
    Perform SCAN disk scheduling.

    Parameters:
    - requests: list of disk track numbers (integers)
    - start: initial position of the disk head
    - direction: 'right' or 'left'

    Returns:
    - sequence: list of serviced disk tracks in order
    - movement: total head movement
    """
    if not requests:
        return [], 0

    sorted_requests = sorted(requests)
    left = [r for r in sorted_requests if r < start]
    right = [r for r in sorted_requests if r >= start]

    sequence = []
    if direction == 'right':
        sequence.extend(right)
        if right and right[-1] != max(sorted_requests):
            sequence.append(max(sorted_requests))
        sequence.extend(reversed(left))
    elif direction == 'left':
        sequence.extend(reversed(left))
        if left and left[0] != min(sorted_requests):
            sequence.append(min(sorted_requests))
        sequence.extend(right)
    else:
        raise ValueError("Direction must be 'right' or 'left'")

    movement = 0
    current = start
    for track in sequence:
        movement += abs(track - current)
        current = track

    return sequence, movement
