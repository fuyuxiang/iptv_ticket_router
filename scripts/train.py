# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import json
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split

from iptv_router.config import load_config, abs_path
from iptv_router.model import TicketClassifier
from iptv_router.metrics import report_metrics
from iptv_router.feature import build_text_from_row

def build_route_map(df, label_field, dept_field):
    # 统计：每个 label 对应的 dept 众数（多数投票）
    route_map = {}
    grouped = df.groupby([label_field, dept_field]).size().reset_index(name="cnt")
    for label in df[label_field].dropna().unique():
        sub = grouped[grouped[label_field] == label].sort_values("cnt", ascending=False)
        if len(sub) > 0:
            route_map[str(label)] = str(sub.iloc[0][dept_field])
    return route_map

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
    dept_field = data_cfg["dept_field"]

    # 构造文本
    texts = [build_text_from_row(r, text_fields) for _, r in df.iterrows()]
    y = df[label_field].astype(str).tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        texts, y, test_size=args.test_size, random_state=args.random_state, stratify=y
    )

    clf = TicketClassifier().fit(X_train, y_train)

    pred = clf.predict(X_test)
    print("=== Offline Evaluation (label=%s) ===" % label_field)
    print(report_metrics(y_test, pred))

    model_dir = abs_path(cfg, cfg["model"]["model_dir"])
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    model_path = os.path.join(model_dir, cfg["model"]["model_file"])
    label_map_path = os.path.join(model_dir, cfg["model"]["label_map_file"])
    clf.save(model_path, label_map_path)

    route_map = build_route_map(df, label_field, dept_field)
    route_map_path = os.path.join(model_dir, cfg["model"]["route_map_file"])
    with open(route_map_path, "w", encoding="utf-8") as f:
        json.dump(route_map, f, ensure_ascii=False, indent=2)

    print("Saved model to:", model_path)
    print("Saved label map to:", label_map_path)
    print("Saved route map to:", route_map_path)

if __name__ == "__main__":
    main()
