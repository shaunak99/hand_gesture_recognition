import cv2
import pyautogui
from src.hand_tracker import HandTracker
from src.dyn_gesture import Gesture

WINDOW = "Hand Tracking"
PALM_MODEL_PATH = "models/palm_detection_without_custom_op.tflite"
LANDMARK_MODEL_PATH = "models/hand_landmark.tflite"
ANCHORS_PATH = "models/anchors.csv"

POINT_COLOR = (0, 255, 0)
CONNECTION_COLOR = (255, 0, 0)
THICKNESS = 4

cv2.namedWindow(WINDOW)
capture = cv2.VideoCapture(0)

if capture.isOpened():
    hasFrame, frame = capture.read()
else:
    hasFrame = False

#        8   12  16  20
#        |   |   |   |
#        7   11  15  19
#    4   |   |   |   |
#    |   6   10  14  18
#    3   |   |   |   |
#    |   5---9---13--17
#    2    \         /
#     \    \       /
#      1    \     /
#       \    \   /
#        ------0-
connections = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (5, 6), (6, 7), (7, 8),
    (9, 10), (10, 11), (11, 12),
    (13, 14), (14, 15), (15, 16),
    (17, 18), (18, 19), (19, 20),
    (0, 5), (5, 9), (9, 13), (13, 17), (0, 17)
]

detector = HandTracker(
    PALM_MODEL_PATH,
    LANDMARK_MODEL_PATH,
    ANCHORS_PATH,
    box_shift=0.2,
    box_enlarge=1.3
)

#Creating Gesture object and initialising timestamp
action = Gesture(connections)
action.timestamp = [capture.get(cv2.CAP_PROP_POS_MSEC)]

while hasFrame:
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    points, _ = detector(image)

    action.update_time(capture.get(cv2.CAP_PROP_POS_MSEC))

    if points is not None:

        action.update_points(points)
        action.get_gesture()

        for connection in connections:
            x0, y0, z0 = points[connection[0]]
            x1, y1, z1 = points[connection[1]]
            if (connection[1] % 4) == 0:
                #Fingertip joints are represented in grayscale using depth data
                cv2.circle(frame, (int(x1), int(y1)), THICKNESS * 2, (int(-z1)*3,int(-z1)*3,int(-z1)*3), THICKNESS)
            elif connection[1] == 1:
                #Hand basejoint
                cv2.circle(frame, (int(x0), int(y0)), THICKNESS * 2, (int(-z0)*3,int(-z0)*3,int(-z0)*3), THICKNESS)

    cv2.imshow(WINDOW, frame)
    hasFrame, frame = capture.read()
    key = cv2.waitKey(1)
    if key == 27:
        break

capture.release()
cv2.destroyAllWindows()
