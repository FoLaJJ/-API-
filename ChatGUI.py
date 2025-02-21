import tkinter as tk
import threading
from datetime import datetime
from ConnectToHunyuan import HunyuanChat
from tkinter import ttk, scrolledtext, messagebox
import time
from typing import Dict, Any


class HunyuanChatGUI:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.chat_bot = HunyuanChat(config)
        self.setup_window()
        self.create_widgets()
        self.setup_tags()
        self.show_welcome_message()

    def setup_window(self):
        self.window = tk.Tk()
        self.window.title(self.config['WINDOW_TITLE'])
        self.window.geometry(self.config['WINDOW_SIZE'])

        # 配置样式
        style = ttk.Style()
        style.configure("Send.TButton", font=(self.config['FONT_FAMILY'], self.config['FONT_SIZE']))

    def create_widgets(self):
        # 创建聊天显示区域
        self.chat_display = scrolledtext.ScrolledText(
            self.window,
            wrap=tk.WORD,
            font=(self.config['FONT_FAMILY'], self.config['FONT_SIZE']),
            bg=self.config['BG_COLOR']
        )
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_display.config(state='disabled')

        # 创建底部输入框架
        input_frame = ttk.Frame(self.window)
        input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

        # 创建输入框
        self.input_box = ttk.Entry(
            input_frame,
            font=(self.config['FONT_FAMILY'], self.config['FONT_SIZE'])
        )
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # 创建发送按钮
        self.send_button = ttk.Button(
            input_frame,
            text="发送",
            style="Send.TButton",
            command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT)

        # 绑定回车键发送消息
        self.input_box.bind('<Return>', lambda e: self.send_message())

    def setup_tags(self):
        # 设置各种文本样式标签
        self.chat_display.tag_configure("welcome_title",
                                      font=(self.config['FONT_FAMILY'], 14, 'bold'),
                                      foreground='#2C3E50',
                                      justify='center'
                                      )
        self.chat_display.tag_configure("welcome_content",
                                      font=(self.config['FONT_FAMILY'], self.config['FONT_SIZE']),
                                      foreground='#666666',
                                      justify='center'
                                      )
        self.chat_display.tag_configure("welcome_divider",
                                      font=(self.config['FONT_FAMILY'], self.config['FONT_SIZE']),
                                      foreground='#95A5A6',
                                      justify='center'
                                      )

    def show_welcome_message(self):
        self.chat_display.config(state='normal')

        # 添加装饰性分隔线
        self.chat_display.insert(tk.END, "\n" + "=" * 50 + "\n\n", "welcome_divider")

        # 添加标题
        self.chat_display.insert(tk.END, f"{self.config['WELCOME_TITLE']}\n\n", "welcome_title")

        # 添加内容
        self.chat_display.insert(tk.END, f"{self.config['WELCOME_CONTENT']}\n", "welcome_content")

        # 添加底部分隔线
        self.chat_display.insert(tk.END, "\n" + "=" * 50 + "\n\n", "welcome_divider")

        self.chat_display.config(state='disabled')

    def append_message(self, role, message):
        self.chat_display.config(state='normal')
        timestamp = datetime.now().strftime('%H:%M:%S')

        if role == "user":
            self.chat_display.insert(tk.END, f"\n你 ({timestamp}):\n", "user")
        else:
            self.chat_display.insert(tk.END, f"\n小小混元 ({timestamp}):\n", "assistant")

        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')

    def send_message(self):
        user_input = self.input_box.get().strip()
        if not user_input:
            return

        # 清空输入框
        self.input_box.delete(0, tk.END)

        # 显示用户输入
        self.append_message("user", user_input)

        # 禁用发送按钮，防止重复发送
        self.send_button.config(state='disabled')
        self.input_box.config(state='disabled')

        # 在新线程中处理API请求
        def process_response():
            response = self.chat_bot.chat(user_input)

            # 如果响应包含系统命令，显示确认对话框
            if "执行命令:" in response:
                # 使用 self.window.after 来确保在主线程中显示对话框
                dialog_result = []
                self.window.after(0, lambda: dialog_result.append(
                    messagebox.askyesno("确认", "此操作将执行系统命令，是否继续？")
                ))

                # 等待对话框结果
                while not dialog_result:
                    time.sleep(0.1)

                if not dialog_result[0]:
                    self.window.after(0, lambda: self.append_message("assistant", "已取消执行命令。"))
                    self.window.after(0, lambda: self.send_button.config(state='normal'))
                    self.window.after(0, lambda: self.input_box.config(state='normal'))
                    self.window.after(0, lambda: self.input_box.focus())
                    return

            # 在主线程中更新UI
            self.window.after(0, lambda: self.append_message("assistant", response))
            self.window.after(0, lambda: self.send_button.config(state='normal'))
            self.window.after(0, lambda: self.input_box.config(state='normal'))
            self.window.after(0, lambda: self.input_box.focus())

        threading.Thread(target=process_response, daemon=True).start()

    def run(self):
        self.window.mainloop()