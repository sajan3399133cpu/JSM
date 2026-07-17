import gradio as gr,asyncio,edge_tts,uuid,random,requests,re,os,json,base64,urllib.parse,datetime
from moviepy.editor import VideoFileClip,ColorClip,concatenate_videoclips,AudioFileClip,CompositeVideoClip,ImageClip,TextClip
from PIL import Image
import secrets,string
CONTACT="03043399133|03022246271";ADMIN_PASS="JamSaeed@786#Motha_Owner_0304!";ON="JAM SAEED MOTHA";ONUM="03043399133";MN="MUJAHID HUSSAIN";MNUM="03022246271"
K4=['Uk9LSnZmWXV1U2tjN1FWVkw2VmpDZ1lGeUI4VVFaQ0xMQ2N0RDJTZlRKY2xJckRHbzVFeDNKTVg2','em5pWXZhdmhhbDY2Vkd3dVYya1VJcFJtN3ZHM1kwcmRkREx1enJJVHZtUHFRMjZrZEcwdmN5eTA=','ZjZJS3hySFI4TUhqMWdlRDYyY3JMVGZEVFFYMHM3ZXdGa3czaEVJNGQ0Q2VuUlRaWENrcENXRDk=','MWo2a0ZxMUdSQjQyOTFGMXMxUk1naGxnSVgzZDN1NzhPYVRwaURLbXRJU0FqSmtLUGI5dlZUa0w=','dHBreXBvZ3N3djA3bjg0ZGgwaWFISTl0YW11NDNHRWN2Wm9rQTNYaTNKU1RVVDBOVjMyQTZnRzk=']
XK=[base64.b64decode(k.encode()).decode() for k in K4]
VOICES={"EN Motivational":"en-US-GuyNeural","EN News":"en-US-DavisNeural","EN Deep":"en-US-JasonNeural","EN Female":"en-US-JennyNeural","EN Female News":"en-US-AriaNeural","UK Male":"en-GB-RyanNeural","Urdu Male":"ur-PK-AsadNeural","Urdu Female":"ur-PK-UzmaNeural","Hindi Male":"hi-IN-MadhurNeural","Hindi Female":"hi-IN-SwaraNeural","Arabic M":"ar-SA-HamedNeural","Arabic F":"ar-SA-ZariyahNeural","Spanish M":"es-ES-AlvaroNeural","Spanish F":"es-ES-ElviraNeural","French M":"fr-FR-HenriNeural","French F":"fr-FR-DeniseNeural","German M":"de-DE-ConradNeural","German F":"de-DE-KatjaNeural","Turkish M":"tr-TR-AhmetNeural","Turkish F":"tr-TR-EmelNeural","Motivational 2":"en-US-EricNeural","News F2":"en-US-MichelleNeural","Story Female":"en-US-SaraNeural","AU Male":"en-AU-WilliamNeural"}
PACKAGES={"ASIF":100,"ALI":100,"JSM":100,"ASIF786":600,"JSM30":30,"JSM100":100,"JSM300":300,"JSM500":500,"JSM786":600,"JSM600":600,"JSMGOLD":1000,"JSM786GOLD":9999}
BASE_DIR="/data" if os.path.exists("/data") else "."
FREE_DB=os.path.join(BASE_DIR,"free_daily.json");LICENSE_DB=os.path.join(BASE_DIR,"jsm_licenses_final.json");os.makedirs(BASE_DIR,exist_ok=True);USED=set()
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
   c=f"JSM{mins}-{''.join(secrets.choice(string.ascii_uppercase+string.digits) for _ in range(6))}";db[c]={"bound_email":"","total":int(mins),"used":0.0,"expiry":str(datetime.date.today()+datetime.timedelta(days=30))};o.append(c)
  Sj(LICENSE_DB,db);return f"✅ {cnt} Codes Ban Gaye!","\n".join(o),""
 if not email:return "Email likho","",""
 c=f"JSM{mins}-{''.join(secrets.choice(string.ascii_uppercase+string.digits) for _ in range(6))}";db[c]={"bound_email":email.strip().lower(),"total":int(mins),"used":0.0,"expiry":str(datetime.date.today()+datetime.timedelta(days=30))};Sj(LICENSE_DB,db);return f"✅ Code Ban Gaya {email} ke liye",c,""
def AdminView(pw):
 if pw!=ADMIN_PASS:return "Galat Owner Key"
 db=Lj(LICENSE_DB);t=""
 for k,v in db.items():t+=f"{k} | {v['bound_email'] or 'UNUSED'} | {v['used']:.1f}/{v['total']} | {v['expiry']}\n"
 return t or "Koi Code Nahi"
def clean_analyze(script):
 clean=re.sub(r"(sex\s*video|porn|xxx|nude|naked|boobs|bikini\s+girl\s+sexy|fuck)"," ",script,flags=re.I)
 sens=[s.strip() for s in re.split(r'[.!?]+',clean) if len(s.strip())>5];kws=[]
 for s in sens:
  l=s.lower()
  if any(x in l for x in ["doctor","hospital","health"]):kws.append(("doctor hospital patient care medical","medical"))
  elif any(x in l for x in ["finance","money","stock","crypto","business"]):kws.append(("finance business money stock market office","finance"))
  elif any(x in l for x in ["islam","quran","namaz","masjid","allah"]):kws.append(("mosque islamic interior beautiful light","islamic"))
  elif any(x in l for x in ["news","politics","election","parliament","trump","biden","modi","imran"]):kws.append(("news anchor studio professional","news"))
  elif any(x in l for x in ["farm","kisan","tractor","wheat","crop","farming"]):kws.append(("farmer tractor agriculture field harvest","farming"))
  elif any(x in l for x in ["cricket","football","sports","match","stadium"]):kws.append(("cricket stadium match crowd professional","sports"))
  elif any(x in l for x in ["cooking","kitchen","recipe","food","chef"]):kws.append(("cooking kitchen chef food restaurant","cooking"))
  elif any(x in l for x in ["motivation","success","mindset","inspiration"]):kws.append(("motivational speaker stage audience success","motivational"))
  elif any(x in l for x in ["story","kahani","moral","horror"]):kws.append(("storytelling book library cinematic","story"))
  elif any(x in l for x in ["tech","ai","robot","computer","mobile"]):kws.append(("technology AI robot future office","technology"))
  elif any(x in l for x in ["travel","beach","mountain","tour"]):kws.append(("travel nature beautiful drone","travel"))
  else:kws.append((s[:50]+" professional cinematic 4k","general"))
 return clean,kws
def Kw(text,cat):
 l=text.lower()
 SENS={"trump":"Donald Trump podium white house","biden":"Joe Biden white house","imran khan":"Imran Khan Pakistan jalsa crowd","nawaz":"Nawaz Sharif speech","modi":"Narendra Modi India parliament","parliament":"parliament government meeting debate","election":"voting election crowd","farmer":"farmer tractor agriculture field","tractor":"tractor ploughing field farming","farming":"farming agriculture tractor harvest","wheat":"wheat field harvesting farmer","finance":"finance money business office professional","crypto":"bitcoin crypto trading chart office","bitcoin":"bitcoin cryptocurrency trading","dollar":"dollar money finance office","islamic":"islamic mosque beautiful interior","quran":"quran reading mosque islamic","news":"news anchor studio breaking","cricket":"Pakistan cricket stadium match crowd","football":"football match stadium goal","doctor":"doctor hospital patient operation","hospital":"hospital doctor patient care","cooking":"chef cooking food kitchen","technology":"technology AI robot future office","ai":"artificial intelligence robot future","motivational":"motivational speaker success stage","story":"storytelling book library cinematic","travel":"travel airplane airport beautiful","car":"sports car driving highway"}
 for k in sorted(SENS.keys(),key=len,reverse=True):
  if k in l:return SENS[k]+f" {random.randint(1,99)}"
 w=[x for x in re.findall(r'\w+',l) if len(x)>4][:3]
 return " ".join(w)+" professional cinematic 4k" if w else "nature cinematic 4k"
def Ai(p,path,W=960,H=540):
 q=urllib.parse.quote(p[:200])
 try:
  r=requests.get(f"https://image.pollinations.ai/prompt/{q}?width={W}&height={H}&model=flux&nologo=true&seed={random.randint(1,9999)}",timeout=12)
  if r.status_code==200 and len(r.content)>3000:open(path,'wb').write(r.content);return path
 except:pass
 Image.new('RGB',(W,H),color=(20,20,20)).save(path);return path
def St(k,d,W,H,cat):
 if cat in ["finance","news","islamic","medical"]:k=k.replace("girl","").replace("bikini","").replace("sexy","")+" professional office"
 q=Kw(k,cat)
 for key in XK:
  try:
   r=requests.get(f"https://api.pexels.com/videos/search?query={urllib.parse.quote(q)}&per_page=3&page={random.randint(1,5)}",headers={"Authorization":key},timeout=6)
   j=r.json()
   if 'videos' in j and j['videos']:
    for vid in j['videos']:
     lk=vid['video_files'][0]['link']
     if lk in USED:continue
     USED.add(lk);t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4";open(t,'wb').write(requests.get(lk,timeout=8).content)
     if os.path.getsize(t)>4000:
      cl=VideoFileClip(t).resize((W,H));return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
  except:continue
 for pkey in ["45206122-5ac148b5cb7d59b24b24b24b","38754577-3b5a6c8a9d0e1f2a3b4c5d6e7f8a9b0c1d2"]:
  try:
   r=requests.get(f"https://pixabay.com/api/videos/?key={pkey}&q={urllib.parse.quote(q)}&per_page=3",timeout=7)
   j=r.json()
   if j.get('hits'):
    lk=j['hits'][0]['videos']['medium']['url'];t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4";open(t,'wb').write(requests.get(lk,timeout=8).content)
    if os.path.getsize(t)>4000:
     cl=VideoFileClip(t).resize((W,H));return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
  except:continue
 try:
  r=requests.get(f"https://archive.org/advancedsearch.php?q={urllib.parse.quote(q)}+mediatype:movies&fl=identifier&rows=2&output=json",timeout=6)
  j=r.json()
  for doc in j.get('response',{}).get('docs',[]):
   ident=doc['identifier']
   for ext in [".mp4","_512kb.mp4"]:
    try:
     lk=f"https://archive.org/download/{ident}/{ident}{ext}";t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4";open(t,'wb').write(requests.get(lk,timeout=8).content)
     if os.path.getsize(t)>10000:
      cl=VideoFileClip(t).resize((W,H));return cl.loop(duration=d) if cl.duration<d else cl.subclip(0,d)
    except:continue
 except:pass
 try:
  p=f"/tmp/{uuid.uuid4().hex[:4]}.jpg";Ai(q,p,W,H);return ImageClip(p).set_duration(d).resize((W,H))
 except:pass
 return ColorClip((W,H),color=(15,25,40),duration=d)
def MakeSEO(s):
 l=s.lower()
 if any(x in l for x in ["doctor","health"]):t="Health & Doctor Tips"
 elif any(x in l for x in ["finance","money","stock","business","crypto"]):t="Business & Finance"
 elif any(x in l for x in ["islamic","quran","masjid","islam"]):t="Islamic Knowledge"
 elif any(x in l for x in ["politics","election","parliament","news"]):t="Politics & News"
 elif any(x in l for x in ["farm","kisan","tractor","wheat","crop"]):t="Farming & Agriculture"
 elif any(x in l for x in ["cricket","football","sports","match"]):t="Sports Highlights"
 elif any(x in l for x in ["cooking","kitchen","recipe","food"]):t="Cooking & Food"
 elif any(x in l for x in ["motivational","success","mindset","inspiration"]):t="Motivational Speech"
 elif any(x in l for x in ["story","kahani","moral","horror"]):t="Moral Story"
 elif any(x in l for x in ["technology","ai","computer","mobile"]):t="Technology"
 elif any(x in l for x in ["travel","beach","mountain","tour"]):t="Travel Vlog"
 else:t="General"
 b=s[:70].strip().replace("\n"," ");title=f"{b} | {t} 2026"
 desc=f"{s[:500]}\n\nAbout {t}: {b} with complete details.\n\n📌 Topics: {b}, {t} Update 2026\n🔔 Subscribe for Daily {t} Videos\n📢 Disclaimer: Educational only. Stock videos from Pexels, Pixabay, Archive.org. YouTube compliant.\n"
 ht=f"#{t.replace(' ','').replace('&','')} #LatestUpdate #ViralVideo #{t.split()[0]}2026 #Trending"
 tags=f"{t}, {b}, Latest {t} 2026, Trending"
 return title[:95],desc,ht,tags
async def Tt(t,o,v):await edge_tts.Communicate(t,v).save(o)
def run_tts(tx,out,vc):
 try:
  loop=asyncio.new_event_loop();asyncio.set_event_loop(loop);loop.run_until_complete(Tt(tx,out,vc));loop.close()
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
   lic={"bound_email":email,"total":PACKAGES[code],"used":0.0,"expiry":str(today+datetime.timedelta(days=30))};db[code]=lic;Sj(LICENSE_DB,db)
  else:
   if lic["bound_email"]!=email:return None,None,"","","",f"LOCKED! {lic['bound_email']}"
   if today>datetime.date.fromisoformat(lic["expiry"]):return None,None,"","","",f"EXPIRED! {CONTACT}"
   if lic["used"]>=lic["total"]:return None,None,"","","",f"Khatam! {lic['used']:.1f}/{lic['total']}"
  rem=lic["total"]-lic["used"];free=False
 cs,kws=clean_analyze(script);title,desc,ht,vt=MakeSEO(cs);pvs=[]
 try:
  sents=[s.strip() for s in re.split(r'[.!?]+',cs) if s.strip()];chs=[];cur=""
  for s in sents:
   if len(cur)+len(s)<500:cur+=s+". "
   else:chs.append(cur);cur=s+". "
  if cur:chs.append(cur)
  if not chs:chs=[cs]
  chs=chs[:20];need=0.0;USED.clear()
  for idx,ch in enumerate(chs):
   ap=f"/tmp/{uuid.uuid4().hex[:5]}.mp3";run_tts(ch,ap,VOICES.get(lang,"en-US-GuyNeural"))
   if not os.path.exists(ap):continue
   au=AudioFileClip(ap)
   if not au or au.duration==0:continue
   nd=au.duration/60.0;need+=nd
   if need>rem+0.1:au.close();return None,None,"","","",f"Need {need:.1f}m Baki {rem:.1f}m"
   if need>22:au.close();break
   per_clip=4.5;num_clips=max(1,int(au.duration/per_clip)+1);clips=[]
   for i in range(num_clips):
    total_len=len(ch);start=int(i*total_len/num_clips);end=int((i+1)*total_len/num_clips)
    small_text=ch[start:end] if ch[start:end].strip() else ch[:40]
    kw_idx=min(idx,len(kws)-1);search_kw,cat_type=kws[kw_idx] if kws else (small_text,"general")
    clip_dur=per_clip if i<num_clips-1 else au.duration-(i*per_clip)
    if clip_dur<1:clip_dur=per_clip
    base_clip=St(search_kw,clip_dur,W,H,cat_type).set_duration(clip_dur)
    try:
     g1=TextClip("JSM",fontsize=int(W*0.07),color='#FFD700',font='Arial-Black',stroke_color='black',stroke_width=4).set_duration(clip_dur).set_position((W*0.82,H*0.03)).set_opacity(0.95)
     g2=TextClip("JSM",fontsize=int(W*0.07),color='#FF8C00',font='Arial-Black').set_duration(clip_dur).set_position((W*0.821,H*0.032)).set_opacity(0.5)
     base_clip=CompositeVideoClip([base_clip,g2,g1])
    except:pass
    if show_sub:
     try:
      txt=TextClip(small_text[:90],fontsize=int(W*0.035),color='yellow',stroke_color='black',stroke_width=2.5,method='caption',size=(W*0.88,None),font='Arial-Bold').set_duration(clip_dur).set_position(('center',0.78),relative=True)
      base_clip=CompositeVideoClip([base_clip,txt])
     except:
      try:
       txt2=TextClip(small_text[:90],fontsize=int(W*0.03),color='white',bg_color='black',method='caption',size=(W*0.85,None)).set_duration(clip_dur).set_position(('center',0.8),relative=True)
       base_clip=CompositeVideoClip([base_clip,txt2])
      except:pass
    clips.append(base_clip)
   fn=concatenate_videoclips(clips,method="compose").set_audio(au);vp=f"/tmp/P_{idx}_{uuid.uuid4().hex[:4]}.mp4"
   fn.write_videofile(vp,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',threads=8,bitrate="3000k",logger=None);pvs.append(VideoFileClip(vp));au.close()
  if not pvs:return None,None,"","","","No parts - Script chota likho"
  fv=concatenate_videoclips(pvs,method="compose");out="/tmp/gradio";os.makedirs(out,exist_ok=True)
  vf=f"{out}/FINAL_{uuid.uuid4().hex[:4]}.mp4";fv.write_videofile(vf,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',threads=8,bitrate="4000k",logger=None)
  tp=f"{out}/T_{uuid.uuid4().hex[:4]}.jpg";Ai(cs,tp,W,H)
  if free:ft[et]=ut+need;Sj(FREE_DB,ft);return vf,tp,title,desc,ht+vt,f"FREE {need:.1f}m {W}x{H} OK"
  else:db[code]["used"]+=need;Sj(LICENSE_DB,db);nr=db[code]["total"]-db[code]["used"];return vf,tp,title,desc,ht+vt,f"PAID Baki {nr:.1f}m {W}x{H}"
 except Exception as e:return None,None,"","","",f"Error:{str(e)[:180]}"
 finally:
  for c in pvs:
   try:c.close()
   except:pass
css="body{background:#000!important}#header{text-align:center;padding:10px 0;background:radial-gradient(circle at center,#1a1500 0%,#000 70%)!important;border-bottom:2px solid #FFD700}#header h1{color:#FFD700!important;font-size:38px!important;font-weight:900!important;text-shadow:0 0 15px #FFD700!important;margin:0!important}#contact{color:#D4AF37!important;font-size:11px!important;margin-top:4px}footer{display:none!important}button.primary{background:linear-gradient(90deg,#000,#FFD700,#000)!important;color:#FFD700!important;font-weight:900!important;height:60px!important;border-radius:14px!important;font-size:18px!important;border:2px solid #FFD700!important;box-shadow:0 0 15px #FFD700!important}.gr-input,.gr-dropdown,textarea{background:#0a0a0a!important;border:1px solid #FFD700!important;color:#FFD700!important}label{color:#FFD700!important;font-weight:800!important}.gr-box{background:#000!important}"
with gr.Blocks(title="JSM VIDEO GENERATOR",css=css) as demo:
 gr.HTML(f"""<div id="header"><h1>✦ JSM VIDEO GENERATOR ✦</h1><div id="contact">📞 {ON}: {ONUM} | Manager {MN}: {MNUM}</div></div>""")
 with gr.Tab("🎬 Video Generator"):
  with gr.Row():
   email=gr.Textbox(label="Email",placeholder="your@gmail.com");code=gr.Textbox(label="License Code",placeholder="ASIF786 for 600 min");lang=gr.Dropdown(list(VOICES.keys()),value="EN Motivational",label="🎙️ Voice 24 Natural")
  with gr.Row():
   vtype=gr.Dropdown(["YouTube 16:9","TikTok 9:16"],value="YouTube 16:9",label="Type");resolution=gr.Dropdown(["1920x1080 - Full HD","1280x720 - HD","854x480 - SD Fast"],value="1280x720 - HD",label="📺 HD");show_sub=gr.Checkbox(label="✅ Subtitles",value=True);cat_hidden=gr.Textbox(value="Auto",visible=False)
  script=gr.Textbox(lines=5,label="Your Script - 1000 Niches Auto Detect",placeholder="Topic likho - Doctor, Finance, Story, Motivational, Football, Cooking... AI khud samjhega!")
  btn=gr.Button("✨ GENERATE VIDEO ✨",variant="primary")
  with gr.Row():video=gr.Video(label="Final Video - HD Download");thumb=gr.Image(label="Thumbnail")
  with gr.Row():t1=gr.Textbox(label="Title (Auto SEO - No JSM)");d1=gr.Textbox(lines=4,label="Description (Professional)");h1=gr.Textbox(lines=2,label="Hashtags + Tags")
  status=gr.Textbox(label="Status");btn.click(Gen,[email,code,script,lang,vtype,resolution,show_sub,cat_hidden],[video,thumb,t1,d1,h1,status])
 with gr.Tab("🔐 Admin"):
  gr.Markdown("### 🔑 Owner Access Only");admin_pass=gr.Textbox(label="Owner Key",type="password",placeholder="••••••••")
  with gr.Row():user_email=gr.Textbox(label="User Email",placeholder="asif@gmail.com");mins=gr.Dropdown([30,100,300,500,600,1000],value=500,label="Minutes");bulk_count=gr.Number(label="Bulk Count",value=1,precision=0)
  gen_btn=gr.Button("🔑 Generate Code",variant="primary");out_msg=gr.Textbox(label="Message");out_code=gr.Textbox(lines=6,label="Codes - Copy Karo");view_btn=gr.Button("📋 Saare Codes Dekho");view_out=gr.Textbox(lines=12,label="All Licenses")
  gen_btn.click(AdminGen,[admin_pass,user_email,mins,bulk_count],[out_msg,out_code,view_out]);view_btn.click(AdminView,[admin_pass],[view_out])
demo.queue(max_size=20).launch(share=True,server_name="0.0.0.0")
