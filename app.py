import asyncio, uuid, random, requests, re, os, urllib.parse, datetime, time, json, gc
import nest_asyncio
nest_asyncio.apply()

import gradio as gr
import webbrowser
from moviepy.editor import VideoFileClip, ColorClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip, TextClip, CompositeAudioClip
from moviepy.audio.fx.volumex import volumex
import edge_tts

# --- STRICT SECURITY & SHEET AUTO-CUT SYSTEM - JSM BY SAEED ---
SHEET_ID = "1wANoZUC8GOi4BSXQRalm2gKrhP8SDLCy_CfCaSWMkEQ"
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxOqPdND3z0j8lbNDdqVYeBAJ2qCFSrbWSNNJiLXk5tTZr6pf8hcAp7T3A8KcA4zvTuVA/exec"

def strict_cut_mints(email, mins):
    """منٹ کٹ کرنے کا سخت ترین فنکشن - ناکامی پر ویڈیو بلاک"""
    try:
        clean_email = email.strip().lower()
        if not clean_email or mins <= 0: 
            return False, "❌ Invalid email or video duration."
            
        url = f"{WEB_APP_URL}?email={urllib.parse.quote(clean_email)}&mins={mins}"
        res = requests.get(url, timeout=12)
        
        if res.status_code == 200:
            print(f"✅ STRICT SECURITY: {mins:.2f} Mints Deducted for {clean_email}")
            return True, f"✅ {mins:.2f} Mints Deducted Successfully."
        else:
            print(f"⚠️ Mints Cut Server Error: Status {res.status_code}")
            return False, "⚠️ Server Error: Minutes deduction failed."
    except Exception as e:
        print(f"❌ Security Lock: Mints Cut Exception - {e}")
        return False, f"❌ System Error: {str(e)}"

SUPABASE_KEY = "sb_publishable_1W4NK6X7Edacm_eSB1cFDQ_CkT6c4EY"
PIXABAY_KEY = "56386293-14facd94fdac26f9fc37f5f2c"
COVERR_API_KEY = "8c8c592b07a57e05dc49368c399b7659"
PEXELS_KEYS = [
    "ROKJvfYuuSkc7QVVL6VjCgYFyB8UQZCLLCctD2SfTJcIrDGo5Ex3JMX6",
    "zniYyavhal66VGwuV2kUIpRm7vG3Y0rddDLuzrITvmPqQ26kdG0vcyy0",
    "f6IKxrHR8MHj1geD62crLTfDTQX0s7ewFkw3hEI4d4CenRTZXCkpCWD9",
    "1j6kFq1GRB4291F1s1RMghlgIX3d3u78OaTpiDKmtlSAjJkKPb9vVTkL",
    "tpkypogswv07n84dh0iaHI9tamu43GEcvZokA3XiJSTUT0NV32A6gG9"
]
BRAND_NAME = "JSM AI BY JAM SAEED"
XK = PEXELS_KEYS

VOICES = {
    "English Male (Andrew - Professional Studio)": "en-US-AndrewNeural",
    "English Male (Christopher - Deep Motivational)": "en-US-ChristopherNeural",
    "English Male (Guy - News Anchor)": "en-US-GuyNeural",
    "English Male (Ryan - UK Storyteller)": "en-GB-RyanNeural",
    "English Male (Brian - UK Deep)": "en-GB-BrianNeural",
    "English Male (Brandon - Human Natural)": "en-US-BrandonNeural",
    "English Female (Jenny - Clear & Energetic)": "en-US-JennyNeural",
    "English Female (Aria - Natural Human)": "en-US-AriaNeural",
    "English Female (Emma - Human Feel)": "en-US-EmmaNeural",
    "English Female (Sonia - UK Accent)": "en-GB-SoniaNeural",
    "English Female (Libby - UK Human)": "en-GB-LibbyNeural",
    "Urdu Male (Asad - Deep Voice / Narrative Style)": "ur-PK-AsadNeural",
    "Urdu Female (Uzma - Soft & Clear)": "ur-PK-UzmaNeural",
    "Hindi Male (Madhur - Deep)": "hi-IN-MadhurNeural",
    "Hindi Male (Arjun - Motivational Speaker Style)": "hi-IN-ArjunNeural",
    "Hindi Female (Swara - Dynamic & Crisp)": "hi-IN-SwaraNeural",
    "Hindi Female (Ananya - Soft)": "hi-IN-AnanyaNeural",
    "Arabic Male (Hamdan)": "ar-SA-HamdanNeural",
    "Arabic Female (Hanan)": "ar-SA-HananNeural",
    "Russian Female (Svetlana - Viral TikTok)": "ru-RU-SvetlanaNeural",
    "Russian Male (Dmitry - Deep Russian)": "ru-RU-DmitryNeural",
    "Urdu-Hindi Mix (Auto Detect)": "AUTO"
}

CATEGORIES_MAP = {
    "motivational": ["motivation","success","hard work","rich people","money works","iron body","train","winner","dream big","skill","failure","rizq","goal","trophy","inspiration"],
    "finance_stock": ["stock market","stock","trading","share market","kse 100","trader","forex","crypto","bitcoin","ethereum","bull market","bear market","nifty"],
    "finance_money": ["money","wealth","rich","dollars","cash","finance","bank","profit","investing","loan","interest","rupee","dollar"],
    "business": ["business","corporate","office","meeting","boss","strategy","presentation","startup","entrepreneur","company"],
    "news": ["breaking news","journalism","reporter","studio news","media","headline","press","tv news","election","politics","live news"],
    "fitness": ["body","iron","gym","workout","fitness","bodybuilding","exercise","running","yoga","athlete","muscle"],
    "ai_tech": ["ai","artificial intelligence","robot","technology","future","cyberpunk","machine learning","chatgpt","software","coding","programmer"],
    "medical": ["doctor","hospital","patient","medical","health","surgery","clinic","nurse","medicine"],
    "real_estate": ["house","property","mansion","apartment","real estate","villa","home tour","dream house"],
    "food": ["cooking","chef","food","kitchen","restaurant","recipe","delicious","baking","biryani","street food"],
    "travel": ["travel","tourism","airplane","beach","mountains","vacation","hotel","adventure","drone shot","aerial view"],
    "education": ["degrees","skills","student","school","university","book","learning","teacher"],
    "gaming": ["gaming","gamer","esports","playstation","controller","streamer"],
    "fashion": ["fashion","model","clothing","style","runway","dress"],
    "automotive": ["car","supercar","driving","mechanic","engine","vehicle","racing","bike","motorcycle"],
    "nature": ["forest","river","ocean","landscape","sunset","sky","wildlife","flowers","rain","snow","desert","mountains","village"],
    "space": ["space","galaxy","astronaut","planet","stars","universe","nasa","rocket"],
    "luxury": ["luxury","rich lifestyle","millionaire","billionaire","private jet","mansion"],
    "sports": ["football","cricket","soccer","stadium","match","player","cricket stadium"],
    "wedding": ["wedding","bride","groom","marriage","shaadi","mehndi"],
    "family": ["family","love","parents","children","baby","mother","father"],
    "islamic": ["islamic","masjid","mosque","madina","makkah","kaaba","muslim","prayer","quran","dua","allah","islamic history"],
    "youtube": ["youtube","youtuber","subscribe","channel","video editing","vlog","podcast","interview"],
    "abstract": ["abstract","motion background","neon background","particles","animation","3d animation"]
}

BASE_DIR = "./JSM_Outputs"
os.makedirs(BASE_DIR, exist_ok=True)

def SMART_KEYWORD_ENGINE(sentence):
    s_low = sentence.lower()
    best_score = 0
    matched_kws = []
    selected_cat = ""
    for cat, kws in CATEGORIES_MAP.items():
        score = sum(1 for kw in kws if kw in s_low)
        if score > best_score:
            best_score = score
            matched_kws = [kw for kw in kws if kw in s_low]
            selected_cat = cat
    if best_score > 0 and matched_kws:
        primary_kw = matched_kws[0]
        secondary_kw = matched_kws[1] if len(matched_kws) > 1 else selected_cat
        queries = [f"{primary_kw} {secondary_kw}", f"{primary_kw}", f"{selected_cat} HD"]
        return list(dict.fromkeys(queries))
    clean = re.sub(r'[^\w\s]', '', s_low)
    stop_words = {"about","today","video","talk","karenge","baat","shuru","please","subscribe","channel","welcome","dosto","bhai","hello","everyone","the","and","you","will","have","this","that","hai","ke","ki","ka","aur","mein","aaj","ko","se","me","hoga","hain"}
    words = [w for w in clean.split() if w not in stop_words and len(w) > 3]
    if words:
        return [f"{words[0]} {words[1]}" if len(words) > 1 else words[0], "business corporate"]
    return ["cinematic background"]

def clean_analyze(script):
    clean = re.sub(r"(sex\s*video|porn|xxx|nude|naked)", " ", script, flags=re.I)
    raw_sentences = re.split(r'[.!?\n\u06d4]+', clean)
    sens = []
    for s in raw_sentences:
        s_strip = s.strip()
        if len(s_strip) > 8:
            sens.append(s_strip)
    return clean, sens

def download_clip(url, W, H, duration):
    try:
        t_path = f"{BASE_DIR}/{uuid.uuid4().hex[:6]}.mp4"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            with open(t_path, 'wb') as f:
                f.write(res.content)
            clip = VideoFileClip(t_path).resize((W, H))
            clip = clip.fx(lambda c: c.resize(lambda t: 1 + 0.015 * t))
            if clip.duration < duration:
                clip = clip.loop(duration=duration)
            else:
                clip = clip.subclip(0, duration)
            return clip
    except Exception as e:
        print(f"⚠️ Clip Download Error: {e}")
    return None

def get_clip_from_platforms(smart_queries, duration, W, H, clip_index):
    orientation = 'portrait' if H > W else 'landscape'
    for q in smart_queries:
        q_enc = urllib.parse.quote(q)
        for key in PEXELS_KEYS:
            try:
                headers = {"Authorization": key}
                url = f"https://api.pexels.com/videos/search?query={q_enc}&per_page=12&orientation={orientation}"
                r = requests.get(url, headers=headers, timeout=8).json()
                if 'videos' in r and len(r['videos']) > 0:
                    v = r['videos'][clip_index % len(r['videos'])]
                    files = [f for f in v['video_files'] if f.get('height') and f['height'] >= 720]
                    link = files[0]['link'] if files else v['video_files'][0]['link']
                    cl = download_clip(link, W, H, duration)
                    if cl: return cl
            except: continue
        try:
            url = f"https://pixabay.com/api/videos/?key={PIXABAY_KEY}&q={q_enc}&per_page=8"
            r = requests.get(url, timeout=8).json()
            if r.get('hits'):
                v = r['hits'][clip_index % len(r['hits'])]
                link = v['videos']['medium']['url']
                cl = download_clip(link, W, H, duration)
                if cl: return cl
        except: pass
        try:
            url = f"https://api.coverr.co/api/free/videos?query={q_enc}&per_page=8"
            headers = {"Authorization": COVERR_API_KEY, "User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=8).json()
            if r and isinstance(r, dict) and r.get('hits'):
                v = r['hits'][clip_index % len(r['hits'])]
                link = v.get('urls', {}).get('mp4') or v.get('urls', {}).get('mp4_preview')
                if link:
                    cl = download_clip(link, W, H, duration)
                    if cl: return cl
        except: pass
        try:
            url = f"https://pixabay.com/api/videos/?key={PIXABAY_KEY}&q={q_enc}&per_page=10&order=popular"
            r = requests.get(url, timeout=8).json()
            if r.get('hits') and len(r['hits']) > 1:
                v = r['hits'][(clip_index+2) % len(r['hits'])]
                link = v['videos']['medium']['url']
                cl = download_clip(link, W, H, duration)
                if cl: return cl
        except: pass
    return ColorClip((W, H), color=(15, 18, 24), duration=duration)

def get_niche_music(text):
    l = text.lower()
    if any(x in l for x in ["stock", "finance", "money", "bank", "business"]): q = "corporate"
    elif any(x in l for x in ["news", "breaking", "politics"]): q = "news"
    elif any(x in l for x in ["motivation", "success", "dream"]): q = "inspiring"
    else: q = "ambient"
    try:
        url = f"https://pixabay.com/api/music/?key={PIXABAY_KEY}&q={urllib.parse.quote(q)}&per_page=10"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=8).json()
        if r.get('hits'):
            track = random.choice(r['hits'])
            mp3_url = track.get('download_url') or track.get('audio')
            if mp3_url:
                mp = f"{BASE_DIR}/bgm_{uuid.uuid4().hex[:4]}.mp3"
                res = requests.get(mp3_url, headers=headers, timeout=12)
                with open(mp, 'wb') as f: f.write(res.content)
                return mp
    except Exception as e: pass
    return None

async def Tt(t, o, v):
    if "ru-RU" in v: rate_str, pitch_str = "-5%", "+0Hz"
    elif "ur-" in v or "hi-" in v: rate_str, pitch_str = "+0%", "+1Hz"
    else: rate_str, pitch_str = "-4%", "+2Hz"
    communicator = edge_tts.Communicate(t, v, rate=rate_str, pitch=pitch_str)
    await communicator.save(o)

def run_tts(tx, out, vc):
    if len(tx.split()) < 3: tx = tx + "۔"
    for attempt in range(2):
        try:
            try: asyncio.run(Tt(tx, out, vc))
            except:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(Tt(tx, out, vc))
            if os.path.exists(out) and os.path.getsize(out) > 800: return True
        except: time.sleep(1)
    return False

def detect_voice(ch, selected):
    if "AUTO" in selected:
        if any(w in ch.lower() for w in ["breaking news","stock market","finance","dollar","bitcoin"]): return VOICES["English Male (Guy - News Anchor)"]
        return VOICES["Urdu Male (Asad - Deep Voice / Narrative Style)"]
    eng_words = len(re.findall(r'\b[a-zA-Z]{4,}\b', ch))
    if eng_words > len(ch.split()) * 0.6 and "Urdu" in selected: return VOICES["English Male (Guy - News Anchor)"]
    return VOICES.get(selected, "ur-PK-AsadNeural")

# --- CORE GENERATION ENGINE ---
def generate_video_pipeline(email, license_code, voice_lang, video_type, resolution, show_subtitles, script, progress=gr.Progress()):
    # Strict Input Checks
    if not email or not email.strip():
        return None, "❌ SECURITY ERROR: Email field cannot be empty!"
    if not license_code or not license_code.strip():
        return None, "❌ SECURITY ERROR: License Code is required!"

    progress(0.05, desc="🔒 Security Verification & Analyzing Script...")
    cs, kws = clean_analyze(script)
    if not kws:
        return None, "❌ ERROR: Script is too short or empty!"

    W, H = (1280, 720) if "16:9" in video_type else (720, 1280)
    if "480" in resolution: W, H = (854, 480) if W > H else (480, 854)
    
    bgm_path = get_niche_music(script)
    scene_files = []

    for idx, ch in enumerate(kws):
        prog_val = 0.1 + (0.8 * (idx / len(kws)))
        progress(prog_val, desc=f"Processing Scene {idx+1}/{len(kws)}...")
        
        voice_code = detect_voice(ch, voice_lang)
        ap = f"{BASE_DIR}/{uuid.uuid4().hex[:5]}.mp3"
        ok = run_tts(ch, ap, voice_code)
        if not ok: continue
        
        au = AudioFileClip(ap)
        if au.duration > 0.4: au = au.subclip(0, au.duration - 0.1)
        smart_queries = SMART_KEYWORD_ENGINE(ch)
        
        dur_left = au.duration
        sub_clips = []
        counter = idx
        while dur_left > 0:
            cur_dur = min(random.uniform(3.2, 4.5), dur_left)
            sc = get_clip_from_platforms(smart_queries, cur_dur, W, H, counter)
            sub_clips.append(sc)
            dur_left -= cur_dur
            counter += 1
            
        base_clip = concatenate_videoclips(sub_clips, method="compose") if len(sub_clips) > 1 else sub_clips[0]
        base_clip = base_clip.set_duration(au.duration)
        
        if bgm_path and os.path.exists(bgm_path):
            try:
                bgm = AudioFileClip(bgm_path).subclip(0, au.duration).fx(volumex, 0.32)
                final_audio = CompositeAudioClip([au, bgm])
                base_clip = base_clip.set_audio(final_audio)
            except: base_clip = base_clip.set_audio(au)
        else: base_clip = base_clip.set_audio(au)
        
        layers = [base_clip]
        if show_subtitles:
            try:
                txt = TextClip(ch[:100], fontsize=int(W*0.038), color='white', stroke_color='black', stroke_width=2, method='caption', size=(int(W*0.85), None), align='center')
                txt = txt.set_duration(au.duration).set_pos(('center', 0.80), relative=True)
                layers.append(txt)
            except: pass
            
        final_scene = CompositeVideoClip(layers)
        temp_scene_path = f"{BASE_DIR}/scene_{idx}_{uuid.uuid4().hex[:4]}.mp4"
        final_scene.write_videofile(temp_scene_path, fps=24, codec='libx264', audio_codec='aac', preset='ultrafast', threads=1, bitrate="1000k", logger=None)
        scene_files.append(temp_scene_path)
        
        for sc in sub_clips:
            try: sc.close()
            except: pass
        try:
            base_clip.close()
            final_scene.close()
            au.close()
        except: pass
        del sub_clips, base_clip, final_scene, au
        gc.collect()

    if scene_files:
        progress(0.92, desc="Rendering Final Video File...")
        list_path = f"{BASE_DIR}/concat_list.txt"
        with open(list_path, "w") as f:
            for sf in scene_files: f.write(f"file '{os.path.abspath(sf)}'\n")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = f"{BASE_DIR}/JSM_Video_{timestamp}.mp4"
        os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c copy {out_path}")
        if not os.path.exists(out_path) or os.path.getsize(out_path) < 1000:
            os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c:v libx264 -preset ultrafast -c:a aac {out_path}")
        
        # --- STRICT DEDUCTION & VERIFICATION ---
        try:
            final_clip = VideoFileClip(out_path)
final_mins = round(final_clip.duration / 60, 2)
final_clip.close()

            
            # Execute Strict Minutes Cut
            success, msg = strict_cut_mints(email, final_mins)
            
            if not success:
                # Security Lockdown: If deduction failed, block video output
                if os.path.exists(out_path): os.remove(out_path)
                return None, f"🔒 SECURITY LOCK: Minutes Deduction Failed! Video access blocked. Error: {msg}"
            
            status_msg = f"🎉 Video Ready! [{final_mins:.2f} Mints Cut from {email.strip().lower()}]"
        except Exception as e:
            if os.path.exists(out_path): os.remove(out_path)
            return None, f"🔒 SECURITY LOCK: Verification Error ({e})"
            
        for sf in scene_files:
            try: os.remove(sf)
            except: pass
            
        return out_path, status_msg

    return None, "❌ Rendering Failed!"

# --- PURE DARK & SHINEY GOLDEN UI ---
custom_css = """
body, .gradio-container { background-color: #000000 !important; color: #FFFFFF !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
.tabs { background-color: #000000 !important; border: none !important; }
.tab-nav { background-color: #0a0a0a !important; border-bottom: 2px solid #FFD700 !important; }
.tab-nav button { color: #888888 !important; font-weight: bold !important; font-size: 15px !important; }
.tab-nav button.selected { color: #FFD700 !important; border-bottom: 3px solid #FFD700 !important; background-color: #111111 !important; }
button.primary { background: linear-gradient(135deg, #FFD700, #FFA500) !important; color: #000000 !important; font-weight: 900 !important; font-size: 16px !important; border: none !important; border-radius: 8px !important; box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.4) !important; }
button.primary:hover { background: linear-gradient(135deg, #FFA500, #FFD700) !important; box-shadow: 0px 6px 20px rgba(255, 215, 0, 0.7) !important; }
input, select, textarea { background-color: #111111 !important; color: #FFD700 !important; border: 1px solid #FFD700 !important; border-radius: 6px !important; }
label { color: #FFD700 !important; font-weight: 600 !important; font-size: 13px !important; }
.border-box { border: 1px solid #FFD700 !important; padding: 10px; border-radius: 8px; }
"""

with gr.Blocks(css=custom_css, title="JSM VIDEO GENERATOR") as app:
    gr.HTML("""
    <div style='text-align: center; padding: 15px; border-bottom: 2px solid #FFD700; margin-bottom: 15px;'>
        <h1 style='color: #FFD700; font-size: 32px; font-weight
