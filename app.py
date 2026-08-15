from flask import Flask, request, jsonify
import os, requests, asyncio
import edge_tts
import moviepy.editor as mp

app = Flask(__name__)

# KEYS یہاں Hardcode مت کرو۔ Render > Environment میں لگانا
PIXABAY_KEY = os.getenv("PIXABAY_KEY")
PEXELS_KEY = os.getenv("PEXELS_KEY")

async def make_voice(text, voice):
    await edge_tts.Communicate(text, voice).save("temp.mp3")

def detect_niche(script): # AI Brain
    s = script.lower()
    if "kisan" in s: return "farmer village"
    if "funny" in s: return "funny comedy"
    return "cinematic story"

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    script = data['script']
    niche = detect_niche(script)

    # 1. Voice بناؤ
    asyncio.run(make_voice(script, "hi-IN-SwaraNeural"))

    # 2. Pexels سے Stock Video لو
    video_url = requests.get(f"https://api.pexels.com/videos/search?query={niche}",
              headers={"Authorization": PEXELS_KEY}).json()['videos'][0]['video_files'][0]['link']

    # 3. Moviepy سے merge کرو
    #... تمہارا والا merge code...

    return jsonify({"url": "final_video.mp4", "niche": niche})

if __name__ == '__main__':
    app.run()
