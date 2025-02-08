import os
import click
import logging
from .processor import ExcelProcessor
from .utils import get_excel_files, print_summary, setup_logging, DBConfig, backup_table, get_table_info
from .config import Config

@click.group()
def cli():
    """Excel to DB 导入工具"""
    pass

@cli.command()
@click.option('--config', '-c', type=click.Path(exists=True), help='配置文件路径')
@click.option('--host', help='数据库主机')
@click.option('--user', help='数据库用户名')
@click.option('--password', help='数据库密码')
@click.option('--database', help='数据库名')
@click.option('--incremental', '-i', is_flag=True, help='使用增量更新模式')
@click.argument('excel_file', type=click.Path(exists=True))
def import_file(config, host, user, password, database, incremental, excel_file):
    """导入单个Excel文件"""
    # 加载配置
    cfg = Config.load_config(config) if config else {}
    db_cfg = cfg.get('database', {})
    
    # 命令行参数优先级高于配置文件
    db_config = DBConfig.create_config(
        host=host or db_cfg.get('host', 'localhost'),
        user=user or db_cfg.get('user', 'root'),
        password=password or db_cfg.get('password', ''),
        database=database or db_cfg.get('database', 'test_db')
    )
    
    processor = ExcelProcessor(db_config)
    processor.process_excel(excel_file, incremental=incremental)
    click.echo(f"成功导入: {excel_file}")

@cli.command()
@click.option('--config', '-c', type=click.Path(exists=True), help='配置文件路径')
@click.option('--host', help='数据库主机')
@click.option('--user', help='数据库用户名')
@click.option('--password', help='数据库密码')
@click.option('--database', help='数据库名')
@click.option('--directory', help='Excel文件目录')
def batch_import(config, host, user, password, database, directory):
    """批量导入目录下的所有Excel文件"""
    # 加载配置
    cfg = Config.load_config(config) if config else {}
    db_cfg = cfg.get('database', {})
    excel_cfg = cfg.get('excel', {})
    
    # 创建数据库配置
    db_config = DBConfig.create_config(
        host=host or db_cfg.get('host', 'localhost'),
        user=user or db_cfg.get('user', 'root'),
        password=password or db_cfg.get('password', ''),
        database=database or db_cfg.get('database', 'test_db')
    )
    
    # 设置目录
    excel_dir = directory or excel_cfg.get('directory', 'excel_files')
    
    # 设置日志
    setup_logging()
    
    processor = ExcelProcessor(db_config)
    success_files = []
    failed_files = []
    
    for file_name in get_excel_files(excel_dir):
        try:
            file_path = os.path.join(excel_dir, file_name)
            processor.process_excel(file_path)
            success_files.append(file_name)
            logging.info(f"成功处理文件: {file_name}")
        except Exception as e:
            failed_files.append((file_name, str(e)))
            logging.error(f"处理文件失败: {file_name}, 错误: {str(e)}")
    
    print_summary(success_files, failed_files)

@cli.command()
@click.option('--config', '-c', type=click.Path(exists=True), help='配置文件路径')
@click.option('--host', help='数据库主机')
@click.option('--user', help='数据库用户名')
@click.option('--password', help='数据库密码')
@click.option('--database', help='数据库名')
def test_connection(config, host, user, password, database):
    """测试数据库连接"""
    # 加载配置
    cfg = Config.load_config(config) if config else {}
    db_cfg = cfg.get('database', {})
    
    # 创建数据库配置
    db_config = DBConfig.create_config(
        host=host or db_cfg.get('host', 'localhost'),
        user=user or db_cfg.get('user', 'root'),
        password=password or db_cfg.get('password', ''),
        database=database or db_cfg.get('database', 'test_db')
    )
    
    try:
        processor = ExcelProcessor(db_config)
        processor.test_connection()
        click.echo("数据库连接成功！")
    except Exception as e:
        click.echo(f"连接失败: {str(e)}", err=True)

@cli.command()
@click.option('--output', '-o', type=click.Path(), default='config.yml', help='配置文件输出路径')
def init_config(output):
    """生成默认配置文件"""
    default_config = {
        'database': {
            'host': 'localhost',
            'user': 'root',
            'password': 'password',
            'database': 'test_db',
            'connect_timeout': 10
        },
        'excel': {
            'directory': 'excel_files',
            'batch_size': 5000
        },
        'logging': {
            'level': 'INFO',
            'directory': 'logs'
        }
    }
    
    Config.save_config(default_config, output)
    click.echo(f"配置文件已生成: {output}")

@cli.command()
@click.option('--config', '-c', type=click.Path(exists=True), help='配置文件路径')
@click.option('--table', required=True, help='表名')
def backup(config, table):
    """备份数据表"""
    cfg = Config.load_config(config) if config else {}
    db_cfg = cfg.get('database', {})
    
    db_config = DBConfig.create_config(
        host=db_cfg.get('host', 'localhost'),
        user=db_cfg.get('user', 'root'),
        password=db_cfg.get('password', ''),
        database=db_cfg.get('database', 'test_db')
    )
    
    processor = ExcelProcessor(db_config)
    conn = processor.get_connection()
    cursor = conn.cursor()
    
    try:
        backup_name = backup_table(cursor, table)
        conn.commit()
        click.echo(f"表 {table} 已备份为: {backup_name}")
    except Exception as e:
        click.echo(f"备份失败: {str(e)}", err=True)
    finally:
        cursor.close()
        conn.close()

@cli.command()
@click.option('--config', '-c', type=click.Path(exists=True), help='配置文件路径')
@click.option('--table', required=True, help='表名')
def show_info(config, table):
    """显示表信息"""
    cfg = Config.load_config(config) if config else {}
    db_cfg = cfg.get('database', {})
    
    db_config = DBConfig.create_config(
        host=db_cfg.get('host', 'localhost'),
        user=db_cfg.get('user', 'root'),
        password=db_cfg.get('password', ''),
        database=db_cfg.get('database', 'test_db')
    )
    
    processor = ExcelProcessor(db_config)
    conn = processor.get_connection()
    cursor = conn.cursor()
    
    try:
        info = get_table_info(cursor, table)
        click.echo(f"\n表名: {table}")
        click.echo(f"行数: {info['row_count']}")
        click.echo("\n列信息:")
        for col in info['columns']:
            click.echo(f"  {col[0]}: {col[1]}")
    except Exception as e:
        click.echo(f"获取信息失败: {str(e)}", err=True)
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    cli()