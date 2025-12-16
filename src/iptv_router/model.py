# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import json
import joblib
import jieba

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from .text_preprocess import normalize_text

def jieba_tokenize(text):
    # jieba 返回 list[str]
    # normalize 在 preprocessor 里做，tokenizer 再分词
    return jieba.lcut(text, cut_all=False)

class TicketClassifier(object):
    def __init__(self):
        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(
                preprocessor=normalize_text,
                tokenizer=jieba_tokenize,
                lowercase=False,
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.95,
                sublinear_tf=True
            )),
            ("clf", LogisticRegression(
                solver="liblinear",
                max_iter=1000,
                C=2.0,
                class_weight="balanced"
            ))
        ])

    def fit(self, texts, y):
        self.pipeline.fit(texts, y)
        return self

    def predict(self, texts):
        return self.pipeline.predict(texts)

    def predict_proba(self, texts):
        return self.pipeline.predict_proba(texts)

    def classes_(self):
        return list(self.pipeline.named_steps["clf"].classes_)

    def save(self, model_path, label_map_path):
        d = os.path.dirname(model_path)
        if d and not os.path.exists(d):
            os.makedirs(d)
        joblib.dump(self.pipeline, model_path)

        label_map = {"classes_": self.classes_()}
        with open(label_map_path, "w", encoding="utf-8") as f:
            json.dump(label_map, f, ensure_ascii=False, indent=2)

    def load(self, model_path):
        self.pipeline = joblib.load(model_path)
        return self

    @staticmethod
    def load_label_map(label_map_path):
        with open(label_map_path, "r", encoding="utf-8") as f:
            return json.load(f)
