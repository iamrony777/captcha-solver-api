FROM python:3.7-bullseye

WORKDIR /app

COPY ./ /app/

ENV DEBIAN_FRONTEND=noninteractive \
    PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python \
    PORT=8000

COPY --from=iamrony777/captcha-solver-api:build-layer /app/wheels /app/wheels

RUN apt-get update -y && \
    apt-get install -y wget unzip libgl1-mesa-glx libgtk2.0-dev protobuf-compiler

RUN pip install -U pip setuptools wheel && \
    pip install --no-cache-dir --no-index --find-links=/app/wheels -r requirements.txt && \
    rm -rf /app/wheels/

RUN cp -r /app/src/label_map_util.py /usr/local/lib/python3.7/site-packages/object_detection/utils/

EXPOSE ${PORT}

ADD https://models.cloudflare-storage.workers.dev/rucaptcha_model_370.pb /app/src/rucaptcha/

CMD [ "python", "main.py" ]
