from http import HTTPStatus

from fastapi.testclient import TestClient


def test_predict(client: TestClient, sample_image_bytes: bytes):
    files = {
        "image": sample_image_bytes,
    }
    response = client.post("/api/v1/model/predict", files=files)

    assert HTTPStatus.OK == response.status_code

    assert isinstance(response.json()["barcodes"], dict)
