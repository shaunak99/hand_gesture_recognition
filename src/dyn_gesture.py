import numpy as np
import pyautogui

class Gesture():
    """
    Dynamic Gesture recognition for a single hand using
    Google's Mediapipe HandTracking.
    Currently supports two gestures, swipe left and scroll upself.

    Args:
    connections: list of tuple conta joints of hand
    """

    def __init__(self,connections):

        # Middle-finger tracked currently. Change
        # index_tip to change the joint to be tracked
        self.index_tip = connections[9][1]
        self.base_tip = connections[0][0]
        self.timestamp = None
        self.tip_pos = []
        self.base_pos = []
        self.flag = 0
        self.t = 0
        self.write = None

    def getdiff(self):
        """
        1sec wait time before next gesture inferred
        """
        if (self.timestamp[-1] - self.t) > 1000 :
            self.flag = 0
        else:
            self.flag = 1

    def swipe(self):
        """
        Passes right arrow key if hand left swipe gesture detected

        Returns:
        1 - if swipe detected
        0 - if swipe not detected
        """

        check_left_frame = self.tip_pos[-1][0] > self.base_pos[-1][0]
        check_right_frame = self.tip_pos[len(self.tip_pos)-2][0] < self.base_pos[len(self.base_pos)-2][0]
        diff_tip_tip = self.tip_pos[-1][0] -  self.tip_pos[len(self.tip_pos)-2][0]
        diff_tip_base = self.tip_pos[-1][0] - self.base_pos[-1][0]

        if check_left_frame and check_right_frame:
            if diff_tip_tip > 50 and diff_tip_base > 30:
                print("Left Swipe")
                pyautogui.typewrite(["right"])
                return 1
        return 0

    def scroll(self):
        """
        Passes up arrow key if hand up-down gesture detected

        Returns:
        1 - if swipe detected
        0 - if scroll not detected
        """
        disp = self.tip_pos[-1][1] - self.tip_pos[len(self.tip_pos)-2][1]
        if disp >= 100:
            print("scroll up")
            pyautogui.typewrite(["up"])
            return 1
        return 0

    def update_time(self,timestamp_val):
        """
        Updates timestamps of new frames
        Updates flag
        """

        self.timestamp.append(timestamp_val)
        self.getdiff()

    def update_points(self,points):
        """
        Updates position of finger and base

        Args:
        points: array containing coordinates of joints
        """

        self.tip_pos.append(points[self.index_tip])
        self.base_pos.append(points[self.base_tip])

    def get_gesture(self):
        """
        Detects 1 of 2 gestures
        """
        if self.flag == 0:
            self.flag = self.swipe()
            if self.flag == 1:
                self.t = self.timestamp[-1]
                self.write = "Left Swipe"
            else:
                self.flag = self.scroll()
                if self.flag == 1:
                    self.t = self.timestamp[-1]
                    self.write = "scroll up"
