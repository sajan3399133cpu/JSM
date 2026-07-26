import asyncio, uuid, random, requests, re, os, urllib.parse, datetime, time, json, gc
from moviepy.editor import VideoFileClip, ColorClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip, TextClip, CompositeAudioClip, ImageClip
from moviepy.audio.fx.volumex import volumex
import edge_tts, gradio as gr
from PIL import Image

BASE_DIR = "./JSM_Outputs"
os.makedirs(BASE_DIR, exist_ok=True)
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyfopJoiGBueO6AsZ5JE-juplXjSa1Lc_klKn4bOswLyhPmPGsvOhT9r6Axow6rsl-rXg/exec"
PIXABAY_KEY = "56386293-14facd94fdac26f9fc37f5f2c"
PEXELS_KEYS = ["ROKJvfYuuSkc7QVVL6VjCgYFyB8UQZCLLCctD2SfTJcIrDGo5Ex3JMX6","zniYyavhal66VGwuV2kUIpRm7vG3Y0rddDLuzrITvmPqQ26kdG0vcyy0","f6IKxrHR8MHj1geD62crLTfDTQX0s7ewFkw3hEI4d4CenRTZXCkpCWD9","1j6kFq1GRB4291F1s1RMghlgIX3d3u78OaTpiDKmtlSAjJkKPb9vVTkL","tpkypogswv07n84dh0iaHI9tamu43GEcvZokA3XiJSTUT0NV32A6gG9"]

VOICES = {
    "English Male (Andrew - Professional Studio)": "en-US-AndrewNeural",
    "English Male (Guy - News Anchor)": "en-US-GuyNeural",
    "English Male (Ryan - UK Storyteller)": "en-GB-RyanNeural",
    "English Female (Jenny)": "en-US-JennyNeural",
    "English Female (Aria)": "en-US-AriaNeural",
    "Urdu Male (Asad - Deep Voice)": "ur-PK-AsadNeural",
    "Urdu Female (Uzma)": "ur-PK-UzmaNeural",
    "Hindi Male (Madhur)": "hi-IN-MadhurNeural",
    "Hindi Female (Swara)": "hi-IN-SwaraNeural",
    "Arabic Male (Hamdan)": "ar-SA-HamdanNeural",
    "Russian Female (Svetlana)": "ru-RU-SvetlanaNeural",
    "Urdu-Hindi Mix (Auto)": "AUTO"
}

CATEGORIES_MAP = {
    "motivational": ["motivation","success","hard work","rich people","winner","dream big","goal"],
    "finance_stock": ["stock market","stock","trading","share market","kse 100","trader","forex","crypto","bitcoin"],
    "finance_money": ["money","wealth","dollars","cash","finance","bank","profit"],
    "business": ["business","corporate","office","meeting","boss","startup","entrepreneur"],
    "news": ["breaking news","journalism","reporter","studio news","media","election"],
    "fitness": ["gym","workout","fitness","bodybuilding","exercise","yoga"],
    "ai_tech": ["ai","artificial intelligence","robot","technology","future","chatgpt","coding"],
    "medical": ["doctor","hospital","patient","medical","health","surgery"],
    "farming": ["farmer","kisan","tractor","wheat","crop","harvest"],
    "islamic": ["islamic","masjid","mosque","madina","makkah","kaaba","quran","allah"],
    "sports": ["football","cricket","soccer","stadium","match"],
    "travel": ["travel","tourism","airplane","beach","mountains","vacation"],
    "nature": ["forest","river","ocean","landscape","sunset","village"],
}

def cut_mints_auto(email, mins):
    try: requests.get(f"{WEB_APP_URL}?email={urllib.parse.quote(email)}&mins={mins}", timeout=10)
    except: pass

def SMART_KEYWORD_ENGINE(sentence):
    s_low=sentence.lower()
    blacklist=" -news -reporter -camera -microphone -journalist -interview"
    best=0; matched=[]; cat=""
    for c,kws in CATEGORIES_MAP.items():
        score=sum(1 for kw in kws if kw in s_low)
        if score>best: best=score; matched=[kw for kw in kws if kw in s_low]; cat=c
    if best>0 and matched: return [f"{matched[0]} {cat}{blacklist}", f"{matched[0]}{blacklist}"]
    words=[w for w in re.sub(r'[^\w\s]','',s_low).split() if len(w)>3][:2]
    return [f"{' '.join(words)}{blacklist}"] if words else [f"cinematic{blacklist}"]

def clean_analyze(script):
    return script, [s.strip() for s in re.split(r'[.!?\n\u06d4]+',script) if len(s.strip())>8]

def Ai_Free_Generator(prompt, path, W, H):
    q=urllib.parse.quote(prompt[:120]); seed=random.randint(1,99999)
    for model in ["flux","turbo"]:
        try:
            url=f"https://image.pollinations.ai/prompt/{q}?width={W}&height={H}&model={model}&nologo=true&seed={seed}&enhance=true"
            r=requests.get(url,timeout=25)
            if r.status_code==200 and len(r.content)>5000:
                open(path,'wb').write(r.content); return path
        except: continue
    Image.new('RGB',(W,H),color=(15,18,24)).save(path); return path

def download_clip_safe(url, W, H, duration):
    t_path=None
    try:
        t_path=f"{BASE_DIR}/tmp_{uuid.uuid4().hex[:6]}.mp4"
        open(t_path,'wb').write(requests.get(url,headers={"User-Agent":"Mozilla/5.0"},timeout=15).content)
        clip=VideoFileClip(t_path).resize((W,H)).resize(lambda t: 1+0.015*t)
        final=clip.loop(duration=duration) if clip.duration<duration else clip.subclip(0,duration)
        clip.close()
        try: os.remove(t_path)
        except: pass
        return final
    except:
        if t_path and os.path.exists(t_path):
            try: os.remove(t_path)
            except: pass
        return None

def get_clip_from_platforms(smart_queries, duration, W, H, clip_index, mode):
    # PURE AI MODE - 100% AI
    if "Pure AI" in mode:
        p=f"{BASE_DIR}/ai_{uuid.uuid4().hex[:4]}.jpg"
        Ai_Free_Generator(smart_queries[0], p, W, H)
        clip=ImageClip(p).set_duration(duration).resize((W,H)).resize(lambda t: 1+0.05*t)
        try: os.remove(p)
        except: pass
        return clip

    # ===== SMART STOCK MIX MODE - AI + PEXELS FIRST + PIXABAY =====
    # Tumhari demand: Pehle AI Image, phir Pexels, phir Pixabay - mix taake relevant rahe
    orientation='portrait' if H>W else 'landscape'

    # 60% scenes AI se, 40% Stock se - Is se relevance best hogi
    use_ai_first = random.random() < 0.6 or clip_index % 3 == 0

    if use_ai_first:
        print(f"🤖 MIX: AI Image First - {smart_queries[0]}")
        p=f"{BASE_DIR}/ai_{uuid.uuid4().hex[:4]}.jpg"
        Ai_Free_Generator(smart_queries[0], p, W, H)
        clip=ImageClip(p).set_duration(duration).resize((W,H)).resize(lambda t: 1+0.04*t)
        try: os.remove(p)
        except: pass
        return clip

    # PEXELS FIRST
    for q in smart_queries:
        q_enc=urllib.parse.quote(q)
        for key in PEXELS_KEYS:
            try:
                r=requests.get(f"https://api.pexels.com/videos/search?query={q_enc}&per_page=4&orientation={orientation}",headers={"Authorization":key},timeout=7).json()
                if r.get('videos'):
                    link=r['videos'][clip_index % len(r['videos'])]['video_files'][0]['link']
                    cl=download_clip_safe(link,W,H,duration)
                    if cl:
                        print(f"✅ MIX: PEXELS - {q}")
                        return cl
            except: continue
        try:
            r=requests.get(f"https://pixabay.com/api/videos/?key={PIXABAY_KEY}&q={q_enc}&per_page=4",timeout=7).json()
            if r.get('hits'):
                link=r['hits'][clip_index % len(r['hits'])]['videos']['medium']['url']
                cl=download_clip_safe(link,W,H,duration)
                if cl:
                    print(f"✅ MIX: PIXABAY - {q}")
                    return cl
        except: pass

    # Fallback AI
    p=f"{BASE_DIR}/ai_{uuid.uuid4().hex[:4]}.jpg"
    Ai_Free_Generator(smart_queries[0], p, W, H)
    clip=ImageClip(p).set_duration(duration).resize((W,H)).resize(lambda t: 1+0.04*t)
    try: os.remove(p)
    except: pass
    return clip

def get_niche_music(text):
    q="corporate" if any(x in text.lower() for x in ["stock","finance","money"]) else "ambient"
    try:
        r=requests.get(f"https://pixabay.com/api/music/?key={PIXABAY_KEY}&q={urllib.parse.quote(q)}&per_page=3",timeout=7).json()
        if r.get('hits'):
            mp3=r['hits'][0].get('download_url')
            if mp3:
                mp=f"{BASE_DIR}/bgm_{uuid.uuid4().hex[:4]}.mp3"
                open(mp,'wb').write(requests.get(mp3,timeout=12).content)
                return mp
    except: pass
    return None

async def Tt(t,o,v): await edge_tts.Communicate(t,v,rate="-4%",pitch="+2Hz").save(o)
def run_tts(tx,out,vc):
    if len(tx.split())<3: tx=tx+"۔"
    for _ in range(2):
        try:
            asyncio.run(Tt(tx,out,vc))
            if os.path.exists(out) and os.path.getsize(out)>800: return True
        except: time.sleep(0.5)
    return False

def detect_voice(ch, sel):
    if "AUTO" in sel: return list(VOICES.values())[1] if "stock" in ch.lower() else list(VOICES.values())[5]
    return VOICES.get(sel, "ur-PK-AsadNeural")

def GenAll(email, script, voice_lang, video_type, resolution, show_subtitles, video_mode):
    if not script.strip(): return None, "Script likho"
    cs, kws = clean_analyze(script)
    W,H = (1280,720) if "16:9" in video_type else (720,1280)
    if "480" in resolution: W,H = (854,480) if W>H else (480,854)
    if "1080" in resolution: W,H = (1920,1080) if W>H else (1080,1920)
    bgm_path = get_niche_music(script)
    scene_files=[]
    for idx, ch in enumerate(kws):
        print(f"\n🎬 SCENE {idx+1}/{len(kws)} MIX MODE")
        ap=f"{BASE_DIR}/{uuid.uuid4().hex[:5]}.mp3"
        if not run_tts(ch, ap, detect_voice(ch, voice_lang)): continue
        au=AudioFileClip(ap)
        if au.duration>0.4: au=au.subclip(0, au.duration-0.1)
        smart_queries=SMART_KEYWORD_ENGINE(ch)
        sub_clips=[]; dur_left=au.duration; counter=idx
        while dur_left>0:
            cur_dur=min(4.0, dur_left)
            sc=get_clip_from_platforms(smart_queries, cur_dur, W, H, counter, video_mode)
            sub_clips.append(sc)
            dur_left-=cur_dur; counter+=1
        base_clip=concatenate_videoclips(sub_clips,method="compose").set_duration(au.duration).set_audio(au)
        if bgm_path and os.path.exists(bgm_path):
            try:
                bgm=AudioFileClip(bgm_path).subclip(0,au.duration).fx(volumex,0.25)
                base_clip=base_clip.set_audio(CompositeAudioClip([au,bgm]))
            except: pass
        layers=[base_clip]
        if show_subtitles:
            try:
                txt=TextClip(ch[:90],fontsize=int(W*0.038),color='white',stroke_color='black',stroke_width=2,method='caption',size=(int(W*0.85),None),align='center')
                layers.append(txt.set_duration(au.duration).set_pos(('center',0.80),relative=True))
            except: pass
        final_scene=CompositeVideoClip(layers)
        temp_path=f"{BASE_DIR}/scene_{idx}.mp4"
        final_scene.write_videofile(temp_path,fps=24,codec='libx264',audio_codec='aac',preset='ultrafast',threads=1,bitrate="900k",logger=None)
        scene_files.append(temp_path)
        # RAM SAFE - HAR SCENE KE BAAD DELETE
        for sc in sub_clips:
            try: sc.close()
            except: pass
        try: base_clip.close(); final_scene.close(); au.close()
        except: pass
        try: os.remove(ap)
        except: pass
        del sub_clips, base_clip, final_scene, au
        gc.collect()
        print(f"✅ Scene {idx+1} RAM Cleared")

    if not scene_files: return None, "Fail"
    list_path=f"{BASE_DIR}/list.txt"
    with open(list_path,"w") as f:
        for sf in scene_files: f.write(f"file '{os.path.abspath(sf)}'\n")
    out_path=f"{BASE_DIR}/JSM_{datetime.datetime.now().strftime('%H%M%S')}.mp4"
    os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c copy {out_path}")
    if not os.path.exists(out_path) or os.path.getsize(out_path)<1000:
        os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c:v libx264 -preset ultrafast -c:a aac {out_path}")
    for sf in scene_files:
        try: os.remove(sf)
        except: pass
    try: os.remove(list_path)
    except: pass
    gc.collect()
    try:
        c=VideoFileClip(out_path); cut_mints_auto(email, round(c.duration/60,2)); c.close()
    except: pass
    return out_path, f"✅ Done MIX MODE - {len(scene_files)} Scenes - Relevant + RAM SAFE"

css_code="#header{text-align:center;padding:20px;background:#000!important;border-bottom:4px solid #FFD700!important} #header h1{color:#FFD700!important;font-size:36px!important;font-weight:900!important} button.primary{background:linear-gradient(90deg,#FFD700,#FFA500)!important;color:#000!important;font-weight:900!important;height:60px!important}"

with gr.Blocks(title="JSM Video Generator") as demo:
    gr.HTML("<div id='header'><h1>✦ JSM VIDEO GENERATOR ✦</h1></div>")
    with gr.Row():
        email=gr.Textbox(label="Email", value="areej3399133@gmail.com")
        voice_lang=gr.Dropdown(list(VOICES.keys()), value="Urdu Male (Asad - Deep Voice)", label="Voice")
    with gr.Row():
        video_type=gr.Dropdown(["YouTube 16:9","TikTok 9:16"], value="YouTube 16:9", label="Type")
        resolution=gr.Dropdown(["854x480 - SD Fast (No RAM Error)","1280x720 - HD"], value="854x480 - SD Fast (No RAM Error)", label="Resolution")
    video_mode=gr.Radio(["Smart Stock + AI Fallback (Fast) - AI + PEXELS FIRST + PIXABAY MIX", "Pure AI 100% Relevant (10-15 min)"], value="Smart Stock + AI Fallback (Fast) - AI + PEXELS FIRST + PIXABAY MIX", label="Video Mode")
    show_subtitles=gr.Checkbox(label="Subtitles ON", value=True)
    script=gr.Textbox(lines=6, label="Script", placeholder="Farmer harvesting wheat. Doctor checking patient. Stock market going up.")
    btn=gr.Button("✨ GENERATE VIDEO ✨", variant="primary")
    with gr.Row():
        video=gr.Video(label="Final Video")
        status=gr.Textbox(label="Status")
    btn.click(GenAll, [email, script, voice_lang, video_type, resolution, show_subtitles, video_mode], [video, status])

demo.queue().launch(server_name="0.0.0.0", server_port=7860, css=css_code, show_error=True)
