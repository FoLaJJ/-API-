from openai import OpenAI
from SystemRunCommands import SystemCommandExecutor
from CommandInterpreter import CommandInterpreter
from typing import Dict, Any


class HunyuanChat:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = OpenAI(
            api_key=config['API_KEY'],
            base_url=config['BASE_URL'],
        )
        self.command_executor = SystemCommandExecutor(config)
        self.command_interpreter = CommandInterpreter(config)
        self.chat_history = []
        self.base_system_prompt = config['BASE_SYSTEM_PROMPT']

    def format_history(self):
        """将历史记录格式化为文本"""
        history_text = "\n\n历史对话：\n"
        for msg in self.chat_history:
            role = "用户" if msg["role"] == "user" else "助手"
            history_text += f"{role}：{msg['content']}\n"
        return history_text

    def chat(self, prompt: str) -> str:
        try:
            # 构建包含历史记录的完整提示
            full_prompt = self.base_system_prompt + self.format_history() + "\n当前用户问题：" + prompt

            # 首先进行普通对话
            messages = [
                {"role": "system", "content": full_prompt},
                {"role": "user", "content": prompt}
            ]

            response = self.client.chat.completions.create(
                model=self.config['MODEL_NAME'],
                messages=messages,
                max_tokens=self.config['MAX_TOKENS'],
                temperature=self.config['TEMPERATURE'],
            )

            response_text = response.choices[0].message.content

            # 仅当回答中包含明确的系统操作请求时，才尝试解释为命令
            if any(keyword in prompt.lower() for keyword in self.config['COMMAND_TRIGGER_KEYWORDS']):
                command_messages = [
                    {"role": "system", "content": self.command_interpreter.system_prompt},
                    {"role": "user", "content": prompt}
                ]

                command_response = self.client.chat.completions.create(
                    model=self.config['MODEL_NAME'],
                    messages=command_messages,
                    max_tokens=self.config['MAX_TOKENS'],
                    temperature=self.config['TEMPERATURE'],
                )

                is_command, command_data, _ = self.command_interpreter.parse_response(
                    command_response.choices[0].message.content
                )

                if is_command and command_data:
                    intro = f"执行命令: {command_data['description']}\n"
                    result = self.command_executor.execute_command(command_data['command'])
                    response_text = f"{intro}\n{result}"

            # 更新对话历史
            self.chat_history.append({"role": "user", "content": prompt})
            self.chat_history.append({"role": "assistant", "content": response_text})

            # 保持历史记录在合理范围内
            if len(self.chat_history) > self.config['MAX_HISTORY_TURNS'] * 2:
                self.chat_history = self.chat_history[-self.config['MAX_HISTORY_TURNS']*2:]

            return response_text

        except Exception as e:
            return f"调用失败: {str(e)}"