import subprocess
import os
import logging
from typing import Union, List, Dict

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


def run_powershell(command: Union[str, List[str], Dict[str, str]]) -> Union[str, List[str], Dict[str, str]]:
    """
    执行 PowerShell 命令或脚本，并返回执行结果。
    支持:
      - str : 单条命令
      - list[str] : 多条命令
      - dict[str, str] : 别名 -> 命令
    """

    if isinstance(command, dict):
        logger.info("检测到带别名的命令字典，将依次执行")
        results = {}
        for alias, cmd in command.items():
            results[alias] = run_powershell(cmd)  # 递归调用
        return results

    if isinstance(command, list):
        logger.info("检测到多个 PowerShell 命令，将依次执行")
        return [run_powershell(cmd) for cmd in command]

    if os.path.isfile(command) and command.lower().endswith(".ps1"):
        logger.debug(f"执行 PowerShell 脚本: {command}")
        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", command]
    else:
        logger.debug(f"执行 PowerShell 命令: {command}")
        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-Command", command]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    if result.returncode != 0:
        logger.error(f"执行失败: {result.stderr.strip()}")
        raise RuntimeError(f"PowerShell 执行失败: {result.stderr.strip()}")

    logger.info(f"命令执行成功 # {command}")
    return result.stdout.strip()


if __name__ == "__main__":
    from config.settings import ps_command

    try:
        output = run_powershell(ps_command)
        logger.info("执行结果:\n%s", output)
    except Exception as e:
        logger.exception("运行过程中发生错误")
