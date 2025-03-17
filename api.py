from fastapi import FastAPI, File,UploadFile, Response, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import torch
import numpy as np
from ultralytics import YOLO
import cv2
from io import BytesIO
from PIL import Image

app = FastAPI()

app.mount("/static", StaticFiles(directory = "static"),name = "static")
templates = Jinja2Templates(directory="templates")

device = "cuda" if torch.cuda.is_available() else "cpu"
model = YOLO("best.pt").to(device)

def process_image(image:np.ndarray) -> np.ndarray:
    results = model(image)
    image_with_boxes = image

    for result in results:
        for box in result.boxes:
            x1,y1,x2,y2 = map(int, box.xyxy[0])
            cv2.rectangle(image_with_boxes, (x1, y1), (x2, y2), (0, 255 , 0) ,2)

    return image_with_boxes

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/detect")
async def detect_face(file: UploadFile = File(...)):
    content = await file.read()
    image = Image.open(BytesIO(content)).convert("RGB")
    image = np.array(image)

    processed_image = process_image(image)

    _, encoded_image = cv2.imencode(".jpg", cv2.cvtColor(processed_image, cv2.COLOR_RGB2BGR))
    return Response(content=encoded_image.tobytes(), media_type="image/jpeg")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0", port = 1080)