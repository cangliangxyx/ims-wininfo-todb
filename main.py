import time
import os
import sys
from src.run_powershell import run_powershell
from src.save_result import save_command_result
from src.insert_data_to_db import insert_daily_check
from src.logger import log  # 日志模块
from config.settings import ps_command, insert_sql, execution_interval

# 停止标记文件名
STOP_FILE = "stop.flag"

def execute_task(command: str, sql: str):
    """
    执行 PowerShell 脚本和数据库插入任务
    :param command: PowerShell 脚本命令
    :param sql: 数据库插入 SQL
    """
    # 1. 执行 PowerShell 脚本
    try:
        output = run_powershell(command)
        save_command_result(output, command, None)
        log(
            f"PowerShell 执行成功，结果已保存到 data.json\n执行结果: {output}",
            f"1. PowerShell executed successfully, result saved to data.json\nExecution Result: {output}"
        )
    except Exception as e:
        save_command_result(None, command, str(e))
        log(f"PowerShell 执行失败，错误已记录: {e}", f"1. PowerShell execution failed, error logged: {e}")
        return

    # 2. 插入数据库
    try:
        insert_daily_check(sql=sql)
        log("data.json 成功插入数据库", "2. data.json successfully inserted into database")
    except Exception as e:
        log(f"插入数据库失败: {e}", f"2. Failed to insert data.json into database: {e}")

    # 3. 记录任务完成
    log("任务完成，等待下一次执行", "3. Job completed, waiting for next execution")


def main():
    """
    主程序入口，动态设定执行间隔和任务管理
    """
    # 获取配置文件中的 PowerShell 脚本命令和执行间隔
    command = ps_command
    sql = insert_sql
    stop_path = os.path.join(os.getcwd(), STOP_FILE)

    # 检查执行间隔有效性（分钟）
    interval_minutes = execution_interval if isinstance(execution_interval, int) and execution_interval > 0 else 360
    if interval_minutes != execution_interval:
        log(
            f"EXECUTION_INTERVAL 配置无效，使用默认间隔：{interval_minutes} 分钟",
            f"Invalid EXECUTION_INTERVAL, using default interval: {interval_minutes} minutes"
        )
    # 转换为秒数
    interval_seconds = interval_minutes * 60

    # 启动任务
    log("程序启动，开始后台运行...", "Program started, running in background...")

    try:
        while True:
            # 停止标记检测
            if os.path.exists(stop_path):
                log("检测到 stop.flag，程序即将退出", "stop.flag detected, program exiting...")
                break

            # 执行任务
            execute_task(command, sql)

            # 等待下次执行
            log(
                f"等待 {interval_minutes} 分钟（{interval_seconds} 秒）后再次执行...",
                f"Waiting {interval_minutes} minutes ({interval_seconds} seconds) before next execution..."
            )

            # 分段睡眠（每 5 分钟检查一次 stop.flag）
            check_interval = 300  # 5 分钟
            for _ in range(0, interval_seconds, check_interval):
                if os.path.exists(stop_path):
                    log("检测到 stop.flag，程序即将退出", "stop.flag detected, program exiting...")
                    return
                time.sleep(min(check_interval, interval_seconds - _))

    except KeyboardInterrupt:
        log("程序收到 Ctrl+C 停止，正在退出...", "KeyboardInterrupt received, exiting program...")
    except Exception as e:
        log(f"程序运行异常: {e}", f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
