import asyncio, uuid, random, requests, re, os, urllib.parse, datetime, time, gc
import nest_asyncio
nest_asyncio.apply()
from moviepy.editor import VideoFileClip, ColorClip, AudioFileClip, CompositeVideoClip, TextClip, CompositeAudioClip, ImageClip
from moviepy.audio.fx.volumex import volumex

SHEET_ID = "1wANoZUC8GOi4BSXQRalm2gKrhP8SDLCy_CfCaSWMkEQ"
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyfopJoiGBueO6AsZ5JE-juplXjSa1Lc_klKn4bOswLyhPmPGsvOhT9r6Axow6rsl-rXg/exec"
def cut_mints_auto(email, mins):
    try:
        if not email or mins <=0: return
        requests.get(f"{WEB_APP_URL}?email={urllib.parse.quote(email)}&mins={mins}", timeout=15)
    except: pass

VOICES = {
    "English Male (Guy - News Anchor)": "en-US-GuyNeural",
    "Urdu Male (Asad - Deep Voice / Narrative Style)": "ur-PK-AsadNeural",
    "Urdu Female (Uzma - Soft & Clear)": "ur-PK-UzmaNeural",
    "Hindi Male (Madhur - Deep)": "hi-IN-MadhurNeural",
    "English Female (Jenny - Clear & Energetic)": "en-US-JennyNeural",
    "English Female (Aria - Natural Human)": "en-US-AriaNeural",
    "Russian Female (Svetlana - Viral TikTok)": "ru-RU-SvetlanaNeural",
    "Turkish Male (Ahmet)": "tr-TR-AhmetNeural",
    "Urdu-Hindi Mix (Auto Detect)": "AUTO"
}

BASE_DIR = "./JSM_Outputs"
os.makedirs(BASE_DIR, exist_ok=True)

def clean_analyze(script):
    clean = re.sub(r"(sex\s*video|porn|xxx|nude|naked)", " ", script, flags=re.I)
    raw_sentences = re.split(r'[.!?\n\u06d4]+', clean)
    return clean, [s.strip() for s in raw_sentences if len(s.strip()) > 8]

def SMART_KEYWORD_ENGINE(sentence):
    s = re.sub(r'[^\w\s]', ' ', sentence.lower())
    words = [w for w in s.split() if len(w) > 3][:5]
    q = " ".join(words) if words else "cinematic story background"
    return [q]

def get_clip_from_platforms(smart_queries, duration, W, H, clip_index):
    query = smart_queries[0] if smart_queries else "cinematic story background"
    # --- ONLY AI VIDEO 5-6 SEC ---
    try:
        print(f"🤖 AI VIDEO GENERATING: {query[:70]}")
        prompt = f"{query}, cinematic motion, slow camera pan, natural movement, ultra realistic 8k, highly detailed"
        q = urllib.parse.quote(prompt[:130])
        video_url = f"https://image.pollinations.ai/prompt/{q}?model=video&width={W}&height={H}&seed={random.randint(1,9999999)}&nologo=true&enhance=true"
        t_path = f"{BASE_DIR}/ai_{uuid.uuid4().hex[:4]}.mp4"
        r = requests.get(video_url, timeout=90)
        if r.status_code == 200 and len(r.content) > 20000:
            open(t_path,'wb').write(r.content)
            clip = VideoFileClip(t_path).resize((W, H))
            print(f"✅ AI VIDEO DONE")
            return clip.subclip(0, duration) if clip.duration > duration else clip
    except Exception as e:
        print(f"AI Video Fail: {e}")

    # --- FALLBACK AI IMAGE WITH ZOOM ---
    try:
        print(f"🎨 AI IMAGE FALLBACK: {query[:50]}")
        prompt = f"{query}, ultra realistic 8k cinematic, photorealistic, dramatic lighting, no text"
        p_path = f"{BASE_DIR}/img_{uuid.uuid4().hex[:4]}.jpg"
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt[:140])}?width={W}&height={H}&model=flux&nologo=true&seed={random.randint(1,999999)}"
        r = requests.get(url, timeout=60)
        if r.status_code == 200 and len(r.content) > 5000:
            open(p_path,'wb').write(r.content)
            return ImageClip(p_path).set_duration(duration).resize((W,H)).resize(lambda t: 1+0.04*t)
    except: pass
    return ColorClip((W,H), color=(12,12,12), duration=duration)

async def Tt(t, o, v):
    import edge_tts
    await edge_tts.Communicate(t, v, rate="-4%", pitch="+1Hz").save(o)

def run_tts(tx, out, vc):
    if len(tx.split()) < 3: tx = tx + "۔"
    for _ in range(2):
        try:
            try: asyncio.run(Tt(tx, out, vc))
            except: loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop); loop.run_until_complete(Tt(tx, out, vc))
            if os.path.exists(out) and os.path.getsize(out) > 800: return True
        except: time.sleep(1)
    try:
        from gtts import gTTS
        v_low = str(globals().get('voice_lang','')).lower()
        lang = 'ur' if 'urdu' in v_low else 'hi' if 'hindi' in v_low else 'en'
        gTTS(text=tx[:400], lang=lang, slow=False).save(out)
        if os.path.exists(out) and os.path.getsize(out) > 1000: return True
    except: pass
    return False

def detect_voice(ch, selected):
    if "AUTO" in selected: return VOICES["Urdu Male (Asad - Deep Voice / Narrative Style)"]
    return VOICES.get(selected, "en-US-GuyNeural")

# ========== MAIN DIRECT COLAB LOGIC ==========
print(f"🎙️ Voice: {voice_lang} | Mode: {video_mode}")
cs, kws = clean_analyze(script)
W, H = (1280,720) if "16:9" in video_type else (720,1280)
if "480" in resolution: W, H = (854,480) if W>H else (480,854)
scene_files = []
print(f"🎬 Total Scenes: {len(kws)}")
for idx, ch in enumerate(kws):
    try:
        print(f"\n🎬 SCENE {idx+1}/{len(kws)}: {ch[:60]}...")
        ap = f"{BASE_DIR}/{uuid.uuid4().hex[:5]}.mp3"
        if not run_tts(ch, ap, detect_voice(ch, voice_lang)): continue
        au = AudioFileClip(ap)
        if au.duration < 0.5: continue
        if au.duration > 0.4: au = au.subclip(0, au.duration-0.1)
        smart_queries = SMART_KEYWORD_ENGINE(ch)
        dur = au.duration
        clip = get_clip_from_platforms(smart_queries, dur, W, H, idx)
        base_clip = clip.set_duration(dur).set_audio(au)
        layers=[base_clip]
        if show_subtitles:
            try:
                txt = TextClip(ch[:90], fontsize=int(W*0.038), color='white', stroke_color='black', stroke_width=2, method='caption', size=(int(W*0.82), None), align='center').set_duration(dur).set_pos(('center',0.80), relative=True)
                layers.append(txt)
            except: pass
        final_scene = CompositeVideoClip(layers)
        temp_path = f"{BASE_DIR}/scene_{idx}_{uuid.uuid4().hex[:4]}.mp4"
        final_scene.write_videofile(temp_path, fps=24, codec='libx264', audio_codec='aac', preset='ultrafast', threads=2, bitrate="1000k", logger=None)
        scene_files.append(temp_path)
        print(f"✅ Scene {idx+1} Done & Saved")
        try: base_clip.close(); final_scene.close(); au.close()
        except: pass
        gc.collect()
    except Exception as e: print(f"❌ Scene {idx+1} Error {e}"); continue

if scene_files:
    print(f"\n🔗 Joining all scenes (FFMPEG)...")
    list_path = f"{BASE_DIR}/concat_list.txt"
    with open(list_path,"w") as f:
        for sf in scene_files: f.write(f"file '{os.path.abspath(sf)}'\n")
    out_path = f"{BASE_DIR}/JSM_Video_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c copy {out_path}")
    if not os.path.exists(out_path) or os.path.getsize(out_path)<5000:
        os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c:v libx264 -preset ultrafast -c:a aac {out_path}")
    print(f"\n🎉 SUCCESS! Video Ready: {out_path}")
    try:
        final_clip = VideoFileClip(out_path)
        cut_mints_auto(globals().get('email',''), round(final_clip.duration/60,2))
        final_clip.close()
    except: pass
    try:
        from google.colab import files; files.download(out_path)
    except: pass
