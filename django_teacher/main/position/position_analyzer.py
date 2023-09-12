import cv2

from ..constants import *


class PositionAnalysis(object):
    def __init__(self, path, detector, predictor):
        self.detector = detector
        self.predictor = predictor
        self.path = path
        self.df_diff = None
        self.df = None

    def analyse(self):
        cap = cv2.VideoCapture(self.path)
        frame_number = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print("YES" + '\n' * 10 + "YES")
        dim = (WIDTH, HEIGHT)

        while cap.isOpened():
            flag, frame = cap.read()
            if not flag:
                break

            frame = cv2.resize(frame, dim)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Проверяем количество лиц на изображении
            faces = self.detector(gray)
            if len(faces) > 1:
                # self.textEdit.setText("Много людей в кадре!")
                flag = False
            elif len(faces) == 0:
                # self.textEdit.setText("Невозможно разобрать лицо!")
                flag = False

            for face in faces:
                if not flag:
                    flag = True
                    continue

                # Получение координат контрольных точек и их построение на изображении
                landmarks = self.predictor(gray, face)

                # нижняя точка
                x_9 = landmarks.part(8).x
                y_9 = landmarks.part(8).y
                cv2.circle(frame, (x_9, y_9), 3, (255, 0, 0), -1)

                # Точка между глазами
                x_27 = landmarks.part(27).x
                y_27 = landmarks.part(27).y
                cv2.circle(frame, (x_27, y_27), 3, (255, 0, 0), -1)

                # Левая точка
                x_0 = landmarks.part(0).x
                y_0 = landmarks.part(0).y
                cv2.circle(frame, (x_0, y_0), 3, (255, 0, 0), -1)

                # Правая точка
                x_16 = landmarks.part(16).x
                y_16 = landmarks.part(16).y
                cv2.circle(frame, (x_16, y_16), 3, (255, 0, 0), -1)

                if y_9 > HEIGHT * 0.75:
                    print("Голова слишком низко")
                elif y_27 < HEIGHT * 0.25:
                    print("Голова слишком высоко")
                elif x_0 < WIDTH * 0.25:
                    print("Голова слишком слева")
                elif x_16 > WIDTH * 0.75:
                    print("Голова слишком справа")
                elif abs(x_27 - x_0) < WIDTH * 0.05:
                    print("Голова повернута влево")
                elif abs(x_27 - x_16) < WIDTH * 0.05:
                    print("Голова повернута вправо")
                else:
                    print("Все хорошо!")

        cap.release()
        cv2.destroyAllWindows()


