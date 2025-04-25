from dependency_injector import containers, providers

from src.services.model import (
    BarcodeAnalytics,
    BarcodeOCRModel,
    BarcodeSegmodel,
)


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    model_seg = providers.Singleton(
        BarcodeSegmodel,
        config=config.services.model_seg,
    )
    model_ocr = providers.Singleton(
        BarcodeOCRModel,
        config=config.services.model_ocr,
    )

    model = providers.Singleton(
        BarcodeAnalytics,
        model_seg=model_seg,
        model_ocr=model_ocr,
    )
