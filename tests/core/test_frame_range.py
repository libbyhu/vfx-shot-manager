from dataclasses import FrozenInstanceError

import pytest

from vfx_shot_manager.core.errors import InvalidFrameRangeError, VfxShotManagerError
from vfx_shot_manager.core.frame_range import FrameRange, compact_frames, parse_range


def test_length_counts_both_ends() -> None:
    assert len(FrameRange(1001, 1006)) == 6


def test_single_frame_range_has_length_one() -> None:
    assert len(FrameRange(1001, 1001)) == 1


def test_contains_first_middle_and_last_frame() -> None:
    frame_range = FrameRange(1001, 1006)
    assert 1001 in frame_range
    assert 1003 in frame_range
    assert 1006 in frame_range


def test_does_not_contain_frames_outside_range() -> None:
    frame_range = FrameRange(1001, 1006)
    assert 1000 not in frame_range
    assert 1007 not in frame_range


def test_does_not_contain_non_integers() -> None:
    assert "1003" not in FrameRange(1001, 1006)


def test_rejects_start_after_end() -> None:
    with pytest.raises(InvalidFrameRangeError):
        FrameRange(1006, 1001)


def test_rejects_negative_start() -> None:
    with pytest.raises(InvalidFrameRangeError):
        FrameRange(-1, 10)


def test_is_immutable() -> None:
    frame_range = FrameRange(1001, 1006)
    with pytest.raises(FrozenInstanceError):
        frame_range.start = 1  # type: ignore[misc]


def test_errors_share_a_base_class() -> None:
    assert issubclass(InvalidFrameRangeError, VfxShotManagerError)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("1001-1006", FrameRange(1001, 1006)),
        ("1001-1001", FrameRange(1001, 1001)),
        (" 1001-1006 ", FrameRange(1001, 1006)),
        ("0-10", FrameRange(0, 10)),
    ],
)
def test_parse_range_accepts_valid_text(text: str, expected: FrameRange) -> None:
    assert parse_range(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "",
        "1001",
        "1001-",
        "-1006",
        "1001..1006",
        "a-b",
        "1001-1006-1010",
        "1001 - 1006",
    ],
)
def test_parse_range_rejects_malformed_text(text: str) -> None:
    with pytest.raises(InvalidFrameRangeError):
        parse_range(text)


def test_parse_range_rejects_start_after_end() -> None:
    with pytest.raises(InvalidFrameRangeError):
        parse_range("1006-1001")


@pytest.mark.parametrize(
    ("frames", "expected"),
    [
        ([], ""),
        ([1001], "1001"),
        ([1001, 1002, 1003], "1001-1003"),
        ([1001, 1002, 1003, 1005], "1001-1003,1005"),
        ([1001, 1002, 1003, 1005, 1007, 1008], "1001-1003,1005,1007-1008"),
        ([1003, 1006], "1003,1006"),
        ([1005, 1001, 1003, 1002], "1001-1003,1005"),
        ([1001, 1001, 1002], "1001-1002"),
    ],
)
def test_compact_frames(frames: list[int], expected: str) -> None:
    assert compact_frames(frames) == expected


def test_compact_frames_accepts_a_set() -> None:
    assert compact_frames({1003, 1001, 1002}) == "1001-1003"
