"""Integration-style localhost HTTP test for SunFounder event forwarding."""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import json
from pathlib import Path
import queue
import threading
import unittest

SOURCE = Path(__file__).parents[1] / "receiver.py"
spec = importlib.util.spec_from_file_location("sunfounder_ir_under_test", SOURCE)
receiver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(receiver)


class EventHandler(BaseHTTPRequestHandler):
    received = queue.Queue()

    def log_message(self, *_args):
        pass

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        body = json.loads(self.rfile.read(length))
        self.received.put((self.path, self.headers.get("Authorization"), body))
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"{}")


class TestHttpDelivery(unittest.TestCase):
    def test_event_is_posted_with_correct_path_and_payload(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), EventHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        previous_url = receiver.API_URL
        receiver.API_URL = f"http://127.0.0.1:{server.server_port}/core/api/events/sunfounder_ir_received"
        receiver.STOP.clear()
        pending = queue.Queue()
        pending.put({"receiver_id": "pironman-test", "timings": [600, -600] * 5, "modulation": None})
        sender = threading.Thread(target=receiver.send_frames, args=("test-token", pending), daemon=True)
        try:
            sender.start()
            path, authorization, data = EventHandler.received.get(timeout=5)
            self.assertEqual(path, "/core/api/events/sunfounder_ir_received")
            self.assertEqual(authorization, "Bearer test-token")
            self.assertEqual(data["receiver_id"], "pironman-test")
            self.assertEqual(data["timings"], [600, -600] * 5)
        finally:
            receiver.STOP.set()
            sender.join(timeout=5)
            receiver.API_URL = previous_url
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)
