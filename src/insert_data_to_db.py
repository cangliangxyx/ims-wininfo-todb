import os
import sys
import json
from datetime import datetime
import pymysql
from pymysql.err import OperationalError, InternalError, DatabaseError
from config.settings import get_database_config
from src.decrypt_message import decrypt_message
from src.logger import log

def build_db_connection_params(db_env):
    db_config = get_database_config(db_env)
    try:
        connection_params = {
            "host": db_config["host"],
            "port": int(db_config["port"]),
            "user": db_config["user"],
            "password": decrypt_message(db_config["password"]),
            "database": db_config["database"],
            "charset": db_config["charset"],
        }
        log(f"成功构建数据库连接参数：{db_env}", f"Successfully build database connection parameters: {db_env}")
        return connection_params
    except KeyError as e:
        log(f"缺少配置项: {e}", f"Missing config item: {e}")
        raise ValueError(f"缺少必要的配置项: {e}")

def get_db_connection(env):
    try:
        connection_params = build_db_connection_params(env)
        connection = pymysql.connect(**connection_params)
        log(f"成功连接到数据库，使用环境：{env}", f"Successfully connected to database: {env}")
        return connection
    except Exception as e:
        log(f"数据库连接失败: {e}", f"Database connection failed: {e}")
        raise

def insert_rds_license(env="prod"):
    """读取 exe/script 路径 log/data.json 并插入 Infra_Daily_Check"""
    conn = get_db_connection(env)

    base_dir = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "log", "data.json")
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        rds_json_str = json.dumps(json_data, ensure_ascii=False)
        log(f"读取 JSON 文件成功: {json_path}", f"Read JSON file successfully: {json_path}")
    except Exception as e:
        log(f"读取 JSON 文件失败: {e}", f"Failed to read JSON file: {e}")
        raise

    creat_time = datetime.now().strftime("%Y-%m-%d")
    insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = """
        INSERT INTO Infra_Daily_Check (Creat_Time, rds_prod_license, Insert_Time)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            rds_prod_license = VALUES(rds_prod_license),
            Insert_Time = VALUES(Insert_Time)
    """
    values = (creat_time, rds_json_str, insert_time)

    try:
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        log(f"成功将 RDS License 插入数据库，影响行数: {cursor.rowcount}",
            f"Successfully inserted RDS License into database, affected rows: {cursor.rowcount}")
        cursor.close()
    except Exception as e:
        log(f"插入数据库失败: {e}", f"Failed to insert into database: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    insert_rds_license("prod")
