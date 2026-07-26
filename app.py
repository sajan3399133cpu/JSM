import asyncio, uuid, random, requests, re, os, urllib.parse, datetime, time, json, gc
import nest_asyncio
nest_asyncio.apply()
from moviepy.editor import VideoFileClip, ColorClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip, TextClip, CompositeAudioClip, ImageClip
from moviepy.audio.fx.volumex import volumex

# --- FINAL URLS ---
SHEET_ID = "1wANoZUC8GOi4BSXQRalm2gKrhP8SDLCy_CfCaSWMkEQ"
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyfopJoiGBueO6AsZ5JE-juplXjSa1Lc_klKn4bOswLyhPmPGsvOhT9r6Axow6rsl-rXg/exec"
def cut_mints_auto(email, mins):
    try:
        if not email or mins <=0: return
        requests.get(f"{WEB_APP_URL}?email={urllib.parse.quote(email)}&mins={mins}", timeout=15)
        print(f"✅ Mints Cut: {mins:.2f} for {email}")
    except: pass

PIXABAY_KEY = "56386293-14facd94fdac26f9fc37f5f2c"

VOICES = {
    "English Male (Andrew - Professional Studio)": "en-US-AndrewNeural",
    "English Male (Christopher - Deep Motivational)": "en-US-ChristopherNeural",
    "English Male (Guy - News Anchor)": "en-US-GuyNeural",
    "English Male (Ryan - UK Storyteller)": "en-GB-RyanNeural",
    "English Male (Brian - UK Deep)": "en-GB-BrianNeural",
    "English Male (Brandon - Human Natural)": "en-US-BrandonNeural",
    "English Male (Eric - Conversational)": "en-US-EricNeural",
    "English Female (Jenny - Clear & Energetic)": "en-US-JennyNeural",
    "English Female (Aria - Natural Human)": "en-US-AriaNeural",
    "English Female (Emma - Human Feel)": "en-US-EmmaNeural",
    "English Female (Sonia - UK Accent)": "en-GB-SoniaNeural",
    "English Female (Libby - UK Human)": "en-GB-LibbyNeural",
    "English Female (Ana - Kids Story)": "en-US-AnaNeural",
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
    "Turkish Male (Ahmet)": "tr-TR-AhmetNeural",
    "Turkish Female (Emel)": "tr-TR-EmelNeural",
    "Urdu-Hindi Mix (Auto Detect)": "AUTO"
}

BASE_DIR = "./JSM_Outputs"
os.makedirs(BASE_DIR, exist_ok=True)

# === POWERFUL AI ENGINE - NO ERROR ===
def clean_analyze(script):
    clean = re.sub(r"(sex\s*video|porn|xxx|nude|naked)", " ", script, flags=re.I)
    raw_sentences = re.split(r'[.!?\n\u06d4]+', clean)
    return clean, [s.strip() for s in raw_sentences if len(s.strip()) > 8]

def get_ai_image_powerful(query, duration, W, H):
    for _ in range(3):
        try:
            prompt = f"{query}, ultra realistic 8k cinematic, dramatic lighting, highly detailed, photorealistic, no text, story scene"
            p_path = f"{BASE_DIR}/img_{uuid.uuid4().hex[:4]}.jpg"
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt[:150])}?width={W}&height={H}&seed={random.randint(1,9999999)}&model=flux&enhance=true&nologo=true"
            r = requests.get(url, timeout=60)
            if r.status_code==200 and len(r.content)>8000:
                open(p_path,'wb').write(r.content)
                print(f"✅ AI IMAGE: {query[:40]}")
                return ImageClip(p_path).set_duration(duration).resize((W,H)).resize(lambda t: 1+0.04*t)
        except: time.sleep(1)
    return ColorClip((W,H), color=(12,12,12), duration=duration)

def get_ai_video_powerful(query, duration, W, H):
    for _ in range(2):
        try:
            print(f"🤖 AI VIDEO: {query[:50]}...")
            prompt = f"{query}, cinematic motion, slow camera pan, natural movement, ultra realistic 8k"
            q = urllib.parse.quote(prompt[:120])
            video_url = f"https://image.pollinations.ai/prompt/{q}?model=video&width={W}&height={H}&seed={random.randint(1,9999999)}&nologo=true&enhance=true"
            t_path = f"{BASE_DIR}/ai_{uuid.uuid4().hex[:4]}.mp4"
            r = requests.get(video_url, timeout=90)
            if r.status_code == 200 and len(r.content) > 20000:
                open(t_path,'wb').write(r.content)
                clip = VideoFileClip(t_path).resize((W, H))
                dur = min(duration, clip.duration if clip.duration > 0 else duration)
                print(f"✅ AI VIDEO DONE")
                return clip.subclip(0, dur) if clip.duration > dur else clip
        except Exception as e:
            print(f"AI Video Retry: {e}")
            time.sleep(2)
    # Fallback to Image
    return get_ai_image_powerful(query, duration, W, H)

def get_clip_from_platforms(smart_queries, duration, W, H, clip_index):
    # اب صرف AI ہی چلے گا - 5-6 سیکنڈ کا کلپ
    query = smart_queries[0] if smart_queries else "cinematic story background"
    return get_ai_video_powerful(query, duration, W, H)

def get_niche_music(text):
    try:
        r = requests.get(f"https://pixabay.com/api/music/?key={PIXABAY_KEY}&q=ambient&per_page=5", timeout=8).json()
        if r.get('hits'):
            mp3_url = r['hits'][0].get('download_url')
            if mp3_url:
                mp = f"{BASE_DIR}/bgm_{uuid.uuid4().hex[:4]}.mp3"
                open(mp,'wb').write(requests.get(mp3_url, timeout=10).content)
                return mp
    except: pass
    return None

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
        lang = 'en'
        v_low = str(globals().get('voice_lang','')).lower()
        if 'urdu' in v_low: lang='ur'
        elif 'hindi' in v_low: lang='hi'
        elif 'arabic' in v_low: lang='ar'
        elif 'russian' in v_low: lang='ru'
        elif 'turkish' in v_low: lang='tr'
        gTTS(text=tx[:400], lang=lang, slow=False).save(out)
        if os.path.exists(out) and os.path.getsize(out) > 1000: return True
    except: pass
    return False

def detect_voice(ch, selected):
    if "AUTO" in selected: return VOICES["Urdu Male (Asad - Deep Voice / Narrative Style)"]
    return VOICES.get(selected, "en-US-GuyNeural")

def SMART_KEYWORD_ENGINE(sentence):
    s = sentence.strip().lower()
    s = re.sub(r'[^\w\s]', ' ', s)
    words = [w for w in s.split() if len(w) > 3][:5]
    q = " ".join(words) if words else "cinematic story"
    return [q, f"{q} cinematic", "cinematic background"]

# ========== MAIN PROCESS ==========
print(f"🎙️ Voice: {voice_lang} | Mode: {video_mode}")
cs, kws = clean_analyze(script)
W, H = (1280,720) if "16:9" in video_type else (720,1280)
if "480" in resolution: W, H = (854,480) if W>H else (480,854)
bgm_path = get_niche_music(script)
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
        print(f"🔑 {smart_queries}")
        dur = au.duration
        clip = get_clip_from_platforms(smart_queries, dur, W, H, idx)
        base_clip = clip.set_duration(dur).set_audio(au)
        if bgm_path:
            try:
                bgm = AudioFileClip(bgm_path).subclip(0, dur).fx(volumex, 0.20)
                base_clip = base_clip.set_audio(CompositeAudioClip([au,bgm]))
            except: pass
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
        print(f"✅ Scene {idx+1} Done")
        try: base_clip.close(); final_scene.close(); au.close()
        except: pass
        gc.collect()
    except Exception as e: print(f"❌ Scene {idx+1} Error {e}"); continue

if scene_files:
    print(f"\n🔗 FINAL JOINING {len(scene_files)} scenes...")
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
