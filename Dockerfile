FROM python:3.10.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
ENV PYTHONPATH /app/src

RUN groupadd --system app && useradd --home-dir /app --system -g app app && chown app:app -R /app

RUN pip install -U pip wheel
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x ./wait-for-it.sh

USER app

EXPOSE 8000

# When use k8s/swarm/nomad - no need to add gunicorn, just scale using containers, one worker per container,
# according to https://fastapi.tiangolo.com/deployment/docker/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# If need to scale within a single container:
# CMD ["gunicorn", "-b", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "--workers=4", "--log-file=-", "main:app"]
