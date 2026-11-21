from vfx_shot_manager.core.validator import find_missing_frames


def main() -> None:
    found_frames = {1001, 1002, 1004, 1005}
    missing_frames = find_missing_frames(found_frames, 1001, 1006)
    print(f"SH010 missing frames: {missing_frames}")
