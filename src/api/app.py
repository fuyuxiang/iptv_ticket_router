# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import time
import json
from flask import Flask, request, jsonify

from iptv_router.config import load_config, abs_path
from iptv_router.logging_conf import setup_logging, get_logger
from iptv_router.model import TicketClassifier
from iptv_router.router import TicketRouter
from iptv_router.utils import argmax

def create_app(config_path):
    cfg = load_config(config_path)
    setup_logging(cfg["logging"])
    log = get_logger(__name__)

    model_dir = abs_path(cfg, cfg["model"]["model_dir"])
    model_path = os.path.join(model_dir, cfg["model"]["model_file"])
    label_map_path = os.path.join(model_dir, cfg["model"]["label_map_file"])
    route_map_path = os.path.join(model_dir, cfg["model"]["route_map_file"])

    clf = TicketClassifier().load(model_path)
    label_map = TicketClassifier.load_label_map(label_map_path)

    with open(route_map_path, "r", encoding="utf-8") as f:
        route_map = json.load(f)

    router = TicketRouter(
        route_map=route_map,
        default_queue=cfg["routing"]["default_queue"],
        dept_to_queue=cfg["routing"].get("dept_to_queue", {}),
        threshold_auto_route=cfg["model"]["threshold_auto_route"],
    )

    app = Flask(__name__)

    @app.route("/healthz", methods=["GET"])
    def healthz():
        return jsonify({"status": "ok", "ts": int(time.time())})

    @app.route("/predict", methods=["POST"])
    def predict():
        payload = request.get_json(force=True, silent=False) or {}
        text = payload.get("text", "")
        ticket_id = payload.get("ticket_id", "")

        proba = clf.predict_proba([text])[0]
        classes_ = clf.classes_()
        best_idx = argmax(proba)
        pred_label = str(classes_[best_idx])
        pred_conf = float(proba[best_idx])

        dept, queue, auto_routed = router.route(pred_label, pred_conf)

        resp = {
            "ticket_id": ticket_id,
            "label": pred_label,
            "confidence": round(pred_conf, 6),
            "dept": dept,
            "queue": queue,
            "auto_routed": bool(auto_routed),
            "classes": classes_,
            "proba": [round(float(x), 6) for x in proba],
            "label_map": label_map
        }
        log.info("predict ticket_id=%s label=%s conf=%.4f dept=%s queue=%s auto=%s",
                 ticket_id, pred_label, pred_conf, dept, queue, auto_routed)
        return jsonify(resp)

    return app
