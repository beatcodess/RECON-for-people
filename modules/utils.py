import json, os
from collections import defaultdict
from jinja2 import Template
from reportlab.platypus import SimpleDocTemplate,Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def resolve(d):
    score=0
    score+=sum(v.get("confidence",0) for v in d.get("mentions",[]))
    score+=sum(v.get("confidence",0) for v in d.get("pdfs",[]))
    d["overall_confidence"]=round(min(score/10,1),2)
    return d

def save_report(d):
    d=resolve(d)
    os.makedirs("output",exist_ok=True)
    with open("output/report.json","w",encoding="utf-8") as f:
        json.dump(d,f,indent=2)

def html_report():
    d=json.load(open("output/report.json"))
    t=Template("<html><body><h2>Summary</h2><pre>{{d}}</pre></body></html>")
    open("output/report.html","w").write(t.render(d=json.dumps(d,indent=2)))

def pdf_report():
    d=json.load(open("output/report.json"))
    doc=SimpleDocTemplate("output/report.pdf")
    styles=getSampleStyleSheet()
    doc.build([Paragraph(json.dumps(d,indent=2).replace("<","&lt;"),styles["Normal"])])

def load_plugins(d):
    if not os.path.isdir("plugins"): return
    for p in os.listdir("plugins"):
        if p.endswith(".py"):
            m=__import__("plugins."+p[:-3],fromlist=["run"])
            if hasattr(m,"run"): m.run(d)
