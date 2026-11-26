class VfxShotManagerError(Exception):
    """Base class for all errors raised by vfx_shot_manager."""


class InvalidFrameRangeError(VfxShotManagerError):
    """Raised when a frame range is malformed or its start is after its end."""


class DirectoryUnreadableError(VfxShotManagerError):
    """Raised when a render directory is missing or cannot be read."""


class PathOutsideRootError(VfxShotManagerError):
    """Raised when a relative path resolves outside its render root."""
