infra_wininfo_todb/
│
├── config
│   ├── settings.py             # 存放数据库配置和PowerShell命令等配置信息
├── log
│   ├── app.log                 # 日志文件
│   └── rds_license_data.json   # 生成数据文件
├── open_incident
│   ├── executor.py             # 执行 powershell 并生成数据文件
│   └── insert_data_to_db.py    # 读取数据文件并插入数据库
├── readme.txt                  # 项目说明文件
├── requirements.txt            # 项目依赖列表
└── scheduler.py                # 定时执行