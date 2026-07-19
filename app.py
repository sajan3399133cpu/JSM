import gradio as gr,asyncio,edge_tts,uuid,random,requests,re,os,json,base64,urllib.parse,datetime,time
from moviepy.editor import VideoFileClip,ColorClip,concatenate_videoclips,AudioFileClip,CompositeVideoClip,ImageClip,TextClip,CompositeAudioClip
from moviepy.audio.fx.volumex import volumex
from PIL import Image
import secrets,string

CONTACT="03043399133|03022246271"
ON="SAEED";ONUM="03043399133";MN="MUJAHID";MNUM="03022246271"

K4=['Uk9LSnZmWXV1U2tjN1FWVkw2VmpDZ1lGeUI4VVFaQ0xMQ2N0RDJTZlRKY2xJckRHbzVFeDNKTVg2','em5pWXZhdmhhbGY2Vkd3dVYya1VJcFJtN3ZHM1kwcmRkREx1enJJVHZtUHFRMjZrZEcwdmN5eTA=','ZjZJS3hySFI4TUhqMWdlRDYyY3JMVGZEVFFYMHM3ZXdGa3czaEVJNGQ0Q2VuUlRaWENrcENXRDk=','MWo2a0ZxMUdSQjQyOTFGMXMxUk1naGxnSVgzZDN1NzhPYVRwaURLbXRJU0FqSmtLUGI5dlZUa0w=','dHBreXBvZ3N3djA3bjg0ZGgwaWFISTl0YW11NDNHRWN2Wm9rQTNYaTNKU1RVVDBOVjMyQTZnRzk=']
XK=[base64.b64decode(k.encode()).decode() for k in K4]
PIXABAY_KEY = "38754577-3b5a6c8a9d0e1f2a3b4c5d6e7f8a9b0c1d2"

VOICES={"English Male":"en-US-AndrewNeural","English Female":"en-US-JennyNeural","English UK Male":"en-GB-RyanNeural","English UK Female":"en-GB-SoniaNeural","Hindi Male":"hi-IN-ArjunNeural","Hindi Female":"hi-IN-SwaraNeural","Urdu Male":"ur-PK-AsadNeural","Urdu Female":"ur-PK-UzmaNeural","Russian Male":"ru-RU-DmitryNeural","Russian Female":"ru-RU-SvetlanaNeural","Chinese Male":"zh-CN-YunxiNeural","Chinese Female":"zh-CN-XiaoxiaoNeural","Arabic Male":"ar-SA-HamedNeural","Arabic Female":"ar-SA-ZariyahAryan","Spanish Male":"es-ES-AlvaroNeural","Spanish Female":"es-ES-ElviraNeural"}

BASE_DIR="./JSM_Outputs"
FREE_DB=os.path.join(BASE_DIR,"free_daily.json")
LICENSE_DB=os.path.join(BASE_DIR,"jsm_licenses_final.json")
os.makedirs(BASE_DIR,exist_ok=True)

STOP_WORDS = {"about", "today", "video", "talk", "karenge", "baat", "shuru", "please", "subscribe", "channel", "welcome", "dosto", "bhai", "hello", "everyone"}

FIXED_LICENSES = {
    "AREEJ786": {"bound_email": "", "total": 300.0, "used": 0.0, "expiry": "2030-12-31"},
    "JSM300": {"bound_email": "", "total": 300.0, "used": 0.0, "expiry": "2030-12-31"},
    "JSM500": {"bound_email": "", "total": 500.0, "used": 0.0, "expiry": "2030-12-31"},
    "JSM600": {"bound_email": "", "total": 600.0, "used": 0.0, "expiry": "2030-12-31"},
    "JSM1000": {"bound_email": "", "total": 1000.0, "used": 0.0, "expiry": "2030-12-31"}
}

# الگ الگ کیٹیگریز کے لیے ڈائنامک فال بیک ویڈیوز کا پول (تاکہ ویڈیو کبھی بھی ریپیٹ نہ ہو)
DYNAMIC_FALLBACKS = {
    "technology": [
        "https://player.vimeo.com/external/371433846.sd.mp4?s=236da2f3c02230b0e5170d9a617651a029c29c8e&profile_id=165",
        "https://player.vimeo.com/external/538569350.sd.mp4?s=8b652ee97d8b36a19f5617bfd69106ec2b9cb525&profile_id=165",
        "https://player.vimeo.com/external/409132226.sd.mp4?s=ebd04cb5038c353b3b194519543e33c7dae2051f&profile_id=165"
    ],
    "finance": [
        "https://player.vimeo.com/external/435649383.sd.mp4?s=7b9a52bc23924df50f3c0e1fc84241e06fa4d5de&profile_id=165",
        "https://player.vimeo.com/external/394142711.sd.mp4?s=7342fbfa7b494d4d3a04297b48a1a364bb2fa02a&profile_id=165"
    ],
    "medical": [
        "https://player.vimeo.com/external/405461244.sd.mp4?s=6c2ef50f32997c4fcfa6d0130f14a60155627f12&profile_id=165",
        "https://player.vimeo.com/external/460144670.sd.mp4?s=5481d6541f6e21aa85aa0ee49fa6b2d2f447f5cf&profile_id=165"
    ],
    "farming": [
        "https://player.vimeo.com/external/390975619.sd.mp4?s=73ef6233a0b5a32ba06d91da3c0c1b489bc37f59&profile_id=165",
        "https://player.vimeo.com/external/517614131.sd.mp4?s=6a51d02c082729a997ef3eb905fb57f6f1943bf1&profile_id=165"
    ],
    "news": [
        "https://player.vimeo.com/external/416487195.sd.mp4?s=319a27f677b02db7b4618e001859e9a65f9ca22a&profile_id=165",
        "https://player.vimeo.com/external/384761655.sd.mp4?s=c6790a316b23b49f96b27d42cf38f9024f8d4380&profile_id=165"
    ],
    "crime": [
        "https://player.vimeo.com/external/510848375.sd.mp4?s=1f7de7b938c4749f50e82da1dfdfec451ef9fc3e&profile_id=165",
        "https://player.vimeo.com/external/507421526.sd.mp4?s=c882855140d7c71f544975e5be2d5eb16e4544b8&profile_id=165"
    ],
    "general": [
        "https://images.pexels.com/videos/4482/motion-background-pms-1.mp4",
        "https://images.pexels.com/videos/3125396/free-video-3125396.mp4",
        "https://player.vimeo.com/external/371433846.sd.mp4?s=236da2f3c02230b0e5170d9a617651a029c29c8e&profile_id=165"
    ]
}

def Lj(p):
 try:
  data = json.load(open(p))
  for k, v in FIXED_LICENSES.items():
   if k not in data: data[k] = v
  return data
 except:
  return FIXED_LICENSES.copy()

def Sj(p,d):
 try:
  for k, v in FIXED_LICENSES.items():
   if k not in d: d[k] = v
  json.dump(d,open(p,'w'))
 except:pass

def clean_analyze(script):
 clean=re.sub(r"(sex\s*video|porn|xxx|nude|naked|boobs|bikini)"," ",script,flags=re.I)
 sens=[s.strip() for s in re.split(r'[.!?\n]+',clean) if len(s.strip())>8]
 return clean,sens

def Kw(text,cat):
 l=text.lower()
 if any(x in l for x in ["farmer", "kisan", "tractor", "agriculture", "field"]): return "pakistan village farmer tractor agriculture field"
 if any(x in l for x in ["bitcoin", "crypto", "finance", "money", "trading"]): return "stock market trading money business corporate"
 if any(x in l for x in ["doctor", "hospital", "patient", "medical", "health"]): return "doctor treating patient hospital medical checkup"
 if any(x in l for x in ["ai", "robot", "coding", "software", "computer", "programming"]): return "cyberpunk tech coding developer typing hands"
 if any(x in l for x in ["news", "khabar", "breaking", "update", "pakistan"]): return "news studio background global map matrix digital"
 if any(x in l for x in ["kahani", "shaitan", "jinn", "bhoot", "crime", "scary"]): return "dark cinematic mystery foggy night dramatic smoke"
 clean_text = re.sub(r'[^\w\s]', '', l)
 words = clean_text.split()
 meaningful_words = [w for w in words if len(w) > 4 and w not in STOP_WORDS]
 if len(meaningful_words) >= 2: return " ".join(meaningful_words[:3]) + " professional cinematic 4k"
 return "beautiful cinematic nature landscape abstract backgrounds"

def get_category(text):
 l=text.lower()
 if any(x in l for x in ["ai","robot","tech","coding","software"]): return "technology"
 if any(x in l for x in ["bitcoin","crypto","stock","money","business","finance"]): return "finance"
 if any(x in l for x in ["doctor","hospital","health","medical"]): return "medical"
 if any(x in l for x in ["farmer","tractor","agriculture","field"]): return "farming"
 if any(x in l for x in ["news","khabar","breaking","update"]): return "news"
 if any(x in l for x in ["kahani","shaitan","jinn","bhoot","crime"]): return "crime"
 return "general"

def get_niche_music(cat):
 music_keywords = {"finance": "corporate business motivation", "technology": "ambient tech electronic", "medical": "calm cinematic soft", "farming": "acoustic guitar country", "general": "cinematic inspiring background", "news": "news corporate dramatic", "crime": "dark suspense mystery"}
 q = music_keywords.get(cat, "cinematic inspiring background")
 try:
  r = requests.get(f"https://pixabay.com/api/soundeffects/?key={PIXABAY_KEY}&q={urllib.parse.quote(q)}&per_page=5", timeout=5)
  if r.json().get('hits'):
   mp = f"{BASE_DIR}/bgm_{uuid.uuid4().hex[:4]}.mp3"
   open(mp, 'wb').write(requests.get(random.choice(r.json()['hits'])['download_url'], timeout=10).content)
   return mp
 except:pass
 return None

# بہتر ملٹی سورس ویڈیو انجن (اب ہر پارٹ کی الگ الگ ویڈیو فیسچ ہوگی)
def St(k,d,W,H,cat, part_idx=0):
 q=Kw(k,cat)
 q_encoded = urllib.parse.quote(q)
 
 # سورس 1: Pexels API
 for key in XK:
  try:
   r=requests.get(f"https://api.pexels.com/videos/search?query={q_encoded}&per_page=5",headers={"Authorization":key},timeout=6)
   if 'videos' in r.json() and r.json()['videos']:
    # ہر پارٹ کے انڈیکس کے حساب سے لسٹ میں سے الگ ویڈیو اٹھانا تاکہ ریپیٹ نہ ہو
    v_list = r.json()['videos']
    v_obj = v_list[part_idx % len(v_list)]
    lk=v_obj['video_files'][0]['link']
    t= f"{BASE_DIR}/{uuid.uuid4().hex[:4]}.mp4"
    open(t,'wb').write(requests.get(lk,timeout=12).content)
    cl=VideoFileClip(t).resize((W,H))
    return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
  except:continue

 # سورس 2: Pixabay API
 try:
  r = requests.get(f"https://pixabay.com/api/videos/?key={PIXABAY_KEY}&q={q_encoded}&per_page=5", timeout=6)
  if r.json().get('hits'):
   v_list = r.json()['hits']
   v_obj = v_list[part_idx % len(v_list)]
   lk = v_obj['videos']['medium']['url']
   t = f"{BASE_DIR}/{uuid.uuid4().hex[:4]}.mp4"
   open(t,'wb').write(requests.get(lk,timeout=12).content)
   cl = VideoFileClip(t).resize((W,H))
   return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
 except:pass

 # سورس 3 سے 6: ڈائنامک پول فال بیک (تاکہ اگر لنک فیل بھی ہوں تو ویڈیو تبدیل ہو)
 pool = DYNAMIC_FALLBACKS.get(cat, DYNAMIC_FALLBACKS["general"])
 fallback_url = pool[part_idx % len(pool)]
 try:
  t = f"{BASE_DIR}/{uuid.uuid4().hex[:4]}.mp4"
  open(t,'wb').write(requests.get(fallback_url,timeout=12).content)
  cl = VideoFileClip(t).resize((W,H))
  return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
 except:pass

 return ColorClip((W,H),color=(random.randint(10,40),random.randint(10,40),random.randint(10,40)),duration=d)

async def Tt(t,o,v):await edge_tts.Communicate(t,v,rate="+4%").save(o)
def run_tts(tx,out,vc):
 try:
  loop=asyncio.new_event_loop();asyncio.set_event_loop(loop);loop.run_until_complete(Tt(tx,out,vc));loop.close()
 except:pass

def Gen(email,code,script,lang,vtype,res,show_sub,cat_hidden, pr=gr.Progress()):
 if not script.strip() or not email.strip():return None, None, "Email/Script likho"
 W,H={"1920x1080 - Full HD":(1920,1080),"1280x720 - HD":(1280,720),"854x480 - SD Fast":(854,480)}.get(res,(1280,720))
 if "TikTok" in vtype:W,H=(720,1280)
 code=code.strip().upper();today=datetime.date.today();email=email.strip().lower()
 
 db=Lj(LICENSE_DB)
 if code in FIXED_LICENSES:
  lic=db[code]
  if lic["used"]>=lic["total"]: return None, None, f"Khatam! {lic['used']:.1f}/{lic['total']}"
  rem=lic["total"]-lic["used"];free=False
 elif not code:
  fd=Lj(FREE_DB);ek=email+"_"+today.isoformat();ut=fd.get(ek,0)
  if ut>=1:return None, None, f"Daily Free Khatam! {CONTACT}"
  rem=1-ut;free=True;ft=fd;et=ek
 else:
  if code not in db: return None, None, f"❌ Invalid Code! {CONTACT}"
  lic=db[code]
  if lic["bound_email"] and lic["bound_email"]!=email: return None, None, f"LOCKED! {lic['bound_email']}"
  if not lic["bound_email"]: lic["bound_email"] = email
  if lic["used"]>=lic["total"]: return None, None, f"Khatam! {lic['used']:.1f}/{lic['total']}"
  rem=lic["total"]-lic["used"];free=False

 cs,kws=clean_analyze(script);pvs=[]
 
 try:
  chs=kws;need=0.0
  total_steps = len(chs)
  
  for idx,ch in enumerate(chs):
   pr(idx/total_steps, desc=f"Processing Part {idx+1}/{total_steps}...")
   current_cat = get_category(ch)
   
   ap=f"{BASE_DIR}/{uuid.uuid4().hex[:5]}.mp3"
   run_tts(ch,ap,VOICES.get(lang,"en-US-AndrewNeural"))
   if not os.path.exists(ap):continue
   au=AudioFileClip(ap)
   if au.duration > 0.4: au = au.subclip(0, au.duration - 0.2)
   
   need+=au.duration/60.0
   if need>rem+0.01:au.close();return None, None, f"Need {need:.1f}m Baki {rem:.1f}m"
   
   # انڈیکس پاس کیا گیا ہے تاکہ ہر لائن پر الگ ویڈیو فیسچ ہو
   base_clip=St(ch,au.duration,W,H,current_cat, part_idx=idx).set_duration(au.duration)
   layers=[base_clip]
   if show_sub:
    try:
     txt=TextClip(ch[:90],fontsize=int(W*0.04),color='yellow',stroke_color='black',stroke_width=3.5,method='caption',size=(W*0.88,None)).set_duration(au.duration).set_position(('center',0.78),relative=True)
     layers.append(txt)
    except:pass
   fn=CompositeVideoClip(layers).set_audio(au)
   vp=f"{BASE_DIR}/P_{idx}.mp4"
   fn.write_videofile(vp,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',threads=4,logger=None)
   pvs.append(VideoFileClip(vp));au.close()
   
  if not pvs:return None, None, "Script check karo"
  
  pr(0.9, desc="Merging and adding background music...")
  fv=concatenate_videoclips(pvs,method="compose")
  video_duration = fv.duration
  original_audio = fv.audio
  
  main_cat = get_category(chs[0] if chs else "general")
  bgm_path = get_niche_music(main_cat)
  
  if bgm_path and os.path.exists(bgm_path):
   try:
    bgm = AudioFileClip(bgm_path).loop(duration=video_duration).fx(volumex, 0.12)
    fv = fv.set_audio(CompositeAudioClip([original_audio, bgm]))
   except:pass
   
  vf=f"./JSM_OUTPUT_VIDEO.mp4"
  fv.write_videofile(vf,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',threads=4,logger=None)
  for pv in pvs: pv.close()
  
  if free:
   ft[et]=ut+need;Sj(FREE_DB,ft);st_msg = f"FREE {need:.1f}m OK"
  else:
   db[code]["used"]+=need;Sj(LICENSE_DB,db);st_msg = f"PAID Baki {(db[code]['total']-db[code]['used']):.1f}m"
   
  return vf, vf, st_msg
 except Exception as e:return None, None, f"Error:{str(e)[:200]}"

css="""
body, .gradio-container { background-color: #000000 !important; color: #FFFFFF !important; }
#header { background-color: #000000 !important; border-bottom: 2px solid #FFD700 !important; padding: 20px; text-align: center; }
#header h1 { color: #FFD700 !important; font-size: 32px !important; font-weight: 900 !important; }
.sub-title { color: #D4AF37 !important; }
.gr-box, .gr-block { background-color: #000000 !important; border: 1px solid #333 !important; }
.gr-textbox, .gr-dropdown, .gr-checkbox { background-color: #000000 !important; color: #FFD700 !important; border: 1px solid #333 !important; }
label { color: #FFD700 !important; }
button.primary { background: linear-gradient(90deg, #FFD700, #FFA500) !important; color: #000000 !important; font-weight: bold !important; border: none !important; }
"""

with gr.Blocks(title="JSM VIDEO GENERATOR", css=css) as demo:
    gr.HTML(f"""
    <div id="header">
        <h1>✦ JSM VIDEO GENERATOR ✦</h1>
        <div class="sub-title">AI POWERED VIDEO STUDIO</div>
        <div style="color:#A0A0A0; font-size:12px; margin-top:10px;">{ON}: {ONUM} | {MN}: {MNUM}</div>
    </div>
    """)
    
    with gr.Row():
        email = gr.Textbox(label="Email", placeholder="your@gmail.com")
        code = gr.Textbox(label="License Code", placeholder="Enter valid key")
        lang = gr.Dropdown(list(VOICES.keys()), value="English Male", label="🌍 Language + Voice Select")
    with gr.Row():
        vtype = gr.Dropdown(["YouTube 16:9", "TikTok 9:16"], value="YouTube 16:9", label="Type")
        resolution = gr.Dropdown(["1920x1080 - Full HD", "1280x720 - HD", "854x480 - SD Fast"], value="1280x720 - HD", label="HD")
        show_sub = gr.Checkbox(label="Subtitles ON/OFF", value=True)
        cat_hidden = gr.Textbox(value="Auto", visible=False)
    script = gr.Textbox(lines=6, label="Your Script - Har Line = 1 New Topic", max_length=2000)
    btn = gr.Button("✨ GENERATE GOLDEN VIDEO ✨", variant="primary")
    
    with gr.Row():
        video = gr.Video(label="Player View")
        download_btn = gr.File(label="📥 DOWNLOAD VIDEO")
        
    status = gr.Textbox(label="Status")
    btn.click(Gen, [email, code, script, lang, vtype, resolution, show_sub, cat_hidden], [video, download_btn, status])

demo.queue(max_size=5).launch(share=True, show_error=True)
