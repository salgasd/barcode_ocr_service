from src.services.model import (BarcodeAnalytics, BarcodeOCRModel,
                                BarcodeSegmodel)


def test_app_container_class_instance(app_container):
    assert isinstance(app_container.model(), BarcodeAnalytics)
