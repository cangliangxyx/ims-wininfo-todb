# src/run_powershell.py
import subprocess
import sys
import os
from src.save_result import save_result

def run_powershell(command: str) -> str:
    """运行 PowerShell 命令或脚本并返回结果"""
    if os.path.isfile(command) and command.lower().endswith(".ps1"):
        # 如果是脚本路径
        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", command]
    else:
        # 如果是 PowerShell 命令
        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-Command", command]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    if result.returncode != 0:
        raise RuntimeError(f"PowerShell 执行失败: {result.stderr}")
    return result.stdout.strip()


if __name__ == "__main__":
    # 允许传入命令行参数，便于单独测试
    if len(sys.argv) < 2:
        print("Usage: python run_powershell.py '<PowerShell Command or Script Path>'")
        sys.exit(1)

    ps_command = sys.argv[1]

    try:
        output = run_powershell(ps_command)
        save_result(output, ps_command, None)
        print("执行成功，结果已保存到 data.json")
    except Exception as e:
        save_result(None, ps_command, str(e))
        print(f"执行失败: {e}")
