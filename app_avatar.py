# JSM AVATAR V3.1 - FINAL FIXED - ReadAsArray Bug Fixed - By Saeed
import asyncio, uuid, random, requests, re, os, urllib.parse, datetime, time, gc, math
import nest_asyncio
nest_asyncio.apply()
from moviepy.editor import VideoFileClip, ColorClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip, TextClip, ImageClip
from PIL import Image

SHEET_ID = "1wANoZUC8GOi4BSXQRalm2gKrhP8SDLCy_CfCaSWMkEQ"
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyfopJoiGBueO6AsZ5JE-juplXjSa1Lc_klKn4bOswLyhPmPGsvOhT9r6Axow6rsl-rXg/exec"
def cut_mints_auto(email, mins):
    try: requests.get(f"{WEB_APP_URL}?email={urllib.parse.quote(email)}&mins={mins}", timeout=15)
    except: pass

PIXABAY_KEY = "56386293-14facd94fdac26f9fc37f5f2c"
PEXELS_KEYS = ["ROKJvfYuuSkc7QVVL6VjCgYFyB8UQZCLLCctD2SfTJcIrDGo5Ex3JMX6","zniYyavhal66VGwuV2kUIpRm7vG3Y0rddDLuzrITvmPqQ26kdG0vcyy0","f6IKxrHR8MHj1geD62crLTfDTQX0s7ewFkw3hEI4d4CenRTZXCkpCWD9"]
BASE_DIR = "./JSM_Outputs"
os.makedirs(BASE_DIR, exist_ok=True)
USED_VIDEOS = set()

VOICES = {"English Male (Brandon - Human Natural)": "en-US-BrandonNeural","English Female (Jenny - Clear & Energetic)": "en-US-JennyNeural","Urdu Male (Asad - Deep Voice / Narrative Style)": "ur-PK-AsadNeural","Hindi Male (Arjun - Motivational Speaker Style)": "hi-IN-ArjunNeural","English Male (Andrew - Professional Studio)": "en-US-AndrewNeural"}
AVATAR_PROMPTS = {
    "1 - Young Boy - Hoodie (Motivational)": "young handsome man hoodie, ultra realistic human face, studio portrait, transparent background, 8k",
    "2 - Business Man - Suit (Finance)": "business man suit tie, ultra realistic human face, professional CEO, 8k",
    "3 - Beard Boy - Casual (YouTube)": "young man beard casual tshirt, ultra realistic human face, youtuber style, 8k",
    "4 - Girl - Professional (News)": "beautiful professional woman, ultra realistic human face, news anchor, 8k",
    "5 - Old Man - Wise (Story)": "old wise man beard, ultra realistic human face, professor style, 8k"
}

def clean_analyze(script):
    clean = re.sub(r"(sex\s*video|porn|xxx|nude|naked)", " ", script, flags=re.I)
    raw_sentences = re.split(r'[.!?\n\u06d4]+', clean)
    return clean, [s.strip() for s in raw_sentences if len(s.strip()) > 8]

def SMART_KEYWORD_ENGINE(sentence):
    s_low = sentence.lower()
    if "elon musk" in s_low: return ["Elon Musk SpaceX rocket launch ultra realistic"]
    words = [w for w in re.sub(r'[^\w\s]', ' ', s_low).split() if len(w)>3][:2]
    return [f"{' '.join(words)} cinematic HD ultra realistic"] if words else ["cinematic story background HD"]

def download_clip(url, W, H):
    try:
        if url in USED_VIDEOS: return None
        t_path = f"{BASE_DIR}/{uuid.uuid4().hex[:6]}.mp4"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=12)
        if res.status_code == 200 and len(res.content) > 40000:
            with open(t_path, 'wb') as f: f.write(res.content)
            USED_VIDEOS.add(url)
            return VideoFileClip(t_path).resize((W, H))
    except: pass
    return None

def get_clip_from_platforms(smart_queries, duration, W, H, clip_index):
    mode = globals().get('video_mode','')
    if "Pure AI" in mode:
        for q in smart_queries:
            try:
                print(f"🤖 AI MODE: {q}")
                prompt = f"{q}, ultra realistic 8k cinematic, dramatic lighting, highly detailed, photorealistic, no text"
                p_path = f"{BASE_DIR}/ai_{uuid.uuid4().hex[:5]}.jpg"
                url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt[:120])}?width={W}&height={H}&seed={random.randint(1,9999999)}&model=flux&nologo=true"
                r = requests.get(url, timeout=40)
                if r.status_code==200 and len(r.content)>8000:
                    open(p_path,'wb').write(r.content)
                    try:
                        im = Image.open(p_path).convert("RGB")
                        im.save(p_path)
                    except: pass
                    print(f"✅ AI Generated: {q}")
                    return ImageClip(p_path).set_duration(duration).resize((W,H)).resize(lambda t: 1+0.04*t)
            except: continue
        return ColorClip((W,H), color=(12,12,12), duration=duration)
    else:
        print(f"🎥 STOCK MODE: {smart_queries}")
        clips_to_join = []; time_covered = 0; q_idx = 0
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
                    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(q[:80])}?width={W}&height={H}&model=flux"
                    r = requests.get(url, timeout=15); open(p_path,'wb').write(r.content)
                    found_clip = ImageClip(p_path).set_duration(4).resize((W,H))
                except: found_clip = ColorClip((W,H), color=(15,18,24), duration=4)
            cut_len = min(random.uniform(3.0, 4.5), duration - time_covered)
            if found_clip.duration > cut_len:
                start = random.uniform(0, max(0.1, found_clip.duration-cut_len-0.1))
                found_clip = found_clip.subclip(start, start+cut_len)
            clips_to_join.append(found_clip.set_duration(cut_len).resize((W,H)))
            time_covered += cut_len
            if len(clips_to_join) >= 5: break
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
        lang = 'ur' if 'urdu' in str(globals().get('voice_lang','')).lower() else 'en'
        gTTS(text=tx[:350], lang=lang, slow=False).save(out)
        return True
    except: return False
def detect_voice(ch, selected): return VOICES.get(selected, "en-US-BrandonNeural")

def get_avatar_clip(duration, W, H):
    try:
        mode = globals().get('avatar_mode','')
        selected = globals().get('selected_avatar','1 - Young Boy - Hoodie (Motivational)')
        if "No Avatar" in mode:
            print("🚫 No Avatar")
            return None
        local_path = f"{BASE_DIR}/av_{selected.split()[0]}.jpg"
        if os.path.exists(local_path) and os.path.getsize(local_path) < 5000:
            os.remove(local_path)
        if not os.path.exists(local_path):
            print(f"🎨 Generating Avatar: {selected}")
            prompt = AVATAR_PROMPTS.get(selected, AVATAR_PROMPTS["1 - Young Boy - Hoodie (Motivational)"])
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=512&height=768&model=flux&seed={random.randint(1,999999)}&nologo=true&enhance=true"
            r = requests.get(url, timeout=45)
            if r.status_code==200 and len(r.content)>8000:
                open(local_path,'wb').write(r.content)
                try:
                    im = Image.open(local_path).convert("RGB")
                    im.save(local_path)
                    print(f"✅ Avatar Generated & Fixed: {local_path}")
                except Exception as e:
                    print(f"PIL Fix Error: {e}")
        if not os.path.exists(local_path) or os.path.getsize(local_path) < 5000:
            print("❌ Avatar file missing/corrupt")
            return None
        try:
            # Validate image
            img = Image.open(local_path)
            img.verify()
        except:
            print("❌ Corrupt image, deleting")
            if os.path.exists(local_path): os.remove(local_path)
            return None
        def talking_effect(t): return 1 + 0.015 * math.sin(t * 14)
        av_w = int(W*0.32); av_h = int(av_w * 1.25)
        avatar = ImageClip(local_path).set_duration(duration).resize((av_w, av_h))
        avatar = avatar.resize(lambda t: talking_effect(t)).set_pos((0.67, 0.55), relative=True)
        print(f"✅ Avatar OK: {selected}")
        return avatar
    except Exception as e:
        print(f"Avatar error: {e}")
        import traceback; traceback.print_exc()
        return None

print(f"🎙️ Voice: {voice_lang} | Video Mode: {video_mode} | Avatar Mode: {avatar_mode} | Selected: {globals().get('selected_avatar','')}")
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
            print("👤 AVATAR ONLY MODE")
            base_clip = ColorClip((W,H), color=(10,10,15), duration=dur)
            base_clip = CompositeVideoClip([base_clip, avatar_clip.set_position('center')]).set_duration(dur)
        elif avatar_clip:
            print("👤 AVATAR + STOCK MODE")
            base_clip = CompositeVideoClip([clip.set_duration(dur), avatar_clip]).set_duration(dur)
        else:
            print("🎥 STOCK ONLY MODE")
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
        gc.collect(); time.sleep(0.2)
    except Exception as e: print(f"❌ Scene {idx+1} Error {e}"); import traceback; traceback.print_exc(); continue

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
