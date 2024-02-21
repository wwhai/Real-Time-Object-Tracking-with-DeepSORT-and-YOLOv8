from ultralytics import YOLO

model = YOLO("yolov8n.pt")

source = "rtsp://192.168.1.210:554/av0_0"

results = model(source, stream=True)
print(results)
