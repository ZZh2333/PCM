# config/config.py
import os
from pathlib import Path

# 项目根目录（向上回退两级：config → 项目根目录）
BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    SECRET_KEY = os.urandom(24)
    # 路径配置
    DATA_DIR = BASE_DIR / "data"
    UPLOAD_FOLDER = DATA_DIR / "uploads"
    # Web路径
    STATIC_FOLDER = str(BASE_DIR / "web/static")
    TEMPLATE_FOLDER = str(BASE_DIR / "web/templates")
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    @classmethod
    def init_app(cls, app):
        # 确保所有目录存在
        required_dirs = [
            cls.DATA_DIR,
            cls.UPLOAD_FOLDER,
            Path(cls.STATIC_FOLDER),
            Path(cls.TEMPLATE_FOLDER)
        ]
        for d in required_dirs:
            d.mkdir(parents=True, exist_ok=True)