import gradio as gr,asyncio,edge_tts,uuid,random,requests,re,os,json,base64,urllib.parse,datetime,time
from moviepy.editor import VideoFileClip,ColorClip,concatenate_videoclips,AudioFileClip,CompositeVideoClip,ImageClip,TextClip
from PIL import Image
import secrets,string
CONTACT="03043399133|03022246271"
ADMIN_PASS="JamSaeed@786#Motha_Owner_0304!"
ON="JAM SAEED MOTHA";ONUM="03043399133";MN="MUJAHID HUSSAIN";MNUM="03022246271"
K4=['Uk9LSnZmWXV1U2tjN1FWVkw2VmpDZ1lGeUI4VVFaQ0xMQ2N0RDJTZlRKY2xJckRHbzVFeDNKTVg2','em5pWXZhdmhhbDY2Vkd3dVYya1VJcFJtN3ZHM1kwcmRkREx1enJJVHZtUHFRMjZrZEcwdmN5eTA=','ZjZJS3hySFI4TUhqMWdlRDYyY3JMVGZEVFFYMHM3ZXdGa3czaEVJNGQ0Q2VuUlRaWENrcENXRDk=','MWo2a0ZxMUdSQjQyOTFGMXMxUk1naGxnSVgzZDN1NzhPYVRwaURLbXRJU0FqSmtLUGI5dlZUa0w=','dHBreXBvZ3N3djA3bjg0ZGgwaWFISTl0YW11NDNHRWN2Wm9rQTNYaTNKU1RVVDBOVjMyQTZnRzk=']
XK=[base64.b64decode(k.encode()).decode() for k in K4]
VOICES={"EN Male Motivational Guy Natural Clone":"en-US-GuyNeural","Urdu Male Asad Natural Clone":"ur-PK-AsadNeural","Urdu Female Uzma Natural":"ur-PK-UzmaNeural","Hindi Male Madhur Motivational Natural":"hi-IN-MadhurNeural","Hindi Female Swara Natural":"hi-IN-SwaraNeural"}
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

def clean_analyze(script):
 clean=re.sub(r"(sex\s*video|porn|xxx|nude|naked|boobs|bikini\s+girl\s+sexy|fuck|birthday girl|birthday party)"," ",script,flags=re.I)
 sens=[s.strip() for s in re.split(r'[.!?]+',clean) if len(s.strip())>8]
 return clean,sens

def Kw(text,cat):
 l=text.lower()
 if any(x in l for x in ["ai","chatgpt","robot"]): return "artificial intelligence robot technology"
 if any(x in l for x in ["bitcoin","crypto"]): return "bitcoin crypto cryptocurrency trading"
 if any(x in l for x in ["doctor","hospital"]): return "doctor hospital medical patient"
 if any(x in l for x in ["farmer","tractor"]): return "farmer tractor agriculture field"
 w=[x for x in re.findall(r'\w+',l) if len(x)>4][:3]
 return " ".join(w)+" professional cinematic 4k" if w else "nature cinematic 4k"

def get_category(text):
 l=text.lower()
 if any(x in l for x in ["ai","tech"]): return "technology"
 if any(x in l for x in ["bitcoin","crypto","money"]): return "finance"
 if any(x in l for x in ["doctor","health"]): return "medical"
 if any(x in l for x in ["farmer"]): return "farming"
 return "general"

def Ai(p,path,W=960,H=540):
 q=urllib.parse.quote(p[:200])
 try:
  r=requests.get(f"https://image.pollinations.ai/prompt/{q}?width={W}&height={H}&model=flux&nologo=true&seed={random.randint(1,9999)}",timeout=12)
  if r.status_code==200 and len(r.content)>3000:
   open(path,'wb').write(r.content)
   return path
 except:pass
 Image.new('RGB',(W,H),color=(0,0,0)).save(path)
 return path

def St(k,d,W,H,cat):
 q=Kw(k,cat)
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
  p=f"/tmp/{uuid.uuid4().hex[:4]}.jpg"
  Ai(q,p,W,H)
  return ImageClip(p).set_duration(d).resize((W,H))
 except:pass
 return ColorClip((W,H),color=(0,0,0),duration=d)

# SEO FIX - AB KHUD BANAYE GA
def MakeSEO(s):
 l=s.lower()
 if any(x in l for x in ["doctor","health"]):t="Health Tips"
 elif any(x in l for x in ["finance","money","crypto","business"]):t="Business & Finance"
 elif any(x in l for x in ["ai","artificial"]):t="AI & Technology"
 elif any(x in l for x in ["farm","kisan"]):t="Farming & Agriculture"
 else:t="Viral News"
 b=s[:60].strip().replace("\n"," ")
 title=f"{b} | {t} 2026"
 desc=f"{s[:400]}\n\n🔥 About {t}: {b}\n✅ AI Generated Video\n📈 Stock: Pexels, Pixabay\n#AI #Viral"
 ht=f"#{t.replace(' ','')} #AI #ViralVideo #Trending2026"
 tags=f"{t}, {b}, AI Video 2026"
 return title[:100],desc,ht,tags

async def Tt(t,o,v):await edge_tts.Communicate(t,v).save(o)
def run_tts(tx,out,vc):
 try:
  if os.path.exists(out):os.remove(out)
  loop=asyncio.new_event_loop();asyncio.set_event_loop(loop);loop.run_until_complete(Tt(tx,out,vc));loop.close()
  for _ in range(12):
   if os.path.exists(out) and os.path.getsize(out)>2000:break
   time.sleep(0.4)
 except:pass

def Gen(email,code,script,lang,vtype,res,show_sub,cat_hidden):
 if not script.strip() or not email.strip():return None,None,"","","","Email/Script likho"
 W,H={"1920x1080 - Full HD":(1920,1080),"1280x720 - HD":(1280,720),"854x480 - SD Fast":(854,480)}.get(res,(1280,720))
 if "TikTok" in vtype:W,H=(720,1280)
 cs,kws=clean_analyze(script);title,desc,ht,vt=MakeSEO(cs);pvs=[];need=0.0;USED.clear()
 try:
  chs=kws[:20]
  for idx,ch in enumerate(chs):
   ap=f"/tmp/{uuid.uuid4().hex[:5]}.mp3"
   run_tts(ch,ap,VOICES.get(lang,"en-US-GuyNeural"))
   if not os.path.exists(ap) or os.path.getsize(ap)<2000:continue
   try:au=AudioFileClip(ap)
   except:continue
   if not au or au.duration==0:au.close();continue
   need+=au.duration/60.0
   per_clip=4.5;num_clips=max(1,int(au.duration/per_clip)+1);clips=[]
   for i in range(num_clips):
    if i>0 and i%5==0: time.sleep(2)
    total_len=len(ch);start=int(i*total_len/num_clips);end=int((i+1)*total_len/num_clips)
    small_text=ch[start:end] if ch[start:end].strip() else ch[:40]
    cat_type=get_category(small_text)
    clip_dur=per_clip if i<num_clips-1 else au.duration-(i*per_clip)
    if clip_dur<1:clip_dur=per_clip
    base_clip=St(small_text,clip_dur,W,H,cat_type).set_duration(clip_dur)
    layers=[base_clip]
    if show_sub:
     try:
      txt=TextClip(small_text[:90],fontsize=int(W*0.04),color='yellow',stroke_color='black',stroke_width=3.5,method='caption',size=(W*0.88,None)).set_duration(clip_dur).set_position(('center',0.78),relative=True)
      layers.append(txt)
     except:pass
    base_clip=CompositeVideoClip(layers)
    clips.append(base_clip)
   fn=concatenate_videoclips(clips,method="compose").set_audio(au)
   vp=f"/tmp/P_{idx}_{uuid.uuid4().hex[:4]}.mp4"
   fn.write_videofile(vp,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',threads=4,bitrate="2500k",logger=None)
   pvs.append(VideoFileClip(vp));au.close()
  if not pvs:return None,None,"","","","No parts - Script check karo"
  fv=concatenate_videoclips(pvs,method="compose");out="/tmp/gradio";os.makedirs(out,exist_ok=True)
  vf=f"{out}/FINAL_{uuid.uuid4().hex[:4]}.mp4";fv.write_videofile(vf,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',threads=4,bitrate="3500k",logger=None)
  tp=f"{out}/T_{uuid.uuid4().hex[:4]}.jpg";Ai(cs,tp,W,H)
  return vf,tp,title,desc,ht+vt,f"✅ Video Ready {need:.1f}m"
 except Exception as e:return None,None,"","","",f"Error:{str(e)[:200]}"

css="body{background:#000!important}#header{text-align:center;padding:20px 0;background:linear-gradient(135deg,#000 0%,#1a1000 50%,#000 100%)!important;border-bottom:4px solid #FFD700!important}#header h1{color:#FFD700!important;font-size:44px!important;font-weight:900!important;text-shadow:0 0 15px #FFD700!important}button.primary{background:linear-gradient(90deg,#FFD700,#FFA500,#FFD700)!important;color:#000!important;font-weight:900!important;height:65px!important;border-radius:16px!important;font-size:20px!important;border:3px solid #FFD700!important}label{color:#FFD700!important;font-weight:800!important}footer{display:none!important}"
with gr.Blocks(title="JSM VIDEO GENERATOR V6.4") as demo:
 gr.HTML(f"""<div id="header"><h1>✦ JSM VIDEO GENERATOR V6.4 FINAL ✦</h1><div>📞 {ON}: {ONUM}</div></div>""")
 with gr.Tab("🎬 Video Generator"):
  email=gr.Textbox(label="Email")
  lang=gr.Dropdown(list(VOICES.keys()),value="EN Male Motivational Guy Natural Clone",label="Voice")
  vtype=gr.Dropdown(["YouTube 16:9","TikTok 9:16"],value="YouTube 16:9",label="Type")
  resolution=gr.Dropdown(["1920x1080 - Full HD","1280x720 - HD","854x480 - SD Fast"],value="1280x720 - HD",label="Quality")
  show_sub=gr.Checkbox(label="Subtitles ON",value=True)
  script=gr.Textbox(lines=6,label="Script Likho - Har Line Alag Topic")
  btn=gr.Button("✨ GENERATE VIDEO ✨",variant="primary")
  video=gr.Video(label="Final Video")
  thumb=gr.Image(label="AI Thumbnail")
  t1=gr.Textbox(label="SEO Title")
  d1=gr.Textbox(lines=4,label="Description")
  h1=gr.Textbox(lines=2,label="Hashtags")
  status=gr.Textbox(label="Status")
  btn.click(Gen,[email,gr.Textbox(visible=False),script,lang,vtype,resolution,show_sub,gr.Textbox(visible=False)],[video,thumb,t1,d1,h1,status])
demo.queue().launch(share=True,css=css) # NO PORT = NO ERROR
