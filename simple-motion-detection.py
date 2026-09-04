import cv2

# Initialize video capture (0 for default webcam, or pass a file path: "video.mp4")
cap = cv2.VideoCapture(0)

# Read two consecutive frames to calculate motion
ret, frame1 = cap.read()
ret, frame2 = cap.read()

# Threshold setting: minimum contour area to consider as motion
MOTION_THRESHOLD_AREA = 1000

while cap.isOpened():
    # 1. Calculate absolute difference between the two frames
    diff = cv2.absdiff(frame1, frame2)

    # 2. Convert difference image to grayscale
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # 3. Apply Gaussian Blur to reduce noise/minor illumination changes
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # 4. Threshold the blurred image to create a binary image (motion = white)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # 5. Dilate the thresholded image to fill in gaps in moving regions
    dilated = cv2.dilate(thresh, None, iterations=3)

    # 6. Find contours of the moving areas
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 7. Draw bounding boxes around regions with motion larger than threshold
    for contour in contours:
        if cv2.contourArea(contour) < MOTION_THRESHOLD_AREA:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            frame1,
            "Motion Detected",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
        )

    # Display the result
    cv2.imshow("Motion Detection Output", frame1)

    # Advance frame window: set current frame2 as next frame1, then read new frame2
    frame1 = frame2
    ret, frame2 = cap.read()

    # Press 'q' or 'ESC' to exit
    if not ret or cv2.waitKey(10) & 0xFF in (ord("q"), 27):
        break

# Clean up resources
cap.release()
cv2.destroyAllWindows()