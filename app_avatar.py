# JSM VEO 3 DIRECTOR MODE V1 - TIGER TRAILER STUDIO - By Saeed - SINGLE FILE ONLY
import os, uuid, random, requests, re, urllib.parse, datetime, time, gc, math
import asyncio
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
VOICES = {"English Male (Brandon - Human Natural)": "en-US-BrandonNeural","English Female (Jenny - Clear & Energetic)": "en-US-JennyNeural","Urdu Male (Asad - Deep Voice / Narrative Style)": "ur-PK-AsadNeural","Hindi Male (Arjun - Motivational Speaker Style)": "hi-IN-ArjunNeural","English Male (Andrew - Professional Studio)": "en-US-AndrewNeural","Trailer Voice (Deep & Powerful)": "en-US-GuyNeural"}

def parse_director_script(script):
    scenes = []
    # Regex for DIRECTOR MODE
    pattern = re.compile(r"SCENE\s*\d*\s*\|?\s*(\d+)s?\s*\nVISUAL:\s*(.*?)\nAUDIO:\s*(.*?)(?=\nSCENE|\Z)", re.IGNORECASE | re.DOTALL)
    matches = pattern.findall(script)
    if matches:
        for dur, visual, audio in matches:
            scenes.append({"duration": int(dur), "visual": visual.strip(), "audio": audio.strip()})
        print(f"🎬 DIRECTOR MODE DETECTED: {len(scenes)} scenes")
        return scenes
    else:
        # Fallback to old mode
        print("⚠️ Old motivational mode - no SCENE tags found")
        clean = re.sub(r"(sex\s*video|porn|xxx|nude|naked)", " ", script, flags=re.I)
        raw = re.split(r'[.!?\n\u06d4]+', clean)
        for s in [x.strip() for x in raw if len(x.strip())>8]:
            scenes.append({"duration": 5, "visual": s, "audio": s})
        return scenes

async def Tt(t, o, v):
    import edge_tts
    await edge_tts.Communicate(t, v, rate="-5%", pitch="-2Hz").save(o)

def run_tts(tx, out, vc):
    if len(tx.split()) < 2: tx = tx + "."
    for _ in range(2):
        try:
            try: asyncio.run(Tt(tx, out, vc))
            except: loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop); loop.run_until_complete(Tt(tx, out, vc))
            if os.path.exists(out) and os.path.getsize(out) > 800: return True
        except: time.sleep(0.5)
    try:
        from gtts import gTTS
        gTTS(text=tx[:350], lang='en', slow=False).save(out)
        return True
    except: return False

def detect_voice(selected): 
    if "Trailer" in selected: return "en-US-GuyNeural"
    return VOICES.get(selected, "en-US-BrandonNeural")

def get_real_video_director(visual_prompt, duration, W, H):
    print(f"\n🎥 DIRECTOR SHOT: {visual_prompt[:70]} | {duration}s")
    v_path = f"{BASE_DIR}/dir_{uuid.uuid4().hex[:5]}.mp4"
    i_path = f"{BASE_DIR}/dir_{uuid.uuid4().hex[:5]}.jpg"

    # 1. TRY REAL VIDEO - Pollinations Wan (Free Unlimited)
    try:
        full_prompt = f"{visual_prompt}, cinematic trailer shot, camera movement, ultra realistic, 8k, highly detailed, dramatic lighting, movie scene, no text"
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(full_prompt[:180])}?width={W}&height={H}&model=wan&seed={random.randint(1,9999999)}&nologo=true&enhance=true"
        print(f"Trying REAL VIDEO: {url[:100]}...")
        r = requests.get(url, timeout=80)
        if r.status_code == 200 and len(r.content) > 80000:
            open(v_path, 'wb').write(r.content)
            try:
                clip = VideoFileClip(v_path)
                if clip.duration > 0.5:
                    print(f"✅ REAL VIDEO SUCCESS - Duration: {clip.duration}")
                    # Trim or extend to required duration
                    if clip.duration > duration:
                        clip = clip.subclip(0, duration)
                    clip = clip.resize((W,H)).set_duration(duration)
                    return clip
            except: pass
    except Exception as e:
        print(f"Real video fail: {e}")

    # 2. FALLBACK - High Quality Image to Video Effect (No Black Screen)
    try:
        print("Fallback to IMAGE->VIDEO with motion")
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(full_prompt[:150])}?width={W}&height={H}&model=flux&seed={random.randint(1,9999999)}&nologo=true&enhance=true"
        r = requests.get(url, timeout=50)
        if r.status_code==200 and len(r.content)>8000:
            open(i_path,'wb').write(r.content)
            im = Image.open(i_path).convert("RGB").resize((W,H), Image.LANCZOS)
            im.save(i_path, "JPEG", quality=95)
            # Cinematic motion
            clip = ImageClip(i_path).set_duration(duration)
            # Random cinematic motion
            motion = random.choice(['zoom_in', 'zoom_out', 'pan_left'])
            if motion == 'zoom_in':
                clip = clip.resize(lambda t: 1 + 0.12*t/duration)
            elif motion == 'zoom_out':
                clip = clip.resize(lambda t: 1.12 - 0.12*t/duration)
            else:
                clip = clip.resize(lambda t: 1.05).set_position(lambda t: ( -20*t/duration, 'center'))
            clip = clip.resize((W,H)).set_position('center')
            print("✅ IMAGE VIDEO Effect Ready")
            return clip
    except Exception as e:
        print(f"Image fallback fail: {e}")

    return ColorClip((W,H), color=(10,10,12), duration=duration)

# --- MAIN DIRECTOR LOGIC ---
print(f"🎬 VEO 3 DIRECTOR MODE | Voice: {voice_lang} | Res: {video_type}")
scenes = parse_director_script(script)
W, H = (1280,720) if "16:9" in video_type else (720,1280)
if "480" in resolution: W, H = (854,480) if W>H else (480,854)
scene_files = []

for idx, scene in enumerate(scenes):
    try:
        visual = scene["visual"]
        audio_text = scene["audio"]
        dur = scene["duration"]
        print(f"\n--- SCENE {idx+1}/{len(scenes)} ---")
        print(f"VISUAL: {visual}")
        print(f"AUDIO: {audio_text}")
        print(f"DUR: {dur}s")

        # 1. Generate Voiceover for this scene
        ap = f"{BASE_DIR}/{uuid.uuid4().hex[:5]}.mp3"
        if not run_tts(audio_text, ap, detect_voice(voice_lang)):
            print("TTS Fail, skipping")
            continue
        au = AudioFileClip(ap)
        # Use actual audio duration if longer than specified, or specified duration
        final_dur = max(dur, au.duration + 0.3)
        if au.duration > 0.4:
            au = au.subclip(0, au.duration)

        # 2. Generate REAL VIDEO for visual prompt
        video_clip = get_real_video_director(visual, final_dur, W, H)
        video_clip = video_clip.set_duration(final_dur).set_audio(au)

        # 3. Add Subtitle if needed
        layers = [video_clip]
        if show_subtitles:
            try:
                txt = TextClip(audio_text[:120], fontsize=int(W*0.035), color='white', stroke_color='black', stroke_width=2, method='caption', size=(int(W*0.85), None), align='center').set_duration(final_dur).set_pos(('center',0.82), relative=True)
                layers.append(txt)
            except: pass

        final_scene = CompositeVideoClip(layers, size=(W,H)).set_duration(final_dur)
        temp_path = f"{BASE_DIR}/scene_{idx}_{uuid.uuid4().hex[:4]}.mp4"
        final_scene.write_videofile(temp_path, fps=24, codec='libx264', audio_codec='aac', preset='ultrafast', threads=2, bitrate="1500k", logger=None)
        scene_files.append(temp_path)
        print(f"✅ SCENE {idx+1} DONE")
        try: video_clip.close(); final_scene.close(); au.close()
        except: pass
        gc.collect()
        time.sleep(0.5)
    except Exception as e:
        print(f"❌ Scene {idx+1} Error: {e}")
        import traceback; traceback.print_exc()
        continue

# --- FINAL JOIN ---
if scene_files:
    print(f"\n🔗 JOINING {len(scene_files)} SCENES - FINAL TRAILER...")
    list_path = f"{BASE_DIR}/concat_list.txt"
    with open(list_path,"w") as f:
        for sf in scene_files: f.write(f"file '{os.path.abspath(sf)}'\n")
    out_path = f"{BASE_DIR}/TIGER_TRAILER_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c copy {out_path}")
    if not os.path.exists(out_path) or os.path.getsize(out_path)<5000:
        os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c:v libx264 -preset ultrafast -c:a aac {out_path}")
    print(f"\n🎉 TIGER TRAILER READY! {out_path}")
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
