# -*- coding: utf-8 -*-
import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(cfg):
    level = getattr(logging, str(cfg.get("level", "INFO")).upper(), logging.INFO)
    log_file = cfg.get("file", "logs/app.log")
    d = os.path.dirname(log_file)
    if d and not os.path.exists(d):
        os.makedirs(d)

    root = logging.getLogger()
    root.setLevel(level)

    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    root.addHandler(sh)

    fh = RotatingFileHandler(log_file, maxBytes=50*1024*1024, backupCount=5, encoding="utf-8")
    fh.setFormatter(fmt)
    root.addHandler(fh)

def get_logger(name):
    return logging.getLogger(name)
