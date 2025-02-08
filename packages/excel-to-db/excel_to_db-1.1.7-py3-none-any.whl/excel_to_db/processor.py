import pandas as pd
import mysql.connector
from mysql.connector import Error
import os
import warnings
from typing import Dict, List, Tuple
from .utils import ProgressBar, handle_error
from mysql.connector.pooling import MySQLConnectionPool
from datetime import datetime
import time

class ExcelProcessor:
    def __init__(self, db_config: dict):
        """初始化处理器"""
        # 优化连接池配置
        pool_config = db_config.copy()
        pool_config.update({
            'pool_name': 'mypool',
            'pool_size': 5,            # 减小连接池大小
            'pool_reset_session': True,
            'use_pure': True,          # 使用纯Python实现
            'get_warnings': False,     
            'raise_on_warnings': False,
            'autocommit': True,        
            'buffered': True,
            'connect_timeout': 20,     # 增加连接超时时间
            'charset': 'utf8mb4',
            'use_unicode': True,
        })
        
        # 移除不支持的参数
        for key in ['connection_attempts', 'time_between_attempts', 'ssl_disabled']:
            pool_config.pop(key, None)
        
        self.pool = MySQLConnectionPool(**pool_config)
        
        # 定义关键词到表名的映射
        self.table_mapping = {
            ('销售', 'sell', 'sale'): 'sales_detail',
            ('门店信息', 'store', 'shop'): 'store_info',
            ('目标', 'target'): 'store_target',
            ('产品', 'product'): 'product_mapping',
            ('库存', 'inventory'): 'physical_inventory',
            ('战役', 'campaign'): 'campaign_target',
            ('服务', 'service'): 'service_mapping',
            ('验机', 'device'): 'device_acceptance'
        }
        
        # 定义字段类型映射
        self.type_mapping = {
            'int64': 'BIGINT',
            'float64': 'DOUBLE',
            'datetime64[ns]': 'DATETIME',
            'object': 'TEXT',
            'bool': 'BOOLEAN'
        }
        
        # 添加特殊字段类型映射
        self.special_columns = {
            'ean': 'TEXT',
            'sku': 'TEXT',
            'barcode': 'TEXT',
            'product_code': 'TEXT',
            'description': 'TEXT',
            'remarks': 'TEXT',
            'comment': 'TEXT',
            'phone': 'VARCHAR(20)',
            'email': 'VARCHAR(100)',
            'address': 'TEXT',
            'price': 'DECIMAL(10,2)',
            'amount': 'DECIMAL(10,2)',
            'quantity': 'INT',
            'percentage': 'DECIMAL(5,2)',
            '机型': 'TEXT',
            'model': 'TEXT',
            'device_model': 'TEXT',
            'name': 'TEXT',
            'title': 'TEXT',
            'content': 'TEXT',
            'detail': 'TEXT',
            'spec': 'TEXT',
            'category': 'TEXT',
            'brand': 'TEXT',
            'remark': 'TEXT',
            'note': 'TEXT',
            'url': 'TEXT',
            'image': 'TEXT',
            'reason': 'TEXT',
            'solution': 'TEXT',
        }
        
        # 添加批量处理配置
        self.batch_size = 5000

    def clean_column_name(self, name: str) -> str:
        """清理列名，转换为数据库友好的格式"""
        return name.strip().lower().replace(' ', '_')

    def get_sql_type(self, dtype: str, column_name: str) -> str:
        """获取SQL数据类型，考虑特殊列名"""
        column_name = column_name.lower()
        if column_name in self.special_columns:
            return self.special_columns[column_name]
        return self.type_mapping.get(str(dtype), 'VARCHAR(255)')

    def get_table_name(self, file_name: str) -> str:
        """根据文件名获取对应的表名"""
        file_name = file_name.lower()
        for keywords, table_name in self.table_mapping.items():
            if any(keyword in file_name for keyword in keywords):
                return table_name
        raise ValueError(f"无法从文件名 {file_name} 确定表名")

    def validate_data(self, df: pd.DataFrame) -> List[str]:
        """验证数据有效性"""
        errors = []
        
        # 检查必填字段
        required_fields = ['id', 'code', 'name']
        for field in required_fields:
            if field in df.columns and df[field].isnull().any():
                errors.append(f"字段 {field} 存在空值")
        
        # 检查数值范围
        numeric_constraints = {
            'price': (0, 1000000),
            'quantity': (0, 100000),
            'percentage': (0, 100)
        }
        
        for col, (min_val, max_val) in numeric_constraints.items():
            if col in df.columns:
                invalid = df[df[col].notnull() & ((df[col] < min_val) | (df[col] > max_val))]
                if not invalid.empty:
                    errors.append(f"字段 {col} 存在超出范围的值")
        
        return errors

    def process_excel(self, file_path: str, incremental: bool = False) -> None:
        """处理Excel文件并导入到数据库"""
        df = pd.read_excel(file_path, engine='openpyxl')
        df = self.preprocess_data(df)
        table_name = self.get_table_name(os.path.basename(file_path))
        
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                with self.pool.get_connection() as conn:
                    cursor = conn.cursor(buffered=True)
                    try:
                        self.create_or_update_table(cursor, table_name, df)
                        self.insert_data(cursor, df, table_name)
                        return  # 成功则返回
                    finally:
                        cursor.close()
            except Exception as e:
                retry_count += 1
                if retry_count == max_retries:
                    raise e
                time.sleep(3)  # 等待3秒后重试

    def test_connection(self):
        """测试数据库连接"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            conn.close()
            return True
        except Error as e:
            raise Error(f"数据库连接测试失败: {str(e)}")

    def get_connection(self):
        """从连接池获取连接"""
        return self.pool.get_connection()

    def create_or_update_table(self, cursor, table_name: str, df: pd.DataFrame):
        """创建或更新表结构"""
        # 获取现有列信息
        try:
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            existing_columns = {col[0]: col[1] for col in cursor.fetchall()}
        except Error:
            # 表不存在，创建新表
            columns = []
            for col in df.columns:
                clean_col = self.clean_column_name(col)
                sql_type = self.get_sql_type(df[col].dtype, clean_col)
                columns.append(f"`{clean_col}` {sql_type}")
            
            create_sql = f"""
            CREATE TABLE {table_name} (
                {', '.join(columns)}
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
            cursor.execute(create_sql)
            return

        # 更新表结构
        for col in df.columns:
            clean_col = self.clean_column_name(col)
            sql_type = self.get_sql_type(df[col].dtype, clean_col)
            
            if clean_col not in existing_columns:
                # 添加新列
                alter_sql = f"ALTER TABLE {table_name} ADD COLUMN `{clean_col}` {sql_type}"
                cursor.execute(alter_sql)
            elif existing_columns[clean_col].upper() != sql_type.upper():
                # 修改列类型
                alter_sql = f"ALTER TABLE {table_name} MODIFY COLUMN `{clean_col}` {sql_type}"
                cursor.execute(alter_sql)

    def insert_data(self, cursor, df: pd.DataFrame, table_name: str):
        """优化的数据插入"""
        try:
            # 准备插入语句
            columns = [f"`{col}`" for col in df.columns]
            placeholders = ', '.join(['%s'] * len(df.columns))
            insert_sql = f"""
            INSERT INTO {table_name} ({', '.join(columns)})
            VALUES ({placeholders})
            """
            
            # 增加批量大小
            self.batch_size = 10000  # 增加批量处理大小
            
            # 优化数据转换
            values = df.where(pd.notnull(df), None).values.tolist()  # 更高效的空值处理
            total_rows = len(values)
            
            with ProgressBar(total_rows, f"导入 {table_name}") as pbar:
                for i in range(0, total_rows, self.batch_size):
                    batch = values[i:i + self.batch_size]
                    try:
                        cursor.executemany(insert_sql, batch)
                        pbar.update(len(batch))
                    except Error as e:
                        error_msg = handle_error(e, f"批量插入 {table_name}")
                        raise Error(error_msg)
                
        except Error as e:
            error_msg = handle_error(e, f"插入数据到 {table_name}")
            raise Error(error_msg)

    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """优化的数据预处理"""
        # 清理列名
        df.columns = [self.clean_column_name(col) for col in df.columns]
        
        # 使用更高效的空值填充
        categorical_cols = df.select_dtypes(include=['object']).columns
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        
        # 批量填充空值
        if not categorical_cols.empty:
            df[categorical_cols] = df[categorical_cols].fillna('')
        if not numeric_cols.empty:
            df[numeric_cols] = df[numeric_cols].fillna(0)
        
        return df

    def incremental_update(self, cursor, df: pd.DataFrame, table_name: str):
        """增量更新数据"""
        # 获取主键列
        cursor.execute(f"SHOW KEYS FROM {table_name} WHERE Key_name = 'PRIMARY'")
        primary_key = cursor.fetchone()[4]  # 获取主键列名
        
        # 备份表
        backup_name = f"{table_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        cursor.execute(f"CREATE TABLE {backup_name} LIKE {table_name}")
        cursor.execute(f"INSERT INTO {backup_name} SELECT * FROM {table_name}")
        
        try:
            # 更新现有记录
            for _, row in df.iterrows():
                pk_value = row[primary_key]
                set_clause = ', '.join([
                    f"`{col}` = {format_sql_value(val)}"
                    for col, val in row.items()
                    if col != primary_key
                ])
                
                update_sql = f"""
                UPDATE {table_name} 
                SET {set_clause}
                WHERE `{primary_key}` = {format_sql_value(pk_value)}
                """
                cursor.execute(update_sql)
                
                # 如果没有更新任何行，说明是新记录
                if cursor.rowcount == 0:
                    columns = [f"`{col}`" for col in df.columns]
                    values = [format_sql_value(val) for val in row]
                    insert_sql = f"""
                    INSERT INTO {table_name} ({', '.join(columns)})
                    VALUES ({', '.join(values)})
                    """
                    cursor.execute(insert_sql)
                    
        except Exception as e:
            # 发生错误时恢复备份
            cursor.execute(f"DROP TABLE {table_name}")
            cursor.execute(f"RENAME TABLE {backup_name} TO {table_name}")
            raise e