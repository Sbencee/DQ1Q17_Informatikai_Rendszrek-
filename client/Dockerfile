FROM python:3.11-slim

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    && pip install pillow \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install requests

CMD ["python", "client.py"]