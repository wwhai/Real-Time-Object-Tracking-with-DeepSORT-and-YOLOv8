# Copyright (C) 2024 wwhai
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess
import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
results = model("rtsp://192.168.10.244:554/av0_0", stream=True)
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
    str(25),  # 帧率
    "-i",
    "-",  # 输入数据来自标准输入流
    "-c:v",
    "libx264",
    # "-preset",
    # "superfast",  # 编码速度
    "-crf",
    "30",  # 编码质量（0-51，越小质量越高）
    # "-tune",
    # "zerolatency",  # 零延迟
    "-f",
    "mpegts",  # 输出为 MPEG-TS 格式
    "http://127.0.0.1:9400/stream/ffmpegPush?liveId=AAA",
]
ffmpegProcess = subprocess.Popen(
    ffmpeg_command, stdin=subprocess.PIPE, stdout=None, stderr=None
)
print("ffmpegProcess==>", " ".join(ffmpeg_command))
while True:
    for result in results:
        annotated_frame = result.plot()
        if ffmpegProcess.returncode is None:
            ffmpegProcess.stdin.write(annotated_frame.tobytes())
        resized_image = cv2.resize(annotated_frame, (640, 480))
        cv2.imshow("YOLOv8 Inference", resized_image)
        # boxes = result.boxes
        # probs = result.probs
        # print(probs)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
cap.release()
cv2.destroyAllWindows()
ffmpegProcess.kill()