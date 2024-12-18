'''
    File name         : object_tracking.py
    File Description  : Kalman Filter Algorithm Implementation
    Author            : Pritesh Raj
    Date created      : 3-12-2020
    Date last modified: 20-12-2020
    Python Version    : 3.7
'''
# Import python libraries
import cv2
import copy
from detectors import Detectors
from tracker import Tracker

file_path = 'D:/computer vision/main/AbandonObject/video/video1.avi'


# Create open cv video capture object
cap = cv2.VideoCapture(0)

# Create Object Detector
detector = Detectors()

# Create Object Tracker
tracker = Tracker(160, 30, 5, 100)

# Variables initialization
skip_frame_count = 0
pause = False

# Infinite loop to process video frames
while True :
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Make copy of original frame
    orig_frame = copy.copy(frame)

    # Skip initial frames that display logo
    if (skip_frame_count < 15):
        skip_frame_count += 1
        continue

    # Detect and return centeroids of the objects in the frame
    centers = detector.Detect(frame)

    # If centroids are detected then track them
    if (len(centers) > 0):

        # Track object using Kalman Filter
        tracker.Update(centers)

        # For identified object tracks draw tracking line
        # Use various colors to indicate different track_id
        for i in range(len(tracker.tracks)):
            if (len(tracker.tracks[i].trace) > 1):
                for j in range(len(tracker.tracks[i].trace)-1):
                    # Draw trace line
                    x1 = tracker.tracks[i].trace[j][0][0]
                    y1 = tracker.tracks[i].trace[j][1][0]
                    x2 = tracker.tracks[i].trace[j+1][0][0]
                    y2 = tracker.tracks[i].trace[j+1][1][0]
                    clr = tracker.tracks[i].track_id % 9
                    cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), 2)

        # Display the resulting tracking frame
        cv2.imshow('Tracking', frame)

    # Display the original frame
    cv2.imshow('Original', orig_frame)

    # Slower the FPS
    cv2.waitKey(50)

    # Check for key strokes
    k = cv2.waitKey(50) & 0xff
    if k == 27:  # 'esc' key has been pressed, exit program.
        break
    if k == 112:  # 'p' has been pressed. this will pause/resume the code.
        pause = not pause
        if (pause is True):
            print("Code is paused. Press 'p' to resume..")
            while (pause is True):
                # stay in this loop until
                key = cv2.waitKey(30) & 0xff
                if key == 112:
                    pause = False
                    print("Resume code..!!")
                    break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
