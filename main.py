import cv2
import mediapipe as mp
import pyautogui
import numpy as np
from typing import List, Tuple, Union
import dataclasses
import math
from utilpack.util import PyImageUtil
from utilpack.core import PyAlgorithm
from mediapipe.framework.formats import landmark_pb2



@dataclasses.dataclass
class DrawingSpec:
    # Color for drawing the annotation. Default to the green color.
    color: Tuple[int, int, int] = (0, 255, 0)
    # Thickness for drawing the annotation. Default to 2 pixels.
    thickness: int = 2
    # Circle radius. Default to 2 pixels.
    circle_radius: int = 2


PRESENCE_THRESHOLD = 0.5
RGB_CHANNELS = 3
RED_COLOR = (0, 0, 255)
VISIBILITY_THRESHOLD = 0.5


def _normalized_to_pixel_coordinates(normalized_x: float, normalized_y: float, image_width: int, image_height: int) -> \
Union[None, Tuple[int, int]]:
    """Converts normalized value pair to pixel coordinates."""

    # Checks if the float value is between 0 and 1.
    def is_valid_normalized_value(value: float) -> bool:
        return (value > 0 or math.isclose(0, value)) and (value < 1 or math.isclose(1, value))

    if not (is_valid_normalized_value(normalized_x) and is_valid_normalized_value(normalized_y)):
        # TODO: Draw coordinates even if it's outside of the image bounds.
        return None
    x_px = min(math.floor(normalized_x * image_width), image_width - 1)
    y_px = min(math.floor(normalized_y * image_height), image_height - 1)
    return x_px, y_px


def get_landmarks(image: np.ndarray,landmark_list: landmark_pb2.NormalizedLandmarkList,connections: List[Tuple[int, int]] = None):
    """Draws the landmarks and the connections on the image.

    Args:
        image: A three channel RGB image represented as numpy ndarray.
        landmark_list: A normalized landmark list proto message to be annotated on
            the image.
        connections: A list of landmark index tuples that specifies how landmarks to
            be connected in the drawing.
        landmark_drawing_spec: A DrawingSpec object that specifies the landmarks'
            drawing settings such as color, line thickness, and circle radius.
        connection_drawing_spec: A DrawingSpec object that specifies the
            connections' drawing settings such as color and line thickness.

    Raises:
        ValueError: If one of the followings:
            a) If the input image is not three channel RGB.
            b) If any connetions contain invalid landmark index.
    """
    if not landmark_list:
        return
    if image.shape[2] != RGB_CHANNELS:
        raise ValueError('Input image must contain three channel rgb data.')
    image_rows, image_cols, _ = image.shape
    idx_to_coordinates = {}
    for idx, landmark in enumerate(landmark_list.landmark):
        if ((landmark.HasField('visibility') and landmark.visibility < VISIBILITY_THRESHOLD) or (
                landmark.HasField('presence') and landmark.presence < PRESENCE_THRESHOLD)):
            continue
        landmark_px = _normalized_to_pixel_coordinates(landmark.x, landmark.y, image_cols, image_rows)

        if landmark_px:
            idx_to_coordinates[idx] = landmark_px

    if connections:
        num_landmarks = len(landmark_list.landmark)
        # Draws the connections if the start and end landmarks are both visible.
        for connection in connections:
            start_idx = connection[0]
            end_idx = connection[1]
            if not (0 <= start_idx < num_landmarks and 0 <= end_idx < num_landmarks):
                raise ValueError(
                    f'Landmark index is out of range. Invalid connection ' f'from landmark #{start_idx} to landmark #{end_idx}.')

    return idx_to_coordinates


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

prev_px = None
click_toggle = False

# For webcam input:
video_wh = 640,480
screen_wh = pyautogui.size()
def video2screen(x,y):
    x = PyAlgorithm.limit_minmax(x, 0, video_wh[0])
    y = PyAlgorithm.limit_minmax(y, 0, video_wh[1])
    return screen_wh[0] / video_wh[0] * x,screen_wh[1] / video_wh[1] * y

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


with mp_hands.Hands(min_detection_confidence=0.75, min_tracking_confidence=0.75, max_num_hands=1) as hands:
    while cap.isOpened():
        success, image = cap.read()

        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        h, w, _ = image.shape
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            hand_landmark = results.multi_hand_landmarks[0]
            landmarks = get_landmarks(image, hand_landmark, mp_hands.HAND_CONNECTIONS)

            if not 8 in landmarks:
                continue
            # mp_drawing.draw_landmarks(image, hand_landmark, mp_hands.HAND_CONNECTIONS)
            # image = cv2.circle(image,landmarks[4],5,(255,0,255),3)
            # image = cv2.circle(image, landmarks[8], 5, (255, 255,0), 3)

            pyautogui.moveTo(video2screen(*landmarks[8]), _pause=False)

            if prev_px:
                distance = np.linalg.norm(np.subtract(landmarks[8], prev_px))

                click_distance = np.linalg.norm(np.subtract(landmarks[8], landmarks[4]))
                if click_toggle == False and click_distance < 20:
                    pyautogui.click(landmarks[8])
                    PyImageUtil.putTextCenter(image, 'Clicked!', (w // 2, h // 2),color = (255,255,255))
                    click_toggle = not click_toggle
                if click_toggle == True and click_distance > 30:
                    click_toggle = not click_toggle

            prev_px = landmarks[8]

        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()