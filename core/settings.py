import os
from pathlib import Path
from typing import List
from fastapi_amis_admin.amis_admin.settings import Settings as AmisSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(AmisSettings):
    '''项目配置'''
    project_name: str = 'FastAPI example application'  # 项目名称
    secret_key: str
    allowed_hosts: List[str] = ["*"]


settings = Settings(_env_file=os.path.join(BASE_DIR, '.env'))
