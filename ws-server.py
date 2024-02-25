import cv2
import asyncio
import websockets
import numpy as np
from av.video.stream import VideoStream
from av.container.flv import FLVMuxer
from io import BytesIO


async def send_video(websocket, path):
    # 打开摄像头
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return

    try:
        while True:
            # 读取摄像头帧
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to read frame.")
                break

            # 编码为FLV格式
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = np.flipud(img)
            stream = VideoStream(width=img.shape[1], height=img.shape[0], rate=30)
            packet = stream.encode(img.tobytes())
            muxer = FLVMuxer("output.flv")
            muxer.mux(packet)

            # 发送视频流给客户端
            with open("output.flv", "rb") as f:
                video_data = f.read()
                await websocket.send(video_data)
    finally:
        # 关闭摄像头
        cap.release()


# 启动WebSocket服务器
start_server = websockets.serve(send_video, "localhost", 8765)

# 运行事件循环
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
