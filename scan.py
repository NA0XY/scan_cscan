def scan_schedule(requests, start, direction='right'):
    """
    Perform SCAN disk scheduling.

    Parameters:
    - requests: list of disk track numbers (integers)
    - start: initial position of the disk head
    - direction: 'right' or 'left' indicating scan direction

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
            sequence.append(max(sorted_requests))  # end of the disk
        sequence.extend(reversed(left))
    elif direction == 'left':
        sequence.extend(reversed(left))
        if left and left[0] != min(sorted_requests):
            sequence.append(min(sorted_requests))  # start of the disk
        sequence.extend(right)
    else:
        raise ValueError("Direction must be 'right' or 'left'")

    movement = 0
    current = start
    for track in sequence:
        movement += abs(track - current)
        current = track

    return sequence, movement


if __name__ == "__main__":
    try:
        # User inputs
        raw_input = input("Enter disk requests (comma-separated): ")
        requests = list(map(int, raw_input.strip().split(',')))

        start = int(input("Enter starting head position: "))
        direction = input("Enter direction (left/right): ").strip().lower()

        if direction not in ['left', 'right']:
            raise ValueError("Direction must be 'left' or 'right'.")

        sequence, total_movement = scan_schedule(requests, start, direction)

        # Output
        print("\n--- SCAN Disk Scheduling ---")
        print(f"Starting Position: {start}")
        print(f"Direction: {direction.capitalize()}")
        print(f"Servicing Sequence: {' → '.join(map(str, sequence))}")
        print(f"Total Head Movement: {total_movement}")
    except Exception as e:
        print(f"Error: {e}")
