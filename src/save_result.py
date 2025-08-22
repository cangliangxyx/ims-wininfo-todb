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

def save_result(data: Optional[str], command: str, error: Optional[str] = None):
    os.makedirs(LOG_DIR, exist_ok=True)

    if data is not None:
        try:
            parsed = json.loads(data)
        except json.JSONDecodeError:
            parsed = {"raw_output": data}
    else:
        parsed = None

    # 保存 data.json
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(parsed, f, ensure_ascii=False, indent=4)

    # 写日志
    log_entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "command": command,
        "status": "success" if error is None else "failed",
        "error": error
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    # 可选控制台输出
    print(f"[{datetime.now().isoformat(timespec='seconds')}] 保存结果: {command}, 状态: {'success' if error is None else 'failed'}")

# 测试用例
if __name__ == "__main__":
    save_result('{"test": 123}', "Get-Process", None)
    save_result(None, "BadCommand", "PowerShell 执行失败: 找不到命令")
    print(f"✅ 测试完成，结果写入 {OUTPUT_JSON}，日志写入 {LOG_FILE}")
