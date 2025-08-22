# src/run_powershell.py powershell执行PS_COMMAND

import subprocess
from config.settings import PS_COMMAND

import subprocess
from config.settings import PS_COMMAND
from src.save_result import save_result

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
        # 使用 save_result 写入日志
        save_result(output, PS_COMMAND, None)
    except Exception as e:
        save_result(None, PS_COMMAND, str(e))

