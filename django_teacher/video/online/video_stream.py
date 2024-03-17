# import base64
#
# import cv2
#
#
# class VideoStream:
#     def __init__(self):
#         self.cap = cv2.VideoCapture(0)
#
#     def __del__(self):
#         self.cap.release()
#
#     def get_frame(self):
#         ret, frame = self.cap.read()
#         if ret:
#             _, buffer = cv2.imencode('.jpg', frame)
#             image_data = buffer.tobytes()
#             return base64.b64encode(image_data).decode('utf-8')
#         else:
#             return None
