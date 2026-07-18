import gradio as gr,asyncio,edge_tts,uuid,random,requests,re,os,json,base64,urllib.parse,datetime,time,threading,torch
from moviepy.editor import VideoFileClip,ColorClip,concatenate_videoclips,AudioFileClip,CompositeVideoClip,ImageClip,TextClip
from PIL import Image
import secrets,string

CONTACT="03043399133|03022246271"
ADMIN_PASS="JamSaeed@786#Motha_Owner_0304!"
ON="JAM SAEED";ONUM="03043399133";MN="MUJAHID HUSSAIN";MNUM="03022246271"

# ===== FINAL 7 SOURCE KEYS =====
PEXELS_KEYS=[
    'tpkypogswv07n84dh0iaHI9tamu43GEcvZokA3Xi3JSTUT0NV32A6gG9',
    'ROKJvfYuuSkc7QVVL6VjCgYFyB8UQZCLLCctD2SfTJcIrDGo5Ex3JMX6'
]
PIXABAY_KEYS=['YAHAN_PIXABAY_KEY_LAGAO'] # jab mile to yahan lagana
# Mixkit, Coverr, Videvo, Archive.org, Videezy = No Key Required
# =================================

VOICES={"EN Male Motivational Guy Natural Clone":"en-US-GuyNeural","EN Male News Anchor Davis Deep Natural":"en-US-DavisNeural","Urdu Male Asad Natural Clone":"ur-PK-AsadNeural","Urdu Female Uzma Natural":"ur-PK-UzmaNeural","Hindi Male Madhur Motivational Natural":"hi-IN-MadhurNeural"}
PACKAGES={"ASIF":100,"ALI":100,"JSM":100,"ASIF786":600,"JSM30":30,"JSM100":100,"JSM300":300,"JSM500":500,"JSM786":600,"JSM600":600,"JSMGOLD":1000,"JSM786GOLD":9999}
BASE_DIR="/data" if os.path.exists("/data") else "."
FREE_DB=os.path.join(BASE_DIR,"free_daily.json")
LICENSE_DB=os.path.join(BASE_DIR,"jsm_licenses_final.json")
os.makedirs(BASE_DIR,exist_ok=True)
USED=set()

def keep_alive():
    while True:
        time.sleep(30)
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] JSM is Alive...")
threading.Thread(target=keep_alive, daemon=True).start()

def Lj(p): try:return json.load(open(p)) except:return{}
def Sj(p,d): try:json.dump(d,open(p,'w')) except:pass
def clean_analyze(script): clean=re.sub(r"(sex\s*video|porn|xxx|nude|naked|boobs|fuck)"," ",script,flags=re.I); return clean,[s.strip() for s in re.split(r'[.!?]+',clean) if len(s.strip())>3]
def Kw(text,cat):
 l=text.lower()
 if any(x in l for x in ["trump","iran","war","missile"]): return "political news war military"
 if any(x in l for x in ["imran khan","pakistan","protest"]): return "pakistan politics protest rally"
 w=[x for x in re.findall(r'\w+',l) if len(x)>4][:3]
 return " ".join(w)+" cinematic 4k" if w else "nature cinematic 4k"

def Ai(p,path,W=960,H=540):
 q=urllib.parse.quote(p[:200])
 try:
  r=requests.get(f"https://image.pollinations.ai/prompt/{q}?width={W}&height={H}&model=flux&nologo=true&seed={random.randint(1,9999)}",timeout=12)
  if r.status_code==200 and len(r.content)>3000:
   open(path,'wb').write(r.content);return path
 except:pass
 Image.new('RGB',(W,H),color=(10,10,10)).save(path);return path

# ===== 7 SOURCE VIDEO FINDER =====
def St(k,d,W,H):
 q=Kw(k,"")
 # 1. PEXELS
 for key in PEXELS_KEYS:
  try:
   r=requests.get(f"https://api.pexels.com/videos/search?query={urllib.parse.quote(q)}&per_page=3",headers={"Authorization":key},timeout=6)
   if r.status_code==200:
    for vid in r.json().get('videos',[]):
     lk=vid['video_files'][0]['link'];
     if lk not in USED:USED.add(lk);t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4";open(t,'wb').write(requests.get(lk,timeout=10).content)
     if os.path.getsize(t)>8000:cl=VideoFileClip(t).resize((W,H));return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
  except:pass
 # 2. PIXABAY
 for key in PIXABAY_KEYS:
  if key=="YAHAN_PIXABAY_KEY_LAGAO":continue
  try:
   r=requests.get(f"https://pixabay.com/api/videos/?key={key}&q={urllib.parse.quote(q)}&per_page=3",timeout=6)
   if r.status_code==200:
    for hit in r.json().get('hits',[]):
     lk=hit['videos']['medium']['url'];
     if lk not in USED:USED.add(lk);t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4";open(t,'wb').write(requests.get(lk,timeout=10).content)
     if os.path.getsize(t)>8000:cl=VideoFileClip(t).resize((W,H));return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
  except:pass
 # 3. COVERR
 try:
  r=requests.get(f"https://api.coverr.co/videos/search?q={urllib.parse.quote(q)}&per_page=3",timeout=6)
  if r.status_code==200:
   for v in r.json():
    lk=v['sources'][0]['url'];
    if lk not in USED:USED.add(lk);t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4";open(t,'wb').write(requests.get(lk,timeout=10).content)
    if os.path.getsize(t)>8000:cl=VideoFileClip(t).resize((W,H));return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
 except:pass
 # 4. VIDEVO
 try:
  r=requests.get(f"https://www.videvo.net/api/search/?query={urllib.parse.quote(q)}&per_page=3",timeout=6)
  if r.status_code==200:
   for v in r.json().get('results',[]):
    lk=v['video_files'][0]['link'];
    if lk and lk not in USED:USED.add(lk);t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4";open(t,'wb').write(requests.get(lk,timeout=10).content)
    if os.path.getsize(t)>8000:cl=VideoFileClip(t).resize((W,H));return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
 except:pass
 # 5. MIXKIT
 try:
  r=requests.get(f"https://mixkit.co/api/v1/videos/search/?q={urllib.parse.quote(q)}&limit=3",timeout=6)
  if r.status_code==200:
   for v in r.json().get('videos',[]):
    lk=v['video_files'][0]['link'];
    if lk and lk not in USED:USED.add(lk);t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4";open(t,'wb').write(requests.get(lk,timeout=10).content)
    if os.path.getsize(t)>8000:cl=VideoFileClip(t).resize((W,H));return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
 except:pass
 # 6. VIDEZY
 try:
  r=requests.get(f"https://www.videezy.com/api/v1/videos?query={urllib.parse.quote(q)}&per_page=3",timeout=6)
  if r.status_code==200:
   for v in r.json().get('videos',[]):
    lk=v['download_url'];
    if lk and lk not in USED:USED.add(lk);t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4";open(t,'wb').write(requests.get(lk,timeout=10).content)
    if os.path.getsize(t)>8000:cl=VideoFileClip(t).resize((W,H));return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
 except:pass
 # 7. ARCHIVE.ORG
 try:
  r=requests.get(f"https://archive.org/advancedsearch.php?q={urllib.parse.quote(q)}&fl[]=identifier&output=json&rows=3",timeout=6)
  if r.status_code==200:
   for doc in r.json().get('response',{}).get('docs',[]):
    id=doc['identifier'];lk=f"https://archive.org/download/{id}/{id}.mp4"
    if lk not in USED:USED.add(lk);t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4";open(t,'wb').write(requests.get(lk,timeout=10).content)
    if os.path.getsize(t)>8000:cl=VideoFileClip(t).resize((W,H));return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
 except:pass
 # 8. AI IMAGE FINAL
 p=f"/tmp/{uuid.uuid4().hex[:4]}.jpg";Ai(q,p,W,H)
 return ImageClip(p).set_duration(d).resize((W,H))

async def Tt(t,o,v):await edge_tts.Communicate(t,v).save(o)
def run_tts(tx,out,vc):
 try:
  if os.path.exists(out):os.remove(out)
  loop=asyncio.new_event_loop();asyncio.set_event_loop(loop);loop.run_until_complete(Tt(tx,out,vc));loop.close()
  time.sleep(1)
  if os.path.exists(out) and os.path.getsize(out)>2000:return True
 except:pass
 return False

def Gen(email,code,script,lang,vtype,res,show_sub,cat_hidden):
 if not script.strip() or not email.strip():return None,None,"","","","Email/Script likho"
 W,H={"1920x1080 - Full HD":(1920,1080),"1280x720 - HD":(1280,720)}.get(res,(1280,720))
 if "TikTok" in vtype:W,H=(720,1280)
 cs,kws=clean_analyze(script)
 if not kws: return None,None,"","","","Script me jumle nahi mile"
 preset_val = 'ultrafast' if torch.cuda.is_available() else 'medium'
 pvs=[];need=0.0;USED.clear()
 for idx,ch in enumerate(kws):
   print(f"Part {idx+1}/{len(kws)}")
   ap=f"/tmp/{uuid.uuid4().hex[:5]}.mp3"
   if not run_tts(ch,ap,VOICES.get(lang,"en-US-GuyNeural")):continue
   try:au=AudioFileClip(ap)
   except:continue
   if au.duration==0:au.close();continue
   need+=au.duration/60.0
   per_clip=5.0;num_clips=max(1,int(au.duration/per_clip)+1);clips=[]
   for i in range(num_clips):
    if i>0 and i%3==0: time.sleep(1)
    start=int(i*len(ch)/num_clips);end=int((i+1)*len(ch)/num_clips)
    small_text=ch[start:end] if ch[start:end].strip() else ch[:40]
    clip_dur=per_clip if i<num_clips-1 else au.duration-(i*per_clip)
    try:
        base_clip=St(small_text,clip_dur,W,H).set_duration(clip_dur)
        layers=[base_clip]
        if show_sub:
         txt=TextClip(small_text[:120],fontsize=int(W*0.04),color='yellow',stroke_color='black',stroke_width=3.5,method='caption',size=(W*0.88,None)).set_duration(clip_dur).set_position(('center',0.78),relative=True)
         layers.append(txt)
        clips.append(CompositeVideoClip(layers))
    except:continue
   try:
    if clips:
     fn=concatenate_videoclips(clips,method="compose").set_audio(au)
     vp=f"/tmp/P_{idx}.mp4"
     fn.write_videofile(vp,fps=24,codec='libx264',audio_codec='aac',preset=preset_val,threads=4,logger=None)
     pvs.append(VideoFileClip(vp))
   except:pass
   au.close()
 if not pvs:return None,None,"","","","Koi bhi clip nahi bani"
 fv=concatenate_videoclips(pvs,method="compose");out="/tmp/gradio";os.makedirs(out,exist_ok=True)
 vf=f"{out}/FINAL.mp4";fv.write_videofile(vf,fps=24,codec='libx264',audio_codec='aac',preset=preset_val,threads=4)
 tp=f"{out}/T.jpg";Ai(cs,tp,W,H)
 return vf,tp,"SEO Title","Description","#Tags",f"Done {need:.1f}m"

css="body{background:#000!important}#header{text-align:center;padding:30px 0;background:linear-gradient(135deg,#000 0%,#1a1000 50%,#000 100%)!important;border-bottom:4px solid #FFD700!important}#header h1{color:#FFD700!important;font-size:48px!important;font-weight:900!important;text-shadow:0 0 20px #FFD700!important}.owner-info{color:#FFD700!important;font-size:18px!important}button.primary{background:linear-gradient(90deg,#FFD700,#FFA500,#FFD700)!important;color:#000!important;font-weight:900!important;height:65px!important;border-radius:16px!important;font-size:20px!important;border:3px solid #FFD700!important}label{color:#FFD700!important;font-weight:800!important}footer{display:none!important}"
with gr.Blocks(title="JSM VIDEO GENERATOR V6.13") as demo:
 gr.HTML(f"""<div id="header"><h1>✦ JSM VIDEO GENERATOR V6.13 - 7 SOURCE ✦</h1><div class="owner-info">OWNER: {ON} - {ONUM} | MANAGER: {MN} - {MNUM}</div></div>""")
 with gr.Tab("🎬 Video Generator"):
  with gr.Row():
   email=gr.Textbox(label="Email")
   code=gr.Textbox(label="License Code")
   lang=gr.Dropdown(list(VOICES.keys()),value="EN Male Motivational Guy Natural Clone",label="Voice")
  with gr.Row():
   vtype=gr.Dropdown(["YouTube 16:9","TikTok 9:16"],value="YouTube 16:9",label="Type")
   resolution=gr.Dropdown(["1920x1080 - Full HD","1280x720 - HD"],value="1280x720 - HD",label="HD")
   show_sub=gr.Checkbox(label="Subtitles ON/OFF",value=True)
   cat_hidden=gr.Textbox(value="Auto",visible=False)
  script=gr.Textbox(lines=8,label="Your Script")
  btn=gr.Button("✨ GENERATE GOLDEN VIDEO ✨",variant="primary")
  with gr.Row():
   video=gr.Video(label="Final Video")
   thumb=gr.Image(label="AI Thumbnail")
  with gr.Row():
   t1=gr.Textbox(label="SEO Title")
   d1=gr.Textbox(lines=4,label="Description")
   h1=gr.Textbox(lines=2,label="Hashtags + Tags")
  status=gr.Textbox(label="Status")
  btn.click(Gen,[email,code,script,lang,vtype,resolution,show_sub,cat_hidden],[video,thumb,t1,d1,h1,status])
demo.queue(max_size=10).launch(share=True,css=css)
