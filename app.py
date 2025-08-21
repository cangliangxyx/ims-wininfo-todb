import schedule, time
from src.utils.logger_config import configure_logger
from src.exporters import insert_data_to_db, executor

# 调用日志配置模块进行配置
logger = configure_logger("app")

def execute_main_task():
    """执行主任务"""
    logger.info("任务执行开始...")
    start_time = time.time()
    try:
        executor.main()
        insert_data_to_db.main()
    except Exception as e:
        logger.error(f"vCenter 插入数据库失败: {e}", exc_info=True)
    elapsed_time = time.time() - start_time
    logger.info(f"任务完成，耗时 {elapsed_time:.2f} 秒。")

def schedule_daily_task():
    """定时任务，每 5 分钟执行一次"""
    logger.info("任务调度器已启动，每 60 分钟执行一次任务。")
    # 启动后立即运行一次
    execute_main_task()
    # 每60分钟执行一次任务
    schedule.every().hour.do(execute_main_task)
    while True:
        schedule.run_pending()
        logger.info("等待下一次任务执行...")
        time.sleep(60)  # 每 60 秒检查一次任务队列

if __name__ == "__main__":
    schedule_daily_task()
