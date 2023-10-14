import cv2
# from math import abs
# from django_teacher.main.constants import *


class PositionAnalyzer(object):
    def __init__(self, path, detector, predictor):
        self.detector = detector
        self.predictor = predictor
        self.face_count = None
        self.array_of_points = {1, 2, 9, 16, 17, 37, 46}
        self.cap = cv2.VideoCapture(path)
        self.frames_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.frame_area = 0
        self.MAE_error = 0

    def check_face_count(self) -> bool:
        if len(self.face_count) > 1:
            print("Много людей в кадре!")
            return False
        elif len(self.face_count) == 0:
            print("Невозможно разобрать лицо!")
            return False

        return True

    def analyse(self):
        frame_now = 0
        while frame_now < self.frames_count:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_now)
            flag, img = self.cap.read()
            frame_now += self.fps / 2
            if not flag:
                break
            self.frame_area = img.shape[1] * img.shape[0]
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            self.face_count = self.detector(gray)
            if not self.check_face_count:
                print('Я еще не знаю, что в этом случае делать...')

            for face in self.face_count:
                landmarks = self.predictor(gray, face)
                for n in self.array_of_points:
                    x = landmarks.part(n).x
                    y = landmarks.part(n).y

                face_area = abs(face.right() - face.left()) * abs(face.top() - face.bottom())
                print(f"Площадь лица {face_area}, площадь кадра {self.frame_area}, размеры кадра {img.shape[1]} на {img.shape[0]}")

        self.cap.release()
        cv2.destroyAllWindows()
