import subprocess
import platform
from typing import Optional, Dict, Any


class SystemCommandExecutor:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.os_type = platform.system().lower()

    def execute_command(self, command: str) -> str:
        """
        执行系统命令的通用方法

        Args:
            command: 要执行的命令

        Returns:
            命令执行结果
        """
        try:
            # 将命令字符串分割成列表
            if isinstance(command, str):
                command = command.split()

            # 执行命令
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=self.config['COMMAND_TIMEOUT']
            )

            if result.returncode == 0:
                return result.stdout
            else:
                return f"命令执行失败:\n{result.stderr}"

        except subprocess.TimeoutExpired:
            return f"命令执行超时（{self.config['COMMAND_TIMEOUT']}秒）"
        except Exception as e:
            return f"执行出错: {str(e)}"