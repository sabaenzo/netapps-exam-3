#!/usr/bin/env python3

import unittest

import canvas

class TestCanvas(unittest.TestCase):
    def test_get_file(self):
        canvas.get_canvas_file("22040212")

    def test_upload(self):
        r = canvas.upload_canvas_file("test2.txt")
        print(r)

def main():
    unittest.main()


if __name__ == "__main__":
    main()
