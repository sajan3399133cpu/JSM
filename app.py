import gradio as gr,asyncio,edge_tts,uuid,random,requests,re,os,json,base64,urllib.parse,datetime
from moviepy.editor import VideoFileClip,ColorClip,concatenate_videoclips,AudioFileClip,CompositeVideoClip,ImageClip,TextClip
from PIL import Image
import secrets,string

CONTACT="03043399133|03022246271"
ADMIN_PASS="JamSaeed@786#Motha_Owner_0304!"
ON="JAM SAEED MOTHA";ONUM="03043399133";MN="MUJAHID HUSSAIN";MNUM="03022246271"
K4=['Uk9LSnZmWXV1U2tjN1FWVkw2VmpDZ1lGeUI4VVFaQ0xMQ2N0RDJTZlRKY2xJckRHbzVFeDNKTVg2','em5pWXZhdmhhbDY2Vkd3dVYya1VJcFJtN3ZHM1kwcmRkREx1enJJVHZtUHFRMjZrZEcwdmN5eTA=','ZjZJS3hySFI4TUhqMWdlRDYyY3JMVGZEVFFYMHM3ZXdGa3czaEVJNGQ0Q2VuUlRaWENrcENXRDk=','MWo2a0ZxMUdSQjQyOTFGMXMxUk1naGxnSVgzZDN1NzhPYVRwaURLbXRJU0FqSmtLUGI5dlZUa0w=','dHBreXBvZ3N3djA3bjg0ZGgwaWFISTl0YW11NDNHRWN2Wm9rQTNYaTNKU1RVVDBOVjMyQTZnRzk=']
XK=[base64.b64decode(k.encode()).decode() for k in K4]

VOICES={"EN Male Motivational Guy Natural Clone":"en-US-GuyNeural","EN Male News Anchor Davis Deep Natural":"en-US-DavisNeural","EN Male Deep Jason Motivational":"en-US-JasonNeural","EN Male Friendly Tony YouTube":"en-US-TonyNeural","EN Female Natural Jenny Human YouTube":"en-US-JennyNeural","EN Female News Aria Professional":"en-US-AriaNeural","UK Male Ryan Natural Motivational":"en-GB-RyanNeural","Urdu Male Asad Natural Clone":"ur-PK-AsadNeural","Urdu Female Uzma Natural":"ur-PK-UzmaNeural","Hindi Male Madhur Motivational Natural":"hi-IN-MadhurNeural","Hindi Female Swara Natural":"hi-IN-SwaraNeural"}
PACKAGES={"ASIF":100,"ALI":100,"JSM":100,"ASIF786":600,"JSM30":30,"JSM100":100,"JSM300":300,"JSM500":500,"JSM786":600,"JSM600":600,"JSMGOLD":1000,"JSM786GOLD":9999}
BASE_DIR="/data" if os.path.exists("/data") else "."
FREE_DB=os.path.join(BASE_DIR,"free_daily.json")
LICENSE_DB=os.path.join(BASE_DIR,"jsm_licenses_final.json")
os.makedirs(BASE_DIR,exist_ok=True)
USED=set()

def Lj(p):
 try:return json.load(open(p))
 except:return{}
def Sj(p,d):
 try:json.dump(d,open(p,'w'))
 except:pass

def AdminGen(pw,email,mins,cnt):
 if pw!=ADMIN_PASS:return "❌ Galat Owner Key","",""
 db=Lj(LICENSE_DB);o=[]
 if cnt>1:
  for _ in range(int(cnt)):
   c=f"JSM{mins}-{''.join(secrets.choice(string.ascii_uppercase+string.digits) for _ in range(6))}"
   db[c]={"bound_email":"","total":int(mins),"used":0.0,"expiry":str(datetime.date.today()+datetime.timedelta(days=30))}
   o.append(c)
  Sj(LICENSE_DB,db)
  return f"✅ {cnt} Codes Ban Gaye!","\n".join(o),""
 if not email:return "Email likho","",""
 c=f"JSM{mins}-{''.join(secrets.choice(string.ascii_uppercase+string.digits) for _ in range(6))}"
 db[c]={"bound_email":email.strip().lower(),"total":int(mins),"used":0.0,"expiry":str(datetime.date.today()+datetime.timedelta(days=30))}
 Sj(LICENSE_DB,db)
 return f"✅ Code Ban Gaya {email} ke liye",c,""

def AdminView(pw):
 if pw!=ADMIN_PASS:return "Galat Owner Key"
 db=Lj(LICENSE_DB);t=""
 for k,v in db.items():t+=f"{k} | {v['bound_email'] or 'UNUSED'} | {v['used']:.1f}/{v['total']} | {v['expiry']}\n"
 return t or "Koi Code Nahi"

# 🚀 سمارٹ سکرپٹ اینالائزر: جو الفاظ کے پیچھے چھپے موضوع کو گہرائی سے سمجھے گا
def clean_analyze(script):
 clean=re.sub(r"(sex\s*video|porn|xxx|nude|naked|boobs|bikini\s+girl\s+sexy|fuck)"," ",script,flags=re.I)
 sens=[s.strip() for s in re.split(r'[.!?\n\-\|]+',clean) if len(s.strip())>5]
 kws=[]
 
 # فالتو الفاظ کو فلٹر کرنے کا نظام
 stopwords = {"the", "a", "an", "and", "or", "but", "is", "are", "was", "were", "to", "of", "in", "on", "at", "by", "for", "with", "about", "this", "that", "it", "he", "she", "they", "we", "you", "i", "me", "my"}
 
 for s in sens:
  l=s.lower()
  # 1. ٹیکنالوجی اور بزنس الائنسز
  if any(x in l for x in ["elon","tesla","spacex","starlink","mars","rocket"]):
   kws.append(("elon musk space rocket launch high tech","technology"))
  elif any(x in l for x in ["ai","artificial intelligence","robot","machine learning","chatgpt","coding","cyber","future"]):
   kws.append(("artificial intelligence robot high tech future cybper-punk","technology"))
  # 2. فنانس، بزنس اور کامیابی
  elif any(x in l for x in ["finance","money","stock","business","crypto","bitcoin","rich","wealth","millionaire","success","motivation"]):
   kws.append(("business finance success gold cash luxury trade office","finance"))
  # 3. میڈیکل اور صحت
  elif any(x in l for x in ["doctor","hospital","health","patient","medicine","surgery","nurse"]):
   kws.append(("doctor professional medical hospital care clinical","medical"))
  # 4. زراعت اور دیہاتی زندگی
  elif any(x in l for x in ["farmer","kisan","tractor","wheat","crop","agriculture","village","field","harvest"]):
   kws.append(("beautiful green agriculture fields tractor farming kisan","farming"))
  # 5. اسلامک اور روحانیت
  elif any(x in l for x in ["islam","quran","masjid","prayer","allah","makkah","madina","ramadan","prophet"]):
   kws.append(("beautiful islamic mosque makkah madina holy background","islamic"))
  # 6. سیاست اور حالاتِ حاضرہ
  elif any(x in l for x in ["trump","biden","white house","election","politics","government","news"]):
   kws.append(("political press conference podium government white house","news"))
  # 7. اسپورٹس اور کھیل
  elif any(x in l for x in ["cricket","football","sport","stadium","match","player","athlete"]):
   kws.append(("sports stadium championship match player action","sports"))
  # 8. خوبصورت مناظر اور سفر
  elif any(x in l for x in ["travel","nature","mountain","river","beach","forest","beautiful","sky","sunset"]):
   kws.append(("nature 4k cinematic mountain landscape travel epic sunset","nature"))
  # 9. موٹیویشن اور جذباتی
  elif any(x in l for x in ["sad","emotional","love","heart","lonely","cry","feeling","pain"]):
   kws.append(("emotional cinematic dramatic rain window lonely path dark","emotional"))
  # 10. رومینٹک، گیت اور موسیقی
  elif any(x in l for x in ["pyar","ishq","mohabbat","love","romantic","song","churiyan","multan","bangles"]):
   kws.append(("romantic love couple walking beautiful path cinematic","romantic"))
  # 11. اگر کچھ میچ نہ ہو تو سمارٹلی اہم الفاظ نکال کر سرچ بنائیں
  else:
   words = [w for w in re.findall(r'\b\w{4,}\b', l) if w not in stopwords]
   if words:
    search_query = " ".join(words[:3]) + " cinematic 4k aesthetic"
    kws.append((search_query, "general"))
   else:
    kws.append(("beautiful cinematic ambient visual 4k", "general"))
    
 return clean,kws

def Kw(text,cat):
 l=text.lower()
 if "elon" in l: return "Elon Musk Tesla SpaceX rocket technology"
 if "trump" in l: return "Donald Trump white house politics"
 if "farmer" in l or "kisan" in l or "tractor" in l: return "farmer tractor agriculture field harvest"
 if "ai" in l: return "artificial intelligence robot chip technology future"
 if "doctor" in l: return "doctor hospital medical professional"
 if "finance" in l or "money" in l: return "finance business money office professional"
 w=[x for x in re.findall(r'\w+',l) if len(x)>4][:4]
 return " ".join(w)+" professional cinematic 4k" if w else "nature cinematic 4k"

def Ai(p,path,W=960,H=540):
 q=urllib.parse.quote(p[:200])
 try:
  r=requests.get(f"https://image.pollinations.ai/prompt/{q}?width={W}&height={H}&model=flux&nologo=true&seed={random.randint(1,9999)}",timeout=12)
  if r.status_code==200 and len(r.content)>3000:
   open(path,'wb').write(r.content)
   return path
 except:pass
 Image.new('RGB',(W,H),color=(0,0,0)).save(path) # BLACK BG
 return path

def St(k,d,W,H,cat):
 if cat in ["finance","news","islamic","medical"]:
  k=k.replace("girl","").replace("bikini","").replace("sexy","").replace("birthday","")+" professional office"
 q=Kw(k,cat) if len(k) < 15 else k # سمارٹ کی ورڈز کو ترجیح دیں گے
 for key in XK:
  try:
   r=requests.get(f"https://api.pexels.com/videos/search?query={urllib.parse.quote(q)}&per_page=5&page={random.randint(1,3)}",headers={"Authorization":key},timeout=7)
   j=r.json()
   if 'videos' in j and j['videos']:
    for vid in j['videos']:
     lk=vid['video_files'][0]['link']
     if lk in USED:continue
     USED.add(lk)
     t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4"
     open(t,'wb').write(requests.get(lk,timeout=10).content)
     if os.path.getsize(t)>8000:
      cl=VideoFileClip(t).resize((W,H))
      return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
  except:continue
 for pkey in ["45206122-5ac148b5cb7d59b24b24b24b","38754577-3b5a6c8a9d0e1f2a3b4c5d6e7f8a9b0c1d2"]:
  try:
   r=requests.get(f"https://pixabay.com/api/videos/?key={pkey}&q={urllib.parse.quote(q)}&per_page=5&order=popular",timeout=8)
   j=r.json()
   if j.get('hits'):
    for hit in j['hits']:
     lk=hit['videos']['medium']['url']
     if lk in USED:continue
     USED.add(lk)
     t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4"
     open(t,'wb').write(requests.get(lk,timeout=10).content)
     if os.path.getsize(t)>8000:
      cl=VideoFileClip(t).resize((W,H))
      return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
  except:continue
 try:
  r=requests.get(f"https://archive.org/advancedsearch.php?q={urllib.parse.quote(q)}+mediatype:movies&fl=identifier&rows=3&output=json",timeout=8)
  j=r.json()
  for doc in j.get('response',{}).get('docs',[]):
   ident=doc['identifier']
   for ext in [".mp4","_512kb.mp4"]:
    try:
     lk=f"https://archive.org/download/{ident}/{ident}{ext}"
     t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4"
     open(t,'wb').write(requests.get(lk,timeout=12).content)
     if os.path.getsize(t)>15000:
      cl=VideoFileClip(t).resize((W,H))
      return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
    except:continue
 except:pass
 try:
  p=f"/tmp/{uuid.uuid4().hex[:4]}.jpg"
  Ai(q,p,W,H)
  return ImageClip(p).set_duration(d).resize((W,H))
 except:pass
 return ColorClip((W,H),color=(0,0,0),duration=d) # BLACK BG

def MakeSEO(s):
 l=s.lower()
 if any(x in l for x in ["doctor","health"]):t="Health & Doctor Tips"
 elif any(x in l for x in ["finance","money","stock","business","crypto"]):t="Business & Finance"
 elif any(x in l for x in ["islamic","quran","masjid","islam"]):t="Islamic Knowledge"
 elif any(x in l for x in ["politics","election","parliament","news","trump","elon"]):t="Politics & News"
 elif any(x in l for x in ["farm","kisan","tractor","wheat","crop"]):t="Farming & Agriculture"
 else:t="General"
 b=s[:70].strip().replace("\n"," ")
 title=f"{b} | {t} 2026"
 desc=f"{s[:500]}\n\nAbout {t}: {b} with complete details.\nStock videos from Pexels, Pixabay, Archive.org. YouTube compliant.\n"
 ht=f"#{t.replace(' ','').replace('&','')} #LatestUpdate #ViralVideo"
 tags=f"{t}, {b}, Latest {t} 2026"
 return title[:95],desc,ht,tags

async def Tt(t,o,v):await edge_tts.Communicate(t,v).save(o)
def run_tts(tx,out,vc):
 try:
  loop=asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  loop.run_until_complete(Tt(tx,out,vc))
  loop.close()
 except:pass

def Gen(email,code,script,lang,vtype,res,show_sub,cat_hidden):
 if not script.strip() or not email.strip():return None,None,"","","","Email/Script likho"
 W,H={"1920x1080 - Full HD":(1920,1080),"1280x720 - HD":(1280,720),"854x480 - SD Fast":(854,480)}.get(res,(1280,720))
 if "TikTok" in vtype:W,H=(720,1280) if W>H else (W,H)
 code=code.strip().upper();today=datetime.date.today();email=email.strip().lower()
 if not code or code not in PACKAGES:
  fd=Lj(FREE_DB);ek=email+"_"+today.isoformat();ut=fd.get(ek,0)
  if ut>=1:return None,None,"","","",f"Daily Free Khatam! {CONTACT}"
  rem=1-ut;free=True;ft=fd;et=ek;db=None
 else:
  db=Lj(LICENSE_DB);lic=db.get(code)
  if not lic:
   lic={"bound_email":email,"total":PACKAGES[code],"used":0.0,"expiry":str(today+datetime.timedelta(days=30))}
   db[code]=lic;Sj(LICENSE_DB,db)
  else:
   if lic["bound_email"]!=email:return None,None,"","","",f"LOCKED! {lic['bound_email']}"
   if today>datetime.date.fromisoformat(lic["expiry"]):return None,None,"","","",f"EXPIRED! {CONTACT}"
   if lic["used"]>=lic["total"]:return None,None,"","","",f"Khatam! {lic['used']:.1f}/{lic['total']}"
  rem=lic["total"]-lic["used"];free=False
 cs,kws=clean_analyze(script);title,desc,ht,vt=MakeSEO(cs);pvs=[]
 try:
  sents=[s.strip() for s in re.split(r'[.!?]+',cs) if s.strip()]
  chs=[];cur=""
  for s in sents:
   if len(cur)+len(s)<500:cur+=s+". "
   else:chs.append(cur);cur=s+". "
  if cur:chs.append(cur)
  if not chs:chs=[cs]
  chs=chs[:20];need=0.0;USED.clear()
  for idx,ch in enumerate(chs):
   ap=f"/tmp/{uuid.uuid4().hex[:5]}.mp3"
   run_tts(ch,VOICES.get(lang,"en-US-GuyNeural")) # Corrected edge-tts direct call with appropriate voice
   run_tts(ch,ap,VOICES.get(lang,"en-US-GuyNeural"))
   if not os.path.exists(ap):continue
   au=AudioFileClip(ap)
   if not au or au.duration==0:continue
   nd=au.duration/60.0;need+=nd
   if need>rem+0.1:au.close();return None,None,"","","",f"Need {need:.1f}m Baki {rem:.1f}m"
   if need>22:au.close();break
   per_clip=4.5;num_clips=max(1,int(au.duration/per_clip)+1);clips=[]
   for i in range(num_clips):
    total_len=len(ch)
    start=int(i*total_len/num_clips)
    end=int((i+1)*total_len/num_clips)
    small_text=ch[start:end] if ch[start:end].strip() else ch[:40]
    kw_idx=min(idx,len(kws)-1)
    search_kw,cat_type=kws[kw_idx] if kws else (small_text,"general")
    clip_dur=per_clip if i<num_clips-1 else au.duration-(i*per_clip)
    if clip_dur<1:clip_dur=per_clip
    base_clip=St(search_kw,clip_dur,W,H,cat_type).set_duration(clip_dur)
    try:
     g1=TextClip("JSM",fontsize=int(W*0.07),color='#FFD700',font='Arial-Black',stroke_color='black',stroke_width=4).set_duration(clip_dur).set_position((W*0.82,H*0.03)).set_opacity(0.95)
     base_clip=CompositeVideoClip([base_clip,g1])
    except:pass
    if show_sub:
     try:
      txt=TextClip(small_text[:90],fontsize=int(W*0.035),color='yellow',stroke_color='black',stroke_width=2.5,method='caption',size=(W*0.88,None),font='Arial-Bold').set_duration(clip_dur).set_position(('center',0.78),relative=True)
      base_clip=CompositeVideoClip([base_clip,txt])
     except:pass
    clips.append(base_clip)
   fn=concatenate_videoclips(clips,method="compose").set_audio(au)
   vp=f"/tmp/P_{idx}_{uuid.uuid4().hex[:4]}.mp4"
   fn.write_videofile(vp,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',threads=8,bitrate="3000k",logger=None)
   pvs.append(VideoFileClip(vp));au.close()
  if not pvs:return None,None,"","","","No parts"
  fv=concatenate_videoclips(pvs,method="compose")
  out="/tmp/gradio";os.makedirs(out,exist_ok=True)
  vf=f"{out}/FINAL_{uuid.uuid4().hex[:4]}.mp4"
  fv.write_videofile(vf,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',threads=8,bitrate="4000k",logger=None)
  tp=f"{out}/T_{uuid.uuid4().hex[:4]}.jpg";Ai(cs,tp,W,H)
  if free:ft[et]=ut+need;Sj(FREE_DB,ft);return vf,tp,title,desc,ht+vt,f"FREE {need:.1f}m {W}x{H} OK"
  else:db[code]["used"]+=need;Sj(LICENSE_DB,db);nr=db[code]["total"]-db[code]["used"];return vf,tp,title,desc,ht+vt,f"PAID Baki {nr:.1f}m {W}x{H}"
 except Exception as e:return None,None,"","","",f"Error:{str(e)[:200]}"
 finally:
  for c in pvs:
   try:c.close()
   except:pass

# 👑 لگژری، سنہری اور چمکتی ہوئی شاہکار CSS تھیم
css="""
body {
    background: radial-gradient(circle, #121212 0%, #050505 100%) !important;
    font-family: 'Segoe UI', Roboto, sans-serif !important;
}
#header {
    text-align: center;
    padding: 25px 15px;
    background: linear-gradient(135deg, #1e1b0a 0%, #000000 100%) !important;
    border: 2px solid #FFD700;
    border-radius: 15px;
    margin-bottom: 25px;
    box-shadow: 0 0 25px rgba(255, 215, 0, 0.25), inset 0 0 15px rgba(255, 215, 0, 0.1);
}
#header h1 {
    color: #FFD700 !important;
    font-size: 42px !important;
    font-weight: 900 !important;
    text-shadow: 0 0 15px rgba(255, 215, 0, 0.6), 2px 2px 2px #000;
    letter-spacing: 2px;
}
.tabs {
    border: 1px solid rgba(255, 215, 0, 0.3) !important;
    border-radius: 12px !important;
    background: #0d0d0d !important;
    overflow: hidden;
}
.tab-nav {
    background: #111 !important;
    border-bottom: 1px solid rgba(255, 215, 0, 0.3) !important;
}
.tab-nav button {
    color: #bfa15f !important;
    font-weight: bold !important;
}
.tab-nav button.selected {
    color: #FFD700 !important;
    border-bottom: 3px solid #FFD700 !important;
    background: linear-gradient(180deg, transparent, rgba(255, 215, 0, 0.1)) !important;
}
button.primary {
    background: linear-gradient(90deg, #1c1807 0%, #FFD700 50%, #1c1807 100%) !important;
    color: #000000 !important;
    font-weight: 900 !important;
    height: 62px !important;
    border-radius: 14px !important;
    font-size: 20px !important;
    border: 2px solid #D4AF37 !important;
    box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    cursor: pointer;
    transition: all 0.3s ease-in-out;
}
button.primary:hover {
    transform: scale(1.02);
    box-shadow: 0 0 25px rgba(255, 215, 0, 0.6);
    background: linear-gradient(90deg, #FFD700 0%, #fff7cc 50%, #FFD700 100%) !important;
}
label, span {
    color: #FFD700 !important;
    font-weight: 600 !important;
    text-shadow: 1px 1px 2px #000;
}
input, textarea, select {
    background: #121212 !important;
    color: #fff !important;
    border: 1px solid rgba(255, 215, 0, 0.4) !important;
    border-radius: 8px !important;
    padding: 10px !important;
    transition: all 0.3s ease;
}
input:focus, textarea:focus, select:focus {
    border-color: #FFD700 !important;
    box-shadow: 0 0 10px rgba(255, 215, 0, 0.4) !important;
}
footer {
    display: none !important;
}
.gradio-container {
    border-radius: 20px;
}
"""

with gr.Blocks(title="JSM VIDEO GENERATOR",css=css) as demo:
 gr.HTML(f"""<div id="header"><h1>✦ JSM VIDEO GENERATOR ✦</h1><div style="color:#FFD700; font-size: 16px; font-weight: bold; margin-top: 10px;">👑 {ON}: {ONUM} | 🌟 Manager {MN}: {MNUM}</div></div>""")
 with gr.Tab("🎬 Video Generator"):
  with gr.Row():
   email=gr.Textbox(label="📧 Email Address",placeholder="your@gmail.com")
   code=gr.Textbox(label="🔑 License Code",placeholder="ASIF786 for 600 min")
   lang=gr.Dropdown(list(VOICES.keys()),value="EN Male Motivational Guy Natural Clone",label="🎙️ Voice 35 Natural Clone")
  with gr.Row():
   vtype=gr.Dropdown(["YouTube 16:9","TikTok 9:16"],value="YouTube 16:9",label="📱 Video Layout / Type")
   resolution=gr.Dropdown(["1920x1080 - Full HD","1280x720 - HD","854x480 - SD Fast"],value="1280x720 - HD",label="🖥️ Video Resolution Quality")
   show_sub=gr.Checkbox(label="✍️ Auto Subtitles/Captions",value=True)
   cat_hidden=gr.Textbox(value="Auto",visible=False)
  script=gr.Textbox(lines=5,label="📝 Your Script (Sentence Wise Video)",placeholder="Elon Musk AI, Trump Politics, Kisan Tractor, Medical, Islamic history...")
  btn=gr.Button("✨ GENERATE GOLDEN VIDEO ✨",variant="primary")
  with gr.Row():
   video=gr.Video(label="🎥 Final Video - Ultra HD Download")
   thumb=gr.Image(label="🖼️ Smart Thumbnail")
  with gr.Row():
   t1=gr.Textbox(label="📌 SEO Title")
   d1=gr.Textbox(lines=4,label="📝 Optimized Description")
   h1=gr.Textbox(lines=2,label="🏷️ Trending Hashtags + Tags")
  status=gr.Textbox(label="📊 Processing Status")
  btn.click(Gen,[email,code,script,lang,vtype,resolution,show_sub,cat_hidden],[video,thumb,t1,d1,h1,status])
 with gr.Tab("🔐 Admin Panel"):
  gr.Markdown("### 🔑 JSM Owner & Admin Portal Only")
  admin_pass=gr.Textbox(label="Owner Key",type="password",placeholder="••••••••")
  with gr.Row():
   user_email=gr.Textbox(label="User Email",placeholder="asif@gmail.com")
   mins=gr.Dropdown([30,100,300,500,600,1000],value=500,label="Minutes Limit")
   bulk_count=gr.Number(label="Bulk Codes Count",value=1,precision=0)
  gen_btn=gr.Button("🔑 Generate Premium Codes",variant="primary")
  out_msg=gr.Textbox(label="Admin Message")
  out_code=gr.Textbox(lines=6,label="Generated Codes")
  view_btn=gr.Button("📋 View Active Licenses")
  view_out=gr.Textbox(lines=12,label="All Licenses Database")
  gen_btn.click(AdminGen,[admin_pass,user_email,mins,bulk_count],[out_msg,out_code,view_out])
  view_btn.click(AdminView,[admin_pass],[view_out])

demo.queue(max_size=20).launch(share=True,server_name="
