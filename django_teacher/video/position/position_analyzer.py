import cv2
import pandas as pd

from . import constants
from gaze_tracking import GazeTracking

gaze = GazeTracking()


class PositionAnalyzer(object):
    def __init__(self, path, detector, predictor):
        self.detector = detector
        self.predictor = predictor
        self.face_count = None
        self.cap = cv2.VideoCapture(path)
        self.frames_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.MAE_error = 0
        self.df_video = pd.DataFrame(columns=constants.LIST_FOR_DATA)

    def check_face_count(self) -> bool:
        if len(self.face_count) > 1:
            print("Много людей в кадре!")
            return False
        elif len(self.face_count) == 0:
            print("Невозможно разобрать лицо!")
            return False

        return True

    def fill_df(self, gray, img):
        for face in self.face_count:
            landmarks = self.predictor(gray, face)
            data_from_frame = []
            for n in constants.ARRAY_OF_POINTS:
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                data_from_frame.append(x)
                data_from_frame.append(y)
            face_area = abs(face.right() - face.left()) * abs(face.top() - face.bottom())

            gaze.refresh(img)
            left = gaze.pupil_left_coords()
            right = gaze.pupil_right_coords()
            if left is None and right is None:
                print(f'None!!!!')

            data_from_frame.append(face_area)
            data_from_frame.append(int(left[0]))
            data_from_frame.append(int(left[1]))
            data_from_frame.append(int(right[0]))
            data_from_frame.append(int(right[1]))
            self.df_video.loc[len(self.df_video.index)] = data_from_frame
        return

    def check_algorithm(self, third_vertical):
        # 37 и 46 по вертикали
        vertical_points_error = min(self.df_video['37_y'], self.df_video['46_y'])
            # ((abs(self.df_video['37_y'] - self.df_video['46_y']) / 2) +
            #                       min(self.df_video['37_y'], self.df_video['46_y']))
        print(vertical_points_error)
        return

    def analyse(self):
        frame_now = 0
        third_vertical = 0
        while frame_now < self.frames_count:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_now)
            flag, img = self.cap.read()
            frame_area = img.shape[1] * img.shape[0]
            third_vertical = img[constants.VERTICAL] / 3
            frame_now += self.fps / 2
            if not flag:
                break

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            self.face_count = self.detector(gray)
            if not self.check_face_count:
                print('Я еще не знаю, что в этом случае делать...')

            self.fill_df(gray, img)
        # self.check_algorithm(third_vertical)

        print(self.df_video)
        self.cap.release()
        cv2.destroyAllWindows()
