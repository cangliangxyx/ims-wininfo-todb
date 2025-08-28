import os
import sys
import yaml

DATABASE_CONFIG = {
    "prod": {
        "host": "10.36.24.253",
        "port": 3306,
        "user": "dbpa_elp_autocmdb",
        "password": "gAAAAABoJX0Y_pKkcjbZ1zaSUqCdRRgrk7WbLz-s3dL4KZ2PLU0Xrhwkl_-2DrDHC9Gy18dEnk3nX0ItOOyA8NH2DcpV6Adaug==",
        "database": "auto_cmdb",
        "charset": "utf8mb4"
    },
    "test": {
        "host": "10.33.16.33",
        "port": 3306,
        "user": "dbta_db_cmdbapp",
        "password": "gAAAAABoJX0z4UP7xK9xicG7uXGurTI7PVJ9qDrnbHqokEK_62m8wk3b-OWwGWQ1CcOJxK2xPjR0reRL9T5XWORgJrwz9Eb_E_VTEv8ebFcpGh33USQ7uro=",
        "database": "auto_cmdb",
        "charset": "utf8mb4"
    }
}


def load_config():
    """从 EXE 文件所在目录加载 YAML 配置文件"""
    # 获取 EXE 文件或脚本所在的真实目录
    if getattr(sys, 'frozen', False):
        # 如果是 PyInstaller 打包后的运行环境
        base_path = os.path.dirname(sys.executable)  # EXE 文件所在目录
    else:
        # 开发环境下（未打包时）
        base_path = os.path.abspath(os.path.dirname(__file__))

    # 指定配置文件路径，与 EXE 同级
    config_file = os.path.join(base_path, 'config.yaml')

    if not os.path.exists(config_file):
        raise FileNotFoundError(f"配置文件未找到: {config_file}")

    # 使用 `yaml.safe_load` 解析 YAML 文件
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_database_config():
    """根据config.yaml中DB_ENV字段获取数据库配置"""
    CONFIG = load_config()
    db_env = CONFIG.get("DB_ENV", "test")
    if db_env == "test":
        return DATABASE_CONFIG["test"]
    else:
        return DATABASE_CONFIG["prod"]


# 加载配置
CONFIG = load_config()

# 从配置中获取值 ps_command, insert_sql, execution_interval
ps_command = CONFIG.get("PS_COMMAND", "")
insert_sql = CONFIG.get("INSERT_SQL", "")
execution_interval = CONFIG.get("EXECUTION_INTERVAL", "")
database_config = get_database_config()
# 测试代码
if __name__ == "__main__":
    try:
        print(f"PS_COMMAND: {ps_command}")
        print(f"INSERT_SQL: {insert_sql}")
        print(f"EXECUTION_INTERVAL (seconds): {execution_interval}")
        print(f"Database Config: {database_config}")
    except Exception as e:
        print(f"配置加载失败: {e}")
        sys.exit(1)
