import time
from src.run_powershell import run_powershell
from src.save_result import save_result
from config.settings import PS_COMMAND


def job():
    """执行 PowerShell 并保存结果"""
    try:
        output = run_powershell(PS_COMMAND)
        save_result(output, PS_COMMAND, None)
        print("PowerShell 执行成功，结果已保存到 data.json")
    except Exception as e:
        save_result(None, PS_COMMAND, str(e))
        print(f"执行失败，错误已记录到 wininfo.log: {e}")


def main():
    while True:
        job()
        print("等待 12 小时后再次执行...")
        time.sleep(12 * 60 * 60)  # 12 小时（秒）


if __name__ == "__main__":
    main()
