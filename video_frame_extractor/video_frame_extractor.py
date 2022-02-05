
from datetime import timedelta
import cv2
import numpy as np
import os

SAVING_FRAMES_PER_SECOND = 6

def format_timedelta(td):
    """Utility function to format timedelta objects in a cool way (e.g 00:00:20.05) 
    omitting microseconds and retaining milliseconds"""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return result + ".00".replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")

def get_frames(cap, saving_fps):
    s = []
    print(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(cap.get(cv2.CAP_PROP_FPS))
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s

def main(video_file):
    print(f"Extracting frames of video file: {video_file}");
    filename, _ = os.path.splitext(video_file)
    file_raw_name, _ = os.path.splitext(os.path.basename(video_file))
    #filename += "-opencv"
    if not os.path.isdir(filename):
        print(f"Creating directory: {filename}")
        os.mkdir(filename)
    else:
        print(f"Directory: {filename} already exists")
    
    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    saving_frames_durations = get_frames(cap, saving_frames_per_second)
    count,frame_count = 0,0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            # break out of the loop if there are no frames to read
            break
        # get the duration by dividing the frame count by the FPS
        frame_duration = count / fps
        try:
            # get the earliest duration to save
            closest_duration = saving_frames_durations[0]
        except IndexError:
            # the list is empty, all duration frames were saved
            break
        if frame_duration >= closest_duration:
            frame_count += 1
            # if closest duration is less than or equals the frame duration, 
            # then save the frame
            frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
            print(f"Extracted frame {frame_count}")
            cv2.imwrite(os.path.join(filename, f"Shield Hero - S01E01 - frame {frame_count}.jpg"), frame) 
            # drop the duration spot from the list, since this duration spot is already saved
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        # increment the frame count
        count += 1
    print("Frames extracted!")

if __name__ == '__main__':
    import sys
    video_file = sys.argv[1]
    print(cv2.__version__)
    if(os.path.isfile(video_file)):
        main(video_file)        
    else:
        print("No file found")