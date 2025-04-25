import cv2
import numpy as np
import torch
from numpy.typing import NDArray

from src.services.predict_utils import matrix_to_string
from src.services.preprocess_utils import preprocess_image


class BarcodeSegmodel:
    def __init__(self, config: dict):  # type: ignore
        self._model_path = config["model_path"]
        self._device = config["device"]

        self._model = torch.jit.load(
            self._model_path,
            map_location=self._device,
        )
        self._model.eval()
        self._threshold = config["threshold"]
        self._size = config["image_size"]

    def predict(self, image: NDArray[np.float32]) -> tuple[int]:
        mask = self._predict_mask(image)
        x_arr, y_arr = np.where(mask[:, :, 0])
        x_min = int(x_arr.min())
        x_max = int(x_arr.max())
        y_min = int(y_arr.min())
        y_max = int(y_arr.max())
        return (x_min, x_max, y_min, y_max)

    def _predict_mask(self, image: NDArray[np.float32]) -> NDArray:
        image_pr = preprocess_image(image, self._size).to(self._device)

        with torch.no_grad():
            logits = self._model(image_pr).detach().cpu()[0, :, :, :]
            probas = torch.sigmoid(logits).numpy()
            probas = probas.transpose(1, 2, 0)

            mask = (probas >= self._threshold).astype("float32")
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
            mask = cv2.resize(mask, (image.shape[1], image.shape[0]))

        return mask


class BarcodeOCRModel:
    def __init__(self, config: dict):  # type: ignore
        self._model_path = config["model_path"]
        self._device = config["device"]

        self._model = torch.jit.load(
            self._model_path,
            map_location=self._device,
        )
        self._model.eval()
        self._vocab = config["vocab"]
        self._size = config["image_size"]

    @property
    def vocab(self) -> str:
        return self._vocab

    def predict(self, image: NDArray[np.float32]) -> str:
        probas = self._predict_raw(image)
        string_pred, _ = matrix_to_string(probas, self._vocab)
        return string_pred[0]

    def _predict_raw(self, image: NDArray[np.float32]) -> NDArray:
        if image.shape[0] > image.shape[1]:
            image = cv2.rotate(image, 2)

        image_pr = preprocess_image(image, self._size).to(self._device)

        with torch.no_grad():
            logits = self._model(image_pr).detach().cpu()
            probas = torch.sigmoid(logits)
        return probas


class BarcodeAnalytics:
    def __init__(self, model_seg: BarcodeSegmodel, model_ocr: BarcodeOCRModel):
        self._model_seg = model_seg
        self._model_ocr = model_ocr

    @property
    def vocab(self) -> str:
        return self._model_ocr.vocab

    def predict(self, image: NDArray) -> dict:  # type: ignore
        x_min, x_max, y_min, y_max = self._model_seg.predict(image)
        image = image[x_min:x_max, y_min:y_max, :]
        string_pred = self._model_ocr.predict(image)
        return {
            "bbox": {
                "x_min": x_min,
                "x_max": x_max,
                "y_min": y_min,
                "y_max": y_max,
            },
            "value": string_pred,
        }
