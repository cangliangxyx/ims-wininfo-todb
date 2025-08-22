import json
import os
import sys
from datetime import datetime
from typing import Optional

def get_base_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
LOG_DIR = os.path.join(BASE_DIR, "log")
OUTPUT_JSON = os.path.join(LOG_DIR, "data.json")
LOG_FILE = os.path.join(LOG_DIR, "wininfo.log")

def save_result(data: Optional[str], command: str, error: Optional[str] = None, env: str = "prod"):
    os.makedirs(LOG_DIR, exist_ok=True)

    # 处理输出数据
    parsed = None
    if data is not None:
        try:
            parsed = json.loads(data)
        except json.JSONDecodeError:
            parsed = {"raw_output": data}

        # 成功时才写 data.json
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(parsed, f, ensure_ascii=False, indent=4)

    # 写 wininfo.log
    log_entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "env": env,
        "command": command,
        "status": "success" if error is None else "failed",
        "error": error
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    # 控制台输出
    print(f"[{datetime.now().isoformat(timespec='seconds')}] Command executed ({env}): {command} -> {log_entry['status']}")

# 测试用例
if __name__ == "__main__":
    save_result('{"test": 123}', "Get-Process", None, env="test")
    save_result(None, "BadCommand", "PowerShell 执行失败: 找不到命令", env="prod")
    print(f"结果写入 {OUTPUT_JSON}，日志写入 {LOG_FILE}")
