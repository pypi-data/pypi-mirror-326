from typing import List, Tuple, Dict, Any
import os
from tqdm import tqdm
import logging
from datetime import datetime
import traceback

class DBConfig:
    """数据库配置管理"""
    @staticmethod
    def get_default_config():
        """获取默认配置"""
        return {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'test',
            'connect_timeout': 10
        }
    
    @staticmethod
    def create_config(host: str, user: str, password: str, database: str, **kwargs):
        """创建数据库配置"""
        config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'connect_timeout': kwargs.get('connect_timeout', 10)
        }
        return config

def setup_logging(log_dir: str = "logs") -> None:
    """设置日志系统"""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f"excel_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    # 禁用一些不必要的日志
    logging.getLogger('openpyxl').setLevel(logging.WARNING)
    logging.getLogger('mysql.connector').setLevel(logging.WARNING)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

class ProgressBar:
    """进度条管理器"""
    def __init__(self, total: int, desc: str = "处理进度"):
        self.pbar = tqdm(total=total, desc=desc)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pbar.close()
    
    def update(self, n: int = 1):
        self.pbar.update(n)

def get_excel_files(directory: str) -> List[str]:
    """获取目录下的所有Excel文件"""
    if not os.path.exists(directory):
        raise FileNotFoundError(f"目录不存在: {directory}")
    
    excel_files = []
    for file in os.listdir(directory):
        if file.endswith(('.xlsx', '.xls')):
            excel_files.append(file)
    return excel_files

def print_summary(success_files: List[str], failed_files: List[Tuple[str, str]]) -> None:
    """优化的处理结果汇总"""
    print("\n处理完成!")
    print(f"\n成功导入 {len(success_files)} 个文件:")
    for file in success_files:
        print(f"✓ {file}")
    
    if failed_files:
        print(f"\n导入失败 {len(failed_files)} 个文件:")
        for file, error in failed_files:
            print(f"✗ {file}: {error}")
    
    print("\n总结:")
    print(f"总文件数: {len(success_files) + len(failed_files)}")
    print(f"成功导入: {len(success_files)}")
    print(f"导入失败: {len(failed_files)}")

def handle_error(error: Exception, context: str) -> str:
    """处理错误并返回友好的错误信息"""
    error_msg = str(error)
    error_type = type(error).__name__
    
    # 记录完整错误信息到日志
    logging.error(f"{context} - 错误类型: {error_type}\n完整错误信息:\n{traceback.format_exc()}")
    
    # 用户友好提示
    error_mapping = {
        'ValueError': f"{context}: 数据格式错误",
        'TypeError': f"{context}: 数据类型错误",
        'IntegrityError': f"{context}: 数据完整性错误",
        'OperationalError': f"{context}: 数据库操作错误",
        'ProgrammingError': f"{context}: SQL语法错误"
    }
    
    return error_mapping.get(error_type, f"{context}: 发生未知错误 - {error_msg}")[:500]  # 限制错误信息长度

def backup_table(cursor, table_name: str) -> str:
    """备份数据表"""
    backup_name = f"{table_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    cursor.execute(f"CREATE TABLE {backup_name} LIKE {table_name}")
    cursor.execute(f"INSERT INTO {backup_name} SELECT * FROM {table_name}")
    return backup_name

def restore_table(cursor, table_name: str, backup_name: str):
    """从备份恢复数据表"""
    cursor.execute(f"TRUNCATE TABLE {table_name}")
    cursor.execute(f"INSERT INTO {table_name} SELECT * FROM {backup_name}")

def get_table_info(cursor, table_name: str) -> Dict:
    """获取表信息"""
    # 获取列信息
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    columns = cursor.fetchall()
    
    # 获取表统计信息
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]
    
    return {
        'columns': columns,
        'row_count': row_count
    }

def format_sql_value(value: Any) -> str:
    """格式化SQL值"""
    if value is None:
        return 'NULL'
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, datetime):
        return f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'"
    else:
        return f"'{str(value)}'"