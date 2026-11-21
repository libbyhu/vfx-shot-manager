def find_missing_frames(frame_numbers, start_frame, end_frame):
    missing_frames = []
    for frame_number in range(start_frame, end_frame + 1):
        if frame_number not in frame_numbers:
            missing_frames.append(frame_number)
    return missing_frames