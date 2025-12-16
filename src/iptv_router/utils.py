# -*- coding: utf-8 -*-
import math

def safe_float(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return default

def argmax(arr):
    best_i = 0
    best_v = None
    for i, v in enumerate(arr):
        if best_v is None or v > best_v:
            best_v = v
            best_i = i
    return best_i
