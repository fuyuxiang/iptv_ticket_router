# -*- coding: utf-8 -*-
import re

_re_space = re.compile(r"\s+")
_re_punct = re.compile(r"[^\w\u4e00-\u9fff]+")

def normalize_text(text):
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)

    text = text.strip().lower()
    text = _re_space.sub(" ", text)
    text = _re_punct.sub(" ", text)
    text = _re_space.sub(" ", text).strip()
    return text
