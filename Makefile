.PHONY: *

APP_PORT := 5000
SERVICE_PORT := 10024
DOCKER_TAG := latest
DOCKER_IMAGE := s.gadzhibekov_barcode_service

DEPLOY_HOST := demo_host

create_env:
	python3 -m venv venv

install_reqs: create_env
	./venv/bin/python3 -m pip install -r requirements.txt \
		--index-url=https://download.pytorch.org/whl/cpu \
		--extra-index-url=https://pypi.org/simple

install_reqs_dev: create_env
	./venv/bin/python3 -m pip install -r requirements_dev.txt \
		--index-url=https://download.pytorch.org/whl/cpu \
		--extra-index-url=https://pypi.org/simple

inst_dvc:
	pip install dvc==3.50.1
	pip install dvc-ssh==4.1.1

run_unit_tests:
	PYTHONPATH=. ./venv/bin/python3 -m pytest ./tests/unit -v

run_integration_tests:
	PYTHONPATH=. ./venv/bin/python3 -m pytest ./tests/integration -v

run_linters:
	flake8 ./src

download_weights:
	dvc pull -R weights

run_app:
	PYTHONPATH=. ./venv/bin/python3 -m uvicorn src.main:app \
			   --port=$(APP_PORT) \
			   --host='0.0.0.0'

run_app_docker:
	PYTHONPATH=. python3 -m uvicorn src.main:app \
			   --port=$(APP_PORT) \
			   --host='0.0.0.0'

build_image:
	docker build -f Dockerfile . --force-rm=true -t $(DOCKER_IMAGE):$(DOCKER_TAG)

run_container:
	docker run --rm -p $(SERVICE_PORT):$(APP_PORT) $(DOCKER_IMAGE):$(DOCKER_TAG)

deploy:
	ansible-playbook -i deploy/inventory.ini  deploy/deploy.yml \
		-e host=$(DEPLOY_HOST) \
		-e docker_image=$(DOCKER_IMAGE) \
		-e docker_tag=$(DOCKER_TAG) \
		-e docker_registry_user=$(CI_REGISTRY_USER) \
		-e docker_registry_password=$(CI_REGISTRY_PASSWORD) \
		-e docker_registry=$(CI_REGISTRY) \

destroy:
	ansible-playbook -i deploy/inventory.ini deploy/destroy.yml \
		-e host=$(DEPLOY_HOST)
