import asyncio, uuid, random, requests, re, os, urllib.parse, datetime, time, json, gc, base64
import nest_asyncio
nest_asyncio.apply()
from moviepy.editor import VideoFileClip, ColorClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip, TextClip, CompositeAudioClip, ImageClip
from moviepy.audio.fx.volumex import volumex
import edge_tts, gradio as gr
from PIL import Image

# --- CONFIG ---
BASE_DIR = "./JSM_Outputs"
os.makedirs(BASE_DIR, exist_ok=True)
SHEET_ID = "1nD6trNVFzhBAPwGiGYn8lzN5yAXVY5lIe05DvAjP5kU"
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyfopJoiGBueO6AsZ5JE-juplXjSa1Lc_klKn4bOswLyhPmPGsvOhT9r6Axow6rsl-rXg/exec"
PIXABAY_KEY = "56386293-14facd94fdac26f9fc37f5f2c"
PEXELS_KEYS = ["ROKJvfYuuSkc7QVVL6VjCgYFyB8UQZCLLCctD2SfTJcIrDGo5Ex3JMX6","zniYyavhal66VGwuV2kUIpRm7vG3Y0rddDLuzrITvmPqQ26kdG0vcyy0","f6IKxrHR8MHj1geD62crLTfDTQX0s7ewFkw3hEI4d4CenRTZXCkpCWD9","1j6kFq1GRB4291F1s1RMghlgIX3d3u78OaTpiDKmtlSAjJkKPb9vVTkL","tpkypogswv07n84dh0iaHI9tamu43GEcvZokA3XiJSTUT0NV32A6gG9"]
COVERR_API_KEY = "8c8c592b07a57e05dc49368c399b7659"
BRAND_NAME = "JSM AI BY JAM SAEED MOTHA"

VOICES = {
    "English Male (Andrew - Professional Studio)": "en-US-AndrewNeural",
    "English Male (Christopher - Deep Motivational)": "en-US-ChristopherNeural",
    "English Male (Guy - News Anchor)": "en-US-GuyNeural",
    "English Male (Ryan - UK Storyteller)": "en-GB-RyanNeural",
    "English Female (Jenny - Clear & Energetic)": "en-US-JennyNeural",
    "English Female (Aria - Natural Human)": "en-US-AriaNeural",
    "Urdu Male (Asad - Deep Voice)": "ur-PK-AsadNeural",
    "Urdu Female (Uzma)": "ur-PK-UzmaNeural",
    "Hindi Male (Madhur - Deep)": "hi-IN-MadhurNeural",
    "Hindi Female (Swara - Dynamic)": "hi-IN-SwaraNeural",
    "Arabic Male (Hamdan)": "ar-SA-HamdanNeural",
    "Russian Female (Svetlana)": "ru-RU-SvetlanaNeural",
    "Urdu-Hindi Mix (Auto Detect)": "AUTO"
}

CATEGORIES_MAP = {
    "motivational": ["motivation","success","hard work","rich people","winner","dream big","goal","trophy"],
    "finance_stock": ["stock market","stock","trading","share market","trader","forex","crypto","bitcoin"],
    "finance_money": ["money","wealth","dollars","cash","finance","bank","profit","investing"],
    "business": ["business","corporate","office","meeting","boss","startup","entrepreneur"],
    "news": ["breaking news","journalism","reporter","studio news","media","election","politics"],
    "fitness": ["gym","workout","fitness","bodybuilding","exercise","yoga","athlete"],
    "ai_tech": ["ai","artificial intelligence","robot","technology","future","chatgpt","coding"],
    "medical": ["doctor","hospital","patient","medical","health","surgery","medicine"],
    "food": ["cooking","chef","food","kitchen","restaurant","recipe","biryani"],
    "travel": ["travel","tourism","airplane","beach","mountains","vacation","hotel"],
    "education": ["student","school","university","book","learning","teacher","degrees","skills"],
    "nature": ["forest","river","ocean","landscape","sunset","wildlife","village"],
    "islamic": ["islamic","masjid","mosque","madina","makkah","kaaba","quran","allah"],
}

def cut_mints_auto(email, mins):
    try:
        if not email or mins<=0: return
        url = f"{WEB_APP_URL}?email={urllib.parse.quote(email)}&mins={mins}"
        requests.get(url, timeout=15)
        print(f"✅ Mints Cut: {mins} for {email}")
    except: pass

def SMART_KEYWORD_ENGINE(sentence):
    s_low = sentence.lower()
    blacklist = " -news -reporter -camera -microphone -journalist -interview"
    best_score=0; matched=[]; selected_cat=""
    for cat, kws in CATEGORIES_MAP.items():
        score=sum(1 for kw in kws if kw in s_low)
        if score>best_score:
            best_score=score
            matched=[kw for kw in kws if kw in s_low]
            selected_cat=cat
    if best_score>0 and matched:
        primary=matched[0]
        secondary=matched[1] if len(matched)>1 else selected_cat
        return [f"{primary} {secondary}{blacklist}", f"{primary}{blacklist}", f"{selected_cat} cinematic{blacklist}"]
    clean=re.sub(r'[^\w\s]','',s_low)
    stop_words={"about","today","video","talk","please","subscribe","channel","the","and","you","hai","ke","ki","ka","aur","mein","aaj"}
    words=[w for w in clean.split() if w not in stop_words and len(w)>3][:5]
    if words:
        return [f"{' '.join(words[:2])}{blacklist}", f"{words[0]} cinematic{blacklist}"]
    return [f"cinematic background{blacklist}"]

def clean_analyze(script):
    clean=re.sub(r"(sex\s*video|porn|xxx|nude|naked)"," ",script,flags=re.I)
    raw=re.split(r'[.!?\n\u06d4]+',clean)
    sens=[s.strip() for s in raw if len(s.strip())>8]
    return clean, sens

# FREE AI GENERATOR - 100% FREE
def Ai_Free_Generator(prompt, path, W=960, H=540):
    q=urllib.parse.quote(prompt[:120])
    seed=random.randint(1,999999)
    for model in ["flux","turbo"]:
        try:
            url=f"https://image.pollinations.ai/prompt/{q}?width={W}&height={H}&model={model}&nologo=true&seed={seed}&enhance=true"
            r=requests.get(url,timeout=20)
            if r.status_code==200 and len(r.content)>5000:
                open(path,'wb').write(r.content)
                return path
        except: continue
    Image.new('RGB',(W,H),color=(15,18,24)).save(path)
    return path

def download_clip(url, W, H, duration):
    try:
        t_path=f"{BASE_DIR}/{uuid.uuid4().hex[:6]}.mp4"
        res=requests.get(url,headers={"User-Agent":"Mozilla/5.0"},timeout=15)
        with open(t_path,'wb') as f: f.write(res.content)
        clip=VideoFileClip(t_path).resize((W,H))
        clip=clip.resize(lambda t: 1+0.015*t)
        return clip.loop(duration=duration) if clip.duration<duration else clip.subclip(0,duration)
    except: return None

def get_clip_from_platforms(smart_queries, duration, W, H, clip_index, mode):
    # PURE AI MODE
    if "Pure AI" in mode:
        p=f"{BASE_DIR}/{uuid.uuid4().hex[:4]}.jpg"
        Ai_Free_Generator(smart_queries[0], p, W, H)
        clip=ImageClip(p).set_duration(duration).resize((W,H))
        return clip.resize(lambda t: 1+0.05*t)

    # SMART STOCK + AI FALLBACK MODE
    orientation='portrait' if H>W else 'landscape'
    for q in smart_queries:
        q_enc=urllib.parse.quote(q)
        # PEXELS
        for key in PEXELS_KEYS:
            try:
                r=requests.get(f"https://api.pexels.com/videos/search?query={q_enc}&per_page=8&orientation={orientation}",headers={"Authorization":key},timeout=8).json()
                if r.get('videos'):
                    v=r['videos'][clip_index % len(r['videos'])]
                    link=v['video_files'][0]['link']
                    cl=download_clip(link,W,H,duration)
                    if cl:
                        print(f"✅ PEXELS: {q}")
                        return cl
            except: continue
        # PIXABAY
        try:
            r=requests.get(f"https://pixabay.com/api/videos/?key={PIXABAY_KEY}&q={q_enc}&per_page=8",timeout=8).json()
            if r.get('hits'):
                link=r['hits'][clip_index % len(r['hits'])]['videos']['medium']['url']
                cl=download_clip(link,W,H,duration)
                if cl:
                    print(f"✅ PIXABAY: {q}")
                    return cl
        except: pass

    # FINAL FALLBACK - AI IMAGE (NO BLACK SCREEN)
    print(f"⚠️ Stock nahi mila, AI bana raha: {smart_queries[0]}")
    p=f"{BASE_DIR}/{uuid.uuid4().hex[:4]}.jpg"
    Ai_Free_Generator(smart_queries[0], p, W, H)
    clip=ImageClip(p).set_duration(duration).resize((W,H))
    return clip.resize(lambda t: 1+0.04*t)

def get_niche_music(text):
    l=text.lower()
    q="corporate" if any(x in l for x in ["stock","finance","money","business"]) else "inspiring" if "motivation" in l else "ambient"
    try:
        r=requests.get(f"https://pixabay.com/api/music/?key={PIXABAY_KEY}&q={urllib.parse.quote(q)}&per_page=10",timeout=8).json()
        if r.get('hits'):
            track=random.choice(r['hits'])
            mp3_url=track.get('download_url') or track.get('audio')
            if mp3_url:
                mp=f"{BASE_DIR}/bgm_{uuid.uuid4().hex[:4]}.mp3"
                res=requests.get(mp3_url,timeout=12)
                open(mp,'wb').write(res.content)
                return mp
    except: pass
    return None

async def Tt(t,o,v):
    rate="-5%" if "ru-RU" in v else "-4%"
    pitch="+2Hz"
    await edge_tts.Communicate(t,v,rate=rate,pitch=pitch).save(o)

def run_tts(tx,out,vc):
    if len(tx.split())<3: tx=tx+"۔"
    for _ in range(2):
        try:
            try: asyncio.run(Tt(tx,out,vc))
            except:
                loop=asyncio.new_event_loop(); asyncio.set_event_loop(loop); loop.run_until_complete(Tt(tx,out,vc))
            if os.path.exists(out) and os.path.getsize(out)>800: return True
        except: time.sleep(0.5)
    return False

def detect_voice(ch, selected):
    if "AUTO" in selected:
        return VOICES["English Male (Guy - News Anchor)"] if any(w in ch.lower() for w in ["breaking news","stock market","finance"]) else VOICES["Urdu Male (Asad - Deep Voice)"]
    return VOICES.get(selected, "ur-PK-AsadNeural")

def GenAll(email, script, voice_lang, video_type, resolution, show_subtitles, video_mode):
    if not script.strip(): return None, "Script likho"
    cs, kws = clean_analyze(script)
    W,H = (1280,720) if "16:9" in video_type else (720,1280)
    if "480" in resolution: W,H = (854,480) if W>H else (480,854)
    if "1080" in resolution: W,H = (1920,1080) if W>H else (1080,1920)
    bgm_path = get_niche_music(script)
    scene_files=[]
    print(f"🎬 Total Scenes: {len(kws)} Mode: {video_mode}")

    for idx, ch in enumerate(kws):
        voice_code=detect_voice(ch, voice_lang)
        ap=f"{BASE_DIR}/{uuid.uuid4().hex[:5]}.mp3"
        ok=run_tts(ch, ap, voice_code)
        if not ok: continue
        au=AudioFileClip(ap)
        if au.duration>0.4: au=au.subclip(0, au.duration-0.1)
        smart_queries=SMART_KEYWORD_ENGINE(ch)
        dur_left=au.duration; sub_clips=[]; counter=idx
        while dur_left>0:
            cur_dur=min(random.uniform(3.2,4.5), dur_left)
            sc=get_clip_from_platforms(smart_queries, cur_dur, W, H, counter, video_mode)
            sub_clips.append(sc)
            dur_left-=cur_dur; counter+=1
        base_clip=concatenate_videoclips(sub_clips,method="compose") if len(sub_clips)>1 else sub_clips[0]
        base_clip=base_clip.set_duration(au.duration)
        if bgm_path and os.path.exists(bgm_path):
            try:
                bgm=AudioFileClip(bgm_path).subclip(0,au.duration).fx(volumex,0.25)
                base_clip=base_clip.set_audio(CompositeAudioClip([au,bgm]))
            except: base_clip=base_clip.set_audio(au)
        else: base_clip=base_clip.set_audio(au)
        layers=[base_clip]
        if show_subtitles:
            try:
                txt=TextClip(ch[:100],fontsize=int(W*0.038),color='white',stroke_color='black',stroke_width=2,method='caption',size=(int(W*0.85),None),align='center')
                txt=txt.set_duration(au.duration).set_pos(('center',0.80),relative=True)
                layers.append(txt)
            except: pass
        final_scene=CompositeVideoClip(layers)
        temp_path=f"{BASE_DIR}/scene_{idx}_{uuid.uuid4().hex[:4]}.mp4"
        final_scene.write_videofile(temp_path,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',threads=1,bitrate="1000k",logger=None)
        scene_files.append(temp_path)
        for sc in sub_clips:
            try: sc.close()
            except: pass
        try: base_clip.close(); final_scene.close(); au.close()
        except: pass
        gc.collect()

    if not scene_files: return None, "Fail"
    list_path=f"{BASE_DIR}/concat_list.txt"
    with open(list_path,"w") as f:
        for sf in scene_files: f.write(f"file '{os.path.abspath(sf)}'\n")
    timestamp=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path=f"{BASE_DIR}/JSM_Video_{timestamp}.mp4"
    os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c copy {out_path}")
    if not os.path.exists(out_path) or os.path.getsize(out_path)<1000:
        os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c:v libx264 -preset ultrafast -c:a aac {out_path}")
    try:
        final_clip=VideoFileClip(out_path)
        final_mins=round(final_clip.duration/60,2)
        final_clip.close()
        cut_mints_auto(email, final_mins)
    except: pass
    return out_path, f"✅ Done! {len(scene_files)} scenes | Mode: {video_mode}"

css="body{background:#000!important} #header{text-align:center;padding:15px;background:radial-gradient(ellipse at center,#2a2000 0%,#000 70%)!important;border-bottom:3px solid #FFD700!important} #header h1{color:#FFD700!important;font-size:38px!important;font-weight:900!important} button.primary{background:linear-gradient(90deg,#000,#FFD700,#000)!important;color:#000!important;font-weight:900!important;height:60px!important;border-radius:12px!important}"
with gr.Blocks(title="JSM V7 FINAL", css=css) as demo:
    gr.HTML(f"<div id='header'><h1>✦ JSM V7 DUAL MODE - FINAL ✦</h1><div>📞 JAM SAEED MOTHA | {BRAND_NAME}</div></div>")
    with gr.Row():
        email=gr.Textbox(label="Email (for mint cut)", value="areej3399133@gmail.com")
        voice_lang=gr.Dropdown(list(VOICES.keys()), value="Urdu Male (Asad - Deep Voice)", label="Voice (22 Voices)")
    with gr.Row():
        video_type=gr.Dropdown(["YouTube 16:9","TikTok 9:16"], value="YouTube 16:9", label="Type")
        resolution=gr.Dropdown(["1280x720 - HD","1920x1080 - Full HD","854x480 - SD Fast"], value="1280x720 - HD", label="Resolution")
        video_mode=gr.Radio(["Smart Stock + AI Fallback (Fast 2min)", "Pure AI 100% Relevant (10-15 min support)"], value="Smart Stock + AI Fallback (Fast 2min)", label="✨ NAYA VIDEO MODE")
    show_subtitles=gr.Checkbox(label="Subtitles ON/OFF", value=True)
    script=gr.Textbox(lines=6, label="Your Script - 1 Sentence = 1 Scene", placeholder="Farmer is harvesting wheat with tractor. Doctor is checking patient in hospital. Elon Musk launched rocket.")
    btn=gr.Button("✨ GENERATE VIDEO V7 ✨", variant="primary")
    with gr.Row():
        video=gr.Video(label="Final Video")
        status=gr.Textbox(label="Status")
    btn.click(GenAll, [email, script, voice_lang, video_type, resolution, show_subtitles, video_mode], [video, status])

demo.queue(max_size=10).launch(share=True)
