# JSM PURE AI TRAILER V1 - 100% FREE UNLIMITED - Pollinations FIXED - By Saeed
import asyncio, uuid, random, requests, re, os, urllib.parse, datetime, time, gc
import nest_asyncio
nest_asyncio.apply()
from moviepy.editor import VideoFileClip, ColorClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip, TextClip, ImageClip
from PIL import Image

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyfopJoiGBueO6AsZ5JE-juplXjSa1Lc_klKn4bOswLyhPmPGsvOhT9r6Axow6rsl-rXg/exec"
def cut_mints_auto(email, mins):
    try: requests.get(f"{WEB_APP_URL}?email={urllib.parse.quote(email)}&mins={mins}", timeout=15)
    except: pass

BASE_DIR = "./JSM_Outputs"
os.makedirs(BASE_DIR, exist_ok=True)

VOICES = {"English Male (Brandon - Human Natural)": "en-US-BrandonNeural","English Female (Jenny - Clear & Energetic)": "en-US-JennyNeural","Urdu Male (Asad - Deep Voice / Narrative Style)": "ur-PK-AsadNeural","Hindi Male (Arjun - Motivational Speaker Style)": "hi-IN-ArjunNeural","English Male (Andrew - Professional Studio)": "en-US-AndrewNeural"}

def clean_analyze(script):
    clean = re.sub(r"(sex\s*video|porn|xxx|nude|naked)", " ", script, flags=re.I)
    raw_sentences = re.split(r'[.!?\n\u06d4]+', clean)
    return clean, [s.strip() for s in raw_sentences if len(s.strip()) > 8]

def SMART_KEYWORD_ENGINE(sentence):
    s_low = sentence.lower()
    if "elon musk" in s_low: return "Elon Musk in SpaceX control room, cinematic lighting, ultra realistic 8k, dramatic"
    if "success" in s_low or "motivation" in s_low: return "successful businessman on top of mountain sunrise, ultra realistic 8k cinematic"
    if "money" in s_low or "stock" in s_low: return "stock market trading floor, wall street, cinematic ultra realistic 8k"
    if "hard work" in s_low: return "man working hard late night in office, cinematic ultra realistic"
    if "dream" in s_low: return "man looking at stars dreaming big, cinematic ultra realistic 8k"
    words = ' '.join([w for w in re.sub(r'[^\w\s]', ' ', s_low).split() if len(w)>3][:4])
    return f"{words}, ultra realistic 8k cinematic, dramatic lighting, highly detailed, photorealistic, movie trailer scene, no text"

async def Tt(t, o, v):
    import edge_tts
    await edge_tts.Communicate(t, v, rate="-4%", pitch="+1Hz").save(o)
def run_tts(tx, out, vc):
    if len(tx.split()) < 3: tx = tx + "."
    for _ in range(2):
        try:
            try: asyncio.run(Tt(tx, out, vc))
            except: loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop); loop.run_until_complete(Tt(tx, out, vc))
            if os.path.exists(out) and os.path.getsize(out) > 800: return True
        except: time.sleep(0.8)
    try:
        from gtts import gTTS
        lang = 'ur' if 'urdu' in str(globals().get('voice_lang','')).lower() else 'en'
        gTTS(text=tx[:350], lang=lang, slow=False).save(out)
        return True
    except: return False
def detect_voice(ch, selected): return VOICES.get(selected, "en-US-BrandonNeural")

# --- 100% FIXED AI VIDEO GENERATOR - NO BLACK SCREEN ---
def get_pure_ai_clip(prompt_text, duration, W, H, retry=0):
    if retry > 3:
        print("⚠️ AI failed 3 times, using color")
        return ColorClip((W,H), color=(15,15,20), duration=duration)

    p_path = f"{BASE_DIR}/ai_{uuid.uuid4().hex[:6]}.jpg"
    try:
        print(f"🤖 Generating: {prompt_text[:60]}... | Retry: {retry}")
        # Enhanced prompt for trailer
        full_prompt = f"{prompt_text}, movie trailer style, ultra realistic, 8k, cinematic lighting, dramatic atmosphere, highly detailed, photorealistic, no text, no watermark"
        # Pollinations - Flux is best for realistic
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(full_prompt[:200])}?width={W}&height={H}&seed={random.randint(1, 99999999)}&model=flux&nologo=true&enhance=true&nofeed=true"
        
        r = requests.get(url, timeout=60)
        if r.status_code != 200 or len(r.content) < 8000:
            print(f"❌ Pollinations failed: {r.status_code}")
            time.sleep(1)
            return get_pure_ai_clip(prompt_text, duration, W, H, retry+1)

        open(p_path, 'wb').write(r.content)
        
        # PIL FIX - 100% black screen fix
        try:
            im = Image.open(p_path)
            im = im.convert("RGB")
            # Resize to exact W,H to avoid black borders
            im = im.resize((W, H), Image.LANCZOS)
            im.save(p_path, "JPEG", quality=95)
        except Exception as e:
            print(f"PIL Error: {e}")
            if os.path.exists(p_path): os.remove(p_path)
            time.sleep(0.5)
            return get_pure_ai_clip(prompt_text, duration, W, H, retry+1)

        # Check file again
        if not os.path.exists(p_path) or os.path.getsize(p_path) < 5000:
            return get_pure_ai_clip(prompt_text, duration, W, H, retry+1)

        # Create video with Ken Burns effect (slow zoom) - NO BLACK SCREEN
        clip = ImageClip(p_path).set_duration(duration)
        # Slow zoom in effect for trailer feel
        clip = clip.resize(lambda t: 1 + 0.08 * t / duration)  # 8% zoom over duration
        clip = clip.set_position(('center','center')).resize((W,H))
        
        print(f"✅ AI OK: {prompt_text[:40]}")
        return clip

    except Exception as e:
        print(f"AI Error: {e}")
        if os.path.exists(p_path):
            try: os.remove(p_path)
            except: pass
        time.sleep(1)
        return get_pure_ai_clip(prompt_text, duration, W, H, retry+1)

print(f"🎙️ Voice: {voice_lang} | MODE: PURE AI 100% FREE UNLIMITED TRAILER")
cs, kws = clean_analyze(script)
W, H = (1280,720) if "16:9" in video_type else (720,1280)
if "480" in resolution: W, H = (854,480) if W>H else (480,854)
scene_files = []
print(f"🎬 Total Scenes: {len(kws)} - PURE AI TRAILER MODE")

for idx, ch in enumerate(kws):
    try:
        print(f"\n🎬 SCENE {idx+1}/{len(kws)}: {ch[:70]}...")
        ap = f"{BASE_DIR}/{uuid.uuid4().hex[:5]}.mp3"
        if not run_tts(ch, ap, detect_voice(ch, voice_lang)): continue
        au = AudioFileClip(ap)
        if au.duration < 0.5: continue
        if au.duration > 0.4: au = au.subclip(0, au.duration-0.1)
        
        ai_prompt = SMART_KEYWORD_ENGINE(ch)
        dur = au.duration
        
        # PURE AI CLIP
        clip = get_pure_ai_clip(ai_prompt, dur, W, H)
        base_clip = clip.set_duration(dur).set_audio(au)
        
        layers=[base_clip]
        if show_subtitles:
            try:
                txt = TextClip(ch[:100], fontsize=int(W*0.038), color='white', stroke_color='black', stroke_width=2, method='caption', size=(int(W*0.82), None), align='center').set_duration(dur).set_pos(('center',0.80), relative=True)
                layers.append(txt)
            except: pass
        
        final_scene = CompositeVideoClip(layers, size=(W,H)).set_duration(dur)
        temp_path = f"{BASE_DIR}/scene_{idx}_{uuid.uuid4().hex[:4]}.mp4"
        final_scene.write_videofile(temp_path, fps=24, codec='libx264', audio_codec='aac', preset='ultrafast', threads=2, bitrate="1200k", logger=None)
        scene_files.append(temp_path)
        print(f"✅ Scene {idx+1} Done")
        try: base_clip.close(); final_scene.close(); au.close(); clip.close()
        except: pass
        gc.collect()
        time.sleep(0.3)
    except Exception as e:
        print(f"❌ Scene {idx+1} Error {e}")
        import traceback; traceback.print_exc()
        continue

if scene_files:
    print(f"\n🔗 FINAL JOINING {len(scene_files)} scenes...")
    list_path = f"{BASE_DIR}/concat_list.txt"
    with open(list_path,"w") as f:
        for sf in scene_files: f.write(f"file '{os.path.abspath(sf)}'\n")
    out_path = f"{BASE_DIR}/JSM_TRAILER_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c copy {out_path}")
    if not os.path.exists(out_path) or os.path.getsize(out_path)<5000:
        os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c:v libx264 -preset ultrafast -c:a aac {out_path}")
    print(f"\n🎉 TRAILER SUCCESS! Video Ready: {out_path}")
    try:
        final_clip = VideoFileClip(out_path)
        cut_mints_auto(globals().get('email',''), round(final_clip.duration/60,2))
        final_clip.close()
    except: pass
    try:
        from google.colab import files; files.download(out_path)
    except: pass
else:
    print("❌ No scenes created!")
