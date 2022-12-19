FROM python:3.10.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /test
ENV  FASTAPI_HOST: fastapi
ENV  REDIS_HOST: redis
ENV  ELASTIC_HOST: elastic

RUN groupadd --system app && useradd --home-dir /test --system -g app app && chown app:app -R /app

RUN pip install -U pip wheel
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ../../../tests .
USER app

RUN sh -c "python3 ./functional/utils/wait_for_es.py  \
    && python3 ./functional/utils/wait_for_redis.py  \
    && python3 -m pytest ./functional/src"

