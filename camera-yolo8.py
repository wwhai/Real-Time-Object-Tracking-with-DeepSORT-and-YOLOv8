import cv2
from ultralytics import YOLO
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# device = torch.device("cpu")
# Load the YOLOv8 model
model = YOLO("./yolov8n.pt").to(device=device)

clazz = model.names

# Open the video file
video_path = "rtsp://192.168.1.210:554/av0_0"
# results = model.predict(video_path, verbose=False, stream=True)
# while True:
#     for result in results:
#         boxes = result.boxes
#         probs = result.probs
cap = cv2.VideoCapture(video_path)
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
ffmpeg_command = [
    "ffmpeg",
    "-err_detect",
    "ignore_err",
    "-y",  # 覆盖输出文件而无需询问
    "-f",
    "rawvideo",
    "-pix_fmt",
    "bgr24",
    "-s",
    "1920x1080",  # 视频分辨率
    "-r",
    str(fps),  # 帧率
    "-i",
    "-",  # 输入数据来自标准输入流
    "-c:v",
    "libx264",
    "-preset",
    "superfast",  # 编码速度
    "-crf",
    "30",  # 编码质量（0-51，越小质量越高）
    "-tune",
    "zerolatency",  # 零延迟
    "-f",
    "flv",  # 输出为 MPEG-TS 格式
    "rtmp://127.0.0.1:1935/live/testv001",
]

import subprocess

# 定义文本和字体参数
text = "Warning: Found person"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 3
font_thickness = 10

# 获取文本的大小
text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
# 计算文本的位置，使其位于图像中央
text_x = (width - text_size[0]) // 2
text_y = (height + text_size[1]) // 2

print(" ".join(ffmpeg_command))
ffmpegProcess = subprocess.Popen(
    ffmpeg_command, stdin=subprocess.PIPE, stdout=None, stderr=None
)
while cap.isOpened():
    success, frame = cap.read()
    if success:
        # 这里应该调用Rpc
        # results = grpc.CallPredict(frame, verbose=False)
        results = model.predict(frame, verbose=False)
        annotated_frame = results[0].plot()
        for result in results:
            for boxes in result.boxes:
                boxesClazz = clazz[int(boxes.cls.item())]
                # print(boxesClazz)
                if boxesClazz == "person":
                    cv2.putText(
                        annotated_frame,
                        text,
                        (text_x, text_y),
                        font,
                        font_scale,
                        (0, 0, 255),
                        font_thickness,
                    )
        resized_image = cv2.resize(annotated_frame, (960, 640))
        cv2.imshow("YOLOv8 Inference", resized_image)
        if ffmpegProcess.returncode is None:
            ffmpegProcess.stdin.write(annotated_frame.tobytes())
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
ffmpegProcess.kill()
