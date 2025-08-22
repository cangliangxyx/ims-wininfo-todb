# src/run_powershell.py
import subprocess
import sys
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
    # 允许传入命令行参数，便于单独测试
    if len(sys.argv) < 2:
        print("Usage: python run_powershell.py '<PowerShell Command>'")
        sys.exit(1)

    ps_command = sys.argv[1]

    try:
        output = run_powershell(ps_command)
        save_result(output, ps_command, None)
        print("执行成功，结果已保存到 data.json")
    except Exception as e:
        save_result(None, ps_command, str(e))
        print(f"执行失败: {e}")
