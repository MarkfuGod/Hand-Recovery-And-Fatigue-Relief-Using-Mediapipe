
import argparse
import sys
import time

import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


# Global variables to calculate FPS
COUNTER, FPS = 0, 0
START_TIME = time.time()


def run(model: str, num_hands: int,
        min_hand_detection_confidence: float,
        min_hand_presence_confidence: float, min_tracking_confidence: float,
        camera_id: int, width: int, height: int) -> None:

  # 从摄像头捕捉手势
  cap = cv2.VideoCapture(camera_id)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

  # 可视化参数
  row_size = 50  # pixels
  left_margin = 24  # pixels
  text_color = (0, 0, 0)  # black
  font_size = 1
  font_thickness = 1
  fps_avg_frame_count = 10

  # 窗格参数
  label_text_color = (255, 255, 255)  # white
  label_font_size = 1
  label_thickness = 2

  recognition_frame = None
  recognition_result_list = []

  def save_result(result: vision.GestureRecognizerResult,
                  unused_output_image: mp.Image, timestamp_ms: int):
      global FPS, COUNTER, START_TIME

      #计算FPS
      if COUNTER % fps_avg_frame_count == 0:
          FPS = fps_avg_frame_count / (time.time() - START_TIME)
          START_TIME = time.time()

      recognition_result_list.append(result)
      COUNTER += 1

  # 初始化手势识别模型
  base_options = python.BaseOptions(model_asset_path=model)
  options = vision.GestureRecognizerOptions(base_options=base_options,
                                          running_mode=vision.RunningMode.LIVE_STREAM,
                                          num_hands=num_hands,
                                          min_hand_detection_confidence=min_hand_detection_confidence,
                                          min_hand_presence_confidence=min_hand_presence_confidence,
                                          min_tracking_confidence=min_tracking_confidence,
                                          result_callback=save_result)
  recognizer = vision.GestureRecognizer.create_from_options(options)

  # 持续从摄像头捕捉图像并进行推理
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      sys.exit(
          'ERROR: Unable to read from webcam. Please verify your webcam settings.'
      )

    image = cv2.flip(image, 1)

    # 将图像从BGR转换为RGB，与TFLite模型所需的格式相匹配
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

    # 使用模型运行手势识别
    recognizer.recognize_async(mp_image, time.time_ns() // 1_000_000)

    # 显示FPS
    fps_text = 'FPS = {:.1f}'.format(FPS)
    text_location = (left_margin, row_size)
    current_frame = image
    cv2.putText(current_frame, fps_text, text_location, cv2.FONT_HERSHEY_DUPLEX,
                font_size, text_color, font_thickness, cv2.LINE_AA)

    if recognition_result_list:
      # 绘制关键点并为每只手写入文本
      for hand_index, hand_landmarks in enumerate(
          recognition_result_list[0].hand_landmarks):
        # 计算手的边界框
        x_min = min([landmark.x for landmark in hand_landmarks])
        y_min = min([landmark.y for landmark in hand_landmarks])
        y_max = max([landmark.y for landmark in hand_landmarks])

        # 将归一化坐标转换为像素值
        frame_height, frame_width = current_frame.shape[:2]
        x_min_px = int(x_min * frame_width)
        y_min_px = int(y_min * frame_height)
        y_max_px = int(y_max * frame_height)

        # 获取手势分类结果
        if recognition_result_list[0].gestures:
          gesture = recognition_result_list[0].gestures[hand_index]
          category_name = gesture[0].category_name
          score = round(gesture[0].score, 2)
          result_text = f'{category_name} ({score})'

          # 计算文本大小
          text_size = \
          cv2.getTextSize(result_text, cv2.FONT_HERSHEY_DUPLEX, label_font_size,
                          label_thickness)[0]
          text_width, text_height = text_size

          # 计算文本位置（在手的上方）
          text_x = x_min_px
          text_y = y_min_px - 10  

          #确保文本在帧边界内
          if text_y < 0:
            text_y = y_max_px + text_height

          # 绘制文本
          cv2.putText(current_frame, result_text, (text_x, text_y),
                      cv2.FONT_HERSHEY_DUPLEX, label_font_size,
                      label_text_color, label_thickness, cv2.LINE_AA)

        # 在帧上绘制手部关键点
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
          landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y,
                                          z=landmark.z) for landmark in
          hand_landmarks
        ])
        mp_drawing.draw_landmarks(
          current_frame,
          hand_landmarks_proto,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style())

      recognition_frame = current_frame
      recognition_result_list.clear()

    if recognition_frame is not None:
        cv2.imshow('gesture_recognition', recognition_frame)

    # 如果按下ESC键，则停止程序
    if cv2.waitKey(1) == 27:
        break

  recognizer.close()
  cap.release()
  cv2.destroyAllWindows()


def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model',
      help='Name of gesture recognition model.',
      required=False,
      default='gesture_recognizer.task')
  parser.add_argument(
      '--numHands',
      help='Max number of hands that can be detected by the recognizer.',
      required=False,
      default=1)
  parser.add_argument(
      '--minHandDetectionConfidence',
      help='The minimum confidence score for hand detection to be considered '
           'successful.',
      required=False,
      default=0.5)
  parser.add_argument(
      '--minHandPresenceConfidence',
      help='The minimum confidence score of hand presence score in the hand '
           'landmark detection.',
      required=False,
      default=0.5)
  parser.add_argument(
      '--minTrackingConfidence',
      help='The minimum confidence score for the hand tracking to be '
           'considered successful.',
      required=False,
      default=0.5)
  
  parser.add_argument(
      '--cameraId', help='Id of camera.', required=False, default=0)
  parser.add_argument(
      '--frameWidth',
      help='Width of frame to capture from camera.',
      required=False,
      default=640)
  parser.add_argument(
      '--frameHeight',
      help='Height of frame to capture from camera.',
      required=False,
      default=480)
  args = parser.parse_args()

  run(args.model, int(args.numHands), args.minHandDetectionConfidence,
      args.minHandPresenceConfidence, args.minTrackingConfidence,
      int(args.cameraId), args.frameWidth, args.frameHeight)


if __name__ == '__main__':
  main()
