import cv2
import os

def split_video(video_path, num_parts):
    # Open video file
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create directory for split videos
    os.makedirs('split_videos', exist_ok=True)

    # Calculate frames per part
    frames_per_part = total_frames // num_parts

    # Split video into parts
    for i in range(num_parts):
        out = cv2.VideoWriter(f'split_videos/part_{i+1}.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, (frame_width, frame_height))
        for _ in range(frames_per_part):
            out.write(image)
            success, image = vidcap.read()
        out.release()
    vidcap.release()
