import gradio as gr,asyncio,edge_tts,uuid,random,requests,re,os,json,base64,urllib.parse,datetime,time
from moviepy.editor import VideoFileClip,ColorClip,concatenate_videoclips,AudioFileClip,CompositeVideoClip,ImageClip,TextClip
from PIL import Image
import secrets,string

CONTACT="03043399133|03022246271"
ADMIN_PASS="JamSaeed@786#Motha_Owner_0304!"
ON="JAM SAEED";ONUM="03043399133";MN="MUJAHID HUSSAIN";MNUM="03022246271"
K4=['Uk9LSnZmWXV1U2tjN1FWVkw2VmpDZ1lGeUI4VVFaQ0xMQ2N0RDJTZlRKY2xJckRHbzVFeDNKTVg2','em5pWXZhdmhhbGY2Vkd3dVYya1VJcFJtN3ZHM1kwcmRkREx1enJJVHZtUHFRMjZrZEcwdmN5eTA=','ZjZJS3hySFI4TUhqMWdlRDYyY3JMVGZEVFFYMHM3ZXdGa3czaEVJNGQ0Q2VuUlRaWENrcENXRDk=','MWo2a0ZxMUdSQjQyOTFGMXMxUk1naGxnSVgzZDN1NzhPYVRwaURLbXRJU0FqSmtLUGI5dlZUa0w=','dHBreXBvZ3N3djA3bjg0ZGgwaWFISTl0YW11NDNHRWN2Wm9rQTNYaTNKU1RVVDBOVjMyQTZnRzk=']
XK=[base64.b64decode(k.encode()).decode() for k in K4]

VOICES={
"English Male":"en-US-AndrewNeural","English Female":"en-US-JennyNeural",
"English UK Male":"en-GB-RyanNeural","English UK Female":"en-GB-SoniaNeural",
"Hindi Male":"hi-IN-ArjunNeural","Hindi Female":"hi-IN-SwaraNeural",
"Urdu Male":"ur-PK-AsadNeural","Urdu Female":"ur-PK-UzmaNeural",
"Russian Male":"ru-RU-DmitryNeural","Russian Female":"ru-RU-SvetlanaNeural",
"Chinese Male":"zh-CN-YunxiNeural","Chinese Female":"zh-CN-XiaoxiaoNeural",
"Arabic Male":"ar-SA-HamedNeural","Arabic Female":"ar-SA-ZariyahNeural",
"Spanish Male":"es-ES-AlvaroNeural","Spanish Female":"es-ES-ElviraNeural",
"Portuguese Male":"pt-BR-AntonioNeural","Portuguese Female":"pt-BR-FranciscaNeural",
"French Male":"fr-FR-HenriNeural","French Female":"fr-FR-DeniseNeural",
"German Male":"de-DE-ConradNeural","German Female":"de-DE-KatjaNeural",
"Turkish Male":"tr-TR-AhmetNeural","Turkish Female":"tr-TR-EmelNeural",
"Indonesian Male":"id-ID-ArdiNeural","Indonesian Female":"id-ID-GadisNeural",
"Japanese Male":"ja-JP-KeitaNeural","Japanese Female":"ja-JP-NanamiNeural",
"Korean Male":"ko-KR-InJoonNeural","Korean Female":"ko-KR-SunHiNeural",
"Italian Male":"it-IT-DiegoNeural","Italian Female":"it-IT-ElsaNeural",
"Bengali Male":"bn-IN-BashkarNeural","Bengali Female":"bn-IN-TanishaaNeural"
}

# تکے والے ہارڈ کوڈڈ پیکجز، سیکیور جنریٹڈ کوڈز چلیں گے
PACKAGES={ALI"300"٫ALI786"250"}

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
 db[c]["bound_email"]=email.strip().lower()
 Sj(LICENSE_DB,db)
 return f"✅ Code Ban Gaya {email} ke liye",c,""

def AdminView(pw):
 if pw!=ADMIN_PASS:return "Galat Owner Key"
 db=Lj(LICENSE_DB);t=""
 for k,v in db.items():t+=f"{k} | {v['bound_email'] or 'UNUSED'} | {v['used']:.1f}/{v['total']} min | Expiry: {v['expiry']}\n"
 return t or "Koi Code Nahi"

def clean_analyze(script):
 clean=re.sub(r"(sex\s*video|porn|xxx|nude|naked|boobs|bikini\s+girl\s+sexy|fuck|birthday girl|birthday party|birthday|party|fitness girl|workout girl|gym exercise)"," ",script,flags=re.I)
 sens=[s.strip() for s in re.split(r'[.!?]+',clean) if len(s.strip())>8]
 return clean,sens

def Kw(text,cat):
 l=text.lower()
 if any(x in l for x in ["birthday","party","exercise","workout","gym"]):
  if cat == "finance": return "business finance stock market trading corporate"
  if cat == "technology": return "artificial intelligence coding developer tech"
  return "global international news studio corporate cinematic"
 if any(x in l for x in ["ai","artificial intelligence","chatgpt","robot","coding","software"]): return "artificial intelligence robot technology"
 if any(x in l for x in ["bitcoin","crypto","blockchain","finance","money","stock","market"]): return "bitcoin crypto cryptocurrency business trading"
 if any(x in l for x in ["doctor","hospital","patient","medical","health"]): return "doctor hospital medical patient clinical"
 if any(x in l for x in ["farmer","kisan","tractor","wheat","crop","agriculture"]): return "farmer tractor agriculture field farming"
 w=[x for x in re.findall(r'\w+',l) if len(x)>4][:3]
 return " ".join(w)+" professional cinematic 4k" if w else "global news studio corporate cinematic 4k"

def get_category(text):
 l=text.lower()
 if any(x in l for x in ["ai","chatgpt","robot","tech","coding","software"]): return "technology"
 if any(x in l for x in ["bitcoin","crypto","stock","money","business","finance"]): return "finance"
 if any(x in l for x in ["doctor","hospital","health","medical"]): return "medical"
 if any(x in l for x in ["farmer","tractor","agriculture","field"]): return "farming"
 return "general"

def Ai(p,path,W=960,H=540):
 q=urllib.parse.quote(p[:200])
 try:
  r=requests.get(f"https://image.pollinations.ai/prompt/{q}?width={W}?height={H}&model=flux&nologo=true&seed={random.randint(1,9999)}",timeout=12)
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

def MakeSEO(s):
 l=s.lower()
 if any(x in l for x in ["doctor","health"]):t="Health & Doctor Tips"
 elif any(x in l for x in ["finance","money","stock","business","crypto"]):t="Business & Finance"
 else:t="General Update"
 b=s[:70].strip().replace("\n"," ")
 title=f"{b} | {t} 2026"
 desc=f"{s[:500]}\n\nAbout {t}: {b}\nStock videos from Pexels, Pixabay.\n"
 ht=f"#{t.replace(' ','')} #LatestUpdate #ViralVideo"
 tags=f"{t}, {b}, Latest {t} 2026"
 return title[:95],desc,ht,tags

async def Tt(t,o,v):await edge_tts.Communicate(t,v,rate="+4%").save(o)
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
 if len(script.strip()) > 2000: return None,None,"","","", "❌ اسکرپٹ 2000 سے چھوٹا رکھیں۔"

 W,H={"1920x1080 - Full HD":(1920,1080),"1280x720 - HD":(1280,720),"854x480 - SD Fast":(854,480)}.get(res,(1280,720))
 if "TikTok" in vtype:W,H=(720,1280)
 code=code.strip().upper();today=datetime.date.today();email=email.strip().lower()
 
 db=Lj(LICENSE_DB);lic=db.get(code)
 if not lic:
  fd=Lj(FREE_DB);ek=email+"_"+today.isoformat();ut=fd.get(ek,0)
  if ut>=1:return None,None,"","","",f"Daily Free Khatam! {CONTACT}"
  rem=1-ut;free=True;ft=fd;et=ek
 else:
  if lic["bound_email"] and lic["bound_email"]!=email:return None,None,"","","",f"LOCKED ke liye! {lic['bound_email']}"
  if today>datetime.date.fromisoformat(lic["expiry"]):return None,None,"","","",f"EXPIRED! {CONTACT}"
  if lic["used"]>=lic["total"]:return None,None,"","","",f"Khatam! {lic['used']:.1f}/{lic['total']}"
  rem=lic["total"]-lic["used"];free=False
 
 cs,kws=clean_analyze(script);title,desc,ht,vt=MakeSEO(cs);pvs=[]
 try:
  chs=kws;need=0.0;USED.clear()
  for idx,ch in enumerate(chs):
   ap=f"/tmp/{uuid.uuid4().hex[:5]}.mp3"
   run_tts(ch,ap,VOICES.get(lang,"en-US-AndrewNeural"))
   if not os.path.exists(ap) or os.path.getsize(ap)<2000:continue
   try:au=AudioFileClip(ap)
   except:continue
   if not au or au.duration==0:au.close();continue
   nd=au.duration/60.0;need+=nd
   if need>rem+0.1:au.close();return None,None,"","","",f"Need {need:.1f}m Baki {rem:.1f}m"
   per_clip=4.5;num_clips=max(1,int(au.duration/per_clip)+1);clips=[]
   for i in range(num_clips):
    if i>0 and i%5==0: time.sleep(3)
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
  if free:ft[et]=ut+need;Sj(FREE_DB,ft);return vf,tp,title,desc,ht+vt,f"FREE {need:.1f}m OK"
  else:
   db[code]["used"]+=need
   if not db[code]["bound_email"]: db[code]["bound_email"]=email
   Sj(LICENSE_DB,db);nr=db[code]["total"]-db[code]["used"];return vf,tp,title,desc,ht+vt,f"PAID Baki {nr:.1f}m"
 except Exception as e:return None,None,"","","","Error:"+str(e)[:100]

# آپ کی پسند کا 100٪ فل بلیک اور گولڈن الٹرا کلاسک ڈارک CSS تھیم
css="""
body, .gradio-container, html { background-color: #000000 !important; color: #FFFFFF !important; }
#header { text-align: center; padding: 25px 10px; background: #000000 !important; border-bottom: 1px solid #FFD700 !important; }
#header h1 { color: #FFD700 !important; font-size: 36px !important; font-weight: 900 !important; text-shadow: 0 0 10px rgba(255, 215, 0, 0.5) !important; margin-bottom: 5px !important; }
.sub-title { color: #D4AF37 !important; font-size: 14px !important; font-weight: bold; }
button.primary { background: linear-gradient(90deg, #FFD700, #FFA500) !important; color: #000000 !important; font-weight: 900 !important; height: 50px !important; border-radius: 8px !important; border: none !important; box-shadow: 0 4px 12px rgba(255, 165, 0, 0.3) !important; cursor: pointer; }
.gr-textbox, .gr-dropdown, input, textarea, select { background-color: #111111 !important; color: #FFD700 !important; border: 1px solid #222222 !important; border-radius: 6px !important; }
.gr-textbox:focus, .gr-dropdown:focus, input:focus { border-color: #FFD700 !important; }
.tabs, .tab-nav { background: #000000 !important; border-bottom: 1px solid #222222 !important; }
.tab-nav button { color: #A0A0A0 !important; }
.tab-nav button.selected { color: #FFD700 !important; border-bottom: 2px solid #FFD700 !important; background: #111111 !important; }
label, span { color: #FFD700 !important; font-weight: bold !important; }
footer { display: none !important; }
"""

with gr.Blocks(title="JSM VIDEO GENERATOR", css=css) as demo:
    # ہیڈر سے تمام فالتو بیجز غائب، صرف آپ کا نام، مینیجر کا نام اور نمبر باقی
    gr.HTML(f"""
    <div id="header">
        <h1>✦ JSM VIDEO GENERATOR ✦</h1>
        <div class="sub-title">{ON}: {ONUM} | {MN}: {MNUM}</div>
    </div>
    """)
    
    with gr.Tab("🎬 Video Generator"):
        with gr.Row():
            email = gr.Textbox(label="Email", placeholder="your@gmail.com")
            code = gr.Textbox(label="License Code", placeholder="JSM300-XXXXXX")
            lang = gr.Dropdown(list(VOICES.keys()), value="English Male", label="🌍 Language + Voice")
        with gr.Row():
            vtype = gr.Dropdown(["YouTube 16:9", "TikTok 9:16"], value="YouTube 16:9", label="Format")
            resolution = gr.Dropdown(["1920x1080 - Full HD", "1280x720 - HD", "854x480 - SD Fast"], value="1280x720 - HD", label="Quality")
            show_sub = gr.Checkbox(label="Subtitles", value=True)
            cat_hidden = gr.Textbox(value="Auto", visible=False)
        
        script = gr.Textbox(lines=6, label="Your Script (Max 2000 Chars)", max_length=2000)
        btn = gr.Button("✨ GENERATE GOLDEN VIDEO ✨", variant="primary")
        
        with gr.Row():
            video = gr.Video(label="Final Video")
            thumb = gr.Image(label="AI Thumbnail")
        with gr.Row():
            t1 = gr.Textbox(label="SEO Title")
            d1 = gr.Textbox(lines=3, label="Description")
            h1 = gr.Textbox(lines=2, label="Tags")
        status = gr.Textbox(label="Status")
        btn.click(Gen, [email, code, script, lang, vtype, resolution, show_sub, cat_hidden], [video, thumb, t1, d1, h1, status])
        
    with gr.Tab("🔐 Admin Panel"):
        gr.Markdown("### 🔑 OWNER SECURITY ACCESS")
        admin_pass = gr.Textbox(label="Owner Key", type="password")
        with gr.Row():
            user_email = gr.Textbox(label="User Email (Optional for Bulk)")
            mins = gr.Dropdown([30, 100, 300, 500, 600, 1000], value=300, label="Minutes")
            bulk_count = gr.Number(label="Bulk Count", value=1, precision=0)
        gen_btn = gr.Button("🔑 Generate Ultra Secure Code", variant="primary")
        out_msg = gr.Textbox(label="Message")
        out_code = gr.Textbox(lines=6, label="Generated Secure Codes")
        view_btn = gr.Button("📋 Saare Codes Dekho")
        view_out = gr.Textbox(lines=15, label="All Active Licenses")
        gen_btn.click(AdminGen, [admin_pass, user_email, mins, bulk_count], [out_msg, out_code, view_out])
        view_btn.click(AdminView, [admin_pass], [view_out])

demo.queue(max_size=10).launch(share=True)
