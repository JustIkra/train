import torch

from ultralytics import YOLO

device = "cuda" if torch.cuda.is_available() else "cpu"
model = YOLO("best.pt").to(device)

results = model.predict(source="video.mp4", save=True, project="runs/detect", name="exp", show=True)
