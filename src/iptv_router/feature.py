# -*- coding: utf-8 -*-
from .text_preprocess import normalize_text

def build_text_from_row(row, text_fields):
    parts = []
    for f in text_fields:
        if f in row and row[f] is not None:
            v = str(row[f])
            v = v.strip()
            if v and v.lower() != "nan":
                parts.append(v)
    return normalize_text(" ".join(parts))
