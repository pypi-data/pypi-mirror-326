# Excel to DB

一个用于将 Excel 文件批量导入到 MySQL 数据库的 Python 工具。

## 安装

1. **从 PyPI 安装**
```bash
pip install excel-to-db
```

2. **从源码安装**
```bash
git clone https://github.com/yourusername/excel_to_db.git
cd excel_to_db
pip install -e .
```

## 使用方法

1. **命令行使用**

```bash
# 生成配置文件
excel2db init-config -o config.yml

# 导入单个文件
excel2db import-file example.xlsx

# 批量导入目录下的文件
excel2db batch-import --directory excel_files

# 测试数据库连接
excel2db test-connection
```

2. **Python API 使用**

```python
from excel_to_db import ExcelProcessor, DBConfig

# 配置数据库
db_config = DBConfig.create_config(
    host='your_host',
    user='your_username',
    password='your_password',
    database='your_database'
)

# 初始化处理器
processor = ExcelProcessor(db_config)

# 处理单个文件
processor.process_excel("path/to/your/excel_file.xlsx")
```

## 配置文件

配置文件使用 YAML 格式：

```yaml
database:
  host: localhost
  user: root
  password: password
  database: test_db
  connect_timeout: 10

excel:
  directory: excel_files
  batch_size: 5000

logging:
  level: INFO
  directory: logs
```

## 支持的数据表

| 文件关键词 | 数据库表名 | 说明 |
|-----------|------------|------|
| 销售/sell/sale | sales_detail | 销售明细数据 |
| 门店信息/store/shop | store_info | 门店基础信息 |
| 目标/target | store_target | 门店目标数据 |
| 产品/product | product_mapping | 产品信息映射 |
| 库存/inventory | physical_inventory | 实物库存数据 |
| 战役/campaign | campaign_target | 战役目标数据 |
| 服务/service | service_mapping | 服务信息映射 |
| 验机/device | device_acceptance | 电子验机数据 |

## 开发指南

1. **安装开发依赖**
```bash
pip install -r requirements-dev.txt
```

2. **运行测试**
```bash
pytest tests/
```

3. **代码格式化**
```bash
black src/excel_to_db tests examples
```

## 许可证

MIT License