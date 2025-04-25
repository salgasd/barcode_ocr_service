import cv2
import numpy as np
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, File

from src.containers.containers import AppContainer
from src.services.model import BarcodeAnalytics

model_router = APIRouter(tags=["model"], prefix="/model")


@model_router.post("/predict")
@inject
def predict(
    image: bytes = File(),
    service: BarcodeAnalytics = Depends(Provide[AppContainer.model]),
) -> dict[str, dict]:
    img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.COLOR_BGR2RGB)
    pred_classes = service.predict(img)

    return {"barcodes": pred_classes}
