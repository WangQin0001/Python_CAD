import yaml
from pathlib import Path


def load_config(config_path="config/settings.yml"):
    """加载配置文件并返回字典"""
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)

        # 验证模板文件是否存在
        if not Path(config["autocad"]["template_path"]).exists():
            raise FileNotFoundError(f"模板文件不存在: {config['autocad']['template_path']}")

        return config
    except Exception as e:
        print(f"配置加载失败: {str(e)}")
        raise
