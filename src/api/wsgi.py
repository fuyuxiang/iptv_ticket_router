# -*- coding: utf-8 -*-
import os
from api.app import create_app

CONFIG_PATH = os.environ.get("IPTV_CONFIG", "configs/config.yaml")
app = create_app(CONFIG_PATH)

if __name__ == "__main__":
    cfg = os.environ.get("IPTV_CONFIG", "configs/config.yaml")
    app.run(host="0.0.0.0", port=8080, debug=False)
