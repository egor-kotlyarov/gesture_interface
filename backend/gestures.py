import math
from typing import List, Optional

THUMB_TIP = 4
THUMB_IP = 3
INDEX_TIP = 8
INDEX_PIP = 6
MIDDLE_TIP = 12
MIDDLE_PIP = 10
RING_TIP = 16
RING_PIP = 14
PINKY_TIP = 20
PINKY_PIP = 18

WRIST = 0

def distance(a, b) -> float:
    return math.sqrt(
        (a.x - b.x) ** 2 +
        (a.y - b.y) ** 2 +
        (a.z - b.z) ** 2
    )

def is_finger_up(landmarks, tip_id) -> bool:
    """
    Палец считается поднятым,
    если его кончик выше (по оси Y) чем PIP (для всех пальцев кроме большого)
    Для большого пальца сравниваем координаты по оси X (учитывая ориентацию руки)
    """
    if tip_id == THUMB_TIP:
        wrist = landmarks[WRIST]
        thumb_tip = landmarks[THUMB_TIP]
        thumb_ip = landmarks[THUMB_IP]
        if wrist.x < thumb_ip.x:
            return thumb_tip.x > thumb_ip.x
        else:
            return thumb_tip.x < thumb_ip.x
    else:
        tip = landmarks[tip_id]
        pip = landmarks[tip_id - 2]
        return tip.y < pip.y

def recognize_hand_gesture(landmarks: List) -> Optional[str]:
    """
    Принимает 21 landmark одной руки
    Возвращает название жеста
    """

    fingers_up = {
        "thumb": is_finger_up(landmarks, THUMB_TIP),
        "index": is_finger_up(landmarks, INDEX_TIP),
        "middle": is_finger_up(landmarks, MIDDLE_TIP),
        "ring": is_finger_up(landmarks, RING_TIP),
        "pinky": is_finger_up(landmarks, PINKY_TIP),
    }

    count = sum(fingers_up.values())

    if count == 5:
        return "OPEN_PALM"

    if count == 0:
        return "FIST"

    if fingers_up["index"] and not fingers_up["middle"] and count == 1:
        return "POINT"

    thumb = landmarks[THUMB_TIP]
    index = landmarks[INDEX_TIP]

    if distance(thumb, index) < 0.05:
        return "PINCH"

    if fingers_up["index"] and fingers_up["middle"] and count == 2:
        return "VICTORY"

    return "UNKNOWN"