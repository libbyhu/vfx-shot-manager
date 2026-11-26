from dataclasses import dataclass

from vfx_shot_manager.core.errors import InvalidFrameRangeError


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
