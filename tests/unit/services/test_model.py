from copy import deepcopy

import numpy as np
from numpy.typing import NDArray

from src.services.model import (BarcodeAnalytics, BarcodeOCRModel,
                                BarcodeSegmodel)


def test_seg_model_predict_dont_mutate_initial_image(model_seg: BarcodeSegmodel, sample_image_np: NDArray):
    initial_image = deepcopy(sample_image_np)
    model_seg.predict(sample_image_np)

    assert np.allclose(initial_image, sample_image_np)


def test_ocr_model_predict_dont_mutate_initial_image(model_ocr: BarcodeOCRModel, sample_image_np: NDArray):
    initial_image = deepcopy(sample_image_np)
    model_ocr.predict(sample_image_np)

    assert np.allclose(initial_image, sample_image_np)


def test_barcode_analytics_predict_dont_mutate_initial_image(barcode_analytics: BarcodeAnalytics, sample_image_np: NDArray):
    initial_image = deepcopy(sample_image_np)
    barcode_analytics.predict(sample_image_np)

    assert np.allclose(initial_image, sample_image_np)


def test_seg_model_predict_return_value(model_seg: BarcodeSegmodel, sample_image_np: NDArray):
    prediction = model_seg.predict(sample_image_np)

    assert isinstance(prediction, tuple)
    assert all(isinstance(x, int) for x in prediction)


def test_ocr_model_predict_return_value(model_ocr: BarcodeOCRModel, sample_image_np: NDArray):
    prediction = model_ocr.predict(sample_image_np)

    assert isinstance(prediction, str)


def test_barcode_analytics_return_value(barcode_analytics: BarcodeAnalytics, sample_image_np: NDArray):
    prediction = barcode_analytics.predict(sample_image_np)

    assert isinstance(prediction, dict)
    assert "bbox" in prediction
    assert "value" in prediction

    assert isinstance(prediction["value"], str)
    assert isinstance(prediction["bbox"], dict)

    assert all(isinstance(x, int) for x in prediction["bbox"].values())

    assert "x_min" in prediction["bbox"]
    assert "x_max" in prediction["bbox"]
    assert "y_min" in prediction["bbox"]
    assert "y_max" in prediction["bbox"]

    assert prediction["bbox"]["x_min"] < prediction["bbox"]["x_max"]
    assert prediction["bbox"]["y_min"] < prediction["bbox"]["y_max"]

