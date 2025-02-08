from excel_to_db import ExcelProcessor, DBConfig, get_excel_files, print_summary, setup_logging
import logging

def main():
    # 配置数据库
    db_config = DBConfig.create_config(
        host='my4897743842.xincache1.cn',
        user='my4897743842',
        password='My4897743842',
        database='my4897743842',
        connect_timeout=20,        # 增加连接超时时间
        connection_attempts=3,     # 增加重试次数
        time_between_attempts=3    # 重试间隔时间
    )
    
    # 设置日志
    setup_logging()
    logging.info("开始执行Excel导入程序")
    
    try:
        # 创建处理器实例
        processor = ExcelProcessor(db_config)
        
        # 获取并处理所有Excel文件
        success_files = []
        failed_files = []
        
        # 处理所有Excel文件
        for file_name in get_excel_files("excel_files"):
            try:
                processor.process_excel(f"excel_files/{file_name}")
                success_files.append(file_name)
                logging.info(f"成功处理文件: {file_name}")
            except Exception as e:
                failed_files.append((file_name, str(e)))
                logging.error(f"处理文件失败: {file_name}, 错误: {str(e)}")
        
        # 打印汇总信息
        print_summary(success_files, failed_files)
        
    except Exception as e:
        logging.error(f"程序执行出错: {str(e)}")
        raise
    finally:
        logging.info("Excel导入程序执行完成")

if __name__ == "__main__":
    main() 