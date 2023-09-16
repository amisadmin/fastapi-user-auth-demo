import os
import sys
from pathlib import Path
from typing import List

from fastapi_amis_admin import admin

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BACKEND_DIR.__str__())


class Settings(admin.Settings):
    name: str = "FastAPI-User-Auth-Demo"
    host: str = "127.0.0.1"
    port: int = 6699
    secret_key: str = ""
    allow_origins: List[str] = []
    amis_cdn = "https://npm.elemecdn.com"
    amis_pkg = "amis@2.8.0"


# 设置FAA_GLOBALS环境变量
os.environ.setdefault("FAA_GLOBALS", "core.globals")

settings = Settings(_env_file=os.path.join(BACKEND_DIR, ".env"))
