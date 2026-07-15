import gradio as gr,asyncio,edge_tts,uuid,random,requests,re,os,json,base64,urllib.parse,datetime
from moviepy.editor import VideoFileClip,ColorClip,concatenate_videoclips,AudioFileClip,CompositeVideoClip
from PIL import Image

B="JSM VIDEO GENERATOR";CONTACT="03043399133"
K1="c2JfcHVibGlzaGFibGVfMVc0Tks2WDdFZGFjbV9lU0JJY0ZEUV9Da1Q2YzRFWQ=="
K2="NTYzODYyOTMtMTRmYWNkOTRmZGFjMjZmOWZjMzdmNWYyYw=="
K4=['Uk9LSnZmWXV1U2tjN1FWVkw2VmpDZ1lGeUI4VVFaQ0xMQ2N0RDJTZlRKY2xJckRHbzVFeDNKTVg2','em5pWXZhdmhhbDY2Vkd3dVYya1VJcFJtN3ZHM1kwcmRkREx1enJJVHZtUHFRMjZrZEcwdmN5eTA=','ZjZJS3hySFI4TUhqMWdlRDYyY3JMVGZEVFFYMHM3ZXdGa3czaEVJNGQ0Q2VuUlRaWENrcENXRDk=','MWo2a0ZxMUdSQjQyOTFGMXMxUk1naGxnSVgzZDN1NzhPYVRwaURLbXRJU0FqSmtLUGI5dlZUa0w=','dHBreXBvZ3N3djA3bjg0ZGgwaWFISTl0YW11NDNHRWN2Wm9rQTNYaTNKU1RVVDBOVjMyQTZnRzk=']
def D(e):
 try:return base64.b64decode(e.encode()).decode()
 except:return ""
PK=D(K2);XK=[D(k) for k in K4]
VOICES={"English Male":"en-US-GuyNeural","English Female":"en-US-JennyNeural","Urdu Male":"ur-PK-AsadNeural","Urdu Female":"ur-PK-UzmaNeural","Hindi Male":"hi-IN-MadhurNeural","Hindi Female":"hi-IN-SwaraNeural","Arabic Male":"ar-SA-HamedNeural","Arabic Female":"ar-SA-ZariyahNeural","Spanish Male":"es-ES-AlvaroNeural","Spanish Female":"es-ES-ElviraNeural","French Male":"fr-FR-HenriNeural","French Female":"fr-FR-DeniseNeural","German Male":"de-DE-ConradNeural","German Female":"de-DE-KatjaNeural","Turkish Male":"tr-TR-AhmetNeural","Turkish Female":"tr-TR-EmelNeural"}
PACKAGES={"ASIF":100,"ALI":100,"JSM":100,"ASIF786":600,"JSM30":30,"JSM100":100,"JSM300":300,"JSM500":500,"JSM786":600,"JSM600":600,"JSMGOLD":1000,"JSM786GOLD":9999}
FREE_DB="/tmp/free_daily.json";LICENSE_DB="/tmp/jsm_licenses_final.json"
USED_LINKS=set()
def Lj(p):
 try:
  if os.path.exists(p):return json.load(open(p))
 except:pass
 return{}
def Sj(p,d):
 try:json.dump(d,open(p,'w'))
 except:pass
def safe(t):return re.sub(r'[^\w\s\-.,:;()#@ ]','',t)[:80]

def Kw(text,cat):
 l=text.lower()
 SENSORS={"trump":"Donald Trump speaking podium","biden":"Joe Biden speech","imran khan":"Imran Khan Pakistan jalsa","nawaz":"Nawaz Sharif speech","modi":"Narendra Modi speech","parliament":"parliament meeting","election":"election voting crowd","kisan":"farmer tractor field","farmer":"farmer tractor agriculture","tractor":"tractor ploughing field","khet":"wheat field farm","farming":"farming tractor harvest","wheat":"wheat field harvesting","crop":"crop field farmer","business":"business office corporate","stock market":"stock market trading chart","finance":"finance dollar counting","crypto":"bitcoin crypto trading","bitcoin":"bitcoin trading","dollar":"dollar money counting","gold":"gold market","islamic":"islamic mosque","quran":"quran mosque","namaz":"muslim prayer mosque","masjid":"mosque beautiful","news":"news anchor studio","breaking":"breaking news studio","cricket":"cricket stadium match","sports":"sports stadium crowd","football":"football match goal","doctor":"doctor hospital patient","hospital":"hospital doctor patient","health":"doctor health care","kitchen":"cooking kitchen chef","biryani":"biryani cooking kitchen","cooking":"chef cooking food","technology":"technology AI robot","ai":"artificial intelligence robot","computer":"computer coding","mobile":"mobile phone technology","car":"car driving road","bike":"bike driving road","mountain":"mountain nature beautiful","beach":"beach sea beautiful","travel":"travel airplane"}
 for k in sorted(SENSORS.keys(),key=len,reverse=True):
  if k in l:return SENSORS[k]+f" {random.randint(1,50)}"
 words=[w for w in re.findall(r'\w+',l) if len(w)>4][:4]
 if words:return " ".join(words)+" professional cinematic"
 return "nature cinematic"

def Ai(p,path,W=960,H=540):
 q=urllib.parse.quote(p[:300])
 try:
  r=requests.get(f"https://image.pollinations.ai/prompt/{q}?width={W}&height={H}&model=flux&nologo=true&seed={random.randint(1,9999)}",timeout=15)
  if r.status_code==200 and len(r.content)>3000:open(path,'wb').write(r.content);return path
 except:pass
 Image.new('RGB',(W,H),color=(20,20,20)).save(path);return path

def St(k,d,W,H,cat):
 q=Kw(k,cat)
 for key in XK:
  try:
   r=requests.get(f"https://api.pexels.com/videos/search?query={urllib.parse.quote(q)}&per_page=3&page={random.randint(1,3)}",headers={"Authorization":key},timeout=7)
   j=r.json()
   if 'videos' in j and j['videos']:
    for vid in j['videos']:
     link=vid['video_files'][0]['link']
     if link in USED_LINKS:continue
     USED_LINKS.add(link)
     t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4";open(t,'wb').write(requests.get(link,timeout=8).content)
     clip=VideoFileClip(t).resize((W,H))
     return clip.loop(duration=d) if clip.duration<d else clip.subclip(0,d)
  except:continue
 return ColorClip((W,H),color=(20,30,50),duration=d)

async def Tt(t,o,v):await edge_tts.Communicate(t,v).save(o)
def run_tts(text,out,voice):
 try:
  loop=asyncio.new_event_loop();asyncio.set_event_loop(loop);loop.run_until_complete(Tt(text,out,voice));loop.close()
 except:pass

def Gen(email,code,script,lang,vtype,show_sub,cat_hidden):
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
   lic={"bound_email":email,"total":PACKAGES[code],"used":0.0,"expiry":str(today+datetime.timedelta(days=30))}
   lic_db[code]=lic;Sj(LICENSE_DB,lic_db)
  else:
   if lic["bound_email"]!=email:return None,None,"","","",f"LOCKED! {lic['bound_email']}"
   if today>datetime.date.fromisoformat(lic["expiry"]):return None,None,"","","",f"EXPIRED {CONTACT}"
   if lic["used"]>=lic["total"]:return None,None,"","","",f"Khatam {lic['used']:.1f}/{lic['total']}"
  rem=lic["total"]-lic["used"];free=False
 title=safe(script);desc=safe(script[:400]);ht="#JSM"
 pvs=[]
 try:
  sents=[s.strip() for s in re.split(r'[.!?]+',script) if s.strip()];chs=[];cur=""
  for s in sents:
   if len(cur)+len(s)<550:cur+=s+". "
   else:chs.append(cur);cur=s+". "
  if cur:chs.append(cur)
  if not chs:chs=[script]
  chs=chs[:25];needT=0.0;USED_LINKS.clear()
  for idx,ch in enumerate(chs):
   ap=f"/tmp/{uuid.uuid4().hex[:5]}.mp3"
   run_tts(ch,ap,VOICES.get(lang,"en-US-GuyNeural"))
   if not os.path.exists(ap):continue
   au=AudioFileClip(ap)
   if not au or au.duration==0:continue
   nd=au.duration/60.0;needT+=nd
   if needT>rem+0.1:au.close();return None,None,"","","",f"Need {needT:.1f}m Baki {rem:.1f}m"
   if needT>22:au.close();break
   per_clip=4.5
   num_clips=max(1,int(au.duration/per_clip)+1)
   clips=[]
   for i in range(num_clips):
    s_idx=int(i*len(ch)/num_clips);e_idx=int((i+1)*len(ch)/num_clips)
    small_text=ch[s_idx:e_idx] if ch[s_idx:e_idx].strip() else ch[:40]
    clip_dur=per_clip if i<num_clips-1 else au.duration-(i*per_clip)
    if clip_dur<1:clip_dur=per_clip
    base_clip=St(small_text,clip_dur,W,H,cat_hidden).set_duration(clip_dur)
    if show_sub:
     try:
      from moviepy.editor import TextClip
      txt=TextClip(small_text[:90],fontsize=24,color='white',bg_color='black',method='caption',size=(W*0.85,None)).set_duration(clip_dur).set_position(('center',0.8),relative=True)
      base_clip=CompositeVideoClip([base_clip,txt])
     except:pass
    clips.append(base_clip)
   fn=concatenate_videoclips(clips,method="compose").set_audio(au)
   vp=f"/tmp/P_{idx}_{uuid.uuid4().hex[:4]}.mp4"
   fn.write_videofile(vp,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',logger=None)
   pvs.append(VideoFileClip(vp));au.close()
  if not pvs:return None,None,"","","","No parts"
  fv=concatenate_videoclips(pvs,method="compose")
  out_dir="/tmp/gradio";os.makedirs(out_dir,exist_ok=True)
  vf=f"{out_dir}/FINAL_{uuid.uuid4().hex[:4]}.mp4"
  fv.write_videofile(vf,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',logger=None)
  tp=f"{out_dir}/T_{uuid.uuid4().hex[:4]}.jpg";Ai(script,tp,W,H)
  if free:
   ft[et]=ut+needT;Sj(FREE_DB,ft)
   return vf,tp,title,desc,ht,f"FREE {needT:.1f}m"
  else:
   lic_db[code]["used"]+=needT;Sj(LICENSE_DB,lic_db)
   nr=lic_db[code]["total"]-lic_db[code]["used"]
   return vf,tp,title,desc,ht,f"PAID Baki {nr:.1f}m"
 except Exception as e:return None,None,"","","",f"Error:{str(e)[:120]}"
 finally:
  for c in pvs:
   try:c.close()
   except:pass

css="""
#header{text-align:center;padding:16px 0}
#header h1{color:#FFD700!important;font-size:38px!important;font-weight:900!important;text-shadow:0 0 20px gold!important;margin:0!important}
footer{display:none!important}
button.primary{background:linear-gradient(90deg,#D4AF37,#FFD700)!important;color:#000!important;font-weight:900!important;height:56px!important;border-radius:14px!important}
.gr-input,.gr-dropdown,textarea{background:#1e1e1e!important;border:1px solid #333!important;color:#fff!important}
label{color:#FFD700!important}
"""

with gr.Blocks(title="JSM VIDEO GENERATOR",css=css) as demo:
 gr.HTML("""<div id="header"><h1>✦ JSM VIDEO GENERATOR ✦</h1></div>""")
 with gr.Row():
  email=gr.Textbox(label="Email",placeholder="your@gmail.com")
  code=gr.Textbox(label="License Code",placeholder="ASIF786")
  lang=gr.Dropdown(list(VOICES.keys()),value="English Male",label="Language")
 with gr.Row():
  vtype=gr.Dropdown(["YouTube 16:9","TikTok 9:16"],value="YouTube 16:9",label="Video Type")
  show_sub=gr.Checkbox(label="✅ Subtitles",value=False)
  cat_hidden=gr.Textbox(value="Auto",visible=False)
 script=gr.Textbox(lines=6,label="Your Script",placeholder="Type your story...")
 btn=gr.Button("✨ GENERATE VIDEO ✨",variant="primary")
 with gr.Row():
  video=gr.Video(label="Final Video");thumb=gr.Image(label="Thumbnail")
 with gr.Row():
  t1=gr.Textbox(label="Title");d1=gr.Textbox(label="Description");h1=gr.Textbox(label="Hashtags")
 status=gr.Textbox(label="Status")
 btn.click(Gen,[email,code,script,lang,vtype,show_sub,cat_hidden],[video,thumb,t1,d1,h1,status])

demo.queue(max_size=20).launch(share=True,server_name="0.0.0.0")
