import cv2
import numpy as np


woman_path = './woman.mp4' # 합성 대상
background_path = './london_street.mp4' # 배경

# 영상 파일 불러오기
woman_video = cv2.VideoCapture(woman_path)
background_video = cv2.VideoCapture(background_path)

ret, background_frame = background_video.read()
if not ret:
    print("불러오기 실패")
    woman_video.release()
    background_video.release()
    cv2.destroyAllWindows()
    exit()

ret, foreground_frame = woman_video.read()
if not ret:
    print("불러오기 실패")
    woman_video.release()
    background_video.release()
    cv2.destroyAllWindows()
    exit()


while True:

    ret, foreground_frame = woman_video.read()
    ret_bg, background_frame = background_video.read()

    if not ret or not ret_bg:
        break


    background_frame = cv2.resize(background_frame, (foreground_frame.shape[1], foreground_frame.shape[0]))


    hsv = cv2.cvtColor(foreground_frame, cv2.COLOR_BGR2HSV)


    lower_green = np.array([50, 100, 100])
    upper_green = np.array([70, 255, 255])


    mask = cv2.inRange(hsv, lower_green, upper_green)
    mask_inv = cv2.bitwise_not(mask)


    foreground = cv2.bitwise_and(foreground_frame, foreground_frame, mask=mask_inv)
    background = cv2.bitwise_and(background_frame, background_frame, mask=mask)


    combined_frame = cv2.add(foreground, background)

    cv2.imshow('Combined Video', combined_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break
    elif key == 32:  # 스페이스바
        cv2.waitKey(0)  # 영상 일시 정지

woman_video.release()
background_video.release()
cv2.destroyAllWindows()
