import subprocess
import json
from src.utils.settings import PS_COMMAND
from src.utils.logger_config import configure_logger, set_file_paths

# 调用日志配置模块进行配置
logger = configure_logger("excutor")

def read_powershell_output(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            output = f.read()
        return output
    except Exception as e:
        logger.error(f"读取 {file_path} 失败: {e}")
        return None

def execute_powershell_command():
    try:
        logger.info("执行 PowerShell 命令...")
        result = subprocess.run(
            ["powershell", "-Command", PS_COMMAND],
            capture_output=True, text=True, check=True
        )
        data = json.loads(result.stdout)
        logger.info(f"PowerShell 执行成功，结果: {json.dumps(data, indent=4, ensure_ascii=False)}")
        return [data] if isinstance(data, dict) else data
    except subprocess.CalledProcessError as e:
        logger.error(f"PowerShell 执行失败: {e}")
        # output = read_powershell_output('log/output_powershell.txt')
        return None
    except json.JSONDecodeError as e:
        logger.error(f"JSON 解析失败: {e}")
    except Exception as e:
        logger.error(f"未知错误: {e}")

def save_data_to_json(data):
    try:
        rds_license_file_path = set_file_paths("log","test.json")
        # 保存数据到 JSON 文件
        with open(rds_license_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info(f"数据成功保存到: {rds_license_file_path}")
    except Exception as e:
        logger.error(f"保存 JSON 数据失败: {e}")

def main():
    data = execute_powershell_command()
    logger.info(f"执行结果: {data}")
    save_data_to_json(data)

if __name__ == "__main__":
    main()
    print(read_powershell_output("log/output_powershell.txt"))

