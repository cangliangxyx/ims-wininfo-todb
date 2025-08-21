# src/logger_config.py

import logging
import os
import sys
from pathlib import Path
from typing import Dict

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"

# def filename():
#     return {"log_path":os.path.join(project_path(), "log", "app.log"), "rds_license_data_path": os.path.join(project_path(), "log", "rds_license_data.json")}

def get_project_root() -> Path:
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(sys.modules['__main__'].__file__).parent.parent.parent

def ensure_directory_exists(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)

def get_logging_paths() -> Dict[str, str]:
    root = get_project_root()
    log_dir = os.path.join(root, "log")
    ensure_directory_exists(log_dir)
    return {
        "app_log": os.path.join(log_dir,"app.log"),
    }

def configure_logger(module_name: str = "App",
                     level: int = logging.INFO,
                     enable_file_logging: bool = True) -> logging.Logger:
    logger = logging.getLogger(module_name)
    logger.setLevel(level)
    if not logger.handlers:
        return logger

    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATEFMT)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件日志（可选）
    if enable_file_logging:
        log_paths = get_logging_paths()

        # 主日志文件（app.log）
        file_handler = logging.FileHandler(
            filename=log_paths["app_log"],
            encoding="utf-8"
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 错误日志单独记录（errors.log）
        error_handler = logging.FileHandler(
            filename=log_paths["error_log"],
            encoding="utf-8"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)

    return logger

def set_file_paths(file_patch, file_name) -> str:
    root_path = get_project_root()
    file_dir = os.path.join(root_path, file_patch, file_name)
    return file_dir

if __name__ == "__main__":
    data = set_file_paths("log","rds_license_data.json")
    print(data)