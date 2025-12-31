import asyncio,aiohttp,itertools,hashlib,time,socket

PLATFORMS={
"GitHub":(["https://github.com/{}"],3),
"GitLab":(["https://gitlab.com/{}"],3),
"Bitbucket":(["https://bitbucket.org/{}"],3),
"Twitter":(["https://twitter.com/{}","https://x.com/{}"],2),
"Instagram":(["https://instagram.com/{}"],2),
"Facebook":(["https://facebook.com/{}"],1),
"Reddit":(["https://reddit.com/user/{}","https://old.reddit.com/user/{}"],2),
"Telegram":(["https://t.me/{}","https://t.me/s/{}"],3),
"TikTok":(["https://tiktok.com/@{}"],2),
"Snapchat":(["https://snapchat.com/add/{}"],1),
"Steam":(["https://steamcommunity.com/id/{}"],2),
"SoundCloud":(["https://soundcloud.com/{}"],2),
"Spotify":(["https://open.spotify.com/user/{}"],2),
"DeviantArt":(["https://deviantart.com/{}"],2),
"Imgur":(["https://imgur.com/user/{}"],2),
"Kaggle":(["https://kaggle.com/{}"],3),
"LeetCode":(["https://leetcode.com/{}"],3),
"HackerRank":(["https://hackerrank.com/{}"],3),
"DockerHub":(["https://hub.docker.com/u/{}"],3),
"PyPI":(["https://pypi.org/user/{}"],3),
"NPM":(["https://www.npmjs.com/~{}"],3),
"Medium":(["https://medium.com/@{}"],2),
"Mastodon":(["https://mastodon.social/@{}"],2),
"VK":(["https://vk.com/{}"],2),
"Pinterest":(["https://pinterest.com/{}"],1),
"Tumblr":(["https://{}.tumblr.com"],2),
"Linktree":(["https://linktr.ee/{}"],2),
"Carrd":(["https://{}.carrd.co"],2),
"TryHackMe":(["https://tryhackme.com/p/{}"],4),
"HackTheBox":(["https://app.hackthebox.com/users/{}"],4),
"RootMe":(["https://www.root-me.org/{}"],4),
"CTFtime":(["https://ctftime.org/user/{}"],4),
"HackerOne":(["https://hackerone.com/{}"],4),
"Bugcrowd":(["https://bugcrowd.com/{}"],4),
"ExploitDB":(["https://www.exploit-db.com/?author={}"],4),
"Pastebin":(["https://pastebin.com/u/{}"],4),
"Keybase":(["https://keybase.io/{}"],4),
"0x00sec":(["https://0x00sec.org/u/{}"],5),
"HackForums":(["https://hackforums.net/member.php?action=profile&uid={}"],5),
"Nulled":(["https://nulled.to/user/{}"],5),
"Cracked":(["https://cracked.io/{}"],5),
"Breached":(["https://breached.vc/User-{}"],5),
"XSS":(["https://xss.is/user/{}"],5),
"BlackHatWorld":(["https://www.blackhatworld.com/members/{}.{}"],5),
"LOLZ":(["https://lolz.guru/members/{}"],5),
"Antichat":(["https://antichat.ru/members/{}"],5),
"Doxbin":(["https://doxbin.org/user/{}","https://doxbin.com/user/{}"],5),
"GreySec":(["https://greysec.net/members/{}"],5),
"OpenBugBounty":(["https://www.openbugbounty.org/researchers/{}"],4),
"HackThisSite":(["https://www.hackthissite.org/user/view/{}"],4),
"PacketStorm":(["https://packetstormsecurity.com/user/{}"],4),
"DefconForums":(["https://forum.defcon.org/member.php?action=profile&uid={}"],4),
"ExploitIN":(["https://exploit.in/members/{}"],5),
"Underc0de":(["https://underc0de.org/foro/index.php?action=profile;u={}"],5)
}

VARIANTS=["{}","@{}","{}.html","{}/","u/{}","user/{}","users/{}","profile/{}","member/{}"]
CACHE={}
TTL=3600

def _tor_available():
    try:
        s=socket.create_connection(("127.0.0.1",9050),2)
        s.close()
        return True
    except:
        return False

def _mutations(u):
    subs={"a":"4","e":"3","i":"1","o":"0","s":"5","t":"7"}
    out={u,u.lower()}
    for k,v in subs.items():
        out.add(u.replace(k,v))
        out.add(u.replace(k,v).lower())
    for i in range(30):
        out.add(f"{u}{i}")
        out.add(f"{u}_{i}")
    return out

def _expand():
    urls=[]
    for bases,_ in PLATFORMS.values():
        for b,v in itertools.product(bases,VARIANTS):
            urls.append(b.replace("{}",v))
    return urls

ALL_URLS=_expand()

async def _check(session,sem,url):
    async with sem:
        try:
            async with session.get(url,allow_redirects=True) as r:
                if r.status in (200,301,302) and "login" not in str(r.url):
                    return url
        except:
            return None

async def _runner(username,use_tor):
    key=hashlib.sha1((username+str(use_tor)).encode()).hexdigest()
    if key in CACHE and time.time()-CACHE[key]["t"]<TTL:
        return CACHE[key]["d"]
    found={}
    sem=asyncio.Semaphore(70 if use_tor else 140)
    proxy="socks5h://127.0.0.1:9050" if use_tor and _tor_available() else None
    conn=aiohttp.TCPConnector(limit=70 if use_tor else 140,ssl=False)
    async with aiohttp.ClientSession(connector=conn) as s:
        tasks=[]
        for m in _mutations(username):
            for u in ALL_URLS:
                tasks.append(_check(s,sem,u.format(m)))
        for r in await asyncio.gather(*tasks):
            if r:
                dom=r.split("/")[2]
                for name,(bases,w) in PLATFORMS.items():
                    if any(b.split("/")[2] in dom for b in bases):
                        found.setdefault(name,{"weight":w,"urls":[]})["urls"].append(r)
    CACHE[key]={"t":time.time(),"d":found}
    return found

def find_socials(username,tor=False):
    return asyncio.run(_runner(username,tor))
