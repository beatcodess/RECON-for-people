from duckduckgo_search import DDGS
import requests, io, re
from PyPDF2 import PdfReader

def search_pdfs(n,c):
    q=f'"{n}" "{c}" filetype:pdf'
    out=[]
    with DDGS() as d:
        for r in d.text(q,max_results=25):
            u=r.get("href","")
            if not u.endswith(".pdf"): continue
            try:
                b=requests.get(u,timeout=10).content
                reader=PdfReader(io.BytesIO(b))
            except:
                continue
            text=" ".join(p.extract_text() or "" for p in reader.pages)
            score=sum(1 for x in [n,c] if x.lower() in text.lower())
            out.append({
                "url":u,
                "pages":len(reader.pages),
                "metadata":reader.metadata,
                "confidence":round(score/2,2),
                "matches":re.findall(rf".{{0,40}}({n}|{c}).{{0,40}}",text,re.I)
            })
    return out
