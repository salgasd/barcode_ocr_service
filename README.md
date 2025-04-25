# Barcode OCR Service

This is a pet project that demonstrates how to build and deploy a simple OCR pipeline

## Running the Service Locally
```bash
make install_reqs
make inst_dvc
make download_weights
make run_app
```

## Running the Service in a Docker Container
```bash
make inst_dvc
make download_weights
make build_image
make run_container
```

## Setting Up the Development Environment
```bash
make install_reqs_dev
make inst_dvc
make download_weights
```

## Running Linters and Tests
```bash
make run_linters
make run_unit_tests
make run_integration_tests
```
