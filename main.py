project_name = "VFX Shot Manager"
print (project_name)

shot_name = "SH010"
print(shot_name)

frame_numbers = [1001, 1002, 1004, 1005]
def print_missing_frames(frame_numbers):
    for frame_number in range(1001,1006):
        if frame_number not in frame_numbers:
            print(frame_number)

print_missing_frames(frame_numbers)