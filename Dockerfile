FROM python:3.10.13

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y  --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 5000

WORKDIR /app

COPY requirements.txt requirements.txt
COPY requirements_dev.txt requirements_dev.txt

RUN python3 -m pip install -r requirements_dev.txt \
		--index-url=https://download.pytorch.org/whl/cpu \
		--extra-index-url=https://pypi.org/simple \
        --no-cache-dir

COPY . /app/

CMD make run_app_docker
