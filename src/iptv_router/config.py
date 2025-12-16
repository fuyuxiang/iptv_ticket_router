# -*- coding: utf-8 -*-
import os
import yaml

def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    cfg["_config_path"] = os.path.abspath(path)
    cfg["_repo_root"] = os.path.abspath(os.path.join(os.path.dirname(path), os.pardir))
    return cfg

def abs_path(cfg, maybe_rel_path):
    if maybe_rel_path is None:
        return None
    p = str(maybe_rel_path)
    if os.path.isabs(p):
        return p
    return os.path.join(cfg["_repo_root"], p)
