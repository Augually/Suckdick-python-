from openai import OpenAI
import time
import tkinter as tk

client = OpenAI(api_key="sk-a499c2e953654a66802c7309021ed11b", base_url="https://api.deepseek.com")
msgs= [{"role": "system", "content": "你是一个乐于回答各种问题的小助手，你的任务是提供专业、准确、有洞察力的建议。"}]

while(1):
   # msg=input("你要对dick说：")
    root = tk.Tk()
    text_box = tk.Text(root)
    text_box.pack()
    root.mainloop()
    config=input("键入以确定")
    msg = text_box.get("1.0", tk.END)
    msgs.append({"role":"user","content":msg})
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=msgs,
        stream=True,
        max_tokens=8192
    )
    print("dick说：",end="")
    msg=""
    for chunk in response:
        delta=chunk.choices[0].delta.content
        print(delta,end="")
        msg+=delta
    print("")
    print("")
    time.sleep(1)
    msgs.append({"role":"assistant","content":msg})
    


