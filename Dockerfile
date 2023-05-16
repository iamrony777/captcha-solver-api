FROM python:3.10-bullseye

WORKDIR /app

COPY ./ /app/

ENV DEBIAN_FRONTEND=noninteractive \
    PORT=8000

# COPY --from=iamrony777/captcha-solver-api:build-layer /app/wheels /app/wheels

RUN apt-get update -y && \
    apt-get install -y wget unzip libgl1-mesa-glx libgtk2.0-dev protobuf-compiler

RUN pip install -U pip setuptools wheel && \
    pip install --no-cache-dir -r requirements-update.txt && \

RUN bash object-detection-api.setup

EXPOSE ${PORT}

ADD https://models.cloudflare-storage.workers.dev/rucaptcha_model_370.pb /app/src/rucaptcha/

CMD [ "python", "main.py" ]
