import tkinter as tk
from tkinter import ttk
import threading, json, webbrowser
from modules.username_search import find_socials,alias_score
from modules.web_mentions import search_mentions,timeline
from modules.image_search import search_images
from modules.pdf_search import search_pdfs
from modules.utils import save_report,html_report,pdf_report,load_plugins

def run():
    root=tk.Tk()
    dark=tk.BooleanVar()
    root.title("beatcodes")
    root.geometry("1000x650")

    style=ttk.Style()
    def theme():
        if dark.get():
            style.theme_use("clam")
            root.configure(bg="#222")
        else:
            style.theme_use("default")
    theme()

    top=ttk.Frame(root,padding=10)
    top.pack(fill="x")

    brand=tk.Label(top,text="beatcodes",fg="blue",cursor="hand2",font=("Arial",14,"bold"))
    brand.grid(row=0,column=2,sticky="e")
    brand.bind("<Button-1>",lambda e:webbrowser.open("https://guns.lol/beatcodes"))

    name=tk.StringVar()
    city=tk.StringVar()
    user=tk.StringVar()
    proxy=tk.StringVar()

    for i,(t,v) in enumerate([("Name",name),("City",city),("Username",user),("Proxy (optional)",proxy)]):
        ttk.Label(top,text=t).grid(row=i,column=0,sticky="w")
        ttk.Entry(top,textvariable=v,width=45).grid(row=i,column=1,padx=5,pady=2)

    ttk.Checkbutton(top,text="Dark Mode",variable=dark,command=theme).grid(row=1,column=2)

    tabs=ttk.Notebook(root)
    tabs.pack(fill="both",expand=True)

    views={}
    for t in ["Socials","Mentions","Images","PDFs","Timeline","Aliases","Log"]:
        f=ttk.Frame(tabs)
        tabs.add(f,text=t)
        txt=tk.Text(f,wrap="word")
        txt.pack(fill="both",expand=True)
        views[t]=txt

    prog=ttk.Progressbar(root,mode="indeterminate")
    prog.pack(fill="x")

    def worker():
        prog.start()
        data={"name":name.get(),"city":city.get(),"username":user.get()}
        data["social_accounts"]=find_socials(user.get(),proxy.get())
        data["mentions"]=search_mentions(name.get(),city.get(),user.get())
        data["images"]=search_images(name.get(),city.get())
        data["pdfs"]=search_pdfs(name.get(),city.get())
        data["timeline"]=timeline(data["mentions"])
        data["alias_scores"]=alias_score(user.get(),data["social_accounts"])
        load_plugins(data)
        save_report(data)
        for k in ["Socials","Mentions","Images","PDFs","Timeline","Aliases"]:
            views[k].insert("end",json.dumps(data.get(k.lower(),data.get(k)),indent=2))
        views["Log"].insert("end","Saved to output/report.json")
        prog.stop()

    ttk.Button(top,text="Run",command=lambda:threading.Thread(target=worker,daemon=True).start()).grid(row=4,column=1,sticky="e")
    ttk.Button(top,text="Export HTML",command=html_report).grid(row=4,column=2,sticky="w")
    ttk.Button(top,text="Export PDF",command=pdf_report).grid(row=4,column=2,sticky="e")

    root.mainloop()