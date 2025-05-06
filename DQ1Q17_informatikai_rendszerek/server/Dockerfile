# server/Dockerfile
FROM python:3.10-slim

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    && pip install pillow \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY server.py .

RUN pip install pillow

EXPOSE 8080

CMD ["python", "-u", "server.py"]

