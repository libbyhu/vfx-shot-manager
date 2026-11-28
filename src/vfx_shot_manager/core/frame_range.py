import re
from collections.abc import Iterable
from dataclasses import dataclass

from vfx_shot_manager.core.errors import InvalidFrameRangeError

_RANGE_PATTERN = re.compile(r"([0-9]+)-([0-9]+)")


@dataclass(frozen=True)
class FrameRange:
    """An inclusive range of frame numbers, such as 1001-1006."""

    start: int
    end: int

    def __post_init__(self) -> None:
        if self.start < 0:
            raise InvalidFrameRangeError(f"Start frame must be >= 0, got {self.start}")
        if self.start > self.end:
            raise InvalidFrameRangeError(
                f"Start frame {self.start} is after end frame {self.end}"
            )

    def __contains__(self, frame: object) -> bool:
        return isinstance(frame, int) and self.start <= frame <= self.end

    def __len__(self) -> int:
        return self.end - self.start + 1


def parse_range(text: str) -> FrameRange:
    """Parse a range written as ``<start>-<end>``, such as ``1001-1006``.

    Args:
        text: The range text. Leading and trailing whitespace is ignored.

    Returns:
        The parsed inclusive frame range.

    Raises:
        InvalidFrameRangeError: If the text is not in ``<start>-<end>`` form,
            or if the start is after the end.
    """
    match = _RANGE_PATTERN.fullmatch(text.strip())
    if match is None:
        raise InvalidFrameRangeError(
            f"Expected a range such as 1001-1006, got {text!r}"
        )
    start, end = (int(group) for group in match.groups())
    return FrameRange(start, end)


def compact_frames(frames: Iterable[int]) -> str:
    """Return frame numbers in compact form, such as ``1001-1003,1005``.

    Consecutive frames are joined with a hyphen and separate runs with commas.
    Input order and duplicates do not matter.

    Args:
        frames: Frame numbers to display.

    Returns:
        The compact text, or an empty string when there are no frames.
    """
    ordered = sorted(set(frames))
    if not ordered:
        return ""

    runs: list[str] = []
    run_start = previous = ordered[0]
    for frame in ordered[1:]:
        if frame == previous + 1:
            previous = frame
            continue
        runs.append(_format_run(run_start, previous))
        run_start = previous = frame
    runs.append(_format_run(run_start, previous))
    return ",".join(runs)


def _format_run(start: int, end: int) -> str:
    return str(start) if start == end else f"{start}-{end}"
