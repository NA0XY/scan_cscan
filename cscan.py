def run_cscan(requests, start, max_cylinder=199):
    """
    Perform CSCAN disk scheduling.

    Parameters:
    - requests: list of disk track numbers
    - start: initial head position
    - max_cylinder: max track number (default 199)

    Returns:
    - sequence: list of tracks in the order they are serviced
    - movement: total head movement
    """
    if not requests:
        return [], 0

    sorted_requests = sorted(requests)
    right = [r for r in sorted_requests if r >= start]
    left = [r for r in sorted_requests if r < start]

    sequence = []
    sequence.extend(right)
    if right:
        sequence.append(max_cylinder)  # Jump to max
    if left:
        sequence.append(0)             # Wrap around
        sequence.extend(left)

    movement = 0
    current = start
    for track in sequence:
        movement += abs(track - current)
        current = track

    return sequence, movement
