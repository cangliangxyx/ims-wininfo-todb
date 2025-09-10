import json
import os
import logging
from datetime import datetime
from typing import Optional, Union, Dict, Any

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def _parse_output(data: Union[str, Dict[str, str]]) -> Dict[str, Any]:
    """解析执行结果，将字符串转换为 JSON 或保留原始输出"""
    parsed: Dict[str, Any] = {}

    if isinstance(data, dict):
        # 多命令模式
        for alias, output in data.items():
            try:
                parsed[alias] = json.loads(output)
            except Exception:
                parsed[alias] = {"raw_output": output}
    elif isinstance(data, str):
        # 单命令模式
        try:
            parsed = json.loads(data)
        except Exception:
            parsed = {"raw_output": data}

    return parsed

def save_command_result(
    data: Union[str, Dict[str, str], None],
    command: Union[str, Dict[str, str]],
    error: Optional[str] = None,
    env: str = "prod",
    base_dir: Optional[str] = None
) -> None:
    """
    保存 PowerShell 执行结果到 data.json 并记录日志
    """
    # 确保目录可写
    base_dir = base_dir or os.getcwd()
    log_dir = os.path.join(base_dir, "log")
    os.makedirs(log_dir, exist_ok=True)

    output_json = os.path.join(log_dir, "data.json")
    log_file = os.path.join(log_dir, "wininfo.log")

    parsed_data: Dict[str, Any] = _parse_output(data) if data else {}

    try:
        if parsed_data and error is None:
            with open(output_json, "w", encoding="utf-8") as f:
                json.dump(parsed_data, f, ensure_ascii=False, indent=4)
            logger.info(f"执行结果已写入 {output_json}")
    except PermissionError as e:
        logger.error(f"无法写入 {output_json}: {e}")
    except OSError as e:
        logger.error(f"写入文件时出错: {e}")

    log_entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "env": env,
        "command": command,
        "status": "success" if error is None else "failed",
        "error": error
    }
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception as e:
        logger.error(f"写入日志失败 {log_file}: {e}")

    if error:
        logger.error("命令执行失败 [%s]: %s", env, error)
    else:
        logger.info("命令执行成功 [%s]", env)
