import asyncio, uuid, random, requests, re, os, urllib.parse, datetime, time, json, gc
import nest_asyncio
nest_asyncio.apply()
from moviepy.editor import VideoFileClip, ColorClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip, TextClip, CompositeAudioClip, ImageClip
from moviepy.audio.fx.volumex import volumex

SHEET_ID = "1wANoZUC8GOi4BSXQRalm2gKrhP8SDLCy_CfCaSWMkEQ"
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyfopJoiGBueO6AsZ5JE-juplXjSa1Lc_klKn4bOswLyhPmPGsvOhT9r6Axow6rsl-rXg/exec"
def cut_mints_auto(email, mins):
    try:
        if not email or mins <=0: return
        requests.get(f"{WEB_APP_URL}?email={urllib.parse.quote(email)}&mins={mins}", timeout=15)
    except: pass

PIXABAY_KEY = "56386293-14facd94fdac26f9fc37f5f2c"
COVERR_API_KEY = "8c8c592b07a57e05dc49368c399b7659"
PEXELS_KEYS = [
    "ROKJvfYuuSkc7QVVL6VjCgYFyB8UQZCLLCctD2SfTJcIrDGo5Ex3JMX6",
    "zniYvavhal66VGwuV2kUlpRm7vG3Y0rddDLuzrITvmPqQ26kdG0vcyy0",
    "f6IKxrHR8MHj1geD62crLTfDTQX0s7ewFkw3hEI4d4CenRTZXCkpCWD9",
    "1j6kFq1GRB4291F1s1RMghlgIX3d3u78OaTpiDKmtISAyJkKPb9vVTkL",
    "tpkypogswv07n84dh0iaHI9tamu43GEcvZokA3Xi3JSTUT0NV32A6gG9"
]

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

CATEGORIES_MAP = {
    "motivational": ["motivation","success","hard work","rich people","money works","train","winner","dream big","skill","failure","rizq","goal","trophy"],
    "finance_stock": ["stock market","trading","share market","kse 100","trader","forex","crypto","bitcoin","bull market","profit","investment"],
    "business": ["business","corporate","office","meeting","startup","entrepreneur","elon musk","tesla"],
    "farming": ["tractor","khet","kheti","farmer","harvest","crop","field","agriculture"],
    "youtube": ["youtube","youtuber","channel","subscriber","freelancing","earn money online"],
    "news": ["news","breaking news","report","update"],
    "food": ["potato","aloo","gobhi","tomato","tamatar","cooking","chef","food","kitchen","recipe","biryani"]
}

BASE_DIR = "./JSM_Outputs"
os.makedirs(BASE_DIR, exist_ok=True)
USED_VIDEOS = set() # No Repeat Logic

def clean_analyze(script):
    clean = re.sub(r"(sex\s*video|porn|xxx|nude|naked)", " ", script, flags=re.I)
    raw_sentences = re.split(r'[.!?\n\u06d4]+', clean)
    return clean, [s.strip() for s in raw_sentences if len(s.strip()) > 8]

def SMART_KEYWORD_ENGINE(sentence):
    s_low = sentence.lower()
    stop_words = {"just","now","then","that","this","these","those","there","here","will","would","very","really","even","still","also","only","next","see","you","thank","go","pick","one","about","today","video","talk","please","welcome","dosto","bhai","hello","everyone","the","and","you","will","have","is","are","was","were","aaj","hai","ke","ki","ka","aur","mein","ko","se","me","hoga","hain","main","hum","raha","rahe","liye"}
    if "elon musk" in s_low: return ["Elon Musk SpaceX rocket launch ultra realistic", "SpaceX Falcon rocket launch"]
    best_cat=""; best_score=0; matched=[]
    for cat, kws in CATEGORIES_MAP.items():
        score = sum(1 for kw in kws if kw in s_low)
        if score > best_score: best_score=score; matched=[kw for kw in kws if kw in s_low]; best_cat=cat
    clean = re.sub(r'[^\w\s]', ' ', s_low)
    words = [w for w in clean.split() if w not in stop_words and len(w) > 3]
    queries=[]
    if best_score > 0 and matched:
        primary = matched[0]
        if words: queries.append(f"{primary} {words[0]} cinematic HD ultra realistic")
        queries.append(f"{primary} {best_cat} HD")
    else:
        if len(words) >= 2: queries.append(f"{words[0]} {words[1]} cinematic HD ultra realistic")
        elif words: queries.append(f"{words[0]} cinematic HD ultra realistic")
        else: queries.append("cinematic story background HD")
    return list(dict.fromkeys(queries))[:2]

def download_clip(url, W, H, duration):
    try:
        if url in USED_VIDEOS: return None
        t_path = f"{BASE_DIR}/{uuid.uuid4().hex[:6]}.mp4"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        if res.status_code == 200 and len(res.content) > 50000:
            with open(t_path, 'wb') as f: f.write(res.content)
            USED_VIDEOS.add(url)
            clip = VideoFileClip(t_path).resize((W, H))
            return clip
    except: pass
    return None

def get_clip_from_platforms(smart_queries, duration, W, H, clip_index):
    mode = globals().get('video_mode','')

    # === 1. PURE AI MODE - TUMHARA PURANA WALA 100% SAME ===
    if "Pure AI" in mode:
        for q in smart_queries:
            print(f"🤖 AI ONLY: {q}")
            try:
                prompt = f"{q}, ultra realistic 8k cinematic, dramatic lighting, highly detailed, photorealistic, no text, story scene"
                p_path = f"{BASE_DIR}/ai_{uuid.uuid4().hex[:5]}.jpg"
                url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt[:150])}?width={W}&height={H}&seed={random.randint(1,9999999)}&model=flux&enhance=true&nologo=true"
                r = requests.get(url, timeout=45)
                if r.status_code==200 and len(r.content)>8000:
                    open(p_path,'wb').write(r.content)
                    print(f"✅ AI Generated: {q}")
                    return ImageClip(p_path).set_duration(duration).resize((W,H)).resize(lambda t: 1+0.04*t)
            except: continue
        return ColorClip((W,H), color=(12,12,12), duration=duration)

    # === 2. FREE STOCK MODE - HUMAN BRAIN + 4 SEC CUT + NO REPEAT ===
    else:
        clips_to_join = []
        time_covered = 0
        q_idx = 0
        print(f"🧠 HUMAN BRAIN STOCK: {smart_queries}")

        while time_covered < duration:
            q = smart_queries[q_idx % len(smart_queries)]
            q_idx += 1
            found_clip = None

            # Pexels First
            for key in PEXELS_KEYS:
                try:
                    hdr = {"Authorization": key}
                    ori = "landscape" if W>H else "portrait"
                    r = requests.get(f"https://api.pexels.com/videos/search?query={urllib.parse.quote(q)}&per_page=5&orientation={ori}", headers=hdr, timeout=10).json()
                    if r.get('videos'):
                        for vid in r['videos']:
                            link = vid['video_files'][0]['link']
                            if link in USED_VIDEOS: continue
                            cl = download_clip(link, W, H, 10)
                            if cl:
                                found_clip = cl
                                break
                        if found_clip: break
                except: continue

            # Pixabay Second
            if not found_clip:
                try:
                    r = requests.get(f"https://pixabay.com/api/videos/?key={PIXABAY_KEY}&q={urllib.parse.quote(q)}&per_page=10", timeout=10).json()
                    if r.get('hits'):
                        for hit in r['hits']:
                            url = hit['videos']['medium']['url']
                            if url in USED_VIDEOS: continue
                            cl = download_clip(url, W, H, 10)
                            if cl:
                                found_clip = cl
                                break
                except: pass

            if not found_clip:
                # AI fallback as image
                p_path = f"{BASE_DIR}/fallback_{uuid.uuid4().hex[:4]}.jpg"
                try:
                    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(q[:100])}?width={W}&height={H}&model=flux"
                    r = requests.get(url, timeout=20)
                    open(p_path,'wb').write(r.content)
                    found_clip = ImageClip(p_path).set_duration(5).resize((W,H))
                except:
                    found_clip = ColorClip((W,H), color=(15,18,24), duration=5)

            cut_len = min(random.uniform(3.5, 5.0), duration - time_covered)
            if found_clip.duration > cut_len:
                start = random.uniform(0, max(0.1, found_clip.duration-cut_len-0.1))
                found_clip = found_clip.subclip(start, start+cut_len)

            clips_to_join.append(found_clip.set_duration(cut_len).resize((W,H)))
            time_covered += cut_len
            if len(clips_to_join) >= 6: break

        if len(clips_to_join) > 1:
            return concatenate_videoclips(clips_to_join, method="compose").set_duration(duration)
        return clips_to_join[0].set_duration(duration)

#... Baki TTS wala hissa same...
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
        return True
    except: return False
def detect_voice(ch, selected):
    if "AUTO" in selected: return VOICES["Urdu Male (Asad - Deep Voice / Narrative Style)"]
    return VOICES.get(selected, "en-US-GuyNeural")

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
        print(f"🔑 {smart_queries}")
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
