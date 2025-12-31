import subprocess, sys, importlib.util
reqs=["requests","duckduckgo-search","Pillow","jinja2","reportlab"]
for r in reqs:
    if importlib.util.find_spec(r.replace("-","_")) is None:
        subprocess.check_call([sys.executable,"-m","pip","install",r])
import app
app.run()