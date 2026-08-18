import os, sys, re, uuid, time, random, gc, requests, urllib.parse, asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import nest_asyncio
nest_asyncio.apply()

app = Flask(__name__)
CORS(app)  # Cross-Origin Requests اجازت دینے کے لیے

BASE_DIR = "./JSM_Outputs"
os.makedirs(BASE_DIR, exist_ok=True)

# -------------------------------------------------------------
# 🧠 SMART TOPIC SENSOR ENGINE
# -------------------------------------------------------------
def smart_topic_sensor(sentence_text):
    stop_words = ["ایک", "اور", "کا", "کی", "کے", "میں", "پر", "سے", "ہے", "ہیں", "تھا", "تھی", "تھے", "کو", "یہ", "وہ"]
    urdu_topic_map = {
        "شہر": "modern city skyline night",
        "گاڑیاں": "traffic night highway cars",
        "سڑک": "city street night",
        "شخص": "man thinking looking street",
        "آدمی": "man business professional",
        "پیسہ": "money stocks trading floor",
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
            
    return " ".join(extracted[:2]) if extracted else sentence_text[:25]

# -------------------------------------------------------------
# VOICE GENERATOR (Edge TTS)
# -------------------------------------------------------------
async def generate_voice(text, out_path, voice_code):
    import edge_tts
    comm = edge_tts.Communicate(text, voice_code, rate="-3%", pitch="+0Hz")
    await comm.save(out_path)

def make_audio(text, out_path, voice_code):
    try:
        asyncio.run(generate_voice(text, out_path, voice_code))
        return os.path.exists(out_path) and os.path.getsize(out_path) > 1000
    except Exception as e:
        print(f"❌ Voice Error: {e}")
        return False

# -------------------------------------------------------------
# STOCK & AI VISUAL GENERATOR
# -------------------------------------------------------------
def get_visual_clip(sentence, duration, mode, W=1280, H=720):
    from moviepy.editor import ImageClip, VideoFileClip
    smart_keyword = smart_topic_sensor(sentence)
    
    if mode == "Free Stock Videos":
        try:
            headers = {"Authorization": "563492ad6f91700001000001cbe2d7c588a44ec4b36d013f9c62957f"}
            clean_q = urllib.parse.quote(smart_keyword)
            url = f"https://api.pexels.com/videos/search?query={clean_q}&per_page=5&orientation=landscape"
            res = requests.get(url, headers=headers, timeout=15).json()
            if "videos" in res and len(res["videos"]) > 0:
                v_choice = random.choice(res["videos"][:3])
                best_url = sorted(v_choice["video_files"], key=lambda x: x.get('width', 0), reverse=True)[0]['link']
                v_path = f"{BASE_DIR}/stock_{uuid.uuid4().hex[:6]}.mp4"
                with open(v_path, 'wb') as f: f.write(requests.get(best_url, timeout=25).content)
                clip = VideoFileClip(v_path).resize((W, H))
                return clip.subclip(0, min(duration, clip.duration)) if clip.duration > duration else clip.loop(duration=duration)
        except Exception as e:
            print(f"Stock Fetch Error: {e}")

    # Fallback / AI Motion Mode
    clean_p = urllib.parse.quote(f"{smart_keyword}, highly detailed, 8k resolution, cinematic lighting, photorealistic")
    img_url = f"https://image.pollinations.ai/prompt/{clean_p}?width={W}&height={H}&seed={random.randint(1,999999)}&nologo=true"
    img_path = f"{BASE_DIR}/img_{uuid.uuid4().hex[:6]}.jpg"
    try:
        res = requests.get(img_url, timeout=25)
        if res.status_code == 200:
            with open(img_path, 'wb') as f: f.write(res.content)
            clip = ImageClip(img_path).set_duration(duration)
            return clip.resize(lambda t: 1 + 0.04 * t).set_position(('center', 'center'))
    except Exception as e:
        print(f"AI Image Error: {e}")
    return None

# -------------------------------------------------------------
# API ROUTE FOR FRONTEND DASHBOARD
# -------------------------------------------------------------
@app.route('/generate-video', methods=['POST'])
def process_video_request():
    from moviepy.editor import AudioFileClip
    data = request.json or {}
    script = data.get('script', '')
    voice = data.get('voice', 'ur-PK-AsadNeural')
    mode = data.get('mode', 'Free Stock Videos')

    if not script:
        return jsonify({"status": "error", "message": "اسکرپٹ خالی ہے!"}), 400

    sentences = [s.strip() for s in re.split(r'[.!?\n\u06d4]+', script) if len(s.strip()) > 3]
    completed_scenes = []

    for idx, sentence in enumerate(sentences):
        audio_file = f"{BASE_DIR}/audio_{idx}_{uuid.uuid4().hex[:4]}.mp3"
        if not make_audio(sentence, audio_file, voice): continue
        
        audio_clip = AudioFileClip(audio_file)
        dur = audio_clip.duration
        clip = get_visual_clip(sentence, dur, mode)
        
        if clip:
            scene_video = clip.set_audio(audio_clip)
            scene_mp4 = f"{BASE_DIR}/scene_{idx}_{uuid.uuid4().hex[:4]}.mp4"
            scene_video.write_videofile(scene_mp4, fps=24, codec='libx264', audio_codec='aac', preset='ultrafast', threads=2, logger=None)
            completed_scenes.append(scene_mp4)
            scene_video.close(); audio_clip.close(); clip.close(); gc.collect()

    if completed_scenes:
        list_txt = f"{BASE_DIR}/concat_list.txt"
        with open(list_txt, "w") as f:
            for sc in completed_scenes: f.write(f"file '{os.path.abspath(sc)}'\n")
            
        out_filename = f"JSM_VIDEO_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        out_mp4 = os.path.join(BASE_DIR, out_filename)
        os.system(f"ffmpeg -y -f concat -safe 0 -i {list_txt} -c copy {out_mp4}")
        
        return jsonify({
            "status": "success",
            "message": "ویڈیو کامیابی سے بن گئی ہے!",
            "download_url": f"/download/{out_filename}"
        })
    
    return jsonify({"status": "error", "message": "ویڈیو بنانے میں ناکامی ہوئی"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
            
