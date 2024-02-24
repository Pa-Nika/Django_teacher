import datetime
import cv2
import pandas as pd

from . import constants
from gaze_tracking import GazeTracking

gaze = GazeTracking()


def get_list_name_columns() -> list:
    name_columns = []
    for i in constants.ARRAY_OF_POINTS:
        name_columns.append(str(i) + '_x')
        name_columns.append(str(i) + '_y')
    name_columns.append('square')
    name_columns.append('width')
    name_columns.append('height')
    name_columns.append('duration')
    return name_columns


def square_mark(row) -> int:
    square = row['height'] * row['width']
    limit_5_up, limit_5_bottom = square * 0.09, square * 0.13
    limit_4_up, limit_4_bottom = square * 0.08, square * 0.14
    limit_3_up, limit_3_bottom = square * 0.06, square * 0.15
    if (row['square'] > limit_5_up) & (row['square'] < limit_5_bottom):
        return 5
    elif (row['square'] > limit_4_up) & (row['square'] < limit_4_bottom):
        return 4
    elif (row['square'] > limit_3_up) & (row['square'] < limit_3_bottom):
        return 3
    else:
        return 2


def ver_mark(row) -> int:
    up = row['height']
    limit_5_up, limit_5_bottom = up * 0.3, up * 0.33
    limit_4_up, limit_4_bottom = up * 0.28, up * 0.33
    limit_3_up, limit_3_bottom = up * 0.19, up * 0.34
    if (row['28_y'] > limit_5_up) & (row['28_y'] < limit_5_bottom):
        return 5
    elif (row['28_y'] > limit_4_up) & (row['28_y'] < limit_4_bottom):
        return 4
    elif (row['28_y'] > limit_3_up) & (row['28_y'] < limit_3_bottom):
        return 3
    else:
        return 2


def hor_mark(row) -> int:
    center = round(row['width'] / 2)
    limit_5, limit_4, limit_3 = center * 0.03, center * 0.05, center * 0.08
    if (row['28_x'] > center - limit_5) & (row['28_x'] < center + limit_5):
        return 5
    elif (row['28_x'] > center - limit_4) & (row['28_x'] < center + limit_4):
        return 4
    elif (row['28_x'] > center - limit_3) & (row['28_x'] < center + limit_3):
        return 3
    else:
        return 2


class PositionAnalyzer(object):
    def __init__(self, path, detector, predictor):
        self.detector = detector
        self.predictor = predictor
        self.face_count = None
        self.cap = cv2.VideoCapture(path)
        self.frames_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.MAE_error = 0
        self.df_video = pd.DataFrame(columns=get_list_name_columns())

    def check_face_count(self) -> bool:
        if len(self.face_count) > 1:
            print("Много людей в кадре!")
            return False
        elif len(self.face_count) == 0:
            print("Невозможно разобрать лицо!")
            return False
        return True

    def fill_df(self, gray, img, duration):
        for face in self.face_count:
            landmarks = self.predictor(gray, face)
            data_from_frame = []
            for n in constants.ARRAY_OF_POINTS:
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                data_from_frame.append(x)
                data_from_frame.append(y)
            face_area = abs(face.right() - face.left()) * abs(face.top() - face.bottom())

            data_from_frame.append(face_area)
            data_from_frame.append(img.shape[1])
            data_from_frame.append(img.shape[0])
            data_from_frame.append(duration)

            # gaze.refresh(img)
            # left = gaze.pupil_left_coords()
            # right = gaze.pupil_right_coords()
            # if left is None and right is None:
            #     print(f'None!!!!')

            # data_from_frame.append(int(left[0]))
            # data_from_frame.append(int(left[1]))
            # data_from_frame.append(int(right[0]))
            # data_from_frame.append(int(right[1]))
            self.df_video.loc[len(self.df_video.index)] = data_from_frame
        return

    def duration_frame(self, frame_now):
        duration = frame_now / self.fps
        duration_str = str(datetime.timedelta(seconds=int(duration)))
        return duration_str

    def fill_marks(self):
        for i in range(len(self.df_video)):
            hor = self.df_video.loc[i, 'hor_mark'] = hor_mark(self.df_video.iloc[i])
            ver = self.df_video.loc[i, 'ver_mark'] = ver_mark(self.df_video.iloc[i])
            square = self.df_video.loc[i, 'square_mark'] = square_mark(self.df_video.iloc[i])
            self.df_video.loc[i, 'mark'] = (hor + ver + square) / 3

    def analyse(self) -> pd.DataFrame:
        frame_now = 0

        while frame_now < self.frames_count:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_now)
            flag, img = self.cap.read()
            frame_now += self.fps / 2
            if not flag:
                break

            duration = self.duration_frame(frame_now)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            self.face_count = self.detector(gray)
            if not self.check_face_count:
                print('Я еще не знаю, что в этом случае делать...')

            self.fill_df(gray, img, duration)

        self.fill_marks()
        self.cap.release()
        cv2.destroyAllWindows()

        print(self.df_video)
        return self.df_video
