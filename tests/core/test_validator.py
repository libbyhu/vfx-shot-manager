from vfx_shot_manager.core.validator import find_missing_frames


def test_finds_missing_frames_in_middle_and_end() -> None:
    found = {1001, 1002, 1004, 1005}
    assert find_missing_frames(found, 1001, 1006) == [1003, 1006]


def test_returns_empty_list_when_sequence_is_complete() -> None:
    found = {1001, 1002, 1003}
    assert find_missing_frames(found, 1001, 1003) == []


def test_returns_every_frame_when_nothing_is_found() -> None:
    assert find_missing_frames(set(), 1001, 1003) == [1001, 1002, 1003]


def test_finds_missing_first_frame() -> None:
    assert find_missing_frames({1002, 1003}, 1001, 1003) == [1001]


def test_handles_single_frame_range() -> None:
    assert find_missing_frames(set(), 1001, 1001) == [1001]


def test_ignores_frames_outside_the_range() -> None:
    found = {999, 1001, 1002, 2000}
    assert find_missing_frames(found, 1001, 1002) == []
