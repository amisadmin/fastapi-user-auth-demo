import os
from pathlib import Path
from typing import List

from fastapi_amis_admin.amis_admin.settings import Settings as AmisSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(AmisSettings):
    name: str = 'FastAPI-User-Auth-Demo'
    host: str = '127.0.0.1'
    port: int = 6699
    secret_key: str = ''
    allow_origins: List[str] = []


settings = Settings(_env_file=os.path.join(BASE_DIR, '.env'))
