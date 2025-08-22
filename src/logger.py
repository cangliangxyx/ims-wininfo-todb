import os
import sys
import time

# 获取程序根目录
def get_base_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
LOG_DIR = os.path.join(BASE_DIR, "log")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "wininfo.log")

def log(msg_zh: str, msg_en: str = None):
    """
    双语日志：
    - msg_zh 写入日志文件（中文）
    - msg_en 打印到控制台（英文），若未提供，则打印 msg_zh
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    # 写入日志文件
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg_zh}\n")
    # 控制台输出
    if msg_en:
        print(f"[{timestamp}] {msg_en}")
    else:
        print(f"[{timestamp}] {msg_zh}")
