import requests
import time
import os

SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8080")

texts = [
    b"Hello world!",
    b"Test.",
    b"Have a nice day!"
]

def send_text(text, version="1.0"):
    response = requests.post(
        SERVER_URL,
        headers={"Content-Type": "text/plain", "X-Version": version},
        data=text
    )
    print(f"Text Response: {response.text}")

def send_bmp(path="sample.bmp", version="1.0"):
    with open(path, "rb") as f:
        data = f.read()
    response = requests.post(
        SERVER_URL,
        headers={"Content-Type": "image/bmp", "X-Version": version},
        data=data
    )
    print(f"BMP Response: {response.text}")

if __name__ == "__main__":
    for text in texts:
        send_text(text)

    send_bmp()
    time.sleep(1)