import pymysql
from src.utils.settings import get_database_config
from src.utils.db_utils import get_db_connection
from src.utils.logger_config import configure_logger
logger = configure_logger()

def insert_data_to_db():
    """插入数据到 Infra_Daily_Check 表"""
    logger.info("开始执行 insert_data_to_db")

    try:
        sql_data = get_database_config()
        query = sql_data["rds_license_data"]["sql"]
        values = sql_data["rds_license_data"]["values"]

        logger.info(f"准备插入 {len(values)} 条数据")
        logger.debug(f"SQL 语句: {query}")
        logger.debug(f"插入参数预览: {values[:1]}...")  # 仅打印前一项，避免日志太长

        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.executemany(query, values)
            connection.commit()
            logger.info("数据成功插入 Infra_Daily_Check.RDS_Prod_License")

    except pymysql.MySQLError as e:
        logger.error(f"[执行错误] 数据库操作失败: {e}")
        if 'connection' in locals() and connection.open:
            connection.rollback()
            logger.warning("数据已回滚")
    except KeyError as e:
        logger.error(f"[配置错误] 缺少配置键: {e}")
    except Exception as e:
        logger.exception(f"[未知错误] 插入过程发生异常: {e}")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
            logger.info("数据库连接已关闭")

def main():
    insert_data_to_db()

if __name__ == "__main__":
    main()