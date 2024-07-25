import cv2
from ultralytics import YOLO
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = YOLO("./yolov8n.pt").to(device=device)
clazz = model.names
rtsp_path = "rtsp://192.168.10.244:554/av0_0"
results = model(rtsp_path, stream=True)

while True:

    for result in results:
        annotated_frame = result.plot()
        resized_image = cv2.resize(annotated_frame, (640, 480))
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        cv2.imshow("YOLOv8 Inference", resized_image)

cv2.destroyAllWindows()
