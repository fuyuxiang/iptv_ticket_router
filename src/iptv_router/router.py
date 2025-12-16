# -*- coding: utf-8 -*-
from __future__ import print_function

class TicketRouter(object):
    def __init__(self, route_map, default_queue, dept_to_queue=None, threshold_auto_route=0.65):
        self.route_map = route_map or {}          # label -> dept
        self.default_queue = default_queue
        self.dept_to_queue = dept_to_queue or {}  # dept -> queue
        self.threshold = float(threshold_auto_route)

    def route(self, pred_label, pred_conf):
        if pred_conf < self.threshold:
            return None, self.default_queue, False

        dept = self.route_map.get(pred_label)
        if not dept:
            return None, self.default_queue, False

        queue = self.dept_to_queue.get(dept, dept)  # 没配置就直接返回 dept
        return dept, queue, True
