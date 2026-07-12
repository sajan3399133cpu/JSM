# JSM ULTIMATE - FINAL - NO VERSION CONFLICT - 100% WORKING
import gradio as gr, asyncio, edge_tts, uuid, random, requests, re, os, json, datetime, urllib.parse
from moviepy.editor import VideoFileClip, ColorClip, concatenate_videoclips, AudioFileClip, ImageClip
from PIL import Image
print("✅ Ready")

PEXELS=["ROKJvfYuuSkc7QVVL6VjCgYFyB8UQZCLLCctD2SfTJcIrDGo5Ex3JMX6","zniYyavhal66VGwuV2kUlpRm7vG3Y0rddDLuzrITvmPqQ26kdG0vcyy0"]
BRAND="JSM AI BY JAM SAEED MOTHA"; CONTACT="03043399133"
CATS=["Business & Finance","Crypto & Trading","Islamic & Quran","News & Breaking","Sports & Cricket","Technology & AI","Health & Fitness","Food & Cooking","Travel & Nature","Education & Facts","Motivation & Success","Real Estate","Cars & Bikes","Cartoon & Kids","Farming & Agriculture","Politics & Trump","USA News","Pakistan News","Science & Space","History & Documentary","Lifestyle & Fashion","Music & Entertainment","Gaming & Esports","Animals & Wildlife","Luxury & Lifestyle","Stock Market","YouTube Viral","TikTok Trending","Podcast & Talk","Cinema & Movie"]
VOICES={"English Male":"en-US-GuyNeural","English Female":"en-US-JennyNeural","Urdu Male":"ur-PK-AsadNeural","Urdu Female":"ur-PK-UzmaNeural","Arabic Male":"ar-SA-HamedNeural","Arabic Female":"ar-SA-ZariyahNeural","Hindi Male":"hi-IN-MadhurNeural","Hindi Female":"hi-IN-SwaraNeural","British Male":"en-GB-RyanNeural","British Female":"en-GB-SoniaNeural","Spanish Male":"es-ES-AlvaroNeural","Spanish Female":"es-ES-ElviraNeural","French Male":"fr-FR-HenriNeural","German Female":"de-DE-KatjaNeural","Turkish Male":"tr-TR-AhmetNeural"}

def get_ai(p,path,W=1280,H=720):
    s=urllib.parse.quote(p[:60])
    try:
        r=requests.get(f"https://image.pollinations.ai/prompt/{s}?width={W}&height={H}&model=flux&nologo=true&seed={random.randint(1,9999)}",timeout=15)
        if r.status_code==200 and len(r.content)>5000: open(path,'wb').write(r.content); return path
    except: pass
    Image.new('RGB',(W,H),color=(15,23,42)).save(path); return path

def get_stock(k,d):
    q=k[:12]+" business"
    for key in PEXELS:
        try:
            r=requests.get(f"https://api.pexels.com/videos/search?query={q}&per_page=1",headers={"Authorization":key},timeout=5).json()
            link=r['videos'][0]['video_files'][0]['link']; tmp=f"/tmp/{uuid.uuid4().hex[:4]}.mp4"; open(tmp,'wb').write(requests.get(link,timeout=5).content)
            return VideoFileClip(tmp).resize((1280,720)).subclip(0,min(d,5))
        except: continue
    return ColorClip((1280,720),color=(20,40,80),duration=d)

async def tts(t,o,v): await edge_tts.Communicate(t,v).save(o)

def create(email,code,script,lang,cat,vtype):
    if not script.strip(): return None,None,"","","","Script likho"
    W,H=(720,1280) if "TikTok" in vtype else (1280,720)
    title=f"{script[:60]} | {cat}"; desc=f"{script[:400]}\n\n{BRAND}"; dis="AI & Stock free license"; htag=f"#{cat.replace(' ','')} #JSM"; tags=cat
    if code.strip().upper() in {"ASIF786","ALI786","JSM100","JSM500","JSM786"}:
        uid=uuid.uuid4().hex[:4]; ap=f"/tmp/{uid}.mp3"; vp=f"/tmp/P_{uid}.mp4"; tp=f"/tmp/T_{uid}.jpg"
        asyncio.run(tts(script,ap,VOICES.get(lang,"en-US-GuyNeural"))); audio=AudioFileClip(ap)
        sents=[s.strip() for s in re.split(r'[.!?]',script) if s.strip()][:5]; per=audio.duration/max(len(sents),1)
        clips=[get_stock(s,per).set_duration(per) for s in sents]
        final=concatenate_videoclips(clips,method="compose").set_audio(audio)
        final.write_videofile(vp,fps=24,codec='libx264',audio_codec='aac',logger=None)
        get_ai(script+" thumbnail",tp,1280,720)
        return vp,tp,title,desc,htag,f"PAID Done {audio.duration:.1f}s"
    uid=uuid.uuid4().hex[:4]; ap=f"/tmp/{uid}.mp3"; vp=f"/tmp/F_{uid}.mp4"; tp=f"/tmp/T_{uid}.jpg"
    asyncio.run(tts(script[:80],ap,VOICES.get(lang,"en-US-GuyNeural"))); audio=AudioFileClip(ap).subclip(0,8)
    img=f"/tmp/I_{uid}.jpg"; get_ai(script[:40]+" "+cat,img,W,H)
    base=ImageClip(img,duration=8).resize((W,H)).set_audio(audio)
    base.write_videofile(vp,fps=24,codec='libx264',audio_codec='aac',logger=None)
    get_ai(script+" thumbnail",tp,1280,720)
    return vp,tp,title,desc,htag,f"FREE Done"

with gr.Blocks(title=BRAND) as demo:
    gr.Markdown(f"# {BRAND} | 30 Cat | 15 Lang | {CONTACT}")
    with gr.Row():
        email=gr.Textbox(label="Email"); code=gr.Textbox(label="Code"); lang=gr.Dropdown(list(VOICES.keys()),value="English Male",label="Language")
    with gr.Row():
        cat=gr.Dropdown(CATS,value="Business & Finance",label="Category"); vtype=gr.Dropdown(["YouTube 16:9","TikTok 9:16"],value="YouTube 16:9",label="Type")
    script=gr.Textbox(lines=4,label="Script", placeholder="Sone ka anda asman se gir raha hai...")
    btn=gr.Button("🚀 GENERATE VIDEO",variant="primary")
    with gr.Row(): video=gr.Video(label="Video"); thumb=gr.Image(label="Thumbnail")
    title_out=gr.Textbox(label="Title"); desc_out=gr.Textbox(label="Description"); htag_out=gr.Textbox(label="Hashtags"); status=gr.Textbox(label="Status")
    btn.click(create,[email,code,script,lang,cat,vtype],[video,thumb,title_out,desc_out,htag_out,status])

demo.launch(share=True)
