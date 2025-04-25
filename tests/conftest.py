import os

import cv2
import pytest
import yaml
from fastapi import FastAPI
from fastapi.testclient import TestClient
from numpy.typing import NDArray

from src.containers.containers import AppContainer
from src.main import set_routers
from src.routers.v1 import api as api_routes
from src.services.model import (BarcodeAnalytics, BarcodeOCRModel,
                                BarcodeSegmodel)

TESTS_DIR = os.path.dirname(__file__)


@pytest.fixture(scope="session")
def sample_image_bytes() -> bytes:
    f = open(os.path.join(TESTS_DIR, "test_data", "test_image.jpg"), "rb")
    yield f.read()
    f.close()


@pytest.fixture
def sample_image_np() -> NDArray:
    img = cv2.imread(os.path.join(TESTS_DIR, "test_data", "test_image.jpg"), cv2.COLOR_BGR2RGB)
    return img


@pytest.fixture(scope="session")
def app_config() -> dict:
    with open(os.path.join(TESTS_DIR, "test_config.yml"), "r") as fin:
        config = yaml.safe_load(fin)
    return config


@pytest.fixture(scope="module")
def model_seg(app_config: dict) -> BarcodeSegmodel:
    model = BarcodeSegmodel(app_config["services"]["model_seg"])
    return model


@pytest.fixture(scope="module")
def model_ocr(app_config: dict) -> BarcodeOCRModel:
    model = BarcodeOCRModel(app_config["services"]["model_ocr"])
    return model


@pytest.fixture(scope="module")
def barcode_analytics(app_config: dict, model_seg: BarcodeSegmodel, model_ocr: BarcodeOCRModel) -> BarcodeAnalytics:
    model = BarcodeAnalytics(model_seg=model_seg, model_ocr=model_ocr)
    return model


@pytest.fixture
def app_container(app_config) -> AppContainer:
    container = AppContainer()
    container.config.from_dict(app_config)
    return container


@pytest.fixture
def wired_app_container(app_config):
    container = AppContainer()
    container.config.from_dict(app_config)
    container.wire([api_routes])
    yield container
    container.unwire()


@pytest.fixture
def test_app(app_config, wired_app_container):
    app = FastAPI()
    set_routers(app)
    return app


@pytest.fixture
def client(test_app):
    return TestClient(test_app)
