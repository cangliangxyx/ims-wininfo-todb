#file_utils.py
import os
import pandas as pd
from src.utils.logger_config import configure_logger, set_file_paths

# 配置日志
logger = configure_logger("file_utils")

def validate_csv_file(csv_filename):
    """验证 CSV 文件是否存在"""
    csv_path = set_file_paths("log",csv_filename)
    if not os.path.exists(csv_path):
        logger.error(f"CSV 文件 {csv_path} 不存在！")
        return False
    return True

def load_csv_to_dataframe(csv_filename):
    """加载 CSV 文件为 Pandas DataFrame"""
    csv_path = set_file_paths("log",csv_filename)
    logger.info(f"正在读取 CSV 文件: {csv_path}")
    if not validate_csv_file(csv_filename):
        raise FileNotFoundError(f"CSV 文件 {csv_path} 不存在！")
    try:
        df = pd.read_csv(csv_path)
        return df
    except pd.errors.EmptyDataError:
        logger.error("CSV 文件为空")
        raise
    except pd.errors.ParserError:
        logger.error("CSV 文件格式错误")
        raise
    except Exception as e:
        logger.error(f"加载 CSV 时发生错误: {e}")
        raise