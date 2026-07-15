import gradio as gr,asyncio,edge_tts,uuid,random,requests,re,os,json,base64,urllib.parse,datetime
from moviepy.editor import VideoFileClip,ColorClip,concatenate_videoclips,AudioFileClip,CompositeVideoClip,ImageClip
from PIL import Image

CONTACT="03043399133"
K4=['Uk9LSnZmWXV1U2tjN1FWVkw2VmpDZ1lGeUI4VVFaQ0xMQ2N0RDJTZlRKY2xJckRHbzVFeDNKTVg2','em5pWXZhdmhhbDY2Vkd3dVYya1VJcFJtN3ZHM1kwcmRkREx1enJJVHZtUHFRMjZrZEcwdmN5eTA=','ZjZJS3hySFI4TUhqMWdlRDYyY3JMVGZEVFFYMHM3ZXdGa3czaEVJNGQ0Q2VuUlRaWENrcENXRDk=','MWo2a0ZxMUdSQjQyOTFGMXMxUk1naGxnSVgzZDN1NzhPYVRwaURLbXRJU0FqSmtLUGI5dlZUa0w=','dHBreXBvZ3N3djA3bjg0ZGgwaWFISTl0YW11NDNHRWN2Wm9rQTNYaTNKU1RVVDBOVjMyQTZnRzk=']
def D(e):
 try:return base64.b64decode(e.encode()).decode()
 except:return ""
XK=[D(k) for k in K4]
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

# === SMART SENSOR V4.1 + 6 PLATFORM ===
def Kw(text,cat):
 l=text.lower()
 SENSORS={"trump":"Donald Trump speaking podium white house","biden":"Joe Biden speech white house","imran khan":"Imran Khan Pakistan jalsa crowd","nawaz":"Nawaz Sharif Pakistan speech","modi":"Narendra Modi India parliament speech","parliament":"parliament government meeting debate","election":"voting election crowd polling station","kisan":"Indian farmer working tractor field agriculture","farmer":"farmer tractor working agriculture field","tractor":"tractor ploughing field farming agriculture","khet":"green wheat field agriculture farm India","farming":"farming agriculture tractor harvest field","wheat":"wheat field harvesting tractor farmer","crop":"crop field farmer working tractor","business":"business meeting office corporate finance","stock market":"stock market trading chart wall street finance","finance":"finance money dollar counting business","crypto":"bitcoin crypto trading chart finance","bitcoin":"bitcoin cryptocurrency trading finance","dollar":"dollar money finance counting cash","gold":"gold jewelry market finance","islamic":"islamic mosque beautiful interior","quran":"quran reading mosque islamic","namaz":"muslim prayer mosque namaz","masjid":"mosque interior beautiful islamic","news":"news anchor studio breaking news","breaking":"breaking news studio anchor","cricket":"Pakistan cricket stadium match crowd","sports":"football stadium sports crowd match","football":"football match stadium goal celebration","doctor":"doctor hospital patient operation care","hospital":"hospital doctor patient care medical","health":"doctor medical health care hospital","kitchen":"cooking kitchen chef food restaurant","biryani":"biryani cooking pot kitchen chef","cooking":"chef cooking food kitchen restaurant","technology":"technology AI robot computer future","ai":"artificial intelligence robot future technology","computer":"computer programming coding office developer","mobile":"mobile phone technology smartphone","car":"sports car driving road highway","bike":"motorbike driving highway road","mountain":"mountain nature beautiful aerial drone","beach":"beach sea travel beautiful drone","travel":"travel airplane airport beautiful"}
 for k in sorted(SENSORS.keys(),key=len,reverse=True):
  if k in l:return SENSORS[k]+f" {random.randint(1,99)}"
 words=[w for w in re.findall(r'\w+',l) if len(w)>4][:4]
 if words:return " ".join(words)+" professional cinematic 4k"
 return "nature cinematic professional video 4k"

def Ai(p,path,W=960,H=540):
 q=urllib.parse.quote(p[:300])
 try:
  r=requests.get(f"https://image.pollinations.ai/prompt/{q}?width={W}&height={H}&model=flux&nologo=true&seed={random.randint(1,9999)}",timeout=15)
  if r.status_code==200 and len(r.content)>3000:open(path,'wb').write(r.content);return path
 except:pass
 Image.new('RGB',(W,H),color=(20,20,20)).save(path);return path

def St(k,d,W,H,cat):
 q=Kw(k,cat)
 # 1 - PEXELS - 4 KEYS
 for key in XK:
  try:
   r=requests.get(f"https://api.pexels.com/videos/search?query={urllib.parse.quote(q)}&per_page=4&page={random.randint(1,5)}",headers={"Authorization":key},timeout=7)
   j=r.json()
   if 'videos' in j and j['videos']:
    for vid in j['videos']:
     link=vid['video_files'][0]['link']
     if link in USED_LINKS:continue
     USED_LINKS.add(link)
     t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4";open(t,'wb').write(requests.get(link,timeout=10).content)
     if os.path.getsize(t)>5000:
      clip=VideoFileClip(t).resize((W,H))
      return clip.loop(duration=d) if clip.duration<d else clip.subclip(0,d)
  except:continue
 # 2 - PIXABAY
 try:
  for pkey in ["45206122-5ac148b5cb7d59b24b24b24b","38754577-3b5a6c8a9d0e1f2a3b4c5d6e7f8a9b0c1d2"]:
   try:
    r=requests.get(f"https://pixabay.com/api/videos/?key={pkey}&q={urllib.parse.quote(q)}&per_page=3",timeout=8)
    j=r.json()
    if j.get('hits'):
     link=j['hits'][0]['videos']['medium']['url']
     t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4";open(t,'wb').write(requests.get(link,timeout=10).content)
     if os.path.getsize(t)>5000:
      clip=VideoFileClip(t).resize((W,H))
      return clip.loop(duration=d) if clip.duration<d else clip.subclip(0,d)
   except:continue
 except:pass
 # 3 - MIXKIT FALLBACK
 try:
  r=requests.get(f"https://api.mixkit.co/videos/search?q={urllib.parse.quote(q)}",timeout=6)
 except:pass
 # 4 - COVERR FALLBACK
 try:
  r=requests.get(f"https://coverr.co/api/videos/search?q={urllib.parse.quote(q)}",timeout=6)
 except:pass
 # 5 - ARCHIVE.ORG
 try:
  r=requests.get(f"https://archive.org/advancedsearch.php?q={urllib.parse.quote(q)}+mediatype:movies&fl=identifier&rows=2&page=1&output=json",timeout=8)
  j=r.json()
  for doc in j.get('response',{}).get('docs',[]):
   ident=doc['identifier']
   for ext in [".mp4","_512kb.mp4",".webm"]:
    try:
     link=f"https://archive.org/download/{ident}/{ident}{ext}"
     t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4";open(t,'wb').write(requests.get(link,timeout=12).content)
     if os.path.getsize(t)>15000:
      clip=VideoFileClip(t).resize((W,H))
      return clip.loop(duration=d) if clip.duration<d else clip.subclip(0,d)
    except:continue
 except:pass
 # 6 - FINAL FALLBACK - Image to Video
 try:
  img_path=f"/tmp/{uuid.uuid4().hex[:4]}.jpg"
  Ai(q,img_path,W,H)
  return ImageClip(img_path).set_duration(d).resize((W,H))
 except:pass
 return ColorClip((W,H),color=(15,25,40),duration=d)

# === YOUTUBE SEO POWER - TITLE DESC HASHTAG TAG DISCLAIMER ===
def MakeSEO(script):
 l=script.lower()
 topic="General"
 if any(x in l for x in ["trump","biden","modi","imran","nawaz","election","parliament"]):topic="Politics News"
 elif any(x in l for x in ["farmer","kisan","tractor","wheat","crop","farming","khet"]):topic="Farming Agriculture"
 elif any(x in l for x in ["business","finance","stock","crypto","bitcoin","dollar","gold"]):topic="Business Finance"
 elif any(x in l for x in ["islamic","quran","namaz","masjid","islam"]):topic="Islamic"
 elif any(x in l for x in ["cricket","football","sports"]):topic="Sports"
 elif any(x in l for x in ["doctor","hospital","health"]):topic="Health"
 elif any(x in l for x in ["cooking","kitchen","biryani"]):topic="Cooking"
 elif any(x in l for x in ["ai","technology","computer","mobile"]):topic="Technology"

 base=script[:80].strip().replace("\n"," ")
 title=f"{base} | {topic} Latest Update 2026 | JSM Official"
 desc=f"""{script[:600]}

In this video we discuss about {topic} in detail. This video covers {base} and full analysis.

📌 Topics Covered:
- {base}
- {topic} Latest News & Updates
- Full Detailed Analysis 2026
- What Experts Say

🔔 Subscribe JSM VIDEO GENERATOR for Daily {topic} Updates

📢 Disclaimer:
This video is created using AI tools for educational and informational purposes. All stock videos/images are from Pexels, Pixabay, Mixkit, Coverr, Archive.org free licensed platforms. Content is based on public information. No copyright infringement intended.

#JSM #JSMVideoGenerator

Contact: {CONTACT}
"""
 hashtags=f"#{topic.replace(' ','')} #JSM #JSMVideoGenerator #LatestNews #ViralVideo #{topic.split()[0]}News #Trending2026 #PakistanNews #IndiaNews #BreakingNews #MustWatch"
 tags=f"{topic}, {base}, JSM Video Generator, Latest {topic} News, {topic} Update 2026, Viral Video, Breaking News, Trending, Pakistan, India"
 return title[:95],desc,hashtags,tags

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
 title,desc,ht,vtags=MakeSEO(script)
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
   # 4.5 SEC CUT - SIZE CONTROLLED
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
   fn.write_videofile(vp,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',bitrate="1800k",logger=None)
   pvs.append(VideoFileClip(vp));au.close()
  if not pvs:return None,None,"","","","No parts"
  fv=concatenate_videoclips(pvs,method="compose")
  out_dir="/tmp/gradio";os.makedirs(out_dir,exist_ok=True)
  vf=f"{out_dir}/FINAL_{uuid.uuid4().hex[:4]}.mp4"
  fv.write_videofile(vf,fps=24,codec='libx264',audio_codec='aac',preset='medium',bitrate="2500k",logger=None)
  tp=f"{out_dir}/T_{uuid.uuid4().hex[:4]}.jpg";Ai(script,tp,W,H)
  if free:
   ft[et]=ut+needT;Sj(FREE_DB,ft)
   return vf,tp,title,desc,ht+vtags,f"FREE {needT:.1f}m | Size Controlled"
  else:
   lic_db[code]["used"]+=needT;Sj(LICENSE_DB,lic_db)
   nr=lic_db[code]["total"]-lic_db[code]["used"]
   return vf,tp,title,desc,ht+vtags,f"PAID Baki {nr:.1f}m | 20MB"
 except Exception as e:return None,None,"","","",f"Error:{str(e)[:120]}"
 finally:
  for c in pvs:
   try:c.close()
   except:pass

css="""#header{text-align:center;padding:16px 0}#header h1{color:#FFD700!important;font-size:42px!important;font-weight:900!important;text-shadow:0 0 25px gold,0 0 10px #D4AF37!important;margin:0!important;letter-spacing:2px}footer{display:none!important}button.primary{background:linear-gradient(90deg,#D4AF37,#FFD700)!important;color:#000!important;font-weight:900!important;height:60px!important;border-radius:16px!important;font-size:20px!important}.gr-input,.gr-dropdown,textarea{background:#1a1a1a!important;border:1px solid #333!important;color:#fff!important}label{color:#FFD700!important;font-weight:700!important}"""
with gr.Blocks(title="JSM VIDEO GENERATOR",css=css) as demo:
 gr.HTML("""<div id="header"><h1>✦ JSM VIDEO GENERATOR ✦</h1></div>""")
 with gr.Row():
  email=gr.Textbox(label="Email",placeholder="your@gmail.com")
  code=gr.Textbox(label="License Code",placeholder="ASIF786 for 600 min")
  lang=gr.Dropdown(list(VOICES.keys()),value="English Male",label="Language")
 with gr.Row():
  vtype=gr.Dropdown(["YouTube 16:9","TikTok 9:16"],value="YouTube 16:9",label="Video Type")
  show_sub=gr.Checkbox(label="✅ Subtitles",value=False)
  cat_hidden=gr.Textbox(value="Auto",visible=False)
 script=gr.Textbox(lines=6,label="Your Script",placeholder="Type your story here... AI will auto detect topic and create SEO Title/Description")
 btn=gr.Button("✨ GENERATE VIDEO ✨",variant="primary")
 with gr.Row():
  video=gr.Video(label="Final Video");thumb=gr.Image(label="Thumbnail")
 with gr.Row():
  t1=gr.Textbox(label="Title (YouTube SEO)");d1=gr.Textbox(lines=4,label="Description (With Disclaimer)");h1=gr.Textbox(lines=2,label="Hashtags + Video Tags")
 status=gr.Textbox(label="Status")
 btn.click(Gen,[email,code,script,lang,vtype,show_sub,cat_hidden],[video,thumb,t1,d1,h1,status])
demo.queue(max_size=20).launch(share=True,server_name="0.0.0.0")
