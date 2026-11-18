project_name = "VFX Shot Manager"
print (project_name)

shot_name = "SH010"
print(shot_name)

frame_numbers = [1001, 1002, 1004, 1005]
def find_missing_frames(frame_numbers, start_frame, end_frame):
    missing_frames = []
    for frame_number in range (start_frame,end_frame+1):
        if frame_number not in frame_numbers:
            missing_frames.append(frame_number)
    return missing_frames

print(find_missing_frames(frame_numbers, 1001, 1006))