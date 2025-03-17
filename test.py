import torch
from ultralytics import YOLO

import os



device = "cuda" if torch.cuda.is_available() else "cpu"
model = YOLO("best.pt").to(device)

# Perform inference on the downloaded video
results = model.predict(source="videoplayback (2).mp4", save=True, project="runs/detect", name="exp", show=True)
