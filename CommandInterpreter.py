from typing import Optional, Tuple, Dict, Any
import json
import platform


class CommandInterpreter:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.os_type = platform.system().lower()
        self.system_prompt = config['COMMAND_INTERPRETER_PROMPT']

    def parse_response(self, response: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        """解析AI响应，判断是否包含合法的系统命令"""
        try:
            command_data = json.loads(response)
            # 检查必要字段
            if all(k in command_data for k in ['command', 'description', 'risk_level']):
                # 检查风险等级
                if command_data['risk_level'] not in ['low', 'medium', 'high']:
                    return False, None, "无效的风险等级"
                # 不执行高风险命令
                if command_data['risk_level'] == 'high':
                    return False, None, "命令风险等级过高"
                return True, command_data, response
        except json.JSONDecodeError:
            pass
        return False, None, response