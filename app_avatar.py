# JSM AVATAR V2 - 5 Human Avatars + Light LipSync Pulse - By Saeed
import asyncio, uuid, random, requests, re, os, urllib.parse, datetime, time, json, gc, math
import nest_asyncio
nest_asyncio.apply()
from moviepy.editor import VideoFileClip, ColorClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip, TextClip, ImageClip
from PIL import Image

# --- 5 REAL HUMAN AVATARS (Free AI Generated - Transparent) ---
AVATAR_LIBRARY = {
    "1 - Young Boy - Hoodie (Motivational)": "https://raw.githubusercontent.com/sajan3399133cpu/JSM/main/avatar1.png",
    "2 - Business Man - Suit (Finance)": "https://raw.githubusercontent.com/sajan3399133cpu/JSM/main/avatar2.png",
    "3 - Beard Boy - Casual (YouTube)": "https://raw.githubusercontent.com/sajan3399133cpu/JSM/main/avatar3.png",
    "4 - Girl - Professional (News)": "https://raw.githubusercontent.com/sajan3399133cpu/JSM/main/avatar4.png",
    "5 - Old Man - Wise (Story)": "https://raw.githubusercontent.com/sajan3399133cpu/JSM/main/avatar5.png"
}

SHEET_ID = "1wANoZUC8GOi4BSXQRalm2gKrhP8SDLCy_CfCaSWMkEQ"
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyfopJoiGBueO6AsZ5JE-juplXjSa1Lc_klKn4bOswLyhPmPGsvOhT9r6Axow6rsl-rXg/exec"
def cut_mints_auto(email, mins):
    try: requests.get(f"{WEB_APP_URL}?email={urllib.parse.quote(email)}&mins={mins}", timeout=15)
    except: pass

PIXABAY_KEY = "56386293-14facd94fdac26f9fc37f5f2c"
PEXELS_KEYS = ["ROKJvfYuuSkc7QVVL6VjCgYFyB8UQZCLLCctD2SfTJcIrDGo5Ex3JMX6","zniYyavhal66VGwuV2kUIpRm7vG3Y0rddDLuzrITvmPqQ26kdG0vcyy0","f6IKxrHR8MHj1geD62crLTfDTQX0s7ewFkw3hEI4d4CenRTZXCkpCWD9"]

VOICES = {
    "English Male (Andrew - Professional Studio)": "en-US-AndrewNeural",
    "English Male (Brandon - Human Natural)": "en-US-BrandonNeural",
    "English Female (Jenny - Clear & Energetic)": "en-US-JennyNeural",
    "Urdu Male (Asad - Deep Voice / Narrative Style)": "ur-PK-AsadNeural",
    "Hindi Male (Arjun - Motivational Speaker Style)": "hi-IN-ArjunNeural",
}
CATEGORIES_MAP = {"motivational": ["motivation","success"],"finance_stock": ["stock market","trading"],"business": ["business","elon musk"],"farming": ["tractor","farmer"],"youtube": ["youtube","earn money"],"news": ["news"],"food": ["cooking","food"]}

BASE_DIR = "./JSM_Outputs"
os.makedirs(BASE_DIR, exist_ok=True)
USED_VIDEOS = set()

def clean_analyze(script):
    clean = re.sub(r"(sex\s*video|porn|xxx|nude|naked)", " ", script, flags=re.I)
    raw_sentences = re.split(r'[.!?\n\u06d4]+', clean)
    return clean, [s.strip() for s in raw_sentences if len(s.strip()) > 8]

def SMART_KEYWORD_ENGINE(sentence):
    s_low = sentence.lower()
    if "elon musk" in s_low: return ["Elon Musk SpaceX launch"]
    words = [w for w in re.sub(r'[^\w\s]', ' ', s_low).split() if len(w)>3][:2]
    return [f"{' '.join(words)} cinematic HD"] if words else ["cinematic background HD"]

def download_clip(url, W, H):
    try:
        if url in USED_VIDEOS: return None
        t_path = f"{BASE_DIR}/{uuid.uuid4().hex[:6]}.mp4"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        if res.status_code == 200 and len(res.content) > 50000:
            with open(t_path, 'wb') as f: f.write(res.content)
            USED_VIDEOS.add(url)
            return VideoFileClip(t_path).resize((W, H))
    except: pass
    return None

def get_clip_from_platforms(smart_queries, duration, W, H, clip_index):
    clips_to_join = []
    time_covered = 0
    q_idx = 0
    while time_covered < duration:
        q = smart_queries[q_idx % len(smart_queries)]; q_idx+=1; found_clip=None
        for key in PEXELS_KEYS:
            try:
                hdr = {"Authorization": key}; ori = "landscape" if W>H else "portrait"
                r = requests.get(f"https://api.pexels.com/videos/search?query={urllib.parse.quote(q)}&per_page=3&orientation={ori}", headers=hdr, timeout=8).json()
                if r.get('videos'):
                    for vid in r['videos']:
                        link = vid['video_files'][0]['link']
                        if link in USED_VIDEOS: continue
                        cl = download_clip(link, W, H)
                        if cl: found_clip=cl; break
                    if found_clip: break
            except: continue
        if not found_clip:
            try:
                r = requests.get(f"https://pixabay.com/api/videos/?key={PIXABAY_KEY}&q={urllib.parse.quote(q)}&per_page=5", timeout=8).json()
                if r.get('hits'):
                    for hit in r['hits']:
                        url = hit['videos']['medium']['url']
                        if url in USED_VIDEOS: continue
                        cl = download_clip(url, W, H)
                        if cl: found_clip=cl; break
            except: pass
        if not found_clip:
            p_path = f"{BASE_DIR}/fallback_{uuid.uuid4().hex[:4]}.jpg"
            try:
                url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(q[:100])}?width={W}&height={H}&model=flux"
                r = requests.get(url, timeout=15); open(p_path,'wb').write(r.content)
                found_clip = ImageClip(p_path).set_duration(4).resize((W,H))
            except: found_clip = ColorClip((W,H), color=(15,18,24), duration=4)
        cut_len = min(random.uniform(3.0, 4.5), duration - time_covered)
        if found_clip.duration > cut_len:
            start = random.uniform(0, max(0.1, found_clip.duration-cut_len-0.1))
            found_clip = found_clip.subclip(start, start+cut_len)
        clips_to_join.append(found_clip.set_duration(cut_len).resize((W,H)))
        time_covered += cut_len
        if len(clips_to_join) >= 6: break
    return concatenate_videoclips(clips_to_join, method="compose").set_duration(duration) if len(clips_to_join)>1 else clips_to_join[0].set_duration(duration)

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
        except: time.sleep(0.8)
    try:
        from gtts import gTTS
        v_low = str(globals().get('voice_lang','')).lower()
        lang = 'ur' if 'urdu' in v_low else 'hi' if 'hindi' in v_low else 'en'
        gTTS(text=tx[:350], lang=lang, slow=False).save(out)
        return True
    except: return False

def detect_voice(ch, selected): return VOICES.get(selected, "en-US-BrandonNeural")

# --- NEW LIGHTWEIGHT TALKING AVATAR LOGIC ---
def get_avatar_clip(duration, W, H):
    try:
        mode = globals().get('avatar_mode','')
        selected_avatar = globals().get('selected_avatar','1 - Young Boy - Hoodie (Motivational)')
        if "No Avatar" in mode: return None

        # Get URL from library
        avatar_url = AVATAR_LIBRARY.get(selected_avatar, list(AVATAR_LIBRARY.values())[0])
        local_path = f"{BASE_DIR}/avatar_{selected_avatar.split()[0]}.png"

        if not os.path.exists(local_path):
            r = requests.get(avatar_url, timeout=15)
            if r.status_code==200: open(local_path,'wb').write(r.content)

        if not os.path.exists(local_path): return None

        # Talking Effect - Pulse like real talking (Halka hai, RAM nahi khata)
        def talking_effect(t):
            # Fast pulse when talking - lipsync illusion
            pulse = 1 + 0.015 * math.sin(t * 12) + 0.008 * math.sin(t * 20)
            return pulse

        av_w = int(W*0.32) # Thora bara taake human lage
        av_h = int(av_w * 1.25)
        avatar = ImageClip(local_path).set_duration(duration)
        avatar = avatar.resize((av_w, av_h))
        # Pulse effect
        avatar = avatar.resize(lambda t: talking_effect(t))
        # Position - Bottom Right (Professional YouTube style)
        avatar = avatar.set_pos((0.67, 0.55), relative=True)
        return avatar
    except Exception as e:
        print(f"Avatar error: {e}")
        return None

print(f"🎙️ Voice: {voice_lang} | Avatar: {globals().get('selected_avatar','')} | Mode: {video_mode}")
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
        avatar_clip = get_avatar_clip(dur, W, H)
        if avatar_clip and "Only" in avatar_mode:
            base_clip = ColorClip((W,H), color=(10,10,15), duration=dur)
            base_clip = CompositeVideoClip([base_clip, avatar_clip.set_position('center')]).set_duration(dur)
        elif avatar_clip:
            base_clip = CompositeVideoClip([clip.set_duration(dur), avatar_clip]).set_duration(dur)
        else:
            base_clip = clip.set_duration(dur)
        base_clip = base_clip.set_audio(au)
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
        time.sleep(0.2) # Halka sa rest taake mobile garam na ho
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
