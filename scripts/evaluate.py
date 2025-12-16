# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split

from iptv_router.config import load_config, abs_path
from iptv_router.model import TicketClassifier
from iptv_router.metrics import report_metrics
from iptv_router.feature import build_text_from_row

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/config.yaml")
    ap.add_argument("--test_size", type=float, default=0.2)
    ap.add_argument("--random_state", type=int, default=42)
    args = ap.parse_args()

    cfg = load_config(args.config)
    data_cfg = cfg["data"]

    df = pd.read_csv(abs_path(cfg, data_cfg["train_csv"]))
    text_fields = data_cfg["text_fields"]
    label_field = data_cfg["label_field"]

    texts = [build_text_from_row(r, text_fields) for _, r in df.iterrows()]
    y = df[label_field].astype(str).tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        texts, y, test_size=args.test_size, random_state=args.random_state, stratify=y
    )

    model_dir = abs_path(cfg, cfg["model"]["model_dir"])
    model_path = os.path.join(model_dir, cfg["model"]["model_file"])

    clf = TicketClassifier().load(model_path)
    pred = clf.predict(X_test)

    print("=== Evaluation (loaded model) ===")
    print(report_metrics(y_test, pred))

if __name__ == "__main__":
    main()
