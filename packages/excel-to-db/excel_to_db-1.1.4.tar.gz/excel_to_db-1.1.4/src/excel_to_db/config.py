import yaml
import os
from typing import Dict, Any

class ValidationConfig:
    """数据验证配置"""
    @staticmethod
    def get_default_rules():
        return {
            'required_fields': ['id', 'code', 'name'],
            'numeric_constraints': {
                'price': (0, 1000000),
                'quantity': (0, 100000),
                'percentage': (0, 100)
            },
            'string_lengths': {
                'code': 50,
                'name': 100,
                'description': 1000
            },
            'date_range': {
                'start_date': '1900-01-01',
                'end_date': '2100-12-31'
            }
        }

class Config:
    @staticmethod
    def load_config(config_file: str = 'config.yml') -> Dict[str, Any]:
        """从YAML文件加载配置"""
        if not os.path.exists(config_file):
            return {}
            
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def save_config(config: Dict[str, Any], config_file: str = 'config.yml'):
        """保存配置到YAML文件"""
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True)

    @staticmethod
    def get_validation_config(config_file: str = 'config.yml') -> dict:
        """获取验证配置"""
        cfg = Config.load_config(config_file)
        return cfg.get('validation', ValidationConfig.get_default_rules())