# -*- coding: utf-8 -*-
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

def report_metrics(y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    rep = classification_report(y_true, y_pred, digits=4)
    return "accuracy=%.4f\n%s" % (acc, rep)

def confusion(y_true, y_pred, labels):
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    return cm
