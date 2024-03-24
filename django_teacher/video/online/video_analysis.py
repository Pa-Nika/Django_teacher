import datetime
import threading

import cv2
import pandas as pd

from gaze_tracking import GazeTracking
from .. import set_marks
from ..upload import constants


class OnlineVideoAnalyzer(object):
    def __init__(self, detector, predictor):
        self.detector = detector
        self.predictor = predictor
        self.cap = cv2.VideoCapture(0)
        self.out_full_video = None
        self.is_stop = False
        self.thread = None
        self.frame_counter = 0  # Счетчик кадров
        self.frame_rate = 2  # Желаемая частота кадров в секунду
        self.face_count = None
        self.df_video = pd.DataFrame(columns=set_marks.get_list_name_columns())
        self.gaze = GazeTracking(predictor, detector)


    def get_df(self):
        return self.df_video
    def check_face_count(self, duration) -> bool:
        if len(self.face_count) > 1:
            self.fill_bad_marks_many_faces(duration)
            return False
        elif len(self.face_count) == 0:
            self.fill_bad_marks_not_face(duration)
            return False
        return True

    def fill_bad_marks_not_face(self, duration):
        data_from_frame = [0] * (len(set_marks.get_list_name_columns()) - 1)
        data_from_frame.append(duration)
        self.df_video.loc[len(self.df_video.index)] = data_from_frame

    def fill_bad_marks_many_faces(self, duration):
        data_from_frame = [-1] * (len(set_marks.get_list_name_columns()) - 1)
        data_from_frame.append(duration)
        self.df_video.loc[len(self.df_video.index)] = data_from_frame

    def set_params_video(self, height, width):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out_full_video = cv2.VideoWriter('output.avi', fourcc, 20.0, (width, height))

    def set_stop(self):
        self.is_stop = True
        self.cap.release()
        # self.out_full_video.release()
        cv2.destroyAllWindows()

    def set_active(self):
        self.is_stop = False

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

    def duration_frame(self, frame_now):
        duration = frame_now / self.cap.get(cv2.CAP_PROP_FPS)
        duration_str = str(datetime.timedelta(seconds=int(duration)))
        return duration_str

    def eyes_mark(self, img, data_from_frame):
        mark_eyes = 5
        self.gaze.refresh(img)
        ratio_hor = self.gaze.horizontal_ratio()
        ratio_ver = self.gaze.vertical_ratio()

        if ratio_hor is None or ratio_ver is None:
            data_from_frame.append(None)
            return data_from_frame

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

    def some_tmp_init(self):
        self.cap.release()  # Освобождаем видео поток
        self.cap = cv2.VideoCapture(0)
        self.df_video = pd.DataFrame(columns=set_marks.get_list_name_columns())
        self.frame_counter = 0

    def read_video(self):
        self.some_tmp_init()

        flag, frame = self.cap.read()
        if flag:
            height, width, _ = frame.shape
            self.set_params_video(height, width)
        else:
            exit()

        while not self.is_stop and self.cap.isOpened():
            flag, frame = self.cap.read()
            self.out_full_video.write(frame)
            self.frame_counter += 1
            if flag:
                fps = self.cap.get(cv2.CAP_PROP_FPS)
                if fps != 0:
                    frames_per_desired_second = fps / self.frame_rate
                    if self.frame_counter % int(frames_per_desired_second) == 0:
                        duration = self.duration_frame(self.frame_counter)
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        self.face_count = self.detector(gray)
                        if not self.check_face_count(duration):
                            continue
                        self.fill_df(gray, frame, duration)

            else:
                break

        self.fill_marks()
        self.set_stop()
        print(self.df_video.iloc[-60:-1, -5:-1])
        self.set_active()
        return
