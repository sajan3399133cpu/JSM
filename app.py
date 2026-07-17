import gradio as gr,uuid,random,requests,re,os,json,base64,urllib.parse,datetime,time
from moviepy.editor import VideoFileClip,ColorClip,concatenate_videoclips,AudioFileClip,CompositeVideoClip,ImageClip,TextClip
from gtts import gTTS
from PIL import Image
import secrets,string
CONTACT="03043399133|03022246271"
ADMIN_PASS="JamSaeed@786#Motha_Owner_0304!"
ON="JAM SAEED MOTHA";ONUM="03043399133";MN="MUJAHID HUSSAIN";MNUM="03022246271"
K4=['Uk9LSnZmWXV1U2tjN1FWVkw2VmpDZ1lGeUI4VVFaQ0xMQ2N0RDJTZlRKY2xJckRHbzVFeDNKTVg2','em5pWXZhdmhhbDY2Vkd3dVYya1VJcFJtN3ZHM1kwcmRkREx1enJJVHZtUHFRMjZrZEcwdmN5eTA=','ZjZJS3hySFI4TUhqMWdlRDYyY3JMVGZEVFFYMHM3ZXdGa3czaEVJNGQ0Q2VuUlRaWENrcENXRDk=','MWo2a0ZxMUdSQjQyOTFGMXMxUk1naGxnSVgzZDN1NzhPYVRwaURLbXRJU0FqSmtLUGI5dlZUa0w=','dHBreXBvZ3N3djA3bjg0ZGgwaWFISTl0YW11NDNHRWN2Wm9rQTNYaTNKU1RVVDBOVjMyQTZnRzk=']
XK=[base64.b64decode(k.encode()).decode() for k in K4]
VOICES={"EN Male":"en","EN Female":"en","Urdu Male":"ur","Urdu Female":"ur","Hindi Male":"hi","Hindi Female":"hi"}
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

def clean_analyze(script):
 clean=re.sub(r"(sex|porn|xxx|nude|naked|boobs|bikini|fuck)"," ",script,flags=re.I)
 sens=[s.strip() for s in re.split(r'[.!?]+',clean) if len(s.strip())>3]
 kws=[]
 for s in sens:
  l=s.lower()
  if any(x in l for x in ["elon","tesla","spacex"]): kws.append(("elon musk tesla spacex rocket technology","technology"))
  elif any(x in l for x in ["trump","biden","white house","election"]): kws.append(("donald trump white house podium politics speech","news"))
  elif any(x in l for x in ["farmer","kisan","tractor","wheat","crop","agriculture"]): kws.append(("farmer tractor agriculture field harvest wheat","farming"))
  elif any(x in l for x in ["ai","artificial intelligence","robot","chatgpt"]): kws.append(("artificial intelligence robot chip technology future","technology"))
  else: kws.append((s[:60]+" professional cinematic 4k","general"))
 return clean,kws

def Kw(text,cat):
 l=text.lower()
 if "elon" in l: return "Elon Musk Tesla SpaceX rocket technology"
 if "trump" in l: return "Donald Trump white house podium politics"
 if "farmer" in l or "kisan" in l or "tractor" in l: return "farmer tractor agriculture field harvest"
 w=[x for x in re.findall(r'\w+',l) if len(x)>4][:4]
 return " ".join(w)+" professional cinematic 4k" if w else "nature cinematic 4k"

def Ai(p,path,W=960,H=540):
 q=urllib.parse.quote(p[:200])
 try:
  r=requests.get(f"https://image.pollinations.ai/prompt/{q}?width={W}&height={H}&model=flux&nologo=true&seed={random.randint(1,9999)}",timeout=15)
  if r.status_code==200 and len(r.content)>3000:
   open(path,'wb').write(r.content)
   return path
 except:pass
 Image.new('RGB',(W,H),color=(0,0,0)).save(path)
 return path

def St(k,d,W,H,cat):
 q=Kw(k,cat)
 # 1. PEXELS
 for key in XK:
  try:
   r=requests.get(f"https://api.pexels.com/videos/search?query={urllib.parse.quote(q)}&per_page=3&page={random.randint(1,2)}",headers={"Authorization":key},timeout=6)
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
 # 2. PIXABAY
 for pkey in ["45206122-5ac148b5cb7d59b24b24b24b","38754577-3b5a6c8a9d0e1f2a3b4c5d6e7f8a9b0c1d2"]:
  try:
   r=requests.get(f"https://pixabay.com/api/videos/?key={pkey}&q={urllib.parse.quote(q)}&per_page=3",timeout=6)
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
 # 3. MIXKIT
 try:
  r=requests.get(f"https://api.mixkit.co/videos/search/?q={urllib.parse.quote(q)}&limit=3",timeout=6)
  j=r.json()
  if j.get('videos'):
   for hit in j['videos']:
    lk=hit['video_files'][0]['link']
    if lk in USED:continue
    USED.add(lk)
    t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4"
    open(t,'wb').write(requests.get(lk,timeout=10).content)
    if os.path.getsize(t)>8000:
     cl=VideoFileClip(t).resize((W,H))
     return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
 except:pass
 # 4. ARCHIVE.ORG
 try:
  r=requests.get(f"https://archive.org/advancedsearch.php?q={urllib.parse.quote(q)}+mediatype:movies&fl=identifier&rows=2&output=json",timeout=8)
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
 return ColorClip((W,H),color=(0,0,0),duration=d)

def MakeSEO(s):
 l=s.lower()
 if any(x in l for x in ["doctor","health"]):t="Health & Doctor Tips"
 elif any(x in l for x in ["finance","money","stock","business","crypto"]):t="Business & Finance"
 elif any(x in l for x in ["politics","election","parliament","news","trump","elon"]):t="Politics & News"
 elif any(x in l for x in ["farm","kisan","tractor","wheat","crop"]):t="Farming & Agriculture"
 else:t="General"
 b=s[:70].strip().replace("\n"," ")
 title=f"{b} | {t} 2026"
 desc=f"{s[:500]}\n\nAbout {t}: {b} with complete details.\nStock videos from Pexels, Pixabay, Mixkit, Archive.org.\n"
 ht=f"#{t.replace(' ','').replace('&','')} #LatestUpdate #ViralVideo"
 tags=f"{t}, {b}, Latest {t} 2026"
 return title[:95],desc,ht,tags

def run_tts(tx,out,lang_code):
 try:
  gTTS(text=tx, lang=lang_code).save(out)
  time.sleep(0.3)
  return os.path.exists(out) and os.path.getsize(out)>1000
 except:return False

def Gen(email,code,script,lang,vtype,res,show_sub,cat_hidden):
 if not script.strip() or not email.strip():return None,None,"","","","Email/Script likho"
 W,H={"1920x1080 - Full HD":(1920,1080),"1280x720 - HD":(1280,720),"854x480 - SD Fast":(854,480)}.get(res,(1280,720))
 if "TikTok" in vtype:W,H=(720,1280)
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
  chs=[s+". " for s in cs.split('.') if s.strip()][:25]
  if not chs:chs=[cs]
  need=0.0;USED.clear()
  for idx,ch in enumerate(chs):
   ap=f"/tmp/{uuid.uuid4().hex[:5]}.mp3"
   lang_code=VOICES.get(lang,"en")
   ok=run_tts(ch,ap,lang_code)
   if not ok:continue
   au=AudioFileClip(ap)
   if not au or au.duration<0.5:au.close();continue
   nd=au.duration/60.0;need+=nd
   if need>rem+0.1:au.close();return None,None,"","","",f"Minutes Khatam! Need {need:.1f}m Baki {rem:.1f}m"
   clip=St(ch,au.duration,W,H,"general").set_duration(au.duration).set_audio(au)
   try:
    g1=TextClip("JSM",fontsize=int(W*0.06),color='#FFD700',font='Arial-Black',stroke_color='black',stroke_width=4).set_duration(au.duration).set_position((W*0.82,H*0.03)).set_opacity(0.95)
    if show_sub:
     txt=TextClip(ch[:80],fontsize=int(W*0.035),color='yellow',stroke_color='black',stroke_width=2.5,method='caption',size=(W*0.9,None),font='Arial-Bold').set_duration(au.duration).set_position(('center',0.85),relative=True)
     clip=CompositeVideoClip([clip,g1,txt])
    else: clip=CompositeVideoClip([clip,g1])
   except:pass
   vp=f"/tmp/P_{idx}_{uuid.uuid4().hex[:4]}.mp4"
   clip.write_videofile(vp,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',threads=4,logger=None)
   pvs.append(VideoFileClip(vp));au.close();clip.close()
  if not pvs:return None,None,"","","","Video nahi bani. Script choti karo."
  fv=concatenate_videoclips(pvs,method="compose")
  out="/tmp/gradio";os.makedirs(out,exist_ok=True)
  vf=f"{out}/FINAL_{uuid.uuid4().hex[:4]}.mp4"
  fv.write_videofile(vf,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',threads=4,logger=None)
  tp=f"{out}/T_{uuid.uuid4().hex[:4]}.jpg";Ai(cs,tp,W,H)
  if free:ft[et]=ut+need;Sj(FREE_DB,ft);return vf,tp,title,desc,ht+vt,f"SUCCESS! FREE {need:.1f}m"
  else:db[code]["used"]+=need;Sj(LICENSE_DB,db);nr=db[code]["total"]-db[code]["used"];return vf,tp,title,desc,ht+vt,f"SUCCESS! PAID Baki {nr:.1f}m"
 except Exception as e:return None,None,"","","",f"Error:{str(e)[:150]}"
 finally:
  for c in pvs:
   try:c.close()
   except:pass

css="body{background:#000!important}#header{text-align:center;padding:10px;background:#000!important;border-bottom:2px solid #FFD700}#header h1{color:#FFD700!important;font-size:38px!important;font-weight:900!important}footer{display:none!important}button.primary{background:linear-gradient(90deg,#000,#FFD700,#000)!important;color:#FFD700!important;font-weight:900!important;height:60px!important;border-radius:14px!important;font-size:18px!important;border:2px solid #FFD700!important}label{color:#FFD700!important}input,textarea,select{background:#111!important;color:#FFD700!important;border:1px solid #FFD700!important}"
with gr.Blocks(title="JSM VIDEO GENERATOR",css=css) as demo:
 gr.HTML(f"""<div id="header"><h1>✦ JSM VIDEO GENERATOR V4.0 ✦</h1><div style="color:#FFD700">📞 {ON}: {ONUM} | Manager {MN}: {MNUM}</div></div>""")
 with gr.Tab("🎬 Video Generator"):
  with gr.Row():
   email=gr.Textbox(label="Email",placeholder="your@gmail.com")
   code=gr.Textbox(label="License Code",placeholder="ASIF786 for 600 min")
   lang=gr.Dropdown(list(VOICES.keys()),value="EN Male",label="Voice")
  with gr.Row():
   vtype=gr.Dropdown(["YouTube 16:9","TikTok 9:16"],value="YouTube 16:9",label="Type")
   resolution=gr.Dropdown(["1280x720 - HD","1920x1080 - Full HD","854x480 - SD Fast"],value="1280x720 - HD",label="Quality")
   show_sub=gr.Checkbox(label="Subtitles",value=True)
   cat_hidden=gr.Textbox(value="Auto",visible=False)
  script=gr.Textbox(lines=6,label="Your Script",placeholder="1 line = 1 clip. Short sentences likho.")
  btn=gr.Button("✨ GENERATE VIDEO ✨",variant="primary")
  with gr.Row():
   video=gr.Video(label="Final Video - HD Download")
   thumb=gr.Image(label="Thumbnail")
  with gr.Row():
   t1=gr.Textbox(label="Title")
   d1=gr.Textbox(lines=4,label="Description")
   h1=gr.Textbox(lines=2,label="Hashtags + Tags")
  status=gr.Textbox(label="Status")
  btn.click(Gen,[email,code,script,lang,vtype,resolution,show_sub,cat_hidden],[video,thumb,t1,d1,h1,status])
 with gr.Tab("🔐 Admin"):
  gr.Markdown("### 🔑 Owner Access Only")
  admin_pass=gr.Textbox(label="Owner Key",type="password")
  with gr.Row():
   user_email=gr.Textbox(label="User Email")
   mins=gr.Dropdown([30,100,300,500,600,1000],value=500,label="Minutes")
   bulk_count=gr.Number(label="Bulk Count",value=1,precision=0)
  gen_btn=gr.Button("🔑 Generate Code",variant="primary")
  out_msg=gr.Textbox(label="Message")
  out_code=gr.Textbox(lines=6,label="Codes")
  view_btn=gr.Button("📋 Saare Codes Dekho")
  view_out=gr.Textbox(lines=12,label="All Licenses")
  gen_btn.click(AdminGen,[admin_pass,user_email,mins,bulk_count],[out_msg,out_code,view_out])
  view_btn.click(AdminView,[admin_pass],[view_out])
demo.queue(max_size=20).launch(share=True,server_name="0.0.0.0")
