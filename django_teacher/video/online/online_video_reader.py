import cv2
from django.http import JsonResponse, HttpResponse


class OnlineVideoReader(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.out_full_video = None
        self.is_stop = False
        self.thread = None

    def set_params_video(self, height, width):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # self.out_full_video = cv2.VideoWriter('output.avi', fourcc, 20.0, (width, height))

    def set_stop(self):
        self.is_stop = True
        self.cap.release()
        # self.out_full_video.release()
        cv2.destroyAllWindows()

    def rectangle(self, frame, height, width):
        # Определение координат для квадрата
        center = round(width / 2)
        x1 = int(center - (center * 0.3))
        y1 = int(height * 0.3)
        x2 = int(center + (center * 0.3))
        y2 = int(height * 0.33)

        # Нарисуем квадрат на изображении
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), thickness=2)

    def read_video(self):
        flag, frame = self.cap.read()
        if flag:
            height, width, _ = frame.shape
            self.set_params_video(height, width)
        else:
            exit()

        while not self.is_stop and self.cap.isOpened():
            flag, frame = self.cap.read()
            if flag:
                self.rectangle(frame, height, width)
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

            if (cv2.getWindowProperty('frame', cv2.WND_PROP_VISIBLE) < 1) | self.is_stop:
                break

        self.set_stop()

