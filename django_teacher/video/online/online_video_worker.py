import base64

import cv2
from django.http import JsonResponse, HttpResponse


class OnlineVideoWorker(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.out_full_video = None

    def set_preview(self):
        while self.cap.isOpened():
            flag, frame = self.cap.read()
            if flag:
                _, buffer = cv2.imencode('.jpg', frame)
                frame_base64 = base64.b64encode(buffer).decode('utf-8')
                self.cap.release()
                print(JsonResponse(frame_base64, safe=False))
                return JsonResponse(frame_base64, safe=False)
            else:
                self.cap.release()
                print("NO")
                return JsonResponse({'error': 'Не удалось получить кадр'}, status=500)

    # def generate_video_stream(self):
    #     while self.cap.isOpened():
    #         flag, frame = self.cap.read()
    #         if flag:
    #             _, buffer = cv2.imencode('.jpg', frame)
    #             frame_base64 = base64.b64encode(buffer).decode('utf-8')
    #             yield frame_base64
    #         else:
    #             break

    # def video_stream(self, request):
    #     self.cap = cv2.VideoCapture(0)
    #     if not self.cap.isOpened():
    #         return JsonResponse({'error': 'Не удалось открыть камеру'}, status=500)
    #
    #     response = JsonResponse({'status': 'OK'})
    #     response['X-Accel-Buffering'] = 'no'
    #     response['Content-Type'] = 'multipart/x-mixed-replace; boundary=frame'
    #
    #     def generate():
    #         for frame in self.generate_video_stream():
    #             yield (b'--frame\r\n'
    #                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    #
    #     return HttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')

    def set_params_video(self, height, width):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out_full_video = cv2.VideoWriter('output.avi', fourcc, 20.0, (width, height))

    def read_video(self):
        flag, frame = self.cap.read()
        if flag:
            height, width, _ = frame.shape
            self.set_params_video(height, width)
        else:
            exit()

        while self.cap.isOpened():
            flag, frame = self.cap.read()

            if flag:
                self.out_full_video.write(frame)

                cv2.imshow('frame', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        # Освобождаем ресурсы
        self.cap.release()
        self.out_full_video.release()
        cv2.destroyAllWindows()
