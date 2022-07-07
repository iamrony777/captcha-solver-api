FROM python:3.7-slim as build
WORKDIR /app
COPY ./ /app/
ENV DEBIAN_FRONTEND=noninteractive \
    PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
RUN apt update -y && \
    apt install -y wget unzip libgl1-mesa-glx libgtk2.0-dev git tar && \
    wget -qcO protoc.zip https://github.com/protocolbuffers/protobuf/releases/download/v21.2/protoc-21.2-linux-x86_64.zip  && \
    unzip protoc.zip -d protoc && \
    mv protoc/bin/protoc /usr/local/bin/ && \
    mv protoc/include/google/protobuf /usr/local/include/ && \
    rm -rf protoc*
RUN pip install -U pip setuptools wheel && \
    pip wheel --wheel-dir=/app/wheels -r requirements.txt

# Cleanup
FROM python:3.7-slim
WORKDIR /app
COPY --from=build /app/wheels /app/wheels