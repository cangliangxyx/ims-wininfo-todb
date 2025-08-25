import os, sys

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

# PowerShell 由于授权原因需要只能执行相关的powershell脚本,脚本存储位置为以下路径
PS_COMMAND_WSUS = r"C:\wininfo_to_db\wsus_check.ps1"

PS_COMMAND_RDS = """
Get-WmiObject Win32_TSLicenseKeyPack |
    Select-Object KeyPackId, ProductVersion, TypeAndModel, AvailableLicenses, IssuedLicenses |
    ConvertTo-Json
"""

# SQL 插入语句
INSERT_RDS_SQL = """
    INSERT INTO Infra_Daily_Check (Creat_Time, rds_prod_license, Insert_Time)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE
        rds_prod_license = VALUES(rds_prod_license),
        Insert_Time = VALUES(Insert_Time)
"""

INSERT_WSUS_SQL = """
    INSERT INTO Infra_Daily_Check (Creat_Time, wsus_server_info, Insert_Time)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE
        wsus_server_info = VALUES(wsus_server_info),
        Insert_Time = VALUES(Insert_Time)
"""

def get_database_config(env) -> dict:
    if env == "test":
        return DATABASE_CONFIG["test"]
    else:
        return DATABASE_CONFIG["prod"]
