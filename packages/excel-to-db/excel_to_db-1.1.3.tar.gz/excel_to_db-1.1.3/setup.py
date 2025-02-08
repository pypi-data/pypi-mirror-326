from setuptools import setup, find_packages
import io
import os

# 获取项目根目录
here = os.path.abspath(os.path.dirname(__file__))

# 使用 UTF-8 编码读取 README
with io.open(os.path.join(here, "docs", "README.md"), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="excel-to-db",
    version="1.1.3",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for importing Excel files to MySQL database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/excel_to_db",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pandas>=1.3.0",
        "mysql-connector-python>=8.0.26",
        "openpyxl>=3.0.7",
        "tqdm>=4.62.0",
        "click>=8.0.1",
        "PyYAML>=5.4.1"
    ],
    entry_points={
        'console_scripts': [
            'excel2db=excel_to_db.cli:cli',
        ],
    },
    python_requires=">=3.6",
) 