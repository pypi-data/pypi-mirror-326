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
        pool_config = db_config.copy()
        pool_config.update({
            'pool_name': 'mypool',
            'pool_size': 5,            # 根据实际负载调整
            'pool_reset_session': True,
            'use_pure': True,
            'get_warnings': False,     
            'raise_on_warnings': False,
            'autocommit': True,        
            'buffered': True,
            'connect_timeout': 20,     
            'charset': 'utf8mb4',
            'use_unicode': True,
            'collation': 'utf8mb4_unicode_ci',  # 添加字符集校对规则
            'consume_results': True,    # 自动消费结果
            'allow_local_infile': True, # 允许本地文件操作
        })
        
        # 移除不支持的参数
        for key in ['connection_attempts', 'time_between_attempts', 'ssl_disabled']:
            pool_config.pop(key, None)
        
        self.pool = MySQLConnectionPool(**pool_config)
        
        # 修改表名映射，使用更精确的匹配规则
        self.table_mapping = {
            ('销售明细', 'sell_detail', 'sale_detail'): 'sales_detail',
            ('门店信息', 'store_info', 'shop_info'): 'store_info',
            ('门店目标', 'store_target', 'shop_target'): 'store_target',
            ('产品匹配', 'product_mapping'): 'product_mapping',
            ('实物库存', 'physical_inventory'): 'physical_inventory',
            ('战役目标', 'campaign_target'): 'campaign_target',
            ('服务匹配', 'service_mapping'): 'service_mapping',
            ('电子验机', 'device_acceptance'): 'device_acceptance'
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
        
        # 扩展字段类型映射
        self.special_columns.update({
            # 金额相关
            'amount': 'DECIMAL(15,2)',
            'price': 'DECIMAL(12,2)',
            'cost': 'DECIMAL(12,2)',
            'discount': 'DECIMAL(10,2)',
            
            # 数量相关
            'quantity': 'INT',
            'stock': 'INT',
            'count': 'INT',
            'number': 'INT',
            
            # 比率相关
            'percentage': 'DECIMAL(5,2)',
            'rate': 'DECIMAL(5,2)',
            'ratio': 'DECIMAL(5,2)',
            
            # 状态相关
            'status': 'VARCHAR(50)',
            'state': 'VARCHAR(50)',
            'type': 'VARCHAR(50)',
            
            # 时间相关
            'time': 'DATETIME',
            'date': 'DATE',
            'created_at': 'DATETIME',
            'updated_at': 'DATETIME',
            
            # 联系方式
            'mobile': 'VARCHAR(20)',
            'phone': 'VARCHAR(20)',
            'email': 'VARCHAR(100)',
            'address': 'TEXT',
            
            # 编码相关
            'code': 'VARCHAR(50)',
            'number': 'VARCHAR(50)',
            'serial': 'VARCHAR(50)',
            'id_card': 'VARCHAR(18)',
            
            # 描述相关
            'description': 'TEXT',
            'remark': 'TEXT',
            'comment': 'TEXT',
            'note': 'TEXT'
        })
        
        # 添加批量处理配置
        self.batch_size = 10000  # 增加批量处理大小，因为看到现在的处理速度还可以更快

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
        """优化的表名获取逻辑"""
        file_name = file_name.lower()
        # 移除文件扩展名
        file_name = os.path.splitext(file_name)[0]
        
        # 精确匹配
        for keywords, table_name in self.table_mapping.items():
            if any(keyword in file_name and len(file_name) - len(keyword) < 10 
                   for keyword in keywords):
                return table_name
        
        # 如果没有匹配到，抛出更详细的错误
        raise ValueError(f"无法从文件名 '{file_name}' 确定表名。支持的文件名关键词: "
                        f"{[k for keys in self.table_mapping.keys() for k in keys]}")

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
            'percentage': (0, 100),
            'amount': (0, 10000000),
            'discount': (0, 100),
            'age': (0, 150),
            'stock': (0, 1000000)
        }
        
        # 检查字符串长度
        length_constraints = {
            'code': 50,
            'name': 100,
            'phone': 20,
            'email': 100,
            'id_card': 18
        }
        
        # 检查格式
        format_constraints = {
            'email': r'^[\w\.-]+@[\w\.-]+\.\w+$',
            'phone': r'^\d{11}$',
            'id_card': r'^\d{17}[\dXx]$'
        }
        
        # 检查唯一性
        unique_fields = ['id', 'code', 'phone', 'email']
        for field in unique_fields:
            if field in df.columns and df[field].duplicated().any():
                errors.append(f"字段 {field} 存在重复值")
        
        return errors

    def process_excel(self, file_path: str, incremental: bool = False) -> None:
        """处理Excel文件并导入到数据库"""
        # 禁用 openpyxl 警告
        import warnings
        warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
        
        df = pd.read_excel(
            file_path,
            engine='openpyxl',
            dtype_backend='numpy_nullable'
        )
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
            
            # 优化数据转换
            values = []
            for _, row in df.iterrows():
                row_values = []
                for val in row:
                    if pd.isna(val) or val == 'nan':
                        row_values.append(None)
                    elif isinstance(val, str) and val.strip() == '':
                        row_values.append(None)
                    else:
                        row_values.append(val)
                values.append(tuple(row_values))
            
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
        
        # 先将所有列转换为字符串类型
        for col in df.columns:
            if df[col].dtype != 'datetime64[ns]':
                df[col] = df[col].astype(str)
        
        # 处理数值类型的列
        numeric_cols = []
        for col in df.columns:
            try:
                # 尝试转换为数值类型
                df[col] = pd.to_numeric(df[col], errors='raise')
                numeric_cols.append(col)
            except (ValueError, TypeError):
                continue
        
        if numeric_cols:
            df[numeric_cols] = df[numeric_cols].fillna(0)
            # 对浮点数进行精度控制
            float_cols = df[numeric_cols].select_dtypes(include=['float64']).columns
            if not float_cols.empty:
                df[float_cols] = df[float_cols].round(2)
        
        # 处理日期时间列
        datetime_cols = df.select_dtypes(include=['datetime64']).columns
        for col in datetime_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            df[col] = df[col].fillna(pd.NaT).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # 处理其他列
        other_cols = df.select_dtypes(include=['object']).columns
        for col in other_cols:
            df[col] = df[col].fillna('').astype(str).str.strip()
        
        # 处理特殊值
        df = df.replace({
            'nan': '', 
            'None': '', 
            'NaT': '', 
            'NaN': '',
            'nat': '',
            'null': '',
            'NULL': '',
            'Null': '',
            'undefined': '',
            'UNDEFINED': ''
        })
        
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

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """数据清洗"""
        # 移除前后空格
        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].str.strip()
        
        # 统一大小写
        case_sensitive_cols = ['email', 'code', 'id']
        for col in case_sensitive_cols:
            if col in df.columns:
                df[col] = df[col].str.lower()
        
        # 移除特殊字符
        special_chars_pattern = r'[#$%^&*]'
        text_cols = df.select_dtypes(include=['object']).columns
        for col in text_cols:
            df[col] = df[col].str.replace(special_chars_pattern, '', regex=True)
        
        # 标准化日期格式
        date_cols = df.select_dtypes(include=['datetime64']).columns
        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        
        return df