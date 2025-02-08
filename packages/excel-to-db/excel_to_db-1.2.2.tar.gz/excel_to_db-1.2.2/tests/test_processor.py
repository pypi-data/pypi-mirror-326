import unittest
from excel_to_db import ExcelProcessor, DBConfig
import pandas as pd
import os

class TestExcelProcessor(unittest.TestCase):
    def setUp(self):
        self.db_config = DBConfig.create_config(
            host='localhost',
            user='root',
            password='password',
            database='test_db'
        )
        self.processor = ExcelProcessor(self.db_config)

    def test_clean_column_name(self):
        """测试列名清理"""
        test_cases = [
            ('Product Name', 'product_name'),
            ('  Price  ', 'price'),
            ('Store ID', 'store_id')
        ]
        for input_name, expected in test_cases:
            self.assertEqual(
                self.processor.clean_column_name(input_name),
                expected
            )

    def test_get_table_name(self):
        """测试表名映射"""
        test_cases = [
            ('销售明细.xlsx', 'sales_detail'),
            ('store_info.xlsx', 'store_info'),
            ('产品信息.xlsx', 'product_mapping')
        ]
        for file_name, expected in test_cases:
            self.assertEqual(
                self.processor.get_table_name(file_name),
                expected
            )

    def test_get_sql_type(self):
        """测试SQL类型映射"""
        test_cases = [
            ('int64', 'id', 'BIGINT'),
            ('float64', 'price', 'DECIMAL(10,2)'),
            ('object', 'description', 'TEXT')
        ]
        for dtype, col_name, expected in test_cases:
            self.assertEqual(
                self.processor.get_sql_type(dtype, col_name),
                expected
            )

if __name__ == '__main__':
    unittest.main() 