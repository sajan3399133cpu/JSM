# JSM V9 FINAL - ULTRA CLEAN - RAM/DISK CLEAR + WATER SEARCH - By Jam Saeed
import os, uuid, random, requests, re, urllib.parse, datetime, time, gc, shutil
import asyncio
import nest_asyncio
nest_asyncio.apply()
from moviepy.editor import VideoFileClip, ColorClip, AudioFileClip, CompositeVideoClip, TextClip

# 1. DISK BILKUL SAAF - Pehle ka kachra khatam
BASE_DIR = "/tmp/JSM_Outputs"
if os.path.exists(BASE_DIR):
    try: shutil.rmtree(BASE_DIR)
    except: pass
os.makedirs(BASE_DIR, exist_ok=True)
for f in ["/tmp/FINAL_JSM.mp4", "/tmp/JSM_V8_FINAL.mp4"]:
    if os.path.exists(f):
        try: os.remove(f)
        except: pass

USED_LINKS = set()
GROQ_KEY = globals().get('groq_api_key','').strip()
PEXELS_KEYS = globals().get('pexels_keys', [])
PIXABAY_KEY = globals().get('pixabay_key','').strip()

if isinstance(PEXELS_KEYS, str):
    PEXELS_KEYS = [k.strip() for k in PEXELS_KEYS.split(',') if len(k.strip())>10]
else:
    PEXELS_KEYS = [str(k).strip() for k in PEXELS_KEYS if len(str(k).strip())>10]

print(f"✅ CLEAN START | RAM FREE | DISK CLEAR | Groq={'ON' if GROQ_KEY else 'OFF'} Pexels={len(PEXELS_KEYS)}")

VOICES = {"English Male (Brandon)": "en-US-BrandonNeural","Trailer Voice": "en-US-GuyNeural","Urdu Male (Asad)": "ur-PK-AsadNeural"}

# --- V9 INTELLIGENT BRAIN - NEW MODEL ---
def get_keywords_v9(sentence):
    if GROQ_KEY and len(GROQ_KEY)>20:
        try:
            headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
            data = {
                "model": "llama-3.1-8b-instant", # NEW MODEL - FIXED
                "messages": [
                    {"role": "system", "content": "You are viral video editor. For a motivational sentence, give 3 stock video search queries that MATCH the exact visual. Example: 'slept on factory floor' -> factory worker sleeping floor, tesla factory night, hustle working late. Return ONLY 3 comma separated queries."},
                    {"role": "user", "content": sentence}
                ],
                "temperature": 0.3,
                "max_tokens": 80
            }
            r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data, timeout=15)
            if r.status_code==200:
                text = r.json()['choices'][0]['message']['content']
                kws = [k.strip().strip('"').strip("'") for k in text.split(',') if len(k.strip())>2][:3]
                if kws:
                    print(f"🧠 V9 BRAIN: {kws}")
                    return kws
            else:
                print(f"Groq {r.status_code}: {r.text[:100]}")
        except Exception as e:
            print(f"Brain err {e}")

    # ULTRA SMART FALLBACK - Topic wise
    low = sentence.lower()
    if "factory" in low and "sleep" in low: return ["tesla factory worker sleeping floor", "man working late night factory", "elon musk hard work"]
    if "100 hour" in low or "worked" in low: return ["entrepreneur working late night office", "hustle working dark", "man working computer night"]
    if "success" in low: return ["success businessman top mountain", "successful man celebration", "winner motivational"]
    if "fail" in low: return ["failure alone dark sad", "struggle businessman", "rising from failure"]
    if "team" in low: return ["business team startup working", "team meeting success"]
    if "money" in low or "wealth" in low or "buffett" in low: return ["warren buffett money wealth", "rich businessman luxury", "money counting"]
    if "mirror" in low or "3 am" in low: return ["woman scary mirror night", "3am horror mirror", "lipstick mirror writing"]
    words = [w for w in re.sub(r'[^\w\s]',' ',low).split() if len(w)>3][:3]
    return [f"{' '.join(words)} cinematic", f"{words[0]} business motivational", f"{words[0]} dark moody"]

# --- WATER LIKE SEARCHING - PAANI KI TARAH TEZ ---
def water_search(keyword, W, H):
    orientation = "landscape" if W>H else "portrait"
    random.shuffle(PEXELS_KEYS) # Har bar nayi key se start - paani ki tarah

    # Pexels - Fast search
    for p_key in PEXELS_KEYS:
        try:
            headers = {"Authorization": p_key}
            # yeh yeh yeh searching...
            url = f"https://api.pexels.com/videos/search?query={urllib.parse.quote(keyword)}&per_page=2&orientation={orientation}&size=medium"
            res = requests.get(url, headers=headers, timeout=8).json() # Timeout kam - tez
            for vid in res.get('videos', []):
                vfiles = vid.get('video_files', [])
                if not vfiles: continue
                # Medium quality lo - tez download
                link = sorted(vfiles, key=lambda x: x.get('width',0))[1 if len(vfiles)>1 else 0]['link']
                if link in USED_LINKS: continue
                path = f"{BASE_DIR}/{uuid.uuid4().hex[:5]}.mp4"
                vr = requests.get(link, headers={"User-Agent": "Mozilla/5.0"}, timeout=12, stream=True)
                if vr.status_code==200:
                    with open(path,'wb') as f:
                        for chunk in vr.iter_content(8192): f.write(chunk)
                    if os.path.getsize(path)>40000:
                        USED_LINKS.add(link)
                        clip = VideoFileClip(path).resize((W,H))
                        print(f"💧 WATER HIT: '{keyword}' -> {vid['id']}")
                        return clip
        except: continue
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
    return False

# MAIN
sentences = [s.strip() for s in re.split(r'[.!?\n\u06d4]+', script) if len(s.strip())>12]
W,H = (1280,720) if "16:9" in video_type else (720,1280)
if "480" in resolution: W,H = (854,480) if W>H else (480,854)

scene_files = []
for idx, sent in enumerate(sentences):
    try:
        print(f"\n🌊 SCENE {idx+1}/{len(sentences)} | {sent[:60]}...")
        keywords = get_keywords_v9(sent)
        ap = f"{BASE_DIR}/{uuid.uuid4().hex[:4]}.mp3"
        if not run_tts(sent, ap, VOICES.get(voice_lang, "en-US-BrandonNeural")): continue
        au = AudioFileClip(ap)
        dur = max(3.2, au.duration+0.2)

        vclip = None
        for kw in keywords: # yun yun yun searching
            vclip = water_search(kw, W, H)
            if vclip: break
        if not vclip: vclip = ColorClip((W,H), color=(14,14,18), duration=dur)

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

        # RAM BILKUL SAAF - Har scene ke baad
        try:
            vclip.close(); final.close(); au.close()
            del vclip, final, au
        except: pass
        gc.collect()
        if os.path.exists(ap):
            try: os.remove(ap)
            except: pass

    except Exception as e:
        print(f"Err {e}")
        gc.collect()
        continue

if scene_files:
    print(f"\n🔗 FINAL JOIN + DISK CLEAR...")
    list_path = f"{BASE_DIR}/list.txt"
    with open(list_path,"w", encoding='utf-8') as f:
        for sf in scene_files: f.write(f"file '{os.path.abspath(sf)}'\n")
    final_out = f"/tmp/JSM_V9_WATER_{datetime.datetime.now().strftime('%H%M%S')}.mp4"
    os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c copy {final_out}")
    if not os.path.exists(final_out) or os.path.getsize(final_out)<5000:
        os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c:v libx264 -preset ultrafast -c:a aac {final_out}")

    # DISK CLEAR - Scene files delete
    try:
        shutil.rmtree(BASE_DIR)
        print("🧹 DISK CLEANED!")
    except: pass
    gc.collect()

    print(f"🎉 READY {final_out}")
    try:
        from google.colab import files
        files.download(final_out)
    except: pass
