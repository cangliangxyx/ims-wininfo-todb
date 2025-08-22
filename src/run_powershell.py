# src/run_powershell.py powershell执行PS_COMMAND

import subprocess
from config.settings import PS_COMMAND

def run_powershell(command: str) -> str:
    """运行 PowerShell 命令并返回结果"""
    result = subprocess.run(
        ["powershell", "-Command", command],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    if result.returncode != 0:
        raise RuntimeError(f"PowerShell 执行失败: {result.stderr}")
    return result.stdout.strip()


if __name__ == "__main__":
    try:
        output = run_powershell(PS_COMMAND)
        print("PowerShell 执行结果:\n", output)
    except Exception as e:
        print("❌ 出错:", e)
