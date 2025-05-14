import tkinter as tk
from tkinter import scrolledtext
from openai import OpenAI
import time

API_KEY = input('Please enter API_KEY')
URL = input('Please enter URL')
client = OpenAI(api_key=API_KEY, base_url=URL)
msgs= [{"role": "system", "content": "你是一个乐于回答各种问题的小助手，你的任务是提供专业、准确、有洞察力的建议。"}]

class MessageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("you say：")
        
    
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=40)
        self.text_area.pack(padx=10, pady=10)
        self.send_button = tk.Button(root, text="发送", command=self.send_message)
        self.send_button.pack(pady=5)
        self.msg = None
        self.waiting_for_message = False
        
    def send_message(self):
        self.msg = self.text_area.get("1.0", tk.END).strip()
        self.text_area.delete("1.0", tk.END)
        self.text_area.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)
        self.waiting_for_message = True
        self.process_message()
        
    def process_message(self):
        if self.msg:
            msgs.append({"role":"user","content":self.msg})
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=msgs,
                stream=True,
                max_tokens=8000
            )
            print("deepseek says：",end="")
            self.msg=""
            for chunk in response:
                delta=chunk.choices[0].delta.content
                print(delta,end="")
                self.msg+=delta
            print("")
            print("")
            time.sleep(1)
            msgs.append({"role":"assistant","content":self.msg})

            self.finish_processing()
            
    def finish_processing(self):
        self.msg = None
        self.waiting_for_message = False
        self.text_area.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)
        self.text_area.focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    app = MessageApp(root)
    root.mainloop()
