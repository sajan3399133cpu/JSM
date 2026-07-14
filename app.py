# JSM VIDEO GENERATOR - MASTER V1.0 LOCKED - 26 JAN 2026
# CHECKLIST LOCKED: 16 Lang | 30 Cat | 6 Platforms(Pexels5+Pixabay+Coverr+Mixkit+Videvo+Popular) | 20Min | Safe Filter Kw | 540p Internal Golden UI | Download Fix | 20min Chunks 25
import gradio as gr,asyncio,edge_tts,uuid,random,requests,re,os,json,base64,urllib.parse,datetime
from moviepy.editor import VideoFileClip,ColorClip,concatenate_videoclips,AudioFileClip
from PIL import Image
B="JSM VIDEO GENERATOR";CONTACT="03043399133"
K1="c2JfcHVibGlzaGFibGVfMVc0Tks2WDdFZGFjbV9lU0JJY0ZEUV9Da1Q2YzRFWQ=="
K2="NTYzODYyOTMtMTRmYWNkOTRmZGFjMjZmOWZjMzdmNWYyYw=="
K3="OGM4YzU5MmIwN2E1N2UwNWRjNDkzNjhiMzk5Yjc2NTk="
K4=['Uk9LSnZmWXV1U2tjN1FWVkw2VmpDZ1lGeUI4VVFaQ0xMQ2N0RDJTZlRKY2xJckRHbzVFeDNKTVg2','em5pWXZhdmhhbDY2Vkd3dVYya1VJcFJtN3ZHM1kwcmRkREx1enJJVHZtUHFRMjZrZEcwdmN5eTA=','ZjZJS3hySFI4TUhqMWdlRDYyY3JMVGZEVFFYMHM3ZXdGa3czaEVJNGQ0Q2VuUlRaWENrcENXRDk=','MWo2a0ZxMUdSQjQyOTFGMXMxUk1naGxnSVgzZDN1NzhPYVRwaURLbXRJU0FqSmtLUGI5dlZUa0w=','dHBreXBvZ3N3djA3bjg0ZGgwaWFISTl0YW11NDNHRWN2Wm9rQTNYaTNKU1RVVDBOVjMyQTZnRzk=']
def D(e):
 try:return base64.b64decode(e.encode()).decode()
 except:return ""
PK=D(K2);XK=[D(k) for k in K4]
VOICES={"English Male":"en-US-GuyNeural","English Female":"en-US-JennyNeural","Urdu Male":"ur-PK-AsadNeural","Urdu Female":"ur-PK-UzmaNeural","Hindi Male":"hi-IN-MadhurNeural","Hindi Female":"hi-IN-SwaraNeural","Arabic Male":"ar-SA-HamedNeural","Arabic Female":"ar-SA-ZariyahNeural","Spanish Male":"es-ES-AlvaroNeural","Spanish Female":"es-ES-ElviraNeural","French Male":"fr-FR-HenriNeural","French Female":"fr-FR-DeniseNeural","German Male":"de-DE-ConradNeural","German Female":"de-DE-KatjaNeural","Turkish Male":"tr-TR-AhmetNeural","Turkish Female":"tr-TR-EmelNeural"}
CATS=["Business & Finance","Crypto & Trading","Islamic & Quran","News & Breaking","Sports & Cricket","Technology & AI","Health & Doctor","Farming Kisan","Kitchen Cooking","Trending Viral","Politics Trump","Education","Motivation","Real Estate","Gold & Silver","Cars & Bikes","Pets & Animals","Beauty & Fashion","Travel","Food Vlog","Fitness","History","Science","Comedy","Music","Kids","Army & Police","Weather","Property","Jobs"]
PACKAGES={"ASIF":100,"ALI":100,"JSM":100,"ASIF786":600,"JSM30":30,"JSM100":100,"JSM300":300,"JSM500":500,"JSM786":600,"JSM600":600,"JSMGOLD":1000,"JSM786GOLD":9999}
FREE_DB="/tmp/free_daily.json";LICENSE_DB="/tmp/jsm_licenses_final.json"
def Lj(p):
 try:
  if os.path.exists(p):return json.load(open(p))
 except:pass
 return{}
def Sj(p,d):
 try:json.dump(d,open(p,'w'))
 except:pass
def safe(t):return re.sub(r'[^\w\s\-.,:;()#@ ]','',t)[:80]
def Kw(text,category):
    l=text.lower()
    if "trump" in l: return f"Donald Trump {random.choice(['speech','white house','press'])}"
    if "biden" in l: return f"Joe Biden {random.choice(['speech','white house'])}"
    if "imran" in l or "pakistan politics" in l: return f"Pakistan parliament Imran Khan"
    if "kisan" in l or "farming" in l or "khet" in l or "tractor" in l: return random.choice(["farmer tractor field","agriculture farmer working","wheat farm harvest"])
    if "business" in l or "finance" in l or "economy" in l or "inflation" in l or "market" in l: return random.choice(["stock market trading","business finance office","wall street chart"])
    if "cricket" in l: return "cricket stadium match"
    words=re.findall(r'\w+',l)
    clean=[w for w in words if len(w)>3][:4]
    base=" ".join(clean) if clean else l[:20]
    return base+" "+(category or "")+" professional"
def Ai(p,path,W=960,H=540):
 q=urllib.parse.quote(p[:600])
 try:
  r=requests.get(f"https://image.pollinations.ai/prompt/{q} safe?width={W}&height={H}&model=flux&nologo=true&seed={random.randint(1,999999)}",timeout=20)
  if r.status_code==200 and len(r.content)>5000:open(path,'wb').write(r.content);return path
 except:pass
 Image.new('RGB',(W,H),color=(15,23,42)).save(path);return path
def St(k,d,W,H,cat):
    q=Kw(k,cat)
    page=random.randint(1,4)
    for key in XK:
        try:
            r=requests.get(f"https://api.pexels.com/videos/search?query={urllib.parse.quote(q)}&per_page=5&page={page}",headers={"Authorization":key},timeout=8)
            j=r.json()
            if 'videos' in j and j['videos']:
                vid=random.choice(j['videos'])
                link=next((v['link'] for v in vid['video_files'] if 640 <= v['width'] <= 1280), vid['video_files'][0]['link'])
                t=f"/tmp/{uuid.uuid4().hex[:5]}.mp4";open(t,'wb').write(requests.get(link,timeout=10).content)
                clip=VideoFileClip(t).resize((W,H))
                return clip.loop(duration=d) if clip.duration<d else clip.subclip(0,d)
        except:continue
    try:
        if PK:
            r=requests.get(f"https://pixabay.com/api/videos/?key={PK}&q={urllib.parse.quote(q)}&per_page=5&page={page}&safesearch=true",timeout=8)
            hits=r.json().get('hits',[])
            if hits:
                hit=random.choice(hits)
                ln=hit['videos']['tiny']['url'] if 'tiny' in hit['videos'] else hit['videos']['medium']['url']
                t=f"/tmp/{uuid.uuid4().hex[:5]}.mp4";open(t,'wb').write(requests.get(ln,timeout=10).content)
                clip=VideoFileClip(t).resize((W,H))
                return clip.loop(duration=d) if clip.duration<d else clip.subclip(0,d)
    except:pass
    try:
        r=requests.get(f"https://coverr.co/s?q={urllib.parse.quote(q)}",headers={"User-Agent":"Mozilla/5.0"},timeout=8)
        m=re.findall(r'https://coverr\.co/videos/[^"]+',r.text)
        if m:
            r2=requests.get(random.choice(m[:3]),headers={"User-Agent":"Mozilla/5.0"},timeout=8)
            mp4=re.findall(r'https://[^"]+\.mp4',r2.text)
            if mp4:
                t=f"/tmp/{uuid.uuid4().hex[:5]}.mp4";open(t,'wb').write(requests.get(mp4[0],timeout=10).content)
                clip=VideoFileClip(t).resize((W,H))
                return clip.loop(duration=d) if clip.duration<d else clip.subclip(0,d)
    except:pass
    try:
        r=requests.get(f"https://mixkit.co/free-stock-video/{urllib.parse.quote(q.replace(' ','-'))}/",headers={"User-Agent":"Mozilla/5.0"},timeout=8)
        mp4=re.findall(r'https://[^"]*mixkit[^"]*\.mp4',r.text)
        if mp4:
            t=f"/tmp/{uuid.uuid4().hex[:5]}.mp4";open(t,'wb').write(requests.get(random.choice(mp4[:2]),timeout=10).content)
            clip=VideoFileClip(t).resize((W,H))
            return clip.loop(duration=d) if clip.duration<d else clip.subclip(0,d)
    except:pass
    try:
        r=requests.get(f"https://www.videvo.net/search/{urllib.parse.quote(q)}/",headers={"User-Agent":"Mozilla/5.0"},timeout=8)
        mp4=re.findall(r'https://[^"]+\.mp4',r.text)
        uniq=list(set([x for x in mp4 if 'videvo' in x or 'preview' in x]))[:2]
        if uniq:
            t=f"/tmp/{uuid.uuid4().hex[:5]}.mp4";open(t,'wb').write(requests.get(random.choice(uniq),timeout=10).content)
            clip=VideoFileClip(t).resize((W,H))
            return clip.loop(duration=d) if clip.duration<d else clip.subclip(0,d)
    except:pass
    try:
        r=requests.get(f"https://api.pexels.com/videos/popular?per_page=5&page={page}",headers={"Authorization":XK[0]},timeout=8)
        j=r.json()
        if 'videos' in j and j['videos']:
            vid=random.choice(j['videos'])
            link=vid['video_files'][0]['link']
            t=f"/tmp/{uuid.uuid4().hex[:5]}.mp4";open(t,'wb').write(requests.get(link,timeout=8).content)
            clip=VideoFileClip(t).resize((W,H))
            return clip.loop(duration=d) if clip.duration<d else clip.subclip(0,d)
    except:pass
    return ColorClip((W,H),color=(random.randint(10,40),random.randint(20,60),random.randint(60,100)),duration=d)
async def Tt(t,o,v):await edge_tts.Communicate(t,v).save(o)
def run_tts(text,out,voice):
 try:
  loop=asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  loop.run_until_complete(Tt(text,out,voice))
  loop.close()
 except:pass
def Gen(email,code,script,lang,cat,vtype):
 if not script.strip():return None,None,"","","","Script likho"
 if not email.strip():return None,None,"","","","Email likho"
 W,H=(540,960) if "TikTok" in vtype else(960,540)
 code=code.strip().upper() if code else"";today=datetime.date.today();email=email.strip().lower()
 if not code or code not in PACKAGES:
  fd=Lj(FREE_DB);ek=email+"_"+today.isoformat();ut=fd.get(ek,0)
  if ut>=1:return None,None,"","","",f"Daily 1 Min Free Khatam! {CONTACT}"
  rem=1-ut;free=True;ft=fd;et=ek;lic_db=None
 else:
  lic_db=Lj(LICENSE_DB);lic=lic_db.get(code)
  if not lic:
   lic={"bound_email":email,"total":PACKAGES[code],"used":0.0,"expiry":str(today+datetime.timedelta(days=30)),"created":str(today)}
   lic_db[code]=lic;Sj(LICENSE_DB,lic_db)
  else:
   if lic["bound_email"]!=email:return None,None,"","","",f"LOCKED! {lic['bound_email']} se bandha hai!"
   if today>datetime.date.fromisoformat(lic["expiry"]):return None,None,"","","",f"EXPIRED {lic['expiry']} Renew {CONTACT}"
   if lic["used"]>=lic["total"]:return None,None,"","","",f"Khatam {lic['used']:.1f}/{lic['total']}m"
  rem=lic["total"]-lic["used"];free=False
 title=safe(script);desc=safe(script[:400]);ht="#JSM"
 pvs=[]
 try:
  sents=[s.strip() for s in re.split(r'[.!?۔]+',script) if s.strip()];chs=[];cur=""
  for s in sents:
   if len(cur)+len(s)<550:cur+=s+". "
   else:chs.append(cur);cur=s+". "
  if cur:chs.append(cur)
  if not chs:chs=[script]
  chs=chs[:25];needT=0.0
  for idx,ch in enumerate(chs):
   ap=f"/tmp/{uuid.uuid4().hex[:5]}.mp3"
   run_tts(ch,ap,VOICES.get(lang,"en-US-GuyNeural"))
   if not os.path.exists(ap):continue
   au=AudioFileClip(ap)
   if not au or au.duration==0:continue
   nd=au.duration/60.0;needT+=nd
   if needT>rem+0.1:
    au.close()
    return None,None,"","","",f"Need {needT:.1f}m Baki {rem:.1f}m"
   if needT>22:
    au.close()
    break
   inn=[s.strip() for s in re.split(r'[.!?]+',ch) if s.strip()][:2]
   if not inn:inn=[ch[:30]]
   per=au.duration/max(len(inn),1)
   clips=[St(s,per,W,H,cat).set_duration(per) for s in inn]
   fn=concatenate_videoclips(clips,method="compose").set_audio(au)
   vp=f"/tmp/P_{idx}_{uuid.uuid4().hex[:4]}.mp4"
   fn.write_videofile(vp,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',bitrate='800k',logger=None)
   pvs.append(VideoFileClip(vp))
   au.close()
  if not pvs:return None,None,"","","","No parts"
  fv=concatenate_videoclips(pvs,method="compose")
  out_dir="/tmp/gradio";os.makedirs(out_dir,exist_ok=True)
  vf=f"{out_dir}/FINAL_{uuid.uuid4().hex[:5]}.mp4"
  fv.write_videofile(vf,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',bitrate='800k',logger=None)
  tp=f"{out_dir}/T_{uuid.uuid4().hex[:4]}.jpg";Ai(script,tp,W,H)
  if free:
   ft[et]=ut+needT;Sj(FREE_DB,ft)
   return vf,tp,title,desc,ht,f"FREE {needT:.1f}m Used {ft[et]:.1f}/1.0"
  else:
   lic_db[code]["used"]+=needT;Sj(LICENSE_DB,lic_db)
   nr=lic_db[code]["total"]-lic_db[code]["used"]
   return vf,tp,title,desc,ht,f"PAID {code} Baki {nr:.1f}/{lic_db[code]['total']}m Exp {lic_db[code]['expiry']}"
 except Exception as e:return None,None,"","","",f"Error:{str(e)[:120]}"
 finally:
  for c in pvs:
   try:c.close()
   except:pass
css="""
.gradio-container{background:linear-gradient(180deg,#0a0a0a 0%,#141414 100%)!important}
#header{text-align:center;padding:20px 0 10px 0}
#header h1{color:#FFD700!important;font-size:38px!important;font-weight:900!important;letter-spacing:2px!important;text-shadow:0 0 20px rgba(255,215,0,0.5)!important;margin:0!important}
#header p{color:#bfa75a!important;font-size:14px!important;margin-top:5px!important;letter-spacing:1px!important}
#features{display:flex;justify-content:center;gap:12px;margin:15px 0;flex-wrap:wrap}
.feat{background:linear-gradient(135deg,#1a1a1a,#2a2a2a);border:1px solid #FFD700;border-radius:20px;padding:6px 14px;color:#FFD700;font-size:12px;font-weight:600}
button.primary{background:linear-gradient(90deg,#D4AF37,#FFD700,#D4AF37)!important;color:#000!important;font-weight:900!important;font-size:18px!important;height:56px!important;border-radius:14px!important;box-shadow:0 4px 20px rgba(255,215,0,0.4)!important}
.gr-input,.gr-dropdown,textarea{background:#1e1e1e!important;border:1px solid #333!important;color:#fff!important;border-radius:12px!important}
label{color:#FFD700!important;font-weight:600!important}
"""
with gr.Blocks(title="JSM VIDEO GENERATOR",css=css) as demo:
 gr.HTML(f"""
 <div id="header">
 <h1>✦ JSM VIDEO GENERATOR ✦</h1>
 <p>AI POWERED VIDEO STUDIO</p>
 <div id="features">
 <div class="feat">🎙️ 16 Languages</div>
 <div class="feat">🎬 30 Categories</div>
 <div class="feat">⏱️ 20 Min Long</div>
 <div class="feat">🔒 Safe Filter</div>
 <div class="feat">⚡ 6 Platforms</div>
 </div>
 </div>
 """)
 with gr.Row():
  email=gr.Textbox(label="Email",placeholder="your@gmail.com")
  code=gr.Textbox(label="License Code",placeholder="ASIF786 for 600min")
  lang=gr.Dropdown(list(VOICES.keys()),value="English Male",label="Language")
 with gr.Row():
  cat=gr.Dropdown(CATS,value="Business & Finance",label="Category")
  vtype=gr.Dropdown(["YouTube 16:9","TikTok 9:16"],value="YouTube 16:9",label="Video Type")
 script=gr.Textbox(lines=6,label="Your Script",placeholder="Type your 20 minute story here...")
 btn=gr.Button("✨ GENERATE VIDEO ✨",variant="primary")
 with gr.Row():
  video=gr.Video(label="Final Video")
  thumb=gr.Image(label="AI Thumbnail")
 with gr.Row():
  t1=gr.Textbox(label="Title");d1=gr.Textbox(label="Description");h1=gr.Textbox(label="Hashtags")
 status=gr.Textbox(label="Status")
 btn.click(Gen,[email,code,script,lang,cat,vtype],[video,thumb,t1,d1,h1,status])
demo.queue(max_size=50).launch(share=True,server_name="0.0.0.0")
