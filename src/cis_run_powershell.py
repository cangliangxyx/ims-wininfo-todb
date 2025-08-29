# src/vmware_cis_checker.py

import subprocess
import os
import json
import logging
from typing import Union, Dict, Any
from src.decrypt_message import decrypt_message
from config.settings import get_vsphere_config



# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("CISChecker")

# vCenter 登录信息
vsphere_config = get_vsphere_config()
VCENTER_HOST = vsphere_config["host"]
VCENTER_USER = vsphere_config["user"]
VCENTER_PASS = decrypt_message(vsphere_config["password"])

LOGIN_CMD = (
    f'Connect-VIServer -Server {VCENTER_HOST} '
    f'-Protocol https -User "{VCENTER_USER}" -Password "{VCENTER_PASS}"'
)


def run_powercli(command: str) -> Union[str, None]:
    """
    执行单条 PowerCLI 命令，返回 stdout 或 None
    """
    full_cmd = f"{LOGIN_CMD}; {command}"
    cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-NoProfile", "-Command", full_cmd]

    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        logger.error("命令执行失败 [%s]: %s", command, result.stderr.strip())
        return None
    return result.stdout.strip() or None


def cis_check() -> Dict[str, Any]:
    """
    执行部分 VMware CIS 基准检查，返回 JSON 结果
    """
    checks = {
        "no_1.2": 'Get-VMHost | Select-Object Name, @{Name="NTPSetting"; Expression={ ($_ | Get-VMHostNtpServer) }} | ConvertTo-Json -Depth 3',
        "no_1.4": 'Get-VMHost | Get-AdvancedSetting -Name Mem.ShareForceSalting | Select-Object Name, Value, Type, Description | ConvertTo-Json -Depth 3'
    }

    results: Dict[str, Any] = {}
    for alias, cmd in checks.items():
        output = run_powercli(cmd)
        if output:
            try:
                results[alias] = json.loads(output)
                logger.info("%s 执行成功", alias)
            except Exception:
                results[alias] = {"raw_output": output}
                logger.warning("%s 输出解析失败，保存原始结果", alias)
        else:
            results[alias] = None
            logger.warning("%s 执行失败", alias)
    return results


def save_results(results: Dict[str, Any], path: str = None):
    path = path or os.path.join(os.path.dirname(__file__), "log", "cis_results.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    logger.info("CIS 检查结果已保存到 %s", path)


if __name__ == "__main__":
    cis_results = cis_check()
    save_results(cis_results)
