# JSM PURE AI & STOCK VIDEO GENERATOR V100 - PUBLIC WEB DASHBOARD EDITION
# Designed for Netlify Frontend + GitHub Actions Backend Workflow
import os, sys, re, uuid, time, random, gc, requests, urllib.parse, datetime, asyncio
import nest_asyncio
nest_asyncio.apply()

from moviepy.editor import VideoFileClip, ColorClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip, TextClip, ImageClip
from PIL import Image

# -------------------------------------------------------------
# 🌐 ENVIRONMENT INPUTS (From Netlify Web Dashboard)
# -------------------------------------------------------------
script = os.environ.get('SCRIPT_TEXT', '')
voice_lang = os.environ.get('VOICE_LANG', 'ur-PK-AsadNeural')
video_mode = os.environ.get('VIDEO_MODE', 'Free Stock Videos')
video_type = "16:9"
resolution = "720p"
show_subtitles = True

# Fallback script for testing if run manually
if not script:
    script = "ایک جدید اور خوبصورت شہر کی سڑک پر گاڑیوں کی آمدورفت۔ انسان اپنی محنت سے کامیابی حاصل کرتا ہے۔"

BASE_DIR = "./JSM_Outputs"
os.makedirs(BASE_DIR, exist_ok=True)

# -------------------------------------------------------------
# 🎙️ VOICE MAPPING (Supported 30+ Edge-TTS Voices)
# -------------------------------------------------------------
VOICES = {
    "ur-PK-AsadNeural": "ur-PK-AsadNeural",
    "en-US-BrandonNeural": "en-US-BrandonNeural",
    "hi-IN-ArjunNeural": "hi-IN-ArjunNeural",
    "ar-SA-HamedNeural": "ar-SA-HamedNeural",
    "zh-CN-YunxiNeural": "zh-CN-YunxiNeural",
    "es-ES-AlvaroNeural": "es-ES-AlvaroNeural",
    "fr-FR-HenriNeural": "fr-FR-HenriNeural",
    "de-DE-KillianNeural": "de-DE-KillianNeural",
    "ja-JP-KeitaNeural": "ja-JP-KeitaNeural",
    "ru-RU-DmitryNeural": "ru-RU-DmitryNeural",
    "pt-BR-AntonioNeural": "pt-BR-AntonioNeural",
    "tr-TR-AhmetNeural": "tr-TR-AhmetNeural",
    "fa-IR-FaridNeural": "fa-IR-FaridNeural",
    "it-IT-DiegoNeural": "it-IT-DiegoNeural",
    "ko-KR-InJoonNeural": "ko-KR-InJoonNeural"
}

def detect_voice(selected):
    return VOICES.get(selected, selected if selected else "ur-PK-AsadNeural")

# -------------------------------------------------------------
# 🧠 SMART SENSOR ENGINE (Urdu/English Keyword Filtering)
# -------------------------------------------------------------
def smart_topic_sensor(sentence_text):
    stop_words = ["ایک", "اور", "کا", "کی", "کے", "میں", "پر", "سے", "ہے", "ہیں", "تھا", "تھی", "تھے", "کو", "یہ", "وہ", "تک", "بھی", "a", "the", "and", "is", "of", "in", "on"]
    urdu_topic_map = {
        "شہر": "modern city skyline night",
        "گاڑیاں": "traffic night highway cars",
        "سڑک": "city street night",
        "شخص": "man thinking looking street",
        "آدمی": "man business professional",
        "محنت": "hard working man office night",
        "کامیابی": "successful businessman mountain top",
        "پیسہ": "money stocks wall street trading",
        "پہاڑ": "mountains nature landscape",
        "سمندر": "ocean waves aerial"
    }
    extracted = []
    for word in sentence_text.split():
        clean_w = re.sub(r'[^\w\s]', '', word).strip()
        if clean_w in urdu_topic_map:
            extracted.append(urdu_topic_map[clean_w])
        elif len(clean_w) > 3 and clean_w not in stop_words:
            extracted.append(clean_w)
            
    return " ".join(extracted[:2]) if extracted else sentence_text[:30]

def clean_analyze(script_text):
    clean = re.sub(r"(sex\s*video|porn|xxx|nude|naked)", " ", script_text, flags=re.I)
    raw_sentences = re.split(r'[.!?\n\u06d4]+', clean)
    return clean, [s.strip() for s in raw_sentences if len(s.strip()) > 5]

# -------------------------------------------------------------
# 🔊 AUDIO TTS ENGINE
# -------------------------------------------------------------
async def Tt(t, o, v):
    import edge_tts
    await edge_tts.Communicate(t, v, rate="-3%", pitch="+0Hz").save(o)

def run_tts(tx, out, vc):
    if len(tx.split()) < 3: tx = tx + "."
    for _ in range(2):
        try:
            try: asyncio.run(Tt(tx, out, vc))
            except: 
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(Tt(tx, out, vc))
            if os.path.exists(out) and os.path.getsize(out) > 800: return True
        except: time.sleep(0.5)
    return False

# -------------------------------------------------------------
# 📹 VISUAL FETCHERS (Free Stock Videos & AI Motion Clips)
# -------------------------------------------------------------
def get_stock_video_smart(prompt_text, target_duration, W, H):
    smart_keyword = smart_topic_sensor(prompt_text)
    print(f"  🧠 AI Sensor Topic: '{smart_keyword}'")
    headers = {"Authorization": "563492ad6f91700001000001cbe2d7c588a44ec4b36d013f9c62957f"}
    clean_q = urllib.parse.quote(smart_keyword)
    url = f"https://api.pexels.com/videos/search?query={clean_q}&per_page=6&orientation=landscape"
    v_path = f"{BASE_DIR}/stock_{uuid.uuid4().hex[:6]}.mp4"
    try:
        res = requests.get(url, headers=headers, timeout=15).json()
        if "videos" in res and len(res["videos"]) > 0:
            video_choice = random.choice(res["videos"][:3])
            files_list = video_choice["video_files"]
            best_url = sorted(files_list, key=lambda x: x.get('width', 0), reverse=True)[0]['link']
            v_data = requests.get(best_url, timeout=25).content
            with open(v_path, 'wb') as f: f.write(v_data)
            clip = VideoFileClip(v_path).resize((W, H))
            if clip.duration > target_duration:
                clip = clip.subclip(0, target_duration)
            else:
                clip = clip.loop(duration=target_duration)
            return clip
    except Exception as e:
        print(f"  ⚠️ Stock Error: {e}")
    return None

def get_pure_ai_clip(prompt_text, duration, W, H, retry=0):
    if retry > 2:
        return ColorClip((W, H), color=(15, 15, 20), duration=duration)
    smart_keyword = smart_topic_sensor(prompt_text)
    p_path = f"{BASE_DIR}/ai_{uuid.uuid4().hex[:6]}.jpg"
    try:
        full_prompt = f"{smart_keyword}, highly detailed, 8k resolution, cinematic lighting, movie scene, photorealistic"
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(full_prompt)}?width={W}&height={H}&seed={random.randint(1, 999999)}&model=flux&nologo=true"
        r = requests.get(url, timeout=30)
        if r.status_code == 200 and len(r.content) > 5000:
            with open(p_path, 'wb') as f: f.write(r.content)
            im = Image.open(p_path).convert("RGB").resize((W, H), Image.LANCZOS)
            im.save(p_path, "JPEG", quality=95)
            clip = ImageClip(p_path).set_duration(duration)
            clip = clip.resize(lambda t: 1 + 0.05 * t / duration).set_position(('center', 'center')).resize((W, H))
            return clip
    except Exception as e:
        print(f"  ⚠️ AI Image Error: {e}")
    return get_pure_ai_clip(prompt_text, duration, W, H, retry+1)

# -------------------------------------------------------------
# 🎬 MAIN VIDEO BUILDER PROCESS
# -------------------------------------------------------------
def main():
    print("=" * 60)
    print(f"👑 JSM AI V100 - VIDEO GENERATOR ENGINE STARTED")
    print(f"🎙️ Selected Voice: {detect_voice(voice_lang)}")
    print(f"🎥 Selected Mode: {video_mode}")
    print("=" * 60)

    cs, kws = clean_analyze(script)
    W, H = (1280, 720) if "16:9" in video_type else (720, 1280)
    scene_files = []

    print(f"📋 Total Sentences Processed: {len(kws)}")

    for idx, sentence in enumerate(kws):
        try:
            print(f"\n🎥 Scene {idx+1}/{len(kws)}: '{sentence[:40]}...'")
            ap = f"{BASE_DIR}/audio_{idx}_{uuid.uuid4().hex[:4]}.mp3"
            if not run_tts(sentence, ap, detect_voice(voice_lang)): 
                continue
            
            au = AudioFileClip(ap)
            dur = au.duration
            if dur < 0.5: continue

            # Select Clip Type Based on Dashboard Input
            clip = None
            if video_mode == "Free Stock Videos":
                clip = get_stock_video_smart(sentence, dur, W, H)
            
            if clip is None:
                clip = get_pure_ai_clip(sentence, dur, W, H)

            base_clip = clip.set_duration(dur).set_audio(au)
            layers = [base_clip]

            if show_subtitles:
                try:
                    txt = TextClip(sentence[:90], fontsize=int(W*0.035), color='gold', stroke_color='black', stroke_width=2, method='caption', size=(int(W*0.85), None), align='center').set_duration(dur).set_pos(('center', 0.82), relative=True)
                    layers.append(txt)
                except Exception as e: pass

            final_scene = CompositeVideoClip(layers, size=(W, H)).set_duration(dur)
            temp_path = f"{BASE_DIR}/scene_{idx}_{uuid.uuid4().hex[:4]}.mp4"
            
            final_scene.write_videofile(
                temp_path, 
                fps=24, 
                codec='libx264', 
                audio_codec='aac', 
                preset='ultrafast', 
                threads=2, 
                bitrate="1500k", 
                logger=None
            )
            scene_files.append(temp_path)
            print(f"✅ Scene {idx+1} Generated Successfully!")

            try: base_clip.close(); final_scene.close(); au.close(); clip.close()
            except: pass
            gc.collect()

        except Exception as e:
            print(f"❌ Error Scene {idx+1}: {e}")
            continue

    if scene_files:
        print(f"\n🔗 Final Joining {len(scene_files)} Scenes...")
        list_path = f"{BASE_DIR}/concat_list.txt"
        with open(list_path, "w") as f:
            for sf in scene_files: 
                f.write(f"file '{os.path.abspath(sf)}'\n")
        
        out_path = f"{BASE_DIR}/JSM_VIDEO_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c copy {out_path}")
        
        if not os.path.exists(out_path) or os.path.getsize(out_path) < 5000:
            os.system(f"ffmpeg -y -f concat -safe 0 -i {list_path} -c:v libx264 -preset ultrafast -c:a aac {out_path}")
            
        print(f"\n🎉 VIDEO SUCCESS! Saved at: {out_path}")
    else:
        print("\n❌ Process Failed: No scenes generated.")

if __name__ == "__main__":
    main()
    
