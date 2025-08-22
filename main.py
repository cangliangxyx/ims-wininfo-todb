import time
import os
import sys
from src.run_powershell import run_powershell
from src.save_result import save_result
from src.insert_data_to_db import insert_rds_license
from config.settings import PS_COMMAND

STOP_FILE = "stop.flag"

def get_base_dir():
    """获取程序根目录（exe 或脚本）"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
LOG_DIR = os.path.join(BASE_DIR, "log")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "wininfo.log")

def log(msg: str, console_msg: str = None):
    """写入日志文件（中文）并打印控制台（英文）"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[{timestamp}] {console_msg or msg}")

def job():
    """执行 PowerShell 并保存结果，同时插入数据库"""
    # -------------------------------
    # 1. 执行 PowerShell 命令
    # -------------------------------
    try:
        output = run_powershell(PS_COMMAND)
        save_result(output, PS_COMMAND, None)
        log(
            "PowerShell 执行成功，结果已保存到 data.json",
            "1. PowerShell executed successfully, result saved to data.json"
        )
    except Exception as e:
        save_result(None, PS_COMMAND, str(e))
        log(
            f"PowerShell 执行失败，错误已记录: {e}",
            f"1. PowerShell execution failed, error logged: {e}"
        )
        return

    # -------------------------------
    # 2. 插入数据库
    # -------------------------------
    try:
        insert_rds_license(env="prod")
        log(
            "data.json 成功插入数据库",
            "2. data.json successfully inserted into database"
        )
    except Exception as e:
        log(
            f"插入数据库失败: {e}",
            f"2. Failed to insert data.json into database: {e}"
        )

    # -------------------------------
    # 3. 完成任务
    # -------------------------------
    log(
        "任务完成，等待下一次执行",
        "3. Job completed, waiting for next execution"
    )

def main():
    stop_path = os.path.join(BASE_DIR, STOP_FILE)
    log("程序启动，开始后台运行...", "Program started, running in background...")

    try:
        while True:
            if os.path.exists(stop_path):
                log("检测到 stop.flag，程序即将退出", "stop.flag detected, program exiting...")
                break

            job()
            log("等待 12 小时后再次执行...", "Waiting 12 hours before next execution...")

            # 分段睡眠，每分钟检查 stop.flag
            for _ in range(12 * 60):
                if os.path.exists(stop_path):
                    log("检测到 stop.flag，程序即将退出", "stop.flag detected, program exiting...")
                    return
                time.sleep(60)

    except KeyboardInterrupt:
        log("程序收到 Ctrl+C 停止，正在退出...", "KeyboardInterrupt received, exiting program...")

if __name__ == "__main__":
    main()
