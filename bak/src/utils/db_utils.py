#db_utils.py
import pymysql
from pymysql.err import OperationalError, InternalError, DatabaseError
from config.settings import get_database_config
from bak.src.utils.logger_config import configure_logger
from bak.src.utils.decrypt_message import decrypt_message

# 配置日志
logger = configure_logger("db_utils")

def build_db_connection_params(db_config):
    """构建数据库连接参数字典"""
    try:
        connection_params = {
            "host": db_config["host"],
            "port": int(db_config["port"]),
            "user": db_config["user"],
            "password": decrypt_message(db_config["password"]),
            "database": db_config["database"],
            "charset": db_config["charset"],
        }
        return connection_params
    except KeyError as e:
        logger.error(f"缺少配置项: {e}")
        raise ValueError(f"缺少必要的配置项: {e}")

def get_db_connection(env):
    """获取数据库连接"""
    try:
        # 加载数据库配置
        db_config = get_database_config(env)
        if not db_config:
            raise ValueError(f"未找到环境 '{env}' 的数据库配置。")

        # 构建连接参数
        connection_params = build_db_connection_params(db_config)

        # 使用 pymysql 连接数据库
        connection = pymysql.connect(**connection_params)
        logger.info(f"成功连接到数据库，使用环境：{env}")
        return connection
    except (ValueError, OperationalError, InternalError, DatabaseError) as e:
        logger.error(f"数据库连接失败: {e}")
        raise
    except Exception as e:
        logger.error(f"连接数据库时发生了意外错误: {str(e)}")
        raise

def insert_data_to_table(df, table_name, connection):
    """通用方法：将 DataFrame 数据插入到数据库表中"""
    try:
        # 打开数据库游标
        cursor = connection.cursor()

        # 动态构建插入语句
        columns = ", ".join(df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))
        insert_query = f"REPLACE INTO {table_name} ({columns}) VALUES ({placeholders})"

        # 批量插入数据
        cursor.executemany(insert_query, df.values.tolist())
        connection.commit()

        # 返回插入成功的行数
        logger.info(f"成功将 {cursor.rowcount} 行数据插入到表 {table_name}")
        return cursor.rowcount
    except (OperationalError, InternalError, DatabaseError) as e:
        logger.error(f"数据库错误: {e}")
        connection.rollback()
        raise
    except Exception as e:
        logger.error(f"插入数据时发生错误: {str(e)}")
        raise

def get_sql_config ():
    """读取 JSON 文件内容"""
    logger = setup_logging()
    rds_license_file_path = filename()["rds_license_data_path"]
    created_at = datetime.now().strftime("%Y-%m-%d")
    insert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"准备读取 JSON 文件: {rds_license_file_path}")

    try:
        with open(rds_license_file_path, 'r', encoding='utf-8') as f:
            json_content = f.read()
            logger.info(f"文件读取成功，内容长度: {len(json_content)} 字符")
    except Exception as e:
        logger.error(f"读取 JSON 文件失败: {e}")
        raise RuntimeError(f"读取 JSON 文件失败: {e}")
    sql_info = {
        "rds_license_data": {
            "sql": """
                INSERT INTO Infra_Daily_Check (Creat_Time, rds_prod_license, Insert_Time)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                RDS_Prod_License = VALUES(rds_prod_license),
                Insert_Time = VALUES(Insert_Time) """,
                "values": [(created_at, json_content, insert_time)]
        },
        "demo": {
            "sql": "INSERT INTO demo_table (field) VALUES (%s)",
            "values": "demo_value"
        }
    }
    return sql_info