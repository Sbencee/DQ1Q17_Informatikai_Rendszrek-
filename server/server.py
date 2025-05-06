import threading
import time
import queue
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from PIL import Image
import io

CURRENT_VERSION = "1.0"

TaskQueue = queue.Queue()
InvalidQueue = queue.Queue()

class Message:
    def __init__(self, version, data, content_type, reply_queue):
        self.version = version
        self.data = data
        self.content_type = content_type
        self.reply_queue = reply_queue

class TaskProcessor(threading.Thread):
    def run(self):
        while True:
            msg = TaskQueue.get()
            if msg.version != CURRENT_VERSION:
                InvalidQueue.put(msg)
                continue

            if msg.content_type == "text/plain":
                word_count = len(msg.data.decode("utf-8").split())
                msg.reply_queue.put(f"Word count: {word_count}")
            elif msg.content_type == "image/bmp":
                img = Image.open(io.BytesIO(msg.data))
                msg.reply_queue.put(f"Image size: {img.size[0]} x {img.size[1]}")
            else:
                msg.reply_queue.put("Unsupported content type")

class InvalidHandler(threading.Thread):
    def run(self):
        while True:
            msg = InvalidQueue.get()
            time.sleep(5)
            TaskQueue.put(msg)

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_type = self.headers.get("Content-Type")
        version = self.headers.get("X-Version", "0.0")
        length = int(self.headers.get("Content-Length"))
        data = self.rfile.read(length)

        reply_queue = queue.Queue()
        msg = Message(version, data, content_type, reply_queue)
        TaskQueue.put(msg)

        result = reply_queue.get()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(result.encode("utf-8"))

    def do_GET(self):
        html_content = """
        <!DOCTYPE html>
        <html lang="hu">
        <head>
            <meta charset="UTF-8">
            <title>Server state</title>
        </head>
        <body>
            <h1>Server is running!</h1>
        </body>
        </html>
        """.format(version=CURRENT_VERSION)

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html_content.encode("utf-8"))))
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

def run_server():
    server = HTTPServer(('0.0.0.0', 8080), RequestHandler)
    print("Server started at http://0.0.0.0:8080")
    server.serve_forever()

if __name__ == "__main__":
    for _ in range(2):
        TaskProcessor().start()
    InvalidHandler().start()
    run_server()