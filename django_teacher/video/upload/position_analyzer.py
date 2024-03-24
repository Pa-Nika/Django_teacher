import datetime
import cv2
import pandas as pd

from . import constants
from gaze_tracking import GazeTracking
from .. import set_marks


class PositionAnalyzer(object):
    def __init__(self, path, detector, predictor):
        self.detector = detector
        self.predictor = predictor
        self.face_count = None
        self.cap = cv2.VideoCapture(path)
        self.frames_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.MAE_error = 0
        self.df_video = pd.DataFrame(columns=set_marks.get_list_name_columns())
        self.gaze = GazeTracking(predictor, detector)

    def check_face_count(self, duration) -> bool:
        if len(self.face_count) > 1:
            self.fill_bad_marks_many_faces(duration)
            return False
        elif len(self.face_count) == 0:
            self.fill_bad_marks_not_face(duration)
            return False
        return True

    def eyes_mark(self, img, data_from_frame):
        mark_eyes = 5
        self.gaze.refresh(img)
        ratio_hor = self.gaze.horizontal_ratio()
        ratio_ver = self.gaze.vertical_ratio()

        if ratio_hor is None or ratio_ver is None:
            data_from_frame.append(None)
            return data_from_frame
        print(f'ratio глаз: ratio_hor {ratio_hor} ratio_ver {ratio_ver}')

        if ratio_hor <= constants.HOR_LEFT_3_LIMIT or ratio_hor >= constants.HOR_RIGHT_3_LIMIT:
            mark_eyes = 3
        elif ratio_hor <= constants.HOR_LEFT_4_LIMIT or ratio_hor >= constants.HOR_RIGHT_4_LIMIT:
            mark_eyes = 4
        elif ratio_ver <= constants.VER_UP_3_LIMIT or ratio_ver >= constants.VER_DOWN_3_LIMIT:
            mark_eyes = 3
        elif ratio_ver <= constants.VER_UP_4_LIMIT or ratio_ver >= constants.VER_DOWN_4_LIMIT:
            mark_eyes = 4
        data_from_frame.append(mark_eyes)
        return data_from_frame

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
            data_from_frame = self.eyes_mark(img, data_from_frame)
            data_from_frame.append(duration)
            self.df_video.loc[len(self.df_video.index)] = data_from_frame
        return

    def duration_frame(self, frame_now):
        duration = frame_now / self.fps
        duration_str = str(datetime.timedelta(seconds=int(duration)))
        return duration_str

    def fill_marks(self):
        for i in range(len(self.df_video)):
            hor = self.df_video.loc[i, 'hor_mark'] = set_marks.hor_mark(self.df_video.iloc[i])
            ver = self.df_video.loc[i, 'ver_mark'] = set_marks.ver_mark(self.df_video.iloc[i])
            square = self.df_video.loc[i, 'square_mark'] = set_marks.square_mark(self.df_video.iloc[i])
            eye = self.df_video.loc[i, 'eye_mark']
            if eye is not None:
                self.df_video.loc[i, 'mark'] = (hor + ver + square + eye) / 4
            else:
                self.df_video.loc[i, 'mark'] = (hor + ver + square) / 3

    def fill_bad_marks_not_face(self, duration):
        data_from_frame = [0] * (len(set_marks.get_list_name_columns()) - 1)
        data_from_frame.append(duration)
        self.df_video.loc[len(self.df_video.index)] = data_from_frame

    def fill_bad_marks_many_faces(self, duration):
        data_from_frame = [-1] * (len(set_marks.get_list_name_columns()) - 1)
        data_from_frame.append(duration)
        self.df_video.loc[len(self.df_video.index)] = data_from_frame

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
            if not self.check_face_count(duration):
                continue

            self.fill_df(gray, img, duration)

        self.fill_marks()
        self.cap.release()
        cv2.destroyAllWindows()

        # print(self.df_video.iloc[-60:-1, -5:-1])
        return self.df_video
