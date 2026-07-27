import asyncio, uuid, random, requests, re, os, urllib.parse, datetime, time, gc
import nest_asyncio
nest_asyncio.apply()
from moviepy.editor import VideoFileClip, ColorClip, AudioFileClip, CompositeVideoClip, TextClip, CompositeAudioClip, ImageClip, concatenate_videoclips

SUPABASE_KEY = "sb_publishable_1W4NK6X7Edacm_eSBIcFDQ_CkT6c4EY"
PIXABAY_KEY = "56386293-14facd94fdac26f9fc37f5f2c"
COVERR_API_KEY = "8c8c592b07a57e05dc49368c3659"
PEXELS_KEYS = [
    "ROKJvfYuuSkc7QVVL6VjCgYFyB8UQZCLLCctD2SfTJcIrDGo5Ex3JMX6",
    "zniYvavhal66VGwuV2kUlpRm7vG3Y0rddDLuzrITvmPqQ26kdG0vcyy0",
    "f6IKxrHR8MHj1geD62crLTfDTQX0s7ewFkw3hEI4d4CenRTZXCkpCWD9",
    "1j6kFq1GRB4291F1s1RMghlgIX3d3u78OaTpiDKmtISAyJkKPb9vVTkL",
    "tpkypogswv07n84dh0iaHI9tamu43GEcvZokA3Xi3JSTUT0NV32A6gG9"
]
BRAND_NAME = "JSM AI BY JAM SAEED MOTHA"

SHEET_ID = "1wANoZUC8GOi4BSXQRalm2gKrhP8SDLCy_CfCaSWMkEQ"
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyfopJoiGBueO6AsZ5JE-juplXjSa1Lc_klKn4bOswLyhPmPGsvOhT9r6Axow6rsl-rXg/exec"
def cut_mints_auto(email, mins):
    try:
        if not email or mins <=0: return
        requests.get(f"{WEB_APP_URL}?email={urllib.parse.quote(email)}&mins={mins}", timeout=15)
    except: pass

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

def analyze_overall_topic(script):
    s = script.lower()
    if any(x in s for x in ["money","rich","finance","business","invest","dollars"]): return "finance business money"
    if any(x in s for x in ["ai","chatgpt","technology","robot","youtube"]): return "technology ai futuristic"
    if any(x in s for x in ["potato","aloo","gobhi","vegetable","kitchen"]): return "vegetable kitchen cute"
    return "cinematic story"

OVERALL_TOPIC = ""
def clean_analyze(script):
    global OVERALL_TOPIC
    OVERALL_TOPIC = analyze_overall_topic(script)
    clean = re.sub(r"(sex\s*video|porn|xxx|nude|naked)", " ", script, flags=re.I)
    raw_sentences = re.split(r'[.!?\n\u06d4]+', clean)
    return clean, [s.strip() for s in raw_sentences if len(s.strip()) > 8]

def SMART_KEYWORD_ENGINE(sentence):
    s = re.sub(r'[^\w\s]', ' ', sentence.lower())
    words = [w for w in s.split() if len(w) > 3][:4]
    core = " ".join(words) if words else "story"
    return [f"{core} {OVERALL_TOPIC}", core, OVERALL_TOPIC]

def get_stock_video_smart(query, W, H):
    for key in PEXELS_KEYS:
        try:
            hdr = {"Authorization": key}
            ori = "landscape" if W>H else "portrait"
            r = requests.get(f"https://api.pexels.com/videos/search?query={urllib.parse.quote(query)}&per_page=3&orientation={ori}", headers=hdr, timeout=10).json()
            if r.get('videos'):
                for vid in r['videos']:
                    link = vid['video_files'][0]['link']
                    t_path = f"{BASE_DIR}/pex_{uuid.uuid4().hex[:4]}.mp4"
                    open(t_path,'wb').write(requests.get(link, timeout=20).content)
                    if os.path.getsize(t_path) > 50000:
                        print(f"✅ PEXELS FOUND: {query[:30]}")
                        return VideoFileClip(t_path).resize((W,H))
        except: continue
    try:
        r = requests.get(f"https://pixabay.com/api/videos/?key={PIXABAY_KEY}&q={urllib.parse.quote(query)}&per_page=3", timeout=10).json()
        if r.get('hits'):
            v_url = r['hits'][0]['videos']['medium']['url']
            t_path = f"{BASE_DIR}/pixa_{uuid.uuid4().hex[:4]}.mp4"
            open(t_path,'wb').write(requests.get(v_url, timeout=15).content)
            if os.path.getsize(t_path) > 50000:
                print(f"✅ PIXABAY FOUND: {query[:30]}")
                return VideoFileClip(t_path).resize((W,H))
    except: pass
    return None

def get_ai_clip(query, duration, W, H):
    try:
        q = urllib.parse.quote(f"{query}, cinematic motion, 8k"[:130])
        url = f"https://image.pollinations.ai/prompt/{q}?model=video&width={W}&height={H}&seed={random.randint(1,999999)}&nologo=true"
        t_path = f"{BASE_DIR}/ai_{uuid.uuid4().hex[:4]}.mp4"
        r = requests.get(url, timeout=60)
        if r.status_code==200 and len(r.content)>20000 and r.content[:2]!=b'\xff\xd8':
            open(t_path,'wb').write(r.content)
            clip = VideoFileClip(t_path).resize((W,H))
            return clip.subclip(0, duration) if clip.duration > duration else clip
    except: pass
    try:
        p_path = f"{BASE_DIR}/img_{uuid.uuid4().hex[:4]}.jpg"
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(query[:100])}?width={W}&height={H}&model=flux&nologo=true"
        r = requests.get(url, timeout=30)
        open(p_path,'wb').write(r.content)
        return ImageClip(p_path).set_duration(duration).resize((W,H)).resize(lambda t: 1+0.04*t)
    except: pass
    return ColorClip((W,H), color=(12,12,12), duration=duration)

# === FINAL 4 SEC CUT LOGIC ===
def get_clip_from_platforms(smart_queries, duration, W, H, clip_index):
    mode = globals().get('video_mode','Smart Stock + AI Mix')
    if "Pure AI" in mode:
        return get_ai_clip(smart_queries[0], duration, W, H)

    clips_to_join = []
    time_covered = 0
    q_idx = 0
    print(f" ✂️ Building {duration:.1f}s with 4-sec cuts")

    while time_covered < duration:
        q = smart_queries[q_idx % len(smart_queries)]
        q_idx += 1
        stock = get_stock_video_smart(q, W, H)
        if not stock:
            stock = get_ai_clip(q, 5, W, H)

        cut_len = min(random.uniform(3.5, 5.0), duration - time_covered)
        if stock.duration > cut_len:
            start = random.uniform(0, max(0.1, stock.duration - cut_len - 0.1))
            stock = stock.subclip(start, start + cut_len)

        clips_to_join.append(stock.set_duration(cut_len).resize((W,H)))
        time_covered += cut_len
        if len(clips_to_join) >= 6: break

    if len(clips_to_join) > 1:
        return concatenate_videoclips(clips_to_join, method="compose").set_duration(duration)
    return clips_to_join[0].set_duration(duration)

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
    return False
def detect_voice(ch, selected):
    if "AUTO" in selected: return VOICES["Urdu Male (Asad - Deep Voice / Narrative Style)"]
    return VOICES.get(selected, "en-US-GuyNeural")

print(f"🎙️ Voice: {voice_lang} | Mode: {video_mode} | Topic: {OVERALL_TOPIC}")
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
