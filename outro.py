# pip install ultralytics
from ultralytics import YOLO

modelo = YOLO("yolov8n.pt")
modelo.predict(
    source=0, 
    show=True,
    conf=0.65,
    iou=0.55,
    max_det=20
)

# TO-DO: OOP | TEST RPI 4.