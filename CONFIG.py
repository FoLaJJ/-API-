"""
配置文件
"""

# API配置
API_KEY = "sk-xxxx"     # 填入自己的key
BASE_URL = "https://api.hunyuan.cloud.tencent.com/v1"
MODEL_NAME = "hunyuan-pro"
MAX_TOKENS = 1000
TEMPERATURE = 0.7

# 对话历史配置
MAX_HISTORY_TURNS = 10

# GUI配置
WINDOW_TITLE = "腾讯混元AI助手"
WINDOW_SIZE = "800x600"
FONT_FAMILY = "微软雅黑"
FONT_SIZE = 10
BG_COLOR = "#f5f5f5"

# 提示词配置
BASE_SYSTEM_PROMPT = """你是腾讯混元AI助手。请以对话的方式回答问题。
只有当用户明确要求执行系统操作时，才考虑转换为系统命令。
对于一般性的问题（如"你是谁"），请直接回答而不是执行系统命令。

以下是之前的对话历史，请基于这些历史信息回答用户的问题：
"""

COMMAND_INTERPRETER_PROMPT = """你是一个系统命令解释器。
当用户用自然语言描述想要执行的操作时，请将其转换为对应的系统命令。

请按以下格式返回：
{
    "command": "实际的系统命令",
    "description": "命令的简短描述",
    "risk_level": "low/medium/high"  # 命令的风险等级
}

注意事项：
1. 仅返回JSON格式，不要包含其他文字
2. 仅处理查询类和信息获取类命令，不处理修改系统的命令
3. 不允许执行危险命令，如删除、格式化等
4. Windows和Linux命令可能不同，请根据上下文选择合适的命令
"""

# 欢迎信息配置
WELCOME_TITLE = "欢迎使用腾讯混元AI助手"
WELCOME_CONTENT = """您可以在下方输入框中输入问题，按回车键或点击发送按钮与AI进行对话。祝您使用愉快！"""

# 命令执行配置
COMMAND_TIMEOUT = 10
COMMAND_TRIGGER_KEYWORDS = ["帮我执行" , "运行命令"]
