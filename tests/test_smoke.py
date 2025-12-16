# -*- coding: utf-8 -*-
import os
import json
import unittest

from api.app import create_app

class SmokeTest(unittest.TestCase):
    def setUp(self):
        os.environ["IPTV_CONFIG"] = "configs/config.yaml"
        self.app = create_app("configs/config.yaml").test_client()

    def test_healthz(self):
        r = self.app.get("/healthz")
        self.assertEqual(r.status_code, 200)

    def test_predict(self):
        payload = {"ticket_id": "T1", "text": "机顶盒提示无信号，无法播放"}
        r = self.app.post("/predict", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertIn("label", data)
        self.assertIn("queue", data)

if __name__ == "__main__":
    unittest.main()
