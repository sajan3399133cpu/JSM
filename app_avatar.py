# JSM V8 FINAL - MULTI SOURCE INTELLIGENT - GITHUB FILE - By Jam Saeed
import os, uuid, random, requests, re, urllib.parse, datetime, time, gc
import asyncio
import nest_asyncio
nest_asyncio.apply()
from moviepy.editor import VideoFileClip, ColorClip, AudioFileClip, CompositeVideoClip, TextClip

BASE_DIR = "/tmp/JSM_Outputs"
os.makedirs(BASE_DIR, exist_ok=True)
USED_LINKS = set()

# --- KEYS COLAB SE AYENGI - YAHAN HARDCODE NAHI ---
GROQ_KEY = globals().get('groq_api_key','').strip()
PEXELS_KEYS = globals().get('pexels_keys', [])
PIXABAY_KEY = globals().get('pixabay_key','').strip()
COVERR_KEY = globals().get('coverr_api_key','').strip()

# Agar string me aayi to list banao + space clean
if isinstance(PEXELS_KEYS, str):
    PEXELS_KEYS = [k.strip() for k in PEXELS_KEYS.split(',') if len(k.strip())>10]
else:
    PEXELS_KEYS = [str(k).strip() for k in PEXELS_KEYS if len(str(k).strip())>10]

print(f"🔑 LOADED: Groq={'ON' if GROQ_KEY else 'OFF'} | Pexels={len(PEXELS_KEYS)} keys | Pixabay={'ON' if PIXABAY_KEY else 'OFF'} | Coverr={'ON' if COVERR_KEY else 'OFF'}")

VOICES = {
    "English Male (Brandon)": "en-US-BrandonNeural",
    "English Female (Jenny)": "en-US-JennyNeural",
    "Trailer Voice": "en-US-GuyNeural",
    "Urdu Male (Asad)": "ur-PK-AsadNeural",
    "Hindi Male (Arjun)": "hi-IN-ArjunNeural"
}

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyfopJoiGBueO6AsZ5JE-juplXjSa1Lc_klKn4bOswLyhPmPGsvOhT9r6Axow6rsl-rXg/exec"
def cut_mints_auto(email, mins):
    try: requests.get(f"{WEB_APP_URL}?email={urllib.parse.quote(email)}&mins={mins}", timeout=10)
    except: pass

# --- INTELLIGENT BRAIN ---
def get_intelligent_keywords(sentence):
    if GROQ_KEY and len(GROQ_KEY) > 20:
        try:
            print(f"🧠 BRAIN Thinking: {sentence[:60]}...")
            headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
            data = {
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": "You are stock video expert. Convert motivational sentence to 3 highly relevant stock video search queries (2-4 words each). Return ONLY comma separated keywords. Example: 'He worked while world slept' -> man working late night, hustle in dark office, entrepreneur night"},
                    {"role": "user", "content": sentence}
                ],
                "temperature": 0.2,
                "max_tokens": 70
            }
            r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data, timeout=12)
            if r.status_code == 200:
                text = r.json()['choices'][0]['message']['content']
                kws = [k.strip().strip('"').strip("'") for k in text.split(',') if len(k.strip())>2][:3]
                print(f"✅ BRAIN Keywords: {kws}")
                return kws
            else:
                print(f"Groq Error {r.status_code}: {r.text[:150]}")
        except Exception as e:
            print(f"Brain Error: {e}")

    # Fallback Smart Brain
    low = sentence.lower()
    if "sleep" in low and ("factory" in low or "work" in low): return ["man working late night office", "factory worker night shift", "entrepreneur sleeping factory"]
    if "fail" in low: return ["failure sad businessman", "man alone dark struggle", "overcoming failure motivational"]
    if "success" in low or "rich" in low: return ["success businessman mountain top", "rich businessman luxury", "achievement celebration"]
    if "team" in low: return ["business team meeting", "startup team working"]
    if "elon" in low or "musk" in low: return ["elon musk working", "spacex factory worker", "tesla hard work"]
    words = [w for w in re.sub(r'[^\w\s]', ' ', low).split() if len(w)>3][:3]
    if not words: words = ["motivational"]
    return [f"{' '.join(words)} motivational", f"business {words[0]}", f"{words[0]} cinematic broll"]

# --- MULTI SOURCE VIDEO SEARCH ---
def search_video(keyword, W, H):
    orientation = "landscape" if W>H else "portrait"

    # 1. PEXELS - Try all keys one by one
    for p_key in PEXELS_KEYS:
        try:
            headers = {"Authorization": p_key}
            url = f"https://api.pexels.com/videos/search?query={urllib.parse.quote(keyword)}&per_page=3&orientation={orientation}&size=medium"
            res = requests.get(url, headers=headers, timeout=12).json()
            for vid in res.get('videos', []):
                # best file
                vfiles = sorted(vid.get('video_files', []), key=lambda x: x.get('width',0), reverse=True)
                if not vfiles: continue
                link = vfiles[0]['link']
                if link in USED_LINKS: continue
                path = f"{BASE_DIR}/{uuid.uuid4().hex[:6]}.mp4"
                vr = requests.get(link, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
                if vr.status_code==200 and len(vr.content)>50000:
                    open(path,'wb').write(vr.content)
                    USED_LINKS.add(link)
                    clip = VideoFileClip(path).resize((W,H))
                    print(f"✅ PEXELS HIT: '{keyword}' -> ID {vid['id']}")
                    return clip
        except Exception as e:
            continue

    # 2. PIXABAY
    if PIXABAY_KEY:
        try:
            url = f"https://pixabay.com/api/videos/?key={PIXABAY_KEY}&q={urllib.parse.quote(keyword)}&per_page=3&orientation={orientation.replace('landscape','horizontal').replace('portrait','vertical')}"
            res = requests.get(url, timeout=12).json()
            for hit in res.get('hits', []):
                link = hit['videos']['medium']['url']
                if link in USED_LINKS: continue
                path = f"{BASE_DIR}/{uuid.uuid4().hex[:6]}.mp4"
                vr = requests.get(link, timeout=20)
                if vr.status_code==200 and len(vr.content)>50000:
                    open(path,'wb').write(vr.content)
                    USED_LINKS.add(link)
                    clip = VideoFileClip(path).resize((W,H))
                    print(f"✅ PIXABAY HIT: '{keyword}'")
                    return clip
        except Exception as e:
            print(f"Pixabay fail {e}")

    return None

async def Tt(t,o,v):
    import edge_tts
    await edge_tts.Communicate(t,v, rate="-4%", pitch="+1Hz").save(o)

def run_tts(tx,out,vc):
    if len(tx.split()) < 2: tx = tx + "."
    for _ in range(2):
        try:
            try: asyncio.run(Tt(tx,out,vc))
            except:
                loop=asyncio.new_event_loop(); asyncio.set_event_loop(loop); loop.run_until_complete(Tt(tx,out,vc))
            if os.path.exists(out) and os.path.getsize(out)>500:
                return True
        except:
            time.sleep(0.3)
    try:
        from gtts import gTTS
        gTTS(text=tx[:300], lang='en', slow=False).save(out)
        return os.path.exists(out) and os.path.getsize(out)>500
    except:
        return False

# --- MAIN PROCESS ---
print("🚀 JSM V8 START...")
sentences = [s.strip() for s in re.split(r'[.!?\n\u06d4]+', script) if len(s.strip())>12]
W,H = (1280,720) if "16:9" in video_type else (720,1280)
if "480" in resolution: W,H = (854,480) if W>H else (480,854)

scene_files = []
for idx, sent in enumerate(sentences):
    try:
        print(f"\n{'='*20} SCENE {idx+1}/{len(sentences)} {'='*20}")
        print(f"SENT: {sent}")
        keywords = get_intelligent_keywords(sent)

        # Audio
        ap = f"{BASE_DIR}/{uuid.uuid4().hex[:5]}.mp3"
        if not run_tts(sent, ap, VOICES.get(voice_lang, "en-US-BrandonNeural")):
            print("TTS Fail skip")
            continue
        au = AudioFileClip(ap)
        dur = max(3.2, au.duration + 0.2)

        # Video - Try intelligent keywords one by one
        vclip = None
        for kw in keywords:
            vclip = search_video(kw, W, H)
            if vclip: break

        if not vclip:
            print(f"❌ No video for {keywords}, using color")
            vclip = ColorClip((W,H), color=(14,14,18), duration=dur)

        if vclip.duration > dur:
            start = random.uniform(0, max(0.1, vclip.duration - dur - 0.2))
            vclip = vclip.subclip(start, start+dur)
        vclip = vclip.set_duration(dur).resize((W,H)).set_audio(au)

        layers = [vclip]
        if globals().get('show_subtitles', True):
            try:
                txt = TextClip(sent[:115], fontsize=int(W*0.038), color='white', stroke_color='black', stroke_width=2, method='caption', size=(int(W*0.82), None), align='center').set_duration(dur).set_pos(('center',0.82), relative=True)
                layers.append(txt)
            except: pass

        final = CompositeVideoClip(layers, size=(W,H)).set_duration(dur)
        out_path = f"{BASE_DIR}/scene_{idx}_{uuid.uuid4().hex[:4]}.mp4"
        final.write_videofile(out_path, fps=24, codec='libx264', audio_codec='aac', preset='ultrafast', threads=2, bitrate="1300k", logger=None)
        scene_files.append(out_path)
        print(f"✅ SCENE {idx+1} DONE")

        try: vclip.close(); final.close(); au.close()
        except: pass
        gc.collect()
        time.sleep(0.2)

    except Exception as e:
        print(f"❌ SCENE {idx+1} Error: {e}")
        import traceback; traceback.print_exc()
        continue

# FINAL JOIN
if scene_files:
    print(f"\n🔗 JOINING {len(scene_files)} SCENES...")
    list_path = f"{BASE_DIR}/concat_list.txt"
    with open(list_path,"w", encoding='utf-8') as f:
        for sf in scene_files:
            f.write(f"file '{os.path.abspath(sf)}'\n")
    final_out = f"/tmp/JSM_V8_FINAL_{datetime.datetime.now().strftime('%H%M%S')}.mp4"
    os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c copy {final_out}")
    if not os.path.exists(final_out) or os.path.getsize(final_out)<5000:
        os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c:v libx264 -preset ultrafast -c:a aac {final_out}")

    print(f"\n🎉🎉 FINAL VIDEO READY: {final_out} 🎉🎉🎉")
    try:
        fc = VideoFileClip(final_out)
        cut_mints_auto(globals().get('email',''), round(fc.duration/60, 2))
        fc.close()
    except: pass
    try:
        from google.colab import files
        files.download(final_out)
    except: pass
else:
    print("❌ No scenes made!")
