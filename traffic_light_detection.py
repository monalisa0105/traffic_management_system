import cv2
import numpy as np

def classify_light_color(crop):
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])
    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) + cv2.inRange(hsv, lower_red2, upper_red2)

    lower_yellow = np.array([15, 100, 100])
    upper_yellow = np.array([35, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    lower_green = np.array([40, 50, 50])
    upper_green = np.array([90, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    red_count = cv2.countNonZero(mask_red)
    yellow_count = cv2.countNonZero(mask_yellow)
    green_count = cv2.countNonZero(mask_green)

    max_count = max(red_count, yellow_count, green_count)
    if max_count == red_count:
        return "Red", (0, 0, 255)
    elif max_count == yellow_count:
        return "Yellow", (0, 255, 255)
    elif max_count == green_count:
        return "Green", (0, 255, 0)
    else:
        return "Unknown", (255, 255, 255)

# Open the video file
input_video_path = "E:/github project/your_video.mp4"  # Replace with your video path
cap = cv2.VideoCapture(input_video_path)

if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Define the codec and create VideoWriter object
output_video_path = "E:/github project/output_video.avi"  # Change as needed
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can also try 'MP4V' for .mp4
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

# Manually define ROI coordinates (adjust to your video)
x, y, w, h = 900, 400, 110, 200

while True:
    ret, frame = cap.read()
    if not ret:
        break  # End of video

    traffic_light_roi = frame[y:y+h, x:x+w]
    color_name, color_bgr = classify_light_color(traffic_light_roi)

    # Draw rectangle and label on the frame
    cv2.rectangle(frame, (x, y), (x+w, y+h), color_bgr, 2)
    cv2.putText(frame, color_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_bgr, 2)

    # Show the frame
    cv2.imshow("Traffic Light Color Detection", frame)

    # Write the frame to output video
    out.write(frame)

    if cv2.waitKey(30) & 0xFF == 27:  # ESC to exit
        break

# Release everything
cap.release()
out.release()
cv2.destroyAllWindows()
