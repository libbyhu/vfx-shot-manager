def find_missing_frames(found: set[int], start: int, end: int) -> list[int]:
    """Return frames in the inclusive range that are not in ``found``.

    Args:
        found: Frame numbers that exist on disk.
        start: First expected frame, inclusive.
        end: Last expected frame, inclusive.

    Returns:
        Missing frame numbers in ascending order.
    """
    return [frame for frame in range(start, end + 1) if frame not in found]
