# JSM FINAL SMOOTH V5 - WATER FLOW TRAILER - RAM/DISK FIXED - By Saeed
import os, uuid, random, requests, re, urllib.parse, datetime, time, gc, math
import asyncio
import nest_asyncio
nest_asyncio.apply()
from moviepy.editor import *
from PIL import Image

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyfopJoiGBueO6AsZ5JE-juplXjSa1Lc_klKn4bOswLyhPmPGsvOhT9r6Axow6rsl-rXg/exec"
def cut_mints_auto(email, mins):
    try: requests.get(f"{WEB_APP_URL}?email={urllib.parse.quote(email)}&mins={mins}", timeout=10)
    except: pass

BASE_DIR = "/tmp/JSM_Outputs"
os.makedirs(BASE_DIR, exist_ok=True)

VOICES = {"Trailer Voice (Deep & Powerful)": "en-US-GuyNeural","English Male (Brandon)": "en-US-BrandonNeural","English Female (Jenny)": "en-US-JennyNeural","Urdu Male (Asad)": "ur-PK-AsadNeural","Hindi Male (Arjun)": "hi-IN-ArjunNeural"}

def parse_script(script):
    scenes = []
    # DIRECTOR MODE: SCENE 1 | 8s / VISUAL: / AUDIO:
    pattern = re.compile(r"SCENE\s*\d*\s*\|?\s*(\d+)s?\s*\nVISUAL:\s*(.*?)\nAUDIO:\s*(.*?)(?=\nSCENE|\Z)", re.IGNORECASE | re.DOTALL)
    matches = pattern.findall(script)
    if matches:
        for dur, visual, audio in matches:
            scenes.append({"duration": int(dur), "visual": visual.strip(), "audio": audio.strip()})
        print(f"🎬 DIRECTOR MODE: {len(scenes)} scenes found")
        return scenes
    # SIMPLE MODE: Har line ek scene
    else:
        clean = re.sub(r"(sex\s*video|porn|xxx|nude)", " ", script, flags=re.I)
        lines = [x.strip() for x in re.split(r'[.!?\n]+', clean) if len(x.strip())>8]
        for line in lines:
            scenes.append({"duration": 5, "visual": line, "audio": line})
        print(f"🎬 SIMPLE MODE: {len(scenes)} scenes")
        return scenes

async def Tt(t, o, v):
    import edge_tts
    await edge_tts.Communicate(t, v, rate="-4%", pitch="-1Hz").save(o)

def run_tts(tx, out, vc):
    if len(tx.split()) < 2: tx = tx + "."
    for _ in range(2):
        try:
            try: asyncio.run(Tt(tx, out, vc))
            except:
                loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop); loop.run_until_complete(Tt(tx, out, vc))
            if os.path.exists(out) and os.path.getsize(out) > 500: return True
        except: time.sleep(0.4)
    try:
        from gtts import gTTS
        gTTS(text=tx[:300], lang='en', slow=False).save(out)
        return True
    except: return False

# --- PANI KI TARAH SMOOTH - 1 SEC = 1 IMAGE ---
def get_water_flow_clip(visual_prompt, duration, W, H):
    print(f"🌊 FLOW: {visual_prompt[:50]} | {duration}s")
    clips = []
    num_images = max(3, int(duration)) # 1 sec = 1 image
    per_img_dur = duration / num_images

    for i in range(num_images):
        p_path = f"{BASE_DIR}/{uuid.uuid4().hex[:6]}.jpg"
        try:
            # Har image ka prompt thora alag - is se flow lagega
            enhanced_prompt = f"{visual_prompt}, cinematic movie frame {i+1}, ultra realistic 8k, dramatic lighting, highly detailed, photorealistic, no text, movie trailer"
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(enhanced_prompt[:150])}?width={W}&height={H}&seed={random.randint(1,9999999)+i*77}&model=flux&nologo=true&enhance=true"
            r = requests.get(url, timeout=35)
            if r.status_code!=200 or len(r.content)<5000:
                continue
            open(p_path,'wb').write(r.content)
            im = Image.open(p_path).convert("RGB").resize((W,H), Image.LANCZOS)
            im.save(p_path, "JPEG", quality=90)

            # Har image pe alag motion
            clip = ImageClip(p_path).set_duration(per_img_dur + 0.4) # 0.4 sec overlap for crossfade
            # Pani jaisa smooth zoom/pan
            if i % 3 == 0:
                clip = clip.resize(lambda t: 1 + 0.04*t).set_position('center')
            elif i % 3 == 1:
                clip = clip.resize(lambda t: 1.08 - 0.04*t).set_position('center')
            else:
                clip = clip.resize(lambda t: 1.05).set_position(lambda t: (-10*t, 'center'))

            clips.append(clip.resize((W,H)))
        except Exception as e:
            print(f"Img {i} fail {e}")
            continue
        # Disk clean for this image later

    if len(clips)==0:
        return ColorClip((W,H), color=(12,12,15), duration=duration)
    if len(clips)==1:
        return clips[0].set_duration(duration)

    # Crossfade se jorna - pani ki tarah
    final = clips[0]
    for j in range(1, len(clips)):
        final = CompositeVideoClip([final, clips[j].set_start(final.duration - 0.4).crossfadein(0.4)]).set_duration(final.duration + clips[j].duration - 0.4)

    final = final.set_duration(duration)
    print(f"✅ FLOW Ready: {len(clips)} images joined")
    return final

# --- MAIN ---
print(f"🎬 WATER FLOW MODE | Voice: {voice_lang}")
scenes = parse_script(script)
W, H = (1280,720) if "16:9" in video_type else (720,1280)
if "480" in resolution: W, H = (854,480) if W>H else (480,854)
scene_files = []

for idx, scene in enumerate(scenes):
    try:
        print(f"\n--- SCENE {idx+1}/{len(scenes)} | {scene['duration']}s ---")
        visual = scene["visual"]
        audio_text = scene["audio"]

        ap = f"{BASE_DIR}/{uuid.uuid4().hex[:5]}.mp3"
        if not run_tts(audio_text, ap, VOICES.get(voice_lang, "en-US-GuyNeural")):
            continue
        au = AudioFileClip(ap)
        final_dur = max(scene["duration"], au.duration + 0.2)
        if au.duration > 0.3:
            au = au.subclip(0, min(au.duration, final_dur))

        video_clip = get_water_flow_clip(visual, final_dur, W, H)
        video_clip = video_clip.set_duration(final_dur).set_audio(au)

        layers = [video_clip]
        if show_subtitles:
            try:
                txt = TextClip(audio_text[:120], fontsize=int(W*0.035), color='white', stroke_color='black', stroke_width=2, method='caption', size=(int(W*0.84), None), align='center').set_duration(final_dur).set_pos(('center',0.84), relative=True)
                layers.append(txt)
            except: pass

        final_scene = CompositeVideoClip(layers, size=(W,H)).set_duration(final_dur)
        temp_path = f"{BASE_DIR}/scene_{idx}_{uuid.uuid4().hex[:4]}.mp4"
        final_scene.write_videofile(temp_path, fps=24, codec='libx264', audio_codec='aac', preset='ultrafast', threads=2, bitrate="1200k", logger=None)
        scene_files.append(temp_path)
        print(f"✅ SCENE {idx+1} DONE - RAM Clear")

        # RAM + DISK FIX
        try: video_clip.close(); final_scene.close(); au.close()
        except: pass
        # Delete temp images
        for f in os.listdir(BASE_DIR):
            if f.endswith('.jpg'):
                try: os.remove(os.path.join(BASE_DIR,f))
                except: pass
        gc.collect()
        time.sleep(0.3)

    except Exception as e:
        print(f"❌ Scene {idx+1} Error {e}")
        continue

# FINAL JOIN - DISK CLEAN
if scene_files:
    print(f"\n🔗 JOINING {len(scene_files)} scenes...")
    list_path = f"{BASE_DIR}/concat_list.txt"
    with open(list_path,"w") as f:
        for sf in scene_files: f.write(f"file '{os.path.abspath(sf)}'\n")
    out_path = f"/tmp/FINAL_TRAILER_{datetime.datetime.now().strftime('%H%M%S')}.mp4"
    os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c copy {out_path}")
    if not os.path.exists(out_path) or os.path.getsize(out_path)<5000:
        os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c:v libx264 -preset ultrafast -c:a aac {out_path}")

    print(f"\n🎉 FINAL READY: {out_path}")
    try:
        fc = VideoFileClip(out_path)
        cut_mints_auto(globals().get('email',''), round(fc.duration/60,2))
        fc.close()
    except: pass
    try:
        from google.colab import files; files.download(out_path)
    except: pass

    # Final Disk Clean
    for sf in scene_files:
        try: os.remove(sf)
        except: pass
    try: os.remove(list_path)
    except: pass
