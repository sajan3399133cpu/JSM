# JSM V10 FINAL - 25 LANG + BEST HUMAN VOICES + WATER SEARCH - By Jam Saeed
import os, uuid, random, requests, re, urllib.parse, datetime, time, gc, shutil
import asyncio
import nest_asyncio
nest_asyncio.apply()
from moviepy.editor import VideoFileClip, ColorClip, AudioFileClip, CompositeVideoClip, TextClip

# --- DISK / RAM BILKUL SAAF ---
BASE_DIR = "/tmp/JSM_Outputs"
if os.path.exists(BASE_DIR):
    try: shutil.rmtree(BASE_DIR)
    except: pass
os.makedirs(BASE_DIR, exist_ok=True)
USED_LINKS = set()

GROQ_KEY = globals().get('groq_api_key','').strip()
PEXELS_KEYS = globals().get('pexels_keys', [])
PIXABAY_KEY = globals().get('pixabay_key','').strip()

if isinstance(PEXELS_KEYS, str):
    PEXELS_KEYS = [k.strip() for k in PEXELS_KEYS.split(',') if len(k.strip())>10]
else:
    PEXELS_KEYS = [str(k).strip() for k in PEXELS_KEYS if len(str(k).strip())>10]

# --- 25 LANGUAGES - BEST HUMAN VOICES (EDGE TTS) ---
VOICES = {
    # English - Best Motivational / YouTuber Voices
    "English Male - Brandon (Motivational)": "en-US-BrandonNeural",
    "English Male - Guy (Trailer Voice)": "en-US-GuyNeural",
    "English Male - Davis (Deep)": "en-US-DavisNeural",
    "English Female - Jenny (Clear)": "en-US-JennyNeural",
    "English Female - Aria (YouTuber)": "en-US-AriaNeural",
    "English UK Male - Ryan (British)": "en-GB-RyanNeural",
    # Hindi / Urdu / Pakistan
    "Hindi Male - Arjun": "hi-IN-ArjunNeural",
    "Hindi Female - Ananya": "hi-IN-AnanyaNeural",
    "Urdu Male - Asad (Pakistan)": "ur-PK-AsadNeural",
    "Urdu Female - Uzma (Pakistan)": "ur-PK-UzmaNeural",
    # Arabic
    "Arabic Male - Hamed (Saudi)": "ar-SA-HamedNeural",
    "Arabic Female - Zariyah (Saudi)": "ar-SA-ZariyahNeural",
    # Russian
    "Russian Male - Dmitry": "ru-RU-DmitryNeural",
    "Russian Female - Svetlana": "ru-RU-SvetlanaNeural",
    # Spanish / French / German
    "Spanish Male - Jorge": "es-ES-JorgeNeural",
    "Spanish Female - Elvira": "es-ES-ElviraNeural",
    "French Male - Henri": "fr-FR-HenriNeural",
    "French Female - Denise": "fr-FR-DeniseNeural",
    "German Male - Conrad": "de-DE-ConradNeural",
    "German Female - Katja": "de-DE-KatjaNeural",
    # Turkish / Portuguese / Italian / Indonesian
    "Turkish Male - Ahmet": "tr-TR-AhmetNeural",
    "Turkish Female - Emel": "tr-TR-EmelNeural",
    "Portuguese Male - Antonio (Brazil)": "pt-BR-AntonioNeural",
    "Italian Male - Diego": "it-IT-DiegoNeural",
    "Indonesian Male - Ardi": "id-ID-ArdiNeural",
}

print(f"✅ V10 START | 25 Voices Loaded | Groq={'ON' if GROQ_KEY else 'OFF'} Pexels={len(PEXELS_KEYS)}")

# --- V10 BRAIN - FIXED MODEL ---
def get_keywords_v10(sentence):
    if GROQ_KEY and len(GROQ_KEY)>20:
        try:
            headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
            data = {
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": "You are viral stock video expert. Give 3 short stock video search queries matching EXACT visual of sentence. Example: 'slept on factory floor' -> factory worker sleeping floor, elon musk working night, hustle sleeping factory. Return ONLY 3 comma separated queries."},
                    {"role": "user", "content": sentence}
                ],
                "temperature": 0.3, "max_tokens": 80
            }
            r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data, timeout=12)
            if r.status_code==200:
                text = r.json()['choices'][0]['message']['content']
                kws = [k.strip().strip('"').strip("'") for k in text.split(',') if len(k.strip())>2][:3]
                if kws:
                    print(f"🧠 BRAIN: {kws}")
                    return kws
        except Exception as e:
            print(f"Brain Err {e}")

    low = sentence.lower()
    if "factory" in low and "sleep" in low: return ["factory worker sleeping floor", "tesla factory night", "entrepreneur sleeping factory"]
    if "100 hour" in low or "elon" in low: return ["elon musk working night", "man working late office", "hustle night work"]
    if "moon" in low or "armstrong" in low: return ["apollo 11 moon landing", "astronaut moon", "nasa moon landing"]
    if "mirror" in low or "3 am" in low: return ["woman scary mirror night", "red lipstick mirror", "3am mirror horror"]
    if "wealth" in low or "buffett" in low: return ["warren buffett money", "rich businessman", "stock market wealth"]
    if "success" in low: return ["success businessman mountain top", "winner celebration", "motivational success"]
    if "fail" in low: return ["failure sad businessman", "struggle dark", "rising from failure"]
    words = [w for w in re.sub(r'[^\w\s]',' ',low).split() if len(w)>3][:3]
    if not words: words=["motivational business"]
    return [f"{' '.join(words)} cinematic", f"{words[0]} motivational", f"business {words[0]}"]

# --- WATER SEARCH + VIDEO + LOGS ---
def water_search(keyword, W, H):
    orientation = "landscape" if W>H else "portrait"
    if not PEXELS_KEYS:
        print("❌ NO KEYS!")
        return None
    random.shuffle(PEXELS_KEYS)
    for idx, p_key in enumerate(PEXELS_KEYS):
        try:
            headers = {"Authorization": p_key}
            url = f"https://api.pexels.com/videos/search?query={urllib.parse.quote(keyword)}&per_page=2&orientation={orientation}&size=medium"
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code==429:
                print(f" ⏳ Key {idx+1} Limit Khatam")
                continue
            if r.status_code==401:
                print(f" 💀 Key {idx+1} Invalid/Mar Gayi")
                continue
            res = r.json()
            vids = res.get('videos', [])
            if not vids:
                print(f" 🔍 Key {idx+1} '{keyword}' -> 0 videos")
                continue
            print(f" 📹 Key {idx+1} '{keyword}' -> {len(vids)} videos")
            for vid in vids:
                vfiles = vid.get('video_files', [])
                if not vfiles: continue
                link = sorted(vfiles, key=lambda x: x.get('width',0))[0]['link']
                if link in USED_LINKS: continue
                path = f"{BASE_DIR}/{uuid.uuid4().hex[:5]}.mp4"
                vr = requests.get(link, timeout=15, stream=True)
                if vr.status_code==200:
                    with open(path,'wb') as f:
                        for chunk in vr.iter_content(8192): f.write(chunk)
                    if os.path.getsize(path)>40000:
                        USED_LINKS.add(link)
                        print(f" 💧 WATER HIT ID {vid['id']} for '{keyword}'")
                        return VideoFileClip(path).resize((W,H))
        except Exception as e:
            print(f" ❌ Key {idx+1} Err {e}")
            continue
    return None

async def Tt(t,o,v):
    import edge_tts
    await edge_tts.Communicate(t,v, rate="-4%", pitch="+1Hz").save(o)
def run_tts(tx,out,vc):
    if len(tx.split())<2: tx=tx+"."
    for _ in range(2):
        try:
            try: asyncio.run(Tt(tx,out,vc))
            except:
                loop=asyncio.new_event_loop(); asyncio.set_event_loop(loop); loop.run_until_complete(Tt(tx,out,vc))
            if os.path.exists(out) and os.path.getsize(out)>500: return True
        except: time.sleep(0.2)
    try:
        from gtts import gTTS
        gTTS(text=tx[:300], lang='en', slow=False).save(out)
        return os.path.exists(out) and os.path.getsize(out)>500
    except: return False

# --- MAIN LOOP - BRAIN + VIDEO DONO ---
sentences = [s.strip() for s in re.split(r'[.!?\n\u06d4]+', script) if len(s.strip())>12]
W,H = (1280,720) if "16:9" in video_type else (720,1280)
if "480" in resolution: W,H = (854,480) if W>H else (480,854)

scene_files=[]
for idx, sent in enumerate(sentences):
    try:
        print(f"\n🌊 SCENE {idx+1}/{len(sentences)}: {sent[:70]}")
        keywords = get_keywords_v10(sent)

        ap = f"{BASE_DIR}/{uuid.uuid4().hex[:4]}.mp3"
        voice_code = VOICES.get(voice_lang, "en-US-BrandonNeural")
        if not run_tts(sent, ap, voice_code):
            print("❌ TTS Fail")
            continue
        au = AudioFileClip(ap)
        dur = max(3.2, au.duration+0.2)

        vclip=None
        for kw in keywords:
            vclip = water_search(kw, W, H)
            if vclip: break

        if not vclip:
            print(f"⚠️ No video for {keywords}, using Color")
            vclip = ColorClip((W,H), color=(14,14,18), duration=dur)

        if vclip.duration>dur:
            s = random.uniform(0, max(0.1, vclip.duration-dur-0.1))
            vclip = vclip.subclip(s, s+dur)
        vclip = vclip.set_duration(dur).resize((W,H)).set_audio(au)

        layers=[vclip]
        if globals().get('show_subtitles', True):
            try:
                txt = TextClip(sent[:115], fontsize=int(W*0.038), color='white', stroke_color='black', stroke_width=2, method='caption', size=(int(W*0.82),None), align='center').set_duration(dur).set_pos(('center',0.82), relative=True)
                layers.append(txt)
            except: pass

        final = CompositeVideoClip(layers, size=(W,H)).set_duration(dur)
        out = f"{BASE_DIR}/scene_{idx}.mp4"
        final.write_videofile(out, fps=24, codec='libx264', audio_codec='aac', preset='ultrafast', threads=2, bitrate="1200k", logger=None)
        scene_files.append(out)
        print(f"✅ SCENE {idx+1} DONE")

        try: vclip.close(); final.close(); au.close(); del vclip, final, au
        except: pass
        gc.collect()
        try: os.remove(ap)
        except: pass

    except Exception as e:
        print(f"❌ SCENE {idx+1} Err {e}")
        gc.collect()
        continue

if scene_files:
    print(f"\n🔗 JOINING {len(scene_files)} SCENES...")
    list_path = f"{BASE_DIR}/list.txt"
    with open(list_path,"w", encoding='utf-8') as f:
        for sf in scene_files: f.write(f"file '{os.path.abspath(sf)}'\n")
    final_out = f"/tmp/JSM_V10_FINAL_{datetime.datetime.now().strftime('%H%M%S')}.mp4"
    os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c copy {final_out}")
    if not os.path.exists(final_out) or os.path.getsize(final_out)<5000:
        os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c:v libx264 -preset ultrafast -c:a aac {final_out}")

    try: shutil.rmtree(BASE_DIR); print("🧹 DISK + RAM CLEANED!")
    except: pass
    gc.collect()
    print(f"🎉🎉 FINAL VIDEO: {final_out}")
    try:
        from google.colab import files
        files.download(final_out)
    except: pass
else:
    print("❌ NO SCENES!")
