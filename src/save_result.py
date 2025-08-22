import json
import os
from datetime import datetime

# 统一存放日志的目录
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "log")
OUTPUT_JSON = os.path.join(LOG_DIR, "data.json")
LOG_FILE = os.path.join(LOG_DIR, "wininfo.log")


def save_result(data: str | None, command: str, error: str | None = None):
    """保存结果到 data.json，并将日志写入 wininfo.log"""

    os.makedirs(LOG_DIR, exist_ok=True)

    # 如果有结果就尝试解析，否则写 None
    if data is not None:
        try:
            parsed = json.loads(data)
        except json.JSONDecodeError:
            parsed = {"raw_output": data}
    else:
        parsed = None

    # 保存到 data.json（覆盖）
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(parsed, f, ensure_ascii=False, indent=4)

    # 写运行日志到 wininfo.log（追加）
    log_entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "command": command,
        "status": "success" if error is None else "failed",
        "error": error
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    # 测试成功
    save_result('{"test": 123}', "Get-Process", None)
    # 测试失败
    save_result(None, "BadCommand", "PowerShell 执行失败: 找不到命令")
    print(f"✅ 测试完成，结果写入 {OUTPUT_JSON}，日志写入 {LOG_FILE}")
