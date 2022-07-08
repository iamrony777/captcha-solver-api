FROM python:3.7-slim

WORKDIR /app

COPY ./ /app/

# Model.pb for javdb's captcha, stored in google drive , indexed via cf
ADD https://models.cloudflare-storage.workers.dev/javdb_captcha_model.pb /app/src/javdb/

ENV DEBIAN_FRONTEND=noninteractive \
    PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

ENV RELOAD_DELAY='10'

RUN apt update -y && apt install wget && \
    wget -qcO protoc.zip https://github.com/protocolbuffers/protobuf/releases/download/v21.2/protoc-21.2-linux-x86_64.zip  && \
    unzip protoc.zip -d protoc && \
    mv protoc/bin/protoc /usr/local/bin/ && \
    mv protoc/include/google/protobuf /usr/local/include/ && \
    rm -rf protoc*  && \

COPY --from=iamrony777/captcha-solver-api:build-layer /app/wheels /app/wheels

RUN pip install -U pip setuptools wheel && \
    pip install --no-cache-dir --no-index --find-links=/app/wheels -r requirements.txt

RUN cp -r /app/src/label_map_util.py /usr/local/lib/python3.7/site-packages/object_detection/utils/

CMD [ "python", "main.py" ]
