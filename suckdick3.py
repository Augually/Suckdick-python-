import tkinter as tk
from tkinter import scrolledtext
from openai import OpenAI
import time
from datetime import datetime#为日志增加
import threading #引入多线程


API_KEY = ""#enter your api_key here
URL = ""#enter your URL here

BG_COLOR = "#f0f0f0"
TEXT_BG = "#ffffff"
BUTTON_COLOR = "#4a6fa5"
BUTTON_TEXT = "#ffffff"
ACCENT_COLOR = "#166088"

FONT_FAMILY = "Microsoft YaHei"  # Windows默认，可根据系统调整
TEXT_FONT = (FONT_FAMILY, 11)
BUTTON_FONT = (FONT_FAMILY, 10, "bold")


client = OpenAI(api_key=API_KEY, base_url=URL)

button_style = {
    'bg': BUTTON_COLOR,
    'fg': BUTTON_TEXT,
    'font': BUTTON_FONT,
    'activebackground': "#3a5a80",
    'activeforeground': BUTTON_TEXT,
    'relief': tk.RAISED,
    'borderwidth': 2
}

text_style = {
    'wrap':tk.WORD,
    'width':80,
    'height':20,
    'bg':TEXT_BG,
    'fg':"#333333",
    'font':TEXT_FONT,  #字体样式
    'insertbackground':ACCENT_COLOR,  # 光标颜色
    'padx':10,
    'pady':10,
    'relief':tk.SUNKEN,  # 添加凹陷边框效果
    'borderwidth':2,
    'highlightbackground':"#cccccc",
    'highlightthickness':1
    
}

pad_options = {'padx': 10, 'pady': 5}

#按钮效果
def on_enter(e):
    e.widget['background'] = '#3a5a80'

def on_leave(e):
    e.widget['background'] = BUTTON_COLOR

def create_new_window():
    root = tk.Toplevel()  # 使用Toplevel而不是Tk,开启多窗口
    app = MessageApp(root)
    return root

class MessageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("say to deepseek：")
        self.root.configure(bg=BG_COLOR)
        self.msgs = [{"role": "system", "content": "你是一个乐于回答各种问题的小助手，你的任务是提供专业、准确、有洞察力的建议。"}]
        root.grid_rowconfigure(0, weight=1)  # 第一行可扩展
        root.grid_columnconfigure(0, weight=1)  # 第一列可扩展
        root.grid_columnconfigure(1, weight=1)  # 第二列可扩展
        main_frame = tk.Frame(root, bg=BG_COLOR)
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.status_bar = tk.Label(root, text="ready to chat", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=3, column=0, columnspan=2, sticky="we")
        self.text_area = scrolledtext.ScrolledText(root, **text_style)
        self.text_area.grid(row=0, column=0, **pad_options, sticky="nsew")
        self.text_area.config(spacing1=5, spacing2=2, spacing3=5)
        self.send_button = tk.Button(root, text="Send", **button_style, command=self.send_message)
        self.send_button.grid(row=1, column=0, pady=5, sticky="n")
        self.msg = None
        self.waiting_for_message = False
        self.output_area = scrolledtext.ScrolledText(root, **text_style)
        self.output_area.grid(row=0, column=1, **pad_options, sticky="nsew")
        self.output_area.config(spacing1=5, spacing2=2, spacing3=5)
        self.output_area.config(state=tk.DISABLED)  
        self.save_button = tk.Button(root, text="Save", **button_style, command=self.save_to_log)
        self.save_button.grid(row=1, column=1, pady=5, sticky="n")
        self.new_window_btn = tk.Button(root, text="New Chat", **button_style, command=create_new_window)
        self.new_window_btn.grid(row=2, column=0, columnspan=2, pady=5)
        self.send_button.bind("<Enter>", on_enter)
        self.send_button.bind("<Leave>", on_leave)
        self.save_button.bind("<Enter>", on_enter)
        self.save_button.bind("<Leave>", on_leave)
        self.new_window_btn.bind("<Enter>", on_enter)
        self.new_window_btn.bind("<Leave>", on_leave)
    
    def send_message(self):
        self.msg = self.text_area.get("1.0", tk.END).strip()
        self.text_area.delete("1.0", tk.END)
        self.text_area.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)
        self.waiting_for_message = True
        threading.Thread(target=self.process_message, daemon=True).start()
        
    def save_to_log(self):
        content = self.output_area.get("1.0", tk.END)
        try:
            with open("chat_log.txt", "a", encoding="utf-8") as f:
                f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\n\n"+content + "\n")
        except Exception as e:
            print(f"Error saving log: {e}")

    def process_message(self):
        try:
            if self.msg:
                self.msgs.append({"role":"user","content":self.msg})
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=self.msgs,
                    stream=True,
                    max_tokens=8000
                )
                self.display_output("you say to dick:\n"+self.msg)
                self.display_output("\n")
                self.display_output("\n")
                self.display_output("dick says：\n")
                self.msg=""
                for chunk in response:
                    delta=chunk.choices[0].delta.content
                    self.display_output(delta)
                    self.msg+=delta
                time.sleep(1)
                self.display_output("\n")
                self.display_output("\n")
                self.msgs.append({"role":"assistant","content":self.msg})
        except Exception as e:
            self.display_output(f"\nError: {str(e)}\n")
        finally:
            self.root.after(0, self.finish_processing)

    def finish_processing(self):
        self.msg = None
        self.waiting_for_message = False
        self.text_area.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)
        self.text_area.focus_set()
        
    def display_output(self, text):
        """将输出内容添加到输出区域"""
        self.output_area.config(state=tk.NORMAL)
        self.output_area.insert(tk.END, text + "")
        self.output_area.see(tk.END)  
        self.output_area.config(state=tk.DISABLED)
        self.output_area.update() 



if __name__ == "__main__":
    root = tk.Tk()  
    root.withdraw()  
    create_new_window()
    root.mainloop()
