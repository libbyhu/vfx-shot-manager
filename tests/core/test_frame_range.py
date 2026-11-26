from dataclasses import FrozenInstanceError

import pytest

from vfx_shot_manager.core.errors import InvalidFrameRangeError, VfxShotManagerError
from vfx_shot_manager.core.frame_range import FrameRange


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
