from duckduckgo_search import DDGS
import re, hashlib, datetime, requests
from bs4 import BeautifulSoup

def _hash(u):
    return hashlib.sha256(u.encode()).hexdigest()

def _extract_time(html):
    for k in ["time","date","publish","modified"]:
        m=re.search(rf'{k}[^0-9]*(\d{{4}}[-/]\d{{2}}[-/]\d{{2}})',html,re.I)
        if m:
            return m.group(1)
    return None

def _snippet(html,terms):
    soup=BeautifulSoup(html,"html.parser")
    text=soup.get_text(" ",strip=True)
    for t in terms:
        if t.lower() in text.lower():
            i=text.lower().find(t.lower())
            return text[max(0,i-80):i+120]
    return text[:200]

def search_mentions(n,c,u):
    q=f'"{n}" "{c}" OR "{u}"'
    seen={}
    out=[]
    terms=[n,c,u]
    with DDGS() as d:
        for r in d.text(q,max_results=40):
            url=r.get("href")
            if not url: continue
            h=_hash(url)
            if h in seen: continue
            try:
                resp=requests.get(url,timeout=6)
                html=resp.text
            except:
                continue
            t=_extract_time(html) or str(datetime.date.today())
            sn=_snippet(html,terms)
            score=sum(1 for x in terms if x.lower() in html.lower())
            seen[h]=1
            out.append({
                "title":r.get("title"),
                "url":url,
                "date":t,
                "confidence":round(score/len(terms),2),
                "snippet":sn
            })
    return sorted(out,key=lambda x:x["date"])
