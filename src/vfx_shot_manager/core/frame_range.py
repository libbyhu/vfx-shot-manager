import re
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
