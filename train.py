import torch
from ultralytics import YOLO

device = "cuda" if torch.cuda.is_available() else "cpu"
model = YOLO("yolo11n.pt").to(device)

if __name__ == '__main__':
    model.train(data = "data_01.yaml", epochs = 100, batch = 0.7, device = 0, plots = True)