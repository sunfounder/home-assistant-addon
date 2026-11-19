"""Offline frame assembler tests; no Home Assistant installation required."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import unittest

RECEIVER = Path(__file__).parents[1] / "receiver.py"
spec = importlib.util.spec_from_file_location("sunfounder_receiver", RECEIVER)
receiver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(receiver)


class TestFrames(unittest.TestCase):
    def test_short_frame_not_emitted(self):
        a = receiver.FrameAssembler()
        a.feed(receiver.PULSE | 900)
        self.assertIsNone(a.feed(receiver.SPACE | 12000))

    def test_valid_frame(self):
        a = receiver.FrameAssembler()
        for i in range(10):
            a.feed((receiver.PULSE if i % 2 == 0 else receiver.SPACE) | 700)
        self.assertEqual(a.feed(receiver.SPACE | 13000), [700, -700] * 5)

    def test_overflow_drops_frame(self):
        a = receiver.FrameAssembler()
        for i in range(10):
            a.feed((receiver.PULSE if i % 2 == 0 else receiver.SPACE) | 500)
        a.feed(receiver.OVERFLOW)
        self.assertIsNone(a.finish())

    def test_timeout_flushes_frame(self):
        a = receiver.FrameAssembler()
        for i in range(8):
            a.feed((receiver.PULSE if i % 2 == 0 else receiver.SPACE) | 500)
        self.assertEqual(len(a.feed(receiver.TIMEOUT)), 8)


if __name__ == "__main__":
    unittest.main()
