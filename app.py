# JSM VIDEO GENERATOR - FINAL ERROR FREE - 16 LANG + 30 CAT + 6 PLATFORMS + 540p 20MIN
import gradio as gr,asyncio,edge_tts,uuid,random,requests,re,os,json,base64,urllib.parse,datetime
from moviepy.editor import VideoFileClip,ColorClip,concatenate_videoclips,AudioFileClip
from PIL import Image

B="JSM VIDEO GENERATOR";CONTACT="03043399133"
K1="c2JfcHVibGlzaGFibGVfMVc0Tks2WDdFZGFjbV9lU0JJY0ZEUV9Da1Q2YzRFWQ=="
K2="NTYzODYyOTMtMTRmYWNkOTRmZGFjMjZmOWZjMzdmNWYyYw=="
K3="OGM4YzU5MmIwN2E1N2UwNWRjNDkzNjhiMzk5Yjc2NTk="
K4=['Uk9LSnZmWXV1U2tjN1FWVkw2VmpDZ1lGeUI4VVFaQ0xMQ2N0RDJTZlRKY2xJckRHbzVFeDNKTVg2','em5pWXZhdmhhbDY2Vkd3dVYya1VJcFJtN3ZHM1kwcmRkREx1enJJVHZtUHFRMjZrZEcwdmN5eTA=','ZjZJS3hySFI4TUhqMWdlRDYyY3JMVGZEVFFYMHM3ZXdGa3czaEVJNGQ0Q2VuUlRaWENrcENXRDk=','MWo2a0ZxMUdSQjQyOTFGMXMxUk1naGxnSVgzZDN1NzhPYVRwaURLbXRJU0FqSmtLUGI5dlZUa0w=','dHBreXBvZ3N3djA3bjg0ZGgwaWFISTl0YW11NDNHRWN2Wm9rQTNYaTNKU1RVVDBOVjMyQTZnRzk=']
def D(e):
 try:return base64.b64decode(e.encode()).decode()
 except:return ""
PK=D(K2);XK=[D(k) for k in K4]

VOICES={
"English Male":"en-US-GuyNeural","English Female":"en-US-JennyNeural",
"Urdu Male":"ur-PK-AsadNeural","Urdu Female":"ur-PK-UzmaNeural",
"Hindi Male":"hi-IN-MadhurNeural","Hindi Female":"hi-IN-SwaraNeural",
"Arabic Male":"ar-SA-HamedNeural","Arabic Female":"ar-SA-ZariyahNeural",
"Spanish Male":"es-ES-AlvaroNeural","Spanish Female":"es-ES-ElviraNeural",
"French Male":"fr-FR-HenriNeural","French Female":"fr-FR-DeniseNeural",
"German Male":"de-DE-ConradNeural","German Female":"de-DE-KatjaNeural",
"Turkish Male":"tr-TR-AhmetNeural","Turkish Female":"tr-TR-EmelNeural"
}
CATS=["Business & Finance","Crypto & Trading","Islamic & Quran","News & Breaking","Sports & Cricket","Technology & AI","Health & Doctor","Farming Kisan","Kitchen Cooking","Trending Viral","Politics Trump","Education","Motivation","Real Estate","Gold & Silver","Cars & Bikes","Pets & Animals","Beauty & Fashion","Travel","Food Vlog","Fitness","History","Science","Comedy","Music","Kids","Army & Police","Weather","Property","Jobs"]
PACKAGES={"ASIF":100,"ALI":100,"JSM":100,"ASIF786":600,"JSM30":30,"JSM100":100,"JSM300":300,"JSM500":500,"JSM786":600,"JSM600":600,"JSMGOLD":1000,"JSM786GOLD":9999}
FREE_DB="/tmp/free_daily.json";LICENSE_DB="/tmp/jsm_licenses_final.json"

def Lj(p):
 try:
  if os.path.exists(p):return json.load(open(p))
 except:pass
 return{}
def Sj(p,d):
 try:json.dump(d,open(p,'w'))
 except:pass

def Kw(text, category):
 l=text.lower(); cat=(category or "").lower()
 if "trump" in l: return "Donald Trump president speech white house news"
 if "biden" in l: return "Joe Biden president white house speech"
 if "imran" in l: return "Pakistan parliament politics Imran Khan news"
 if "news" in cat or "breaking" in cat: return "news studio anchor professional breaking news"
 if "business" in cat or "finance" in cat or "crypto" in cat: return "finance stock market business trading office"
 if "farming" in cat or "kisan" in l: return "farmer agriculture tractor field working"
 if "kitchen" in cat: return "cooking kitchen chef food professional"
 if "doctor" in cat or "health" in cat: return "doctor hospital medical professional"
 if "cricket" in l or "sports" in cat: return "cricket stadium sports match"
 if "islamic" in cat: return "islamic mosque beautiful"
 if "technology" in cat: return "technology AI computer office"
 m={"tractor":"tractor farming","khet":"farm field","biryani":"cooking kitchen"}
 for k,v in m.items():
  if k in l:return v
 st={"hai","ka","ki","ke","ko","me","ne","aur","ye","wo","to","se","par","bhi","ek","wala","raha","is","the","and","in","on"}
 w=re.findall(r'\w+',l);k=[x for x in w if x not in st and len(x)>2]
 clean=" ".join(k[:3]) if k else l[:25]
 return clean + " professional safe"

def Ai(p,path,W=960,H=540):
 q=urllib.parse.quote(p[:600])
 try:
  r=requests.get(f"https://image.pollinations.ai/prompt/{q} safe?width={W}&height={H}&model=flux&nologo=true&seed={random.randint(1,999999)}",timeout=20)
  if r.status_code==200 and len(r.content)>5000:open(path,'wb').write(r.content);return path
 except:pass
 Image.new('RGB',(W,H),color=(15,23,42)).save(path);return path

def St(k,d,W,H,cat):
 q=Kw(k,cat)
 for key in XK:
  try:
   r=requests.get(f"https://api.pexels.com/videos/search?query={q}&per_page=2",headers={"Authorization":key},timeout=8)
   j=r.json()
   if 'videos' in j and j['videos']:
    vids=j['videos'][0]['video_files']
    # 540p ke liye 640w ya 960w wala lo
    link=next((v['link'] for v in vids if v['width']>=640 and v['width']<=1280), vids[0]['link'])
    t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4";open(t,'wb').write(requests.get(link,timeout=10).content)
    clip=VideoFileClip(t).resize((W,H))
    return clip.loop(duration=d) if clip.duration<d else clip.subclip(0,d)
  except:continue
 try:
  if PK:
   r=requests.get(f"https://pixabay.com/api/videos/?key={PK}&q={q}&per_page=3&safesearch=true",timeout=8)
   hits=r.json().get('hits',[])
   if hits:
    ln=hits[0]['videos']['tiny']['url'] if 'tiny' in hits[0]['videos'] else hits[0]['videos']['medium']['url']
    t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4";open(t,'wb').write(requests.get(ln,timeout=10).content)
    clip=VideoFileClip(t).resize((W,H))
    return clip.loop(duration=d) if clip.duration<d else clip.subclip(0,d)
 except:pass
 try:
  r=requests.get(f"https://api.pexels.com/videos/popular?per_page=2",headers={"Authorization":XK[0]},timeout=8)
  j=r.json()
  if 'videos' in j and j['videos']:
   link=j['videos'][0]['video_files'][0]['link']
   t=f"/tmp/{uuid.uuid4().hex[:4]}.mp4";open(t,'wb').write(requests.get(link,timeout=8).content)
   clip=VideoFileClip(t).resize((W,H))
   return clip.loop(duration=d) if clip.duration<d else clip.subclip(0,d)
 except:pass
 return ColorClip((W,H),color=(20,40,80),duration=d)

async def Tt(t,o,v):await edge_tts.Communicate(t,v).save(o)

def run_tts(text, out, voice):
 try:
  loop=asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  loop.run_until_complete(Tt(text,out,voice))
  loop.close()
 except:pass

def Gen(email,code,script,lang,cat,vtype):
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
   lic={"bound_email":email,"total":PACKAGES[code],"used":0.0,"expiry":str(today+datetime.timedelta(days=30)),"created":str(today)}
   lic_db[code]=lic;Sj(LICENSE_DB,lic_db)
  else:
   if lic["bound_email"]!=email:return None,None,"","","",f"LOCKED! {lic['bound_email']} se bandha hai!"
   if today>datetime.date.fromisoformat(lic["expiry"]):return None,None,"","","",f"EXPIRED {lic['expiry']} Renew {CONTACT}"
   if lic["used"]>=lic["total"]:return None,None,"","","",f"Khatam {lic['used']:.1f}/{lic['total']}m"
  rem=lic["total"]-lic["used"];free=False
 title=f"{script[:60]}";desc=f"{script[:400]}\n\nJSM VIDEO GENERATOR";ht="#JSM"
 pvs=[]
 try:
  sents=[s.strip() for s in re.split(r'[.!?۔]+',script) if s.strip()];chs=[];cur=""
  for s in sents:
   if len(cur)+len(s)<550:cur+=s+". "
   else:chs.append(cur);cur=s+". "
  if cur:chs.append(cur)
  if not chs:chs=[script]
  chs=chs[:25];needT=0.0
  for idx,ch in enumerate(chs):
   ap=f"/tmp/{uuid.uuid4().hex[:5]}.mp3"
   run_tts(ch,ap,VOICES.get(lang,"en-US-GuyNeural"))
   if not os.path.exists(ap):continue
   au=AudioFileClip(ap)
   if not au or au.duration==0:continue
   nd=au.duration/60.0;needT+=nd
   if needT>rem+0.1:
    au.close()
    return None,None,"","","",f"Need {needT:.1f}m Baki {rem:.1f}m - Script chhota karo"
   if needT>22:
    au.close()
    break
   inn=[s.strip() for s in re.split(r'[.!?]+',ch) if s.strip()][:2]
   if not inn:inn=[ch[:30]]
   per=au.duration/max(len(inn),1)
   clips=[]
   for s in inn:
    cl=St(s,per,W,H,cat).set_duration(per)
    clips.append(cl)
   fn=concatenate_videoclips(clips,method="compose").set_audio(au)
   vp=f"/tmp/P_{idx}_{uuid.uuid4().hex[:4]}.mp4"
   fn.write_videofile(vp,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',bitrate='800k',logger=None)
   pvs.append(VideoFileClip(vp))
   au.close()
  if not pvs:return None,None,"","","","No parts - Script badlo"
  fv=concatenate_videoclips(pvs,method="compose");vf=f"/tmp/FINAL_{uuid.uuid4().hex[:5]}.mp4"
  fv.write_videofile(vf,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',bitrate='800k',logger=None)
  tp=f"/tmp/T_{uuid.uuid4().hex[:4]}.jpg";Ai(script,tp,W,H)
  if free:
   ft[et]=ut+needT;Sj(FREE_DB,ft)
   return vf,tp,title,desc,ht,f"FREE {needT:.1f}m Used {ft[et]:.1f}/1.0 540p SAFE OK"
  else:
   lic_db[code]["used"]+=needT;Sj(LICENSE_DB,lic_db)
   nr=lic_db[code]["total"]-lic_db[code]["used"]
   return vf,tp,title,desc,ht,f"PAID {code} Cut {needT:.1f}m Baki {nr:.1f}/{lic_db[code]['total']}m Exp {lic_db[code]['expiry']} 540p SAFE OK"
 except Exception as e:
  return None,None,"","","",f"Error:{e}"
 finally:
  for c in pvs:
   try:c.close()
   except:pass

with gr.Blocks(title="JSM VIDEO GENERATOR") as demo:
 gr.Markdown(f"# JSM AI BY JAM SAEED MOTHA | 30 Cat | 16 Lang | {CONTACT} | 540p LONG 20MIN | 6 PLATFORMS SAFE")
 with gr.Row():
  email=gr.Textbox(label="Email");code=gr.Textbox(label="Code ASIF/ALI/JSM=100min JSM786=600min");lang=gr.Dropdown(list(VOICES.keys()),value="English Male",label="Language - 16")
 with gr.Row():
  cat=gr.Dropdown(CATS,value="Business & Finance",label="Category - 30 Cats");vtype=gr.Dropdown(["YouTube 16:9","TikTok 9:16"],value="YouTube 16:9",label="Type 540p")
 script=gr.Textbox(lines=6,label="Script - 20 MIN TAK",placeholder="20 min kahani likho...")
 btn=gr.Button("GENERATE VIDEO - 20 MIN 540p",variant="primary")
 with gr.Row():
  video=gr.Video(label="Final Video 540p");thumb=gr.Image(label="Thumbnail")
 with gr.Row():
  t1=gr.Textbox(label="Title");d1=gr.Textbox(label="Description");h1=gr.Textbox(label="Hashtags")
 status=gr.Textbox(label="Status - Baki Minutes + Expiry + Lock")
 btn.click(Gen,[email,code,script,lang,cat,vtype],[video,thumb,t1,d1,h1,status])
demo.queue(max_size=50).launch(share=True,server_name="0.0.0.0",show_api=False)
