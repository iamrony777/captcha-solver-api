FROM python:3.7-slim as build
WORKDIR /app
COPY ./ /app/
ENV DEBIAN_FRONTEND=noninteractive
RUN pip install -U pip setuptools wheel && \
    pip wheel --wheel-dir=/app/wheels -r requirements.txt


# Cleanup
FROM python:3.7-slim
WORKDIR /app
COPY --from=build /app/wheels /app/wheels