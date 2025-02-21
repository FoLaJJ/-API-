from ChatGUI import HunyuanChatGUI
import CONFIG
from typing import Dict, Any


def get_config() -> Dict[str, Any]:
    """获取配置字典"""
    return {k: v for k, v in CONFIG.__dict__.items()
            if not k.startswith('_')}


def main():
    try:
        config_dict = get_config()
        app = HunyuanChatGUI(config_dict)
        app.run()
    except Exception as e:
        print(f"程序运行出错: {str(e)}")


if __name__ == "__main__":
    main()