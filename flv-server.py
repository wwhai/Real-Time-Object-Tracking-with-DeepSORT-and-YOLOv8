import cv2
from flask import Flask, Response
from flask_cors import CORS  # 导入CORS扩展

app = Flask(__name__)

CORS(app)


def generate():
    cap = cv2.VideoCapture(0)  # 摄像头设备号，也可以是视频文件路径
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read frame.")
            break

        # 将帧转换为JPEG格式
        ret, jpeg = cv2.imencode(".jpg", frame)
        frame_bytes = jpeg.tobytes()

        # 将帧写入到响应中，并使用multipart格式
        yield (
            b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
        )


@app.route("/")
def index():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(debug=True)
