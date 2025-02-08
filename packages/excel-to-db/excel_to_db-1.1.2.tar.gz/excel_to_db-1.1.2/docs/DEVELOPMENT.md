# 开发指南

## 环境设置

1. **克隆仓库**
```bash
git clone https://github.com/yourusername/excel_to_db.git
cd excel_to_db
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **安装开发依赖**
```bash
pip install -r requirements-dev.txt
```

## 项目结构

```
excel_to_db/
├── src/
│   └── excel_to_db/
│       ├── __init__.py      # 包初始化
│       ├── processor.py     # 核心处理逻辑
│       ├── utils.py         # 工具函数
│       ├── config.py        # 配置管理
│       └── cli.py           # 命令行接口
├── tests/
│   ├── __init__.py
│   └── test_processor.py
├── examples/
│   ├── simple_import.py
│   └── batch_import.py
└── docs/
    ├── README.md
    └── DEVELOPMENT.md
```

## 开发流程

1. **创建新功能分支**
```bash
git checkout -b feature/your-feature-name
```

2. **运行测试**
```bash
pytest tests/
```

3. **代码格式化**
```bash
black src/excel_to_db tests examples
```

4. **代码检查**
```bash
flake8 src/excel_to_db tests examples
mypy src/excel_to_db
```

5. **构建和发布**
```bash
python -m build
twine upload dist/*
```

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 版本发布流程

1. 更新版本号
2. 更新 CHANGELOG.md
3. 创建发布标签
4. 构建并上传到 PyPI 