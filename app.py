import gradio as gr,asyncio,edge_tts,uuid,random,requests,re,os,json,urllib.parse,datetime,time
from moviepy.editor import VideoFileClip,concatenate_videoclips,AudioFileClip,CompositeVideoClip,ImageClip,TextClip
from PIL import Image
import secrets,string

CONTACT="03043399133|03022246271"
ADMIN_PASS="JamSaeed@786#Motha_Owner_0304!"
NAME="سعید احمد مجاہد حسین"

VOICES={"EN Male Motivational Guy":"en-US-GuyNeural","EN Male News Anchor Davis":"en-US-DavisNeural","EN Male Jason":"en-US-JasonNeural","EN Female Jenny":"en-US-JennyNeural","EN Female Aria":"en-US-AriaNeural","UK Male Ryan":"en-GB-RyanNeural","Urdu Male Asad":"ur-PK-AsadNeural","Urdu Female Uzma":"ur-PK-UzmaNeural","Hindi Male Madhur":"hi-IN-MadhurNeural","Hindi Female Swara":"hi-IN-SwaraNeural","Arabic Male Hamed":"ar-SA-HamedNeural","Arabic Female Zariyah":"ar-SA-ZariyahNeural","Turkish Male Emre":"tr-TR-EmreNeural","Persian Male Farid":"fa-IR-FaridNeural","Spanish Male Alvaro":"es-ES-AlvaroNeural","French Male Henri":"fr-FR-HenriNeural","German Male Conrad":"de-DE-ConradNeural","Bengali Male Banik":"bn-IN-BanikNeural","Tamil Male Valluvar":"ta-IN-ValluvarNeural","Telugu Male Mohan":"te-IN-MohanNeural","Punjabi Male Manveer":"pa-IN-ManveerNeural","Gujarati Male Niranjan":"gu-IN-NiranjanNeural"}

PACKAGES={"ASIF":100,"ALI":100,"JSM":100,"ASIF786":600,"JSM30":30,"JSM100":100,"JSM300":300,"JSM500":500,"JSM786":600,"JSM600":600,"JSMGOLD":1000,"JSM786GOLD":9999}
BASE_DIR="/data" if os.path.exists("/data") else "."
FREE_DB=os.path.join(BASE_DIR,"free_daily.json")
LICENSE_DB=os.path.join(BASE_DIR,"jsm_licenses_final.json")
os.makedirs(BASE_DIR,exist_ok=True)
USED=set()

def Lj(p):
 try:f=open(p);data=json.load(f);f.close();return data
 except:return{}
def Sj(p,d):
 try:f=open(p,'w');json.dump(d,f);f.close()
 except:pass

def AdminGen(pw,email,mins,cnt):
 if pw!=ADMIN_PASS:return "Galat Owner Key","",""
 db=Lj(LICENSE_DB);o=[]
 if cnt>1:
  for _ in range(int(cnt)):
   c=f"JSM{mins}-{''.join(secrets.choice(string.ascii_uppercase+string.digits) for _ in range(6))}"
   db[c]={"bound_email":"","total":int(mins),"used":0.0,"expiry":str(datetime.date.today()+datetime.timedelta(days=30))}
   o.append(c)
  Sj(LICENSE_DB,db)
  return f"{cnt} Codes Ban Gaye","\n".join(o),""
 if not email:return "Email likho","",""
 c=f"JSM{mins}-{''.join(secrets.choice(string.ascii_uppercase+string.digits) for _ in range(6))}"
 db[c]={"bound_email":email.strip().lower(),"total":int(mins),"used":0.0,"expiry":str(datetime.date.today()+datetime.timedelta(days=30))}
 Sj(LICENSE_DB,db)
 return f"Code Ban Gaya {email} ke liye",c,""

def AdminView(pw):
 if pw!=ADMIN_PASS:return "Galat Owner Key"
 db=Lj(LICENSE_DB);t=""
 for k,v in db.items():t+=f"{k} | {v['bound_email'] or 'UNUSED'} | {v['used']:.1f}/{v['total']} min | Expiry: {v['expiry']}\n"
 return t or "Koi Code Nahi"

def clean_analyze(script):
 clean=re.sub(r"(sex\s*video|porn|xxx|nude|naked|boobs|fuck)"," ",script,flags=re.I)
 sens=[s.strip() for s in re.split(r'[.!?]+',clean) if len(s.strip())>8]
 return clean,sens

def Kw(text):
 l=text.lower()
 if any(x in l for x in ["ai","artificial intelligence","chatgpt","robot"]): return "artificial intelligence technology"
 if any(x in l for x in ["bitcoin","crypto","blockchain"]): return "bitcoin crypto trading"
 if any(x in l for x in ["doctor","hospital","patient"]): return "doctor hospital medical"
 w=[x for x in re.findall(r'\w+',l) if len(x)>4][:3]
 return " ".join(w)+" cinematic 4k" if w else "nature cinematic 4k"

def get_category(text):
 l=text.lower()
 if any(x in l for x in ["ai","chatgpt","robot","tech"]): return "technology"
 if any(x in l for x in ["bitcoin","crypto","stock","money","business"]): return "finance"
 return "general"

def Ai(p,path,W,H):
 q=urllib.parse.quote(p[:200])
 try:
  r=requests.get(f"https://image.pollinations.ai/prompt/{q}?width={W}&height={H}&model=flux&nologo=true",timeout=10)
  if r.status_code==200 and len(r.content)>3000:
   f=open(path,'wb');f.write(r.content);f.close();return path
 except:pass
 Image.new('RGB',(W,H),color=(0,0,0)).save(path)
 return path

def St(k,d,W,H):
 q=Kw(k)
 # 1. PIXABAY
 for pkey in ["45206122-5ac148b5cb7d59b24b24b24b"]:
  try:
   r=requests.get(f"https://pixabay.com/api/videos/?key={pkey}&q={urllib.parse.quote(q)}&per_page=3",timeout=8)
   j=r.json()
   if j.get('hits'):
    for hit in j['hits']:
     lk=hit['videos']['medium']['url']
     if lk in USED:continue
     USED.add(lk)
     t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4"
     f=open(t,'wb');f.write(requests.get(lk,timeout=10).content);f.close()
     if os.path.getsize(t)>8000:
      cl=VideoFileClip(t).resize((W,H))
      return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
  except:continue
 # 2. AI IMAGE GUARANTEE
 p=f"/tmp/{uuid.uuid4().hex[:4]}.jpg"
 Ai(q,p,W,H)
 return ImageClip(p).set_duration(d).resize((W,H))

def MakeSEO(s):
 l=s.lower()
 if any(x in l for x in ["doctor","health"]):t="Health Tips"
 elif any(x in l for x in ["finance","money","stock","business","crypto"]):t="Business & Finance"
 else:t="General Update"
 b=s[:70].strip().replace("\n"," ")
 title=f"{b} | {t}"
 desc=f"{s[:500]}\n\nAbout {t}: {b}"
 ht=f"#{t.replace(' ','')} #ViralVideo"
 tags=f"{t}, {b}, Latest {t}"
 return title[:95],desc,ht,tags

async def Tt(t,o,v):await edge_tts.Communicate(t,v).save(o)

def run_tts(tx,out,vc):
 try:
  if os.path.exists(out):os.remove(out)
  loop=asyncio.new_event_loop();asyncio.set_event_loop(loop);loop.run_until_complete(Tt(tx,out,vc));loop.close()
  time.sleep(1)
  return os.path.exists(out) and os.path.getsize(out)>2000
 except:return False

def Gen(email,code,script,lang,vtype,res,show_sub):
 if not script.strip() or not email.strip():return None,None,"","","","Email/Script likho"
 W,H=(1280,720) # 720P DEFAULT - STABLE
 if "Full HD" in res:W,H=(1920,1080)
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
  chs=kws[:15];need=0.0;USED.clear() # 15 clip max for stability
  for idx,ch in enumerate(chs):
   ap=f"/tmp/{uuid.uuid4().hex[:5]}.mp3"
   if not run_tts(ch,ap,VOICES.get(lang,"en-US-GuyNeural")):continue
   try:au=AudioFileClip(ap)
   except:continue
   if not au or au.duration==0:au.close();continue
   nd=au.duration/60.0;need+=nd
   if need>rem+0.1:au.close();return None,None,"","","",f"Need {need:.1f}m Baki {rem:.1f}m"

   per_clip=5.0;num_clips=max(1,int(au.duration/per_clip)+1);clips=[]
   for i in range(num_clips):
    start=int(i*len(ch)/num_clips);end=int((i+1)*len(ch)/num_clips)
    small_text=ch[start:end] if ch[start:end].strip() else ch[:40]
    clip_dur=per_clip if i<num_clips-1 else au.duration-(i*per_clip)
    if clip_dur<1:clip_dur=per_clip
    base_clip=St(small_text,clip_dur,W,H).set_duration(clip_dur)
    layers=[base_clip]
    if show_sub:
     try:
      txt=TextClip(small_text[:90],fontsize=int(W*0.035),color='white',stroke_color='black',stroke_width=2.5,method='caption',size=(W*0.9,None)).set_duration(clip_dur).set_position(('center',0.85),relative=True)
      layers.append(txt)
     except:pass
    clips.append(CompositeVideoClip(layers))

   fn=concatenate_videoclips(clips,method="compose").set_audio(au)
   vp=f"/tmp/P_{idx}.mp4"
   fn.write_videofile(vp,fps=24,codec='libx264',audio_codec='aac',preset='medium',threads=2,logger=None)
   pvs.append(VideoFileClip(vp));au.close()

  if not pvs:return None,None,"","","","No parts - Script check karo"
  fv=concatenate_videoclips(pvs,method="compose");out="/tmp/gradio";os.makedirs(out,exist_ok=True)
  vf=f"{out}/FINAL.mp4";fv.write_videofile(vf,fps=24,codec='libx264',audio_codec='aac',preset='medium',threads=2)
  tp=f"{out}/T.jpg";Ai(cs,tp,W,H)

  if free:ft[et]=ut+need;Sj(FREE_DB,ft);status=f"FREE Done {need:.1f}m"
  else:db[code]["used"]+=need;Sj(LICENSE_DB,db);nr=db[code]["total"]-db[code]["used"];status=f"PAID Baki {nr:.1f}m"
  return vf,tp,title,desc,ht+vt,status

 except Exception as e:return None,None,"","","",f"Error:{str(e)[:200]}"

css="body{background:#0a0a0a}#header{text-align:center;padding:25px;border-bottom:3px solid #FFD700}h1{color:#FFD700;font-size:36px;font-weight:900}.owner{color:#FFD700;font-size:18px} button.primary{background:#FFD700;color:#000;font-weight:900;height:60px;border-radius:12px;font-size:18px} label{color:#FFD700;font-weight:700} footer{display:none}"
with gr.Blocks(title="Video Generator") as demo:
 gr.HTML(f"""<div id="header"><h1>سید احمد مجاہد حسین</h1><div class="owner">AI Video Studio</div></div>""")
 with gr.Tab("Video Generator"):
  with gr.Row():
   email=gr.Textbox(label="Email")
   code=gr.Textbox(label="License Code")
   lang=gr.Dropdown(list(VOICES.keys()),value="EN Male Motivational Guy",label="Voice")
  with gr.Row():
   vtype=gr.Dropdown(["YouTube 16:9","TikTok 9:16"],value="YouTube 16:9",label="Type")
   resolution=gr.Dropdown(["1280x720 - HD","1920x1080 - Full HD"],value="1280x720 - HD",label="Resolution")
   show_sub=gr.Checkbox(label="Subtitles",value=True)
  script=gr.Textbox(lines=6,label="Your Script")
  btn=gr.Button("GENERATE VIDEO",variant="primary")
  with gr.Row(): video=gr.Video(label="Final Video"); thumb=gr.Image(label="Thumbnail")
  with gr.Row(): t1=gr.Textbox(label="SEO Title"); d1=gr.Textbox(lines=3,label="Description"); h1=gr.Textbox(label="Hashtags")
  status=gr.Textbox(label="Status")
  btn.click(Gen,[email,code,script,lang,vtype,resolution,show_sub],[video,thumb,t1,d1,h1,status])
 with gr.Tab("Admin Panel"):
  admin_pass=gr.Textbox(label="Owner Key",type="password")
  with gr.Row(): user_email=gr.Textbox(label="User Email"); mins=gr.Dropdown([30,100,300,600],value=600); bulk_count=gr.Number(value=1,precision=0)
  gen_btn=gr.Button("Generate Code"); out_msg=gr.Textbox(); out_code=gr.Textbox(lines=4)
  view_btn=gr.Button("View All Codes"); view_out=gr.Textbox(lines=10)
  gen_btn.click(AdminGen,[admin_pass,user_email,mins,bulk_count],[out_msg,out_code,view_out])
  view_btn.click(AdminView,[admin_pass],[view_out])
demo.queue().launch(share=True,css=css)
